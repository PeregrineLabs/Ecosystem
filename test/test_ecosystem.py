import unittest
import os
import sys

ECO_ROOT = os.environ.get('ECO_ROOT') or os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(ECO_ROOT, 'bin'))
from ecosystem import Tool, Environment, listAvailableTools, main


# class VariableTester(unittest.TestCase):
#
#     def setUp(self):
#         self.variable = Variable()
#
#     def tearDown(self):
#         pass


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
        #
        # os.environ['PG_SW_BASE'] = os.path.join(ECO_ROOT, 'test', 'pg_sw_base')
        # self.tools = ['maya2015', 'yeti1.3.16']
        # self.environment_obj = Environment(self.tools)

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

    def test_getVars(self):
        class Foo():
            def __init__(self):
                self.tools = {}
                self.variables = {}
        foo_obj = Foo()
        self.tool_obj.getVars(foo_obj)
        variable_list = ['DYLD_LIBRARY_PATH', 'PATH', 'MAYA_LOCATION', 'MAYA_VERSION']
        self.assertEqual(foo_obj.variables.keys(), variable_list)

    def test_platformSupported(self):
        self.assertTrue(self.tool_obj.plaformSupported(), True)

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

    def test_getEnv(self):
        test_get_env = '''#Environment created via Ecosystem
setenv MAYA_VERSION 2015
setenv MAYA_LOCATION /Applications/Autodesk/maya${MAYA_VERSION}/Maya.app/Contents
setenv YETI_VERSION 1.3.16
setenv YETI_ROOT ${PG_SW_BASE}/peregrinelabs/Yeti-v${YETI_VERSION}_Maya${MAYA_VERSION}-darwin64
setenv MAYA_MODULE_PATH ${YETI_ROOT}
setenv DYLD_LIBRARY_PATH ${MAYA_LOCATION}/MacOS
setenv PATH ${MAYA_LOCATION}/bin:${YETI_ROOT}/bin:${PATH}
'''
        self.assertEqual(self.environment_obj.getEnv(), test_get_env)


class ListAvailableToolsTester(unittest.TestCase):

    def setUp(self):
        self.environ = os.environ.copy()
        os.environ['ECO_ENV'] = os.path.join(ECO_ROOT, 'env')

    def tearDown(self):
        os.environ = self.environ

    def test_listAvailableTools(self):
        available_tools = listAvailableTools()
        self.assertEqual(available_tools[-1], 'yeti1.3.8')
        self.assertEqual(len(available_tools), 63)


# class MainTester(unittest.TestCase):
#
#     def setUp(self):
#         self.environ = os.environ.copy()
#         os.environ['ECO_ENV'] = os.path.join(ECO_ROOT, 'env')
#
#     def tearDown(self):
#         os.environ = self.environ
