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
import glob
import os
import platform
import subprocess
import sys
from .environment import Tool, Environment
from .preset import Preset
from .settings import MAKE_COMMAND, MAKE_TARGET
import json

_ON_WINDOWS = (platform.system().lower() == 'windows')


def list_available_tools():
    """Reads all of the found .env files, parses the tool name and version creates a list."""
    eco_env = os.environ.get('ECO_ENV')
    if eco_env is None:
        print('Ecosystem environment folder not found; please set environment variable ECO_ENV...')
    environment_files = os.path.join(os.getenv('ECO_ENV'), '*.env')
    possible_tools = [Tool(file_name) for file_name in glob.glob(environment_files)]
    tool_names = [new_tool.tool_plus_version for new_tool in possible_tools if new_tool.platform_supported]
    return sorted(list(set(tool_names)))


def resolve_presets(presets):
    # look in the current and parent directory for a eco.preset file
    if os.path.exists('./eco.preset'):
        preset_file = './eco.preset'
    elif os.path.exists('../eco.preset'):
        preset_file = '../eco.preset'
    else:
        print('Preset requested but Ecosystem can\'t find any eco.preset file.')
        return []

    with open(preset_file, 'r') as f:
        preset_dictionary = json.load(f)

    defined_presets = {}
    found_presets = []

    # read them in and create all possible Preset representations
    # if any, find the one(s) that match the requests presets
    for preset in preset_dictionary:
        defined_presets[preset] = Preset(preset_dictionary[preset])
        if preset in presets:
            found_presets.append(defined_presets[preset])

    # resolve any preset dependencies, this is NOT recursive at this time.
    for preset in found_presets:
        preset.resolve_dependencies(defined_presets)

    # return the flattened and expanded list of tools requested as a list
    tools = []
    for preset in found_presets:
        tools += preset.tools

    return set(tools)


def call_process(arguments):
    if _ON_WINDOWS:
        subprocess.call(arguments, shell=True)
    else:
        subprocess.call(arguments)


def build(tools=None, force_rebuild=False, quick_build=False, deploy=False):
    tools = tools or []
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
                    print("Cache doesn't exist...")

            call_process(['cmake', '-DCMAKE_BUILD_TYPE={0}'.format(build_type), '-G', MAKE_TARGET, '..'])

        if deploy:
            MAKE_COMMAND.append("package")

        call_process(MAKE_COMMAND)


def run(tools=None, run_application=None):
    tools = tools or []
    env = Environment(tools)
    if env.success:
        env.set_env(os.environ)
        call_process([run_application])


def set_environment(tools=None):
    tools = tools or []
    env = Environment(tools)
    if env.success:
        output = env.get_env()
        if output:
            print(output)


def main(argv=None):
    argv = argv or sys.argv[1:]

    # parse the (command line) arguments; python 2.7+ (or download argparse)
    import argparse
    description = 'Peregrine Ecosystem, environment, build and deploy management toolset v0.5.1'
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
    parser.add_argument('-p', '--presets', type=str, default=None,
                        help='specify a list of presets if any')

    args = parser.parse_args(argv)

    tools = args.tools.split(',') if args.tools is not None else []

    # assuming tools defined take precedence over any in a preset
    if args.presets:
        presets = set(args.presets.split(',') if args.presets is not None else [])
        tools += resolve_presets(presets)

    try:
        if args.listtools:
            import pprint
            pprint.pprint(list_available_tools(), width=1)
        elif args.build:
            if args.deploy:
                build(tools, True, False, args.deploy)
            else:
                build(tools, args.force, args.make, args.deploy)
        elif args.run is not None:
            run(tools, args.run)
        elif args.setenv:
            set_environment(tools)
        return 0
    except Exception as e:
        sys.stderr.write('ERROR: {0:s}'.format(str(e)))
        return 1


def eneedenv():
    """Hook for entry_point eneedenv"""
    return main(['--setenv', '-t'] + sys.argv[1:])


def elist(aegv=None):
    """Hook for entry_point elist"""
    return main(['--listtools'])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
