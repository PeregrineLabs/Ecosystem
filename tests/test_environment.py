import unittest
import os
import platform
from ecosystem.environment import Environment

ECO_ROOT = os.environ.get('ECO_ROOT') or os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

_ON_DARWIN = (platform.system().lower() == 'darwin')
_ON_WINDOWS = (platform.system().lower() == 'windows')
_ON_LINUX = (platform.system().lower() == 'linux')




class TestEnvironment(unittest.TestCase):

    def setUp(self):
        self.environ = os.environ.copy()
        os.environ['ECO_ENV'] = os.path.join(ECO_ROOT, 'tests', 'test_env')
        os.environ['PG_SW_BASE'] = os.path.join(ECO_ROOT, 'tests', 'pg_sw_base')
        self.tools = ['maya2015', 'yeti1.3.16']
        self.environment_obj = Environment(self.tools)

    def tearDown(self):
        os.environ = self.environ

    def test_wants(self):
        self.assertEqual(sorted(self.environment_obj.wants.keys()), ['maya', 'yeti'])

    def test_defined_tools(self):
        self.assertEqual(sorted(self.environment_obj.define_tools.keys()), ['maya2015', 'yeti1.3.16'])

    def test_requested_tools(self):
        self.assertEqual(sorted([x.tool for x in self.environment_obj.requested_tools]), ['maya', 'yeti'])

    def test_missing_tools(self):
        self.tools += ['foo0.0.1']
        self.environment_obj = Environment(self.tools)
        self.assertEqual(self.environment_obj.missing_tools, ['foo0.0.1'])

    def test_required_tools(self):
        self.assertEqual(self.environment_obj.required_tools, ['maya'])

    def test_missing_requirements(self):
        self.tools = ['yeti1.3.16']
        self.environment_obj = Environment(self.tools)
        self.assertEqual(self.environment_obj.missing_requirements, ['maya'])

    def test_ext_dependencies(self):
        self.assertEqual(self.environment_obj.ext_dependencies, ['PG_SW_BASE'])

    def test_missing_dependencies(self):
        del os.environ['PG_SW_BASE']
        self.assertEqual(self.environment_obj.missing_dependencies, set(['PG_SW_BASE']))

    def test_get_env(self):
        if _ON_WINDOWS:
            test_get_env = '''#Environment created via Ecosystem
setenv MAYA_VERSION 2015
setenv MAYA_LOCATION C:/Program Files/Autodesk/Maya${MAYA_VERSION}
setenv YETI_VERSION 1.3.16
setenv YETI_ROOT ${PG_SW_BASE}/peregrinelabs/Yeti-v${YETI_VERSION}_Maya${MAYA_VERSION}-windows64
setenv MAYA_MODULE_PATH ${YETI_ROOT}
setenv PATH ${MAYA_LOCATION}/bin;C:/Program Files/Common Files/Autodesk Shared/;C:/Program Files (x86)/Autodesk/Backburner/;${YETI_ROOT}/bin;${PATH}
'''
        elif _ON_DARWIN:
            test_get_env = '''#Environment created via Ecosystem
setenv MAYA_VERSION 2015
setenv MAYA_LOCATION /Applications/Autodesk/maya${MAYA_VERSION}/Maya.app/Contents
setenv YETI_VERSION 1.3.16
setenv YETI_ROOT ${PG_SW_BASE}/peregrinelabs/Yeti-v${YETI_VERSION}_Maya${MAYA_VERSION}-darwin64
setenv MAYA_MODULE_PATH ${YETI_ROOT}
setenv DYLD_LIBRARY_PATH ${MAYA_LOCATION}/MacOS
setenv PATH ${MAYA_LOCATION}/bin:${YETI_ROOT}/bin:${PATH}
'''
        # elif _ON_LINUX:
        #     test_get_env = None
        self.assertEqual(self.environment_obj.get_env(), test_get_env)

    def test_set_env(self):
        self.environment_obj.set_env()
        self.assertEqual(os.environ.get('MAYA_VERSION'), '2015')
        self.assertEqual(os.environ.get('YETI_VERSION'), '1.3.16')
        if _ON_DARWIN:
            self.assertEqual(os.environ.get('MAYA_LOCATION'), '/Applications/Autodesk/maya2015/Maya.app/Contents')
            self.assertTrue('tests/pg_sw_base/peregrinelabs/Yeti-v1.3.16_Maya2015-darwin64' in os.environ.get('YETI_ROOT'))
            self.assertTrue('tests/pg_sw_base/peregrinelabs/Yeti-v1.3.16_Maya2015-darwin64' in os.environ.get('MAYA_MODULE_PATH'))
            self.assertTrue('/Applications/Autodesk/maya2015/Maya.app/Contents/bin' in os.environ.get('PATH'))
            self.assertTrue('tests/pg_sw_base/peregrinelabs/Yeti-v1.3.16_Maya2015-darwin64/bin' in os.environ.get('PATH'))
            self.assertEqual(os.environ.get('DYLD_LIBRARY_PATH'), '/Applications/Autodesk/maya2015/Maya.app/Contents/MacOS')


if __name__ == '__main__':
    unittest.main()
