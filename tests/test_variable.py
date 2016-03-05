import unittest
from ecosystem.variable import ValueWrapper, Variable


class TestValueWrapper(unittest.TestCase):

    # def setUp(self):
    #     self.value_wrapper_obj = ValueWrapper()
    #
    # def tearDown(self):
    #     pass

    def test__current_os(self):
        value_wrapper_obj = ValueWrapper('foo')
        os_list = ['darwin', 'linux', 'windows']
        self.assertTrue(value_wrapper_obj._current_os in os_list)

    def test_value_dict_os(self):
        dict_value = {'darwin': '/some/path',
                      'linux': '/some/path',
                      'windows': '/some/path', }
        value_wrapper_obj = ValueWrapper(dict_value)
        self.assertEqual(value_wrapper_obj.value, '/some/path')

    def test_value_dict_common(self):
        dict_value = {'common': '/some/path'}
        value_wrapper_obj = ValueWrapper(dict_value)
        self.assertEqual(value_wrapper_obj.value, '/some/path')
        dict_value = {'common': '/some/path',
                      'darwin': '/other/path',
                      'linux': '/other/path',
                      'windows': '/other/path'}
        value_wrapper_obj = ValueWrapper(dict_value)
        self.assertEqual(value_wrapper_obj.value, '/other/path')

    def test_strict_value(self):
        dict_value = {'common': '/some/path', 'strict': True}
        value_wrapper_obj = ValueWrapper(dict_value)
        self.assertEqual(value_wrapper_obj.strict_value, True)
        dict_value = {'common': '/some/path'}
        value_wrapper_obj = ValueWrapper(dict_value)
        self.assertEqual(value_wrapper_obj.strict_value, None)

    def test_absolute_value(self):
        dict_value = {'common': '/some/path', 'abs': ['windows', 'linux', 'darwin']}
        value_wrapper_obj = ValueWrapper(dict_value)
        self.assertEqual(value_wrapper_obj.absolute_value, True)
        dict_value = {'common': '/some/path', 'abs': 'foo'}
        value_wrapper_obj = ValueWrapper(dict_value)
        self.assertEqual(value_wrapper_obj.absolute_value, 'foo')
        dict_value = {'common': '/some/path'}
        value_wrapper_obj = ValueWrapper(dict_value)
        self.assertEqual(value_wrapper_obj.absolute_value, None)


class TestVariable(unittest.TestCase):

    def _test_append_value(self, variable, value,
                           dependents=None,
                           values=None,
                           dependencies=None,
                           strict=False,
                           absolute=False):
        variable_obj = Variable(variable)
        variable_obj.append_value(value)
        self.assertEqual(variable_obj.dependents, dependents or [])
        self.assertEqual(variable_obj.values, values or [])
        self.assertEqual(variable_obj.dependencies, dependencies or [])
        self.assertEqual(variable_obj.strict, strict)
        self.assertEqual(variable_obj.absolute, absolute)

    def test_append_value_string(self):
        self._test_append_value('MAYA_VERSION', '2015', values=['2015'])

    def test_append_value_dict(self):
        dict_value = {'darwin': '/some/path',
                      'linux': '/some/path',
                      'windows': '/some/path', }
        self._test_append_value('MAYA_LOCATION', dict_value, values=['/some/path'])
        dict_value = {'foo': '/other/path', }
        self._test_append_value('MAYA_LOCATION', dict_value, values=[])

    def test_append_value_dependency(self):
        self._test_append_value('PATH', '/some/path/${MAYA_VERSION}',
                                values=['/some/path/${MAYA_VERSION}'],
                                dependencies=['MAYA_VERSION'])

    def test_append_value_common(self):
        dict_value = {'common': '/some/path'}
        self._test_append_value('MAYA_LOCATION', dict_value, values=['/some/path'])
        dict_value = {'common': '/some/path',
                      'darwin': '/other/path',
                      'linux': '/other/path',
                      'windows': '/other/path'}
        self._test_append_value('MAYA_LOCATION', dict_value, values=['/other/path'])

    def test_append_value_abs(self):
        dict_value = {'common': '/some/path', 'abs': ['windows', 'linux', 'darwin']}
        self._test_append_value('MAYA_LOCATION', dict_value, values=['/some/path'], absolute=True)

    def test_append_value_strict(self):
        dict_value = {'common': '/some/path', 'strict': True}
        self._test_append_value('MAYA_LOCATION', dict_value, values=['/some/path'],
                                strict=True)

    def test_list_dependencies(self):
        self.variable_obj = Variable('MAYA_LOCATION')
        variable = '/some/path/${MAYA_VERSION}'
        self.assertEqual(self.variable_obj.list_dependencies(variable), ['MAYA_VERSION'])
        self.assertEqual(self.variable_obj.list_dependencies('/some/path'), [])

    def test_has_value(self):
        self.variable_obj = Variable('MAYA_LOCATION')
        self.assertFalse(self.variable_obj.has_value())
        self.variable_obj.append_value('/some/path')
        self.assertTrue(self.variable_obj.has_value())

    def test_env(self):
        self.variable_obj = Variable('MAYA_LOCATION')
        self.variable_obj.append_value('/some/path')
        self.assertEqual(self.variable_obj.env, '/some/path')


if __name__ == '__main__':
    unittest.main()
