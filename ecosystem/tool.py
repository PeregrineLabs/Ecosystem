import platform, json
from .variable import Variable

class Tool(object):
    """Defines a tool - more specifically, a version of a tool"""

    def __init__(self, filename):
        try:
            with open(filename, 'r') as f:
                self.in_dictionary = json.load(f)
        except IOError:
            self.in_dictionary = {}
            print('Unable to find file {0} ...'.format(filename))

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
