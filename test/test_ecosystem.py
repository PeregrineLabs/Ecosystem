import unittest
import os
import sys

ECO_ROOT = os.environ.get('ECO_ROOT') or os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(ECO_ROOT, 'bin'))
from ecosystem import ValueWrapper, Variable, Tool, Environment, list_available_tools, main


class ValueWrapperTester(unittest.TestCase):

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
        self.assertEqual(value_wrapper_obj.strict_value, False)

    def test_absolute_value(self):
        dict_value = {'common': '/some/path', 'abs': ['windows', 'linux', 'darwin']}
        value_wrapper_obj = ValueWrapper(dict_value)
        self.assertEqual(value_wrapper_obj.absolute_value, True)
        dict_value = {'common': '/some/path', 'abs': 'foo'}
        value_wrapper_obj = ValueWrapper(dict_value)
        self.assertEqual(value_wrapper_obj.absolute_value, 'foo')
        dict_value = {'common': '/some/path'}
        value_wrapper_obj = ValueWrapper(dict_value)
        self.assertEqual(value_wrapper_obj.absolute_value, False)


class VariableTester(unittest.TestCase):

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

    def test_get_env(self):
        self.variable_obj = Variable('MAYA_LOCATION')
        self.variable_obj.append_value('/some/path')
        self.assertEqual(self.variable_obj.get_env(), '/some/path')


class ToolTester(unittest.TestCase):

    def setUp(self):
        self.environ = os.environ.copy()
        os.environ['ECO_ENV'] = os.path.join(ECO_ROOT, 'env')
        self.env_file = 'maya_2015.env'
        self.tool = 'maya'
        self.version = '2015'
        self.platforms = ['windows', 'linux', 'darwin']
        self.requirements = []
        self.filename = os.path.join(ECO_ROOT, 'env', self.env_file)
        self.tool_obj = Tool(self.filename)

    def tearDown(self):
        os.environ = self.environ

    def test_tool(self):
        self.assertEqual(self.tool_obj.tool, self.tool)

    def test_version(self):
        self.assertEqual(self.tool_obj.version, self.version)

    def test_platforms(self):
        self.assertEqual(self.tool_obj.platforms, self.platforms)

    def test_requirements(self):
        self.assertEqual(self.tool_obj.requirements, self.requirements)

    def test_get_vars(self):
        class Foo():
            def __init__(self):
                self.tools = {}
                self.variables = {}
        foo_obj = Foo()
        self.tool_obj.get_vars(foo_obj)
        variable_list = ['DYLD_LIBRARY_PATH', 'PATH', 'MAYA_LOCATION', 'MAYA_VERSION']
        self.assertEqual(foo_obj.variables.keys(), variable_list)

    def test_platform_supported(self):
        self.assertTrue(self.tool_obj.platform_supported, True)

    # def test_definesVariable(self):
    #     self.assertTrue(self.tool_obj.definesVariable('foo'), False)


class EnvironmentTester(unittest.TestCase):

    def setUp(self):
        self.environ = os.environ.copy()
        os.environ['ECO_ENV'] = os.path.join(ECO_ROOT, 'env')
        os.environ['PG_SW_BASE'] = os.path.join(ECO_ROOT, 'test', 'pg_sw_base')
        self.tools = ['maya2015', 'yeti1.3.16']
        self.environment_obj = Environment(self.tools)

    def tearDown(self):
        os.environ = self.environ

    def test_get_env(self):
        test_get_env = '''#Environment created via Ecosystem
setenv MAYA_VERSION 2015
setenv MAYA_LOCATION /Applications/Autodesk/maya${MAYA_VERSION}/Maya.app/Contents
setenv YETI_VERSION 1.3.16
setenv YETI_ROOT ${PG_SW_BASE}/peregrinelabs/Yeti-v${YETI_VERSION}_Maya${MAYA_VERSION}-darwin64
setenv MAYA_MODULE_PATH ${YETI_ROOT}
setenv DYLD_LIBRARY_PATH ${MAYA_LOCATION}/MacOS
setenv PATH ${MAYA_LOCATION}/bin:${YETI_ROOT}/bin:${PATH}
'''
        self.assertEqual(self.environment_obj.get_env(), test_get_env)


class ListAvailableToolsTester(unittest.TestCase):

    def setUp(self):
        self.environ = os.environ.copy()
        os.environ['ECO_ENV'] = os.path.join(ECO_ROOT, 'env')
        self.last_tool = 'yeti1.3.8'
        self.no_tools = 63

    def tearDown(self):
        os.environ = self.environ

    def test_list_available_tools(self):
        available_tools = list_available_tools()
        self.assertEqual(available_tools[-1], self.last_tool)
        self.assertEqual(len(available_tools), self.no_tools)


# class MainTester(unittest.TestCase):
#
#     def setUp(self):
#         self.environ = os.environ.copy()
#         os.environ['ECO_ENV'] = os.path.join(ECO_ROOT, 'env')
#
#     def tearDown(self):
#         os.environ = self.environ


if __name__ == '__main__':
    unittest.main()
