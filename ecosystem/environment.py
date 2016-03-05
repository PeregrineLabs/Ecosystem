import os
import glob
import re
import platform


class ValueWrapper(object):
    """Wraps a value to be held by a Variable"""

    def __init__(self,
                 value=None):
        self._value = value

    @property
    def _current_os(self):
        return platform.system().lower()

    @property
    def value(self):
        if isinstance(self._value, dict):
            return self._value.get(self._current_os) or self._value.get('common')
        return self._value

    @property
    def strict_value(self):
        return self._value.get('strict') if isinstance(self._value, dict) else False

    @property
    def absolute_value(self):
        if isinstance(self._value, dict):
            abs_value = self._value.get('abs')
            return (self._current_os in self._value['abs']) if isinstance(abs_value, list) else abs_value
        return None


class Variable(object):
    """Defines a variable required by a tool"""

    def __init__(self, name):
        self.name = name
        self.dependency_re = None
        self.dependents = []
        self.values = []
        self.dependencies = []
        self.strict = False
        self.absolute = False

    @property
    def env(self):
        var_values = [x for x in self.values]
        if self.absolute:
            var_values = [os.path.abspath(x) for x in var_values]
        return os.pathsep.join(var_values)
        # return os.pathsep.join(self.values)

    def list_dependencies(self, value):
        """Checks the value to see if it has any dependency on other Variables, returning them in a list"""
        try:
            self.dependency_re = self.dependency_re or re.compile(r"\${\w*}")
            matched = self.dependency_re.findall(value)
            if matched:
                dependencies = [match[2:-1] for match in matched if match[2:-1] != self.name]
                return list(set(dependencies))
        except:
            pass
        return []

    def append_value(self, value):
        """Sets and/or appends a value to the Variable"""
        value_wrapper = ValueWrapper(value)
        if value_wrapper.strict_value is not None:
            self.strict = value_wrapper.strict_value
        elif value_wrapper.absolute_value is not None:
            self.absolute = value_wrapper.absolute_value

        value_wrapper_value = value_wrapper.value
        if value_wrapper_value not in self.values and value_wrapper_value is not None:
            self.values += [value_wrapper_value]
            for var_dependency in self.list_dependencies(value_wrapper_value):
                if not var_dependency in self.dependencies:
                    self.dependencies.append(var_dependency)

    def has_value(self):
        return self.values


class Tool(object):
    """Defines a tool - more specifically, a version of a tool"""

    def __init__(self, filename):
        try:
            with open(filename, 'r') as f:
                self.in_dictionary = eval(f.read())
        except IOError:
            self.in_dictionary = {}
            print 'Unable to find file {0} ...'.format(filename)

        self.tool = self.in_dictionary.get('tool', None)
        self.version = self.in_dictionary.get('version', None)
        self.platforms = self.in_dictionary.get('platforms', None)
        # self.requirements = self.in_dictionary.get('requires', None)

    @property
    def requirements(self):
        return self.in_dictionary.get('requires', None)

    @property
    def tool_plus_version(self):
        return self.tool + (self.version or '')

    @property
    def platform_supported(self):
        """Check to see if the tool is supported on the current platform"""
        return platform.system().lower() in self.platforms if self.platforms else False

    # TODO: move this to environment?
    def get_vars(self, env):
        for name, value in self.in_dictionary['environment'].items():
            if name not in env.variables:
                env.variables[name] = Variable(name)
            env.variables[name].append_value(value)

        # check for optional parameters
        if 'optional' in self.in_dictionary:
            for optional_name, optional_value in self.in_dictionary['optional'].items():
                if optional_name in env.tools:
                    for name, value in optional_value.items():
                        if name not in env.variables:
                            env.variables[name] = Variable(name)
                        env.variables[name].append_value(value)


class Want(object):
    """Defines a request, possibly with a specific version"""

    def __init__(self,
                 requirement):
        self.requirement = requirement

    @property
    def tool(self):
        return re.findall(r".*?(?=[0-9])", self.requirement + '0')[0]

    @property
    def version(self):
        result = re.findall(r"(?=[0-9]).*", self.requirement)
        return result[0] if result else ''


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
            print 'Unable to resolve all of the requested tools ({0} is missing), ' \
                  'please check your list and try again!'.format(missing_tools)
            self.success = False

        missing_requirements = self.missing_requirements
        if missing_requirements:
            missing_requirements = ', '.join(missing_requirements)
            print 'Unable to resolve all of the requirements ({0} is missing), ' \
                  'please check your list and try again!'.format(missing_requirements)
            self.success = False

        for tool_name, tool in self.tools.items():
            tool.get_vars(self)

        missing_dependencies = self.missing_dependencies
        if missing_dependencies:
            missing_vars = ', '.join(missing_dependencies)
            print 'Unable to resolve all of the required variables ({0} is missing), \
                       please check your list and try again!'.format(missing_vars)
            self.success = False

    @property
    def wants(self):
        wants_dict = {}
        for want in [Want(x) for x in set(self._wants)]:
            if want.version and (want.tool in wants_dict):
                # have maya2015 while 'maya' has been processed
                print 'Duplicate tool specified: {0} using {1}'.format(want.tool, want.requirement)
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
            for var_name, variable in self.variables.items():
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
