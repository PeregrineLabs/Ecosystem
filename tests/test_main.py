import unittest
import os
from ecosystem.main import list_available_tools, main

ECO_ROOT = os.environ.get('ECO_ROOT') or os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class TestListAvailableTools(unittest.TestCase):

    def setUp(self):
        self.environ = os.environ.copy()
        os.environ['ECO_ENV'] = os.path.join(ECO_ROOT, 'tests', 'test_env')
        self.last_tool = 'yeti1.3.16'
        self.no_tools = 2

    def tearDown(self):
        os.environ = self.environ

    def test_list_available_tools(self):
        available_tools = list_available_tools()
        self.assertEqual(available_tools[-1], self.last_tool)
        self.assertEqual(len(available_tools), self.no_tools)


class TestMain(unittest.TestCase):

    def setUp(self):
        self.environ = os.environ.copy()
        os.environ['ECO_ENV'] = os.path.join(ECO_ROOT, 'tests', 'test_env')

    def tearDown(self):
        os.environ = self.environ

    def test_main(self):
        os.environ['PG_SW_BASE'] = '/foo'
        self.assertEqual(main(['-t', 'maya2015,yeti1.3.16']), 0)


if __name__ == '__main__':
    unittest.main()
