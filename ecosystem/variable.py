import os
import platform
import re


class ValueWrapper(object):
    """Wraps a value to be held by a Variable"""

    def __init__(self,
                 value=None):
        self._strict = False
        self._absolute = False
        self._current_os = platform.system().lower()

        if isinstance(value, dict):
            self._strict = value.get('strict')
            abs_value = value.get('abs')
            self._absolute = (self._current_os in value['abs']) if isinstance(abs_value, list) else abs_value

            self._value = value.get(self._current_os) or value.get('common')
        else:
            self._value = value

        if self._absolute:
            self._value = os.path.abspath(self._value)

        if self._value:
            self._value = os.path.normpath(self._value)

            if platform.system().lower() == 'windows':
                self._value = self._value.replace('\\', '/')

    @property
    def value(self):
        return self._value

    @property
    def strict_value(self):
        return self._strict

    @property
    def absolute_value(self):
        return self._absolute


class Variable(object):
    """Defines a variable required by a tool"""

    def __init__(self, name):
        self.name = name
        self.dependency_re = None
        self.dependents = []
        self.values = []
        self.dependencies = []
        self.strict = False

    @property
    def env(self):
        var_values = [x for x in self.values]
        return os.pathsep.join(var_values)

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

        value_wrapper_value = value_wrapper.value
        if value_wrapper_value not in self.values and value_wrapper_value is not None:
            self.values += [value_wrapper_value]
            for var_dependency in self.list_dependencies(value_wrapper_value):
                if var_dependency not in self.dependencies:
                    self.dependencies.append(var_dependency)

    def has_value(self):
        return self.values
