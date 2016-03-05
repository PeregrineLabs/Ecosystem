import os
import platform
import re


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
