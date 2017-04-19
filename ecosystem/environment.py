import os
import glob
from .tool import Tool
from .want import Want


class Environment(object):
    """Once initialized this will represent the environment defined by the wanted tools."""

    def __init__(self, wants, env_dir=None, force=False):
        self._wants = wants
        env_dir = env_dir or os.getenv('ECO_ENV', '')
        self.force = force

        # self.tools = {}
        self.variables = {}
        self.success = True
        self.environment_files = os.path.join(env_dir, '*.env')

        missing_tools = self.missing_tools
        if missing_tools:
            missing_tools = ', '.join(missing_tools)
            print('Unable to resolve all of the requested tools ({0} is missing), ' \
                  'please check your list and try again!'.format(missing_tools))
            self.success = False

        missing_requirements = self.missing_requirements
        if missing_requirements:
            missing_requirements = ', '.join(missing_requirements)
            print('Unable to resolve all of the requirements ({0} is missing), ' \
                  'please check your list and try again!'.format(missing_requirements))
            self.success = False

        for tool_name, tool in self.tools.items():
            tool.get_vars(self)

        missing_dependencies = self.missing_dependencies
        if missing_dependencies:
            missing_vars = ', '.join(missing_dependencies)
            print('Unable to resolve all of the required variables ({0} is missing), \
                       please check your list and try again!'.format(missing_vars))
            self.success = False

    @property
    def wants(self):
        wants_dict = {}
        for want in [Want(x) for x in set(self._wants)]:
            if want.version and (want.tool in wants_dict):
                # have maya2015 while 'maya' has been processed
                print('Duplicate tool specified: {0} using {1}'.format(want.tool, want.requirement))
            if want.version or (want.tool not in wants_dict):
                # have maya2015, or 'maya' has not been processed
                wants_dict[want.tool] = want
        return wants_dict

    @property
    def define_tools(self):
        defined = [Tool(file_name) for file_name in glob.glob(self.environment_files)]
        return dict([(tool.tool_plus_version, tool) for tool in defined])

    @property
    def requested_tools(self):
        defined_tools = self.define_tools
        return [defined_tools[want.requirement] for want in self.wants.values() if want.requirement in defined_tools]

    @property
    def missing_tools(self):
        defined_tools = self.define_tools
        return [want.requirement for want in self.wants.values() if want.requirement not in defined_tools]

    @property
    def required_tools(self):
        required = []
        for requested_tool in self.requested_tools:
            required.extend(requested_tool.requirements)
        return list(set(required))

    @property
    def missing_requirements(self):
        requested_tool_names = [x.tool for x in self.requested_tools]
        return [required_tool for required_tool in self.required_tools if required_tool not in requested_tool_names]

    @property
    def ext_dependencies(self):
        # check and see if any of the variables dependencies are defined locally to the tool or are considered external
        ext_dependency_list = []
        for name, var in self.variables.items():
            if var.dependencies:
                for dep in var.dependencies:
                    if dep not in self.variables:
                        if dep not in ext_dependency_list:
                            ext_dependency_list.append(dep)
                    else:
                        self.variables[dep].dependents.append(name)
        return ext_dependency_list

    @property
    def missing_dependencies(self):
        return set([dep for dep in self.ext_dependencies if not os.getenv(dep)])

    @property
    def tools(self):
        return dict([(new_tool.tool, new_tool) for new_tool in self.requested_tools])

    def get_var(self, var):
        if self.success and var is not None:
            if var.name not in self.defined_variables:
                for dependency in var.dependencies:
                    self.get_var(self.variables.get(dependency, None))
                self.value += 'setenv {0} {1}'.format(var.name, var.env)
                # self.value += 'export {0}={1}'.format(var.name, var.env)
                if os.getenv(var.name):
                    if not self.force and not var.strict:
                        if var.env != '':
                            self.value += os.pathsep
                        self.value += '${{{0}}}'.format(var.name)
                self.value += '\n'
                self.defined_variables.append(var.name)

    def get_var_env(self, var):
        if self.success and var is not None:
            if var.name not in self.defined_variables:
                for dependency in var.dependencies:
                    self.get_var_env(self.variables.get(dependency, None))
                var_value = var.env
                if var.name in os.environ:
                    if not self.force and not var.strict:
                        if var_value != '':
                            var_value += os.pathsep
                        var_value += os.environ[var.name]
                self.defined_variables.append(var.name)
                os.environ[var.name] = var_value

    def get_env(self):
        """Combine all of the variables in all the tools based on a dependency list and return as string."""
        if self.success:
            self.defined_variables = []
            self.value = '#Environment created via Ecosystem\n'
            for var_name, variable in sorted(self.variables.items()):
                if self.variables[var_name].has_value():
                    self.get_var(variable)
            return self.value

    def set_env(self, environ=None):
        """Combine all of the variables in all the tools based on a dependency list and use to set environment."""
        if self.success:
            environ = environ or os.environ
            self.defined_variables = []
            for var_name, variable in self.variables.items():
                if self.variables[var_name].has_value():
                    self.get_var_env(variable)

            # run this code twice to cross-expand any variables
            for _ in range(2):
                for env_name, env_value in environ.items():
                    os.environ[env_name] = os.path.expandvars(env_value)
