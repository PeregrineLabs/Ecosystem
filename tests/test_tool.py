import unittest
import os
from ecosystem.tool import Tool

ECO_ROOT = os.environ.get('ECO_ROOT') or os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class TestTool(unittest.TestCase):

    def setUp(self):
        self.environ = os.environ.copy()
        os.environ['ECO_ENV'] = os.path.join(ECO_ROOT, 'tests', 'test_env')
        self.env_file = 'maya_2015.env'
        self.tool = 'maya'
        self.version = '2015'
        self.platforms = ['windows', 'linux', 'darwin']
        self.requirements = []
        self.filename = os.path.join(ECO_ROOT, 'tests', 'test_env', self.env_file)
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
        variable_list = ['DYLD_LIBRARY_PATH', 'MAYA_LOCATION', 'MAYA_VERSION', 'PATH']
        self.assertEqual(sorted(foo_obj.variables.keys()), variable_list)

    def test_platform_supported(self):
        self.assertTrue(self.tool_obj.platform_supported, True)

    # def test_definesVariable(self):
    #     self.assertTrue(self.tool_obj.definesVariable('foo'), False)


if __name__ == '__main__':
    unittest.main()
