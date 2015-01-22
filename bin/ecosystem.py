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
# import copy
import getopt
import sys
import string
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


class Variable:
    """Defines a variable required by a tool"""

    def __init__(self, name):
        self.name = name
        self.dependency_re = None
        self.dependents = []
        self.values = []
        self.dependencies = []
        self.strict = False
        self.absolute = False

    def append_value(self, value):
        """Sets and/or appends a value to the Variable"""
        # check to see if the value is platform dependent
        platform_value = None
        if type(value) == dict:
            if 'common' in value:
                platform_value = value['common']
                
            if platform.system().lower() in value:
                platform_value = value[platform.system().lower()]
            
        else:
            platform_value = value
            
        if type(value) == dict:
            if 'strict' in value:
                self.strict = value['strict']
            elif 'abs' in value:
                if type(value['abs']) == list:
                    if platform.system().lower() in value['abs']:
                        self.absolute = True
                else:
                    self.absolute = value['abs']
            
        if platform_value:
            if platform_value not in self.values:
                self.values.append(platform_value)
                for var_dependency in self.check_for_dependencies(platform_value):
                    if var_dependency not in self.dependencies:
                        self.dependencies.append(var_dependency)

    def check_for_dependencies(self, value):
        """Checks the value to see if it has any dependency on other Variables, returning them in a list"""
        if not self.dependency_re:
            self.dependency_re = re.compile(r"\${\w*}")

        matched = self.dependency_re.findall(value)
        if matched:
            dependencies = [match[2:-1] for match in matched if match[2:-1] != self.name]
            return list(set(dependencies))
        else:
            return []

    def has_value(self):
        if len(self.values) > 0:
            return True
        return False

    def get_env(self):
        value = ''
        count = 0
        for var_value in self.values:
            if count != 0:
                value = value + os.pathsep
            if self.absolute:
                var_value = os.path.abspath(var_value)
            value = value + var_value
            count += 1
        return value


class Tool:
    """Defines a tool - more specifically, a version of a tool"""

    def __init__(self, filename):
        try:
            with open(filename, 'r') as f:
                self.in_dictionary = eval(f.read())
        except IOError:
            print 'Unable to find file {0} ...'.format(filename)

        if self.in_dictionary:
            self.tool = self.in_dictionary['tool']
            self.version = self.in_dictionary['version']
            self.platforms = self.in_dictionary['platforms']
            self.requirements = self.in_dictionary['requires']

    @property
    def plaform_supported(self):
        """Check to see if the tool is supported on the current platform"""
        return platform.system().lower() in self.platforms if self.platforms else False

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


class Environment:
    """Once initialized this will represent the environment defined by the wanted tools"""
    def __init__(self, wants, environment_directory=None, force=False):
        self.tools = {}
        self.variables = {}
        self.wants = set(wants)         # make sure the set has unique values
        self.success = True
        self.force = force

        self.environment_files = '*.env'

        environment_location = os.getenv('ECO_ENV')
        if environment_location:
            self.environment_files = environment_location + '/*.env'

        # reads all of the found .env files, parses the tool name and version and checked that against our want list
        possible_tools = [Tool(file_name) for file_name in glob.glob(self.environment_files)]
        for new_tool in possible_tools:
            if new_tool.plaform_supported:
                tool_name = new_tool.tool + new_tool.version if new_tool.version != '' else new_tool.tool
                if tool_name in self.wants:
                    if new_tool.tool in self.tools:
                        print 'Duplicate tool specified: \
                               {0} using {1}{2}'.format(new_tool.tool, new_tool.tool, new_tool.version)
                    self.tools[new_tool.tool] = new_tool
                    self.wants.remove(tool_name)
                if new_tool.tool in self.wants:
                    self.wants.remove(new_tool.tool)
                    if new_tool.requirements:
                        for required_tool in new_tool.requirements:
                            if required_tool not in self.tools:
                                self.wants = self.wants or set(list(required_tool))

        if len(self.wants) != 0:
            missing_tools = ', '.join(self.wants)
            print 'Unable to resolve all of the required tools ({0} is missing), \
                   please check your list and try again!'.format(missing_tools)
            self.success = False

        for tool_name, tool in self.tools.items():
            tool.get_vars(self)

        # check and see if any of the variables dependencies are defined locally to the tool or are considered external
        ext_dependencies = []
        for name, var in self.variables.items():
            if var.dependencies:
                for dep in var.dependencies:
                    if dep not in self.variables:
                        if dep not in ext_dependencies:
                            ext_dependencies.append(dep)
                    else:
                        self.variables[dep].dependents.append(name)

        # now check to see if they're already set in the environment
        missing_dependencies = set([dep for dep in ext_dependencies if not os.getenv(dep)])
        if missing_dependencies:
            missing_vars = ', '.join(missing_dependencies)
            print 'Unable to resolve all of the required variables ({0} is missing), \
                       please check your list and try again!'.format(missing_vars)
            self.success = False

    def get_var(self, var):
        if self.success:
            if var.name not in self.defined_variables:
                for dependency in var.dependencies:
                    if dependency in self.variables:
                        self.get_var(self.variables[dependency])
                var_value = var.get_env()
                self.value = self.value + 'setenv ' + var.name + ' ' + var_value
                if os.getenv(var.name):
                    if not self.force and not var.strict:
                        if var_value == '':
                            self.value = self.value + '${' + var.name + '}'
                        else:
                            self.value = self.value + os.pathsep + '${' + var.name + '}'
                self.value = self.value + '\n'
                self.defined_variables.append(var.name)

    def get_var_env(self, var):
        if self.success:
            if var.name not in self.defined_variables:
                for dependency in var.dependencies:
                    if dependency in self.variables:
                        self.get_var_env(self.variables[dependency])
                var_value = var.get_env()
                if var.name in os.environ:
                    if not self.force and not var.strict:
                        if var_value == '':
                            var_value = os.environ[var.name]
                        else:
                            var_value = var_value + os.pathsep + os.environ[var.name]
                self.defined_variables.append(var.name)
                os.environ[var.name] = var_value

    def get_env(self, set_environment=False):
        # combine all of the variable in all the tools based on a dependency list
        if self.success:
            self.defined_variables = []
            self.value = '#Environment created via Ecosystem\n'

            for var_name, variable in self.variables.items():
                if self.variables[var_name].has_value():
                    if not set_environment:
                        self.get_var(variable)
                    else:
                        self.get_var_env(variable)

            if not set_environment:
                return self.value

            # TODO check if we need this repetition
            for env_name, env_value in os.environ.items():
                os.environ[env_name] = os.path.expandvars(env_value)
            for env_name, env_value in os.environ.items():
                os.environ[env_name] = os.path.expandvars(env_value)


def list_available_tools():
    environment_files = '*.env'

    environment_location = os.getenv('ECO_ENV')
    if environment_location:
        environment_files = environment_location + '/*.env'

    # reads all of the found .env files, parses the tool name and version and checked that against our wan list
    tool_list = []
    possible_tools = glob.glob(environment_files)
    for file_name in possible_tools:
        new_tool = Tool(file_name)
        if new_tool.plaform_supported:
            tool_name = new_tool.tool
            if new_tool.version != '':
                tool_name = tool_name + new_tool.version
            if tool_name not in tool_list:
                tool_list.append(tool_name)

    tool_list.sort()

    for tool in tool_list:
        print tool


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
        list_available_tools()
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
                env.get_env(os.environ)
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
                env.get_env(os.environ)
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
