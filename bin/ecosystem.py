#!/usr/bin/python

# Copyright (c) 2014, Peregrine Labs, a division of Peregrine Visual Storytelling Ltd. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of Peregrine Visual Storytelling Ltd., Peregrine Labs
#      and any of it's affiliates nor the names of any other contributors
#      to this software may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# TODO: have ECO set an environment variable with all the loaded tools
# TODO: check environment varialbe for loaded tools
# TODO: unloading tools

import os
import glob
import re
import sys
import subprocess
import platform


def determine_number_of_cpus():
    """
    Number of virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program
    """

    # Python 2.6+
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # POSIX
    try:
        res = int(os.sysconf('SC_NPROCESSORS_ONLN'))

        if res > 0:
            return res
    except (AttributeError, ValueError):
        pass

    # Windows
    try:
        res = int(os.environ['NUMBER_OF_PROCESSORS'])

        if res > 0:
            return res
    except (KeyError, ValueError):
        pass

    # jython
    try:
        from java.lang import Runtime
        runtime = Runtime.getRuntime()
        res = runtime.availableProcessors()
        if res > 0:
            return res
    except ImportError:
        pass

    # BSD
    try:
        sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'], stdout=subprocess.PIPE)
        sc_stdout = sysctl.communicate()[0]
        res = int(sc_stdout)

        if res > 0:
            return res
    except (OSError, ValueError):
        pass

    # Linux
    try:
        res = open('/proc/cpuinfo').read().count('processor\t:')

        if res > 0:
            return res
    except IOError:
        pass

    # Solaris
    try:
        pseudo_devices = os.listdir('/devices/pseudo/')
        expr = re.compile('^cpuid@[0-9]+$')

        res = 0
        for pd in pseudo_devices:
            if expr.match(pd) is not None:
                res += 1

        if res > 0:
            return res
    except OSError:
        pass

    # Other UNIXes (heuristic)
    try:
        try:
            dmesg = open('/var/run/dmesg.boot').read()
        except IOError:
            dmesg_process = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
            dmesg = dmesg_process.communicate()[0]

        res = 0
        while '\ncpu' + str(res) + ':' in dmesg:
            res += 1

        if res > 0:
            return res
    except OSError:
        pass

    raise Exception('Can not determine number of CPUs on this system')


# set up some global variables
NUMBER_OF_PROCESSORS = determine_number_of_cpus()
MAKE_COMMAND = ['make', '-j', str(NUMBER_OF_PROCESSORS)]
CLEAN_COMMAND = ['make', 'clean']
MAKE_TARGET = 'Unix Makefiles'
if platform.system().lower() == 'windows':
    MAKE_COMMAND = ['jom']
    CLEAN_COMMAND = ['jom', 'clean']
    MAKE_TARGET = 'NMake Makefiles'


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
            return self._value.get(self._current_os, None) or self._value.get('common', None)
        return self._value

    @property
    def strict_value(self):
        return self._value.get('strict', False) if isinstance(self._value, dict) else False

    @property
    def absolute_value(self):
        if isinstance(self._value, dict):
            abs_value = self._value.get('abs', False)
            return (self._current_os in self._value['abs']) if isinstance(abs_value, list) else abs_value
        return False


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
        return os.pathsep.join(self.values)

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
        self.strict = value_wrapper.strict_value
        if self.strict is False:
            self.absolute = value_wrapper.absolute_value
        if value_wrapper.value not in self.values and value_wrapper.value is not None:
            self.values += [value_wrapper.value]
            for var_dependency in self.list_dependencies(value_wrapper.value):
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
                        self.value += '${%s}'%var.name
                self.value += '\n'
                self.defined_variables.append(var.name)

    def get_var_env(self, var):
        if self.success and var is not None:
            if var.name not in self.defined_variables:
                for dependency in var.dependencies:
                    self.get_var_env(self.variables.get(dependency, None))
                if var.name in os.environ:
                    if not self.force and not var.strict:
                        if var.env != '':
                            var.env += os.pathsep
                        var.env += os.environ[var.name]
                self.defined_variables.append(var.name)
                os.environ[var.name] = var.env

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
            for env_name, env_value in environ.items():
                os.environ[env_name] = os.path.expandvars(env_value)


def list_available_tools():
    """Reads all of the found .env files, parses the tool name and version creates a list."""
    environment_files = os.path.join(os.getenv('ECO_ENV'), '*.env')
    possible_tools = [Tool(file_name) for file_name in glob.glob(environment_files)]
    tool_names = [new_tool.tool_plus_version for new_tool in possible_tools if new_tool.platform_supported]
    return sorted(list(set(tool_names)))


def call_process(arguments):
    if platform.system().lower() == 'windows':
        subprocess.call(arguments, shell=True)
    else:
        subprocess.call(arguments)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # parse the (command line) arguments; python 2.7+ (or download argparse)
    import argparse
    description = 'Peregrine Ecosystem, environment, build and deploy management toolset v0.1.1'
    parser = argparse.ArgumentParser(prog='ecosystem',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description=description,
                                     epilog='''
Example:
    python ecosystem.py -t maya2014,vray3.05,yeti1.3.0 -r maya
                                     ''')
    parser.add_argument('-t', '--tools', type=str, default=None,
                        help='specify a list of tools required separated by commas')
    parser.add_argument('-l', '--listtools', action='store_true',
                        help='list the available tools')
    parser.add_argument('-b', '--build', action='store_true',
                        help='run the desired build process')
    parser.add_argument('-d', '--deploy', action='store_true',
                        help='build and package the tool for deployment')
    parser.add_argument('-f', '--force', action='store_true',
                        help='force the full CMake cache to be rebuilt')
    parser.add_argument('-m', '--make', action='store_true',
                        help='just run make')
    parser.add_argument('-r', '--run', type=str, default=None,
                        help='run an application')
    parser.add_argument('-s', '--setenv', action='store_true',
                        help='output setenv statements to be used to set the shells environment')

    args = parser.parse_args(argv)

    if args.listtools:
        for tool in list_available_tools():
            print tool
        return 0

    tools = args.tools.split(',') if args.tools is not None else []
    run_application = args.run
    set_environment = args.setenv
    force_rebuild = args.force
    quick_build = args.make
    run_build = args.build
    deploy = args.deploy
    if deploy:
        force_rebuild = True
        run_build = True
        quick_build = False

    try:
        if run_build:
            env = Environment(tools)
            if env.success:
                env.set_env(os.environ)
                build_type = os.getenv('PG_BUILD_TYPE')

                if not quick_build:
                    if force_rebuild:
                        try:
                            open('CMakeCache.txt')
                            os.remove('CMakeCache.txt')
                        except IOError:
                            print "Cache doesn't exist..."

                    call_process(['cmake', '-DCMAKE_BUILD_TYPE={0}'.format(build_type), '-G', MAKE_TARGET, '..'])

                if deploy:
                    MAKE_COMMAND.append("package")

                call_process(MAKE_COMMAND)

        elif run_application:
            env = Environment(tools)
            if env.success:
                env.set_env(os.environ)
                call_process([run_application])

        elif set_environment:
            env = Environment(tools)
            if env.success:
                output = env.get_env()
                if output:
                    print output
        return 0
    except Exception, e:
        sys.stderr.write('ERROR: {0:s}'.format(str(e)))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
