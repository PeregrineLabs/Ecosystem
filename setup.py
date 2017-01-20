import platform
from setuptools import setup
from pkg_resources import resource_string

_ON_POSIX = (platform.system().lower() in ['linux', 'linux2', 'darwin'])


data = {
    'name': 'Ecosystem',
    'author': 'Peregrine*Labs',
    'author_email': 'support@peregrinelabs.com',
    'bin': [
        'bin/eneed'
    ],
    'entry_points': {
        'console_scripts': [
            'eco = ecosystem.main:main',
            'elist = ecosystem.main:elist',
            'eneedenv = ecosystem.main:eneedenv',
        ],
    },
    'description': 'Ecosystem is a cross-platform environment management system',
    'license': resource_string(__name__, 'LICENSE'),
    'long_description': resource_string(__name__, 'README.md'),
    'packages': [
        'ecosystem',
        ],
    'package_data': {
        'ecosystem': [
            'dev/cmake/*.cmake',
            'dev/templates/maya/*.txt',
            'dev/templates/maya/*.cpp',
            'dev/templates/maya/*.mel',
            'dev/templates/maya/*.in',
            'dev/templates/nuke/py/*.py',
            'dev/templates/nuke/*.py',
            'dev/templates/nuke/*.cpp',
            'dev/templates/nuke/*.txt'
            'env/*.txt',
            'etc/*.aliases',
            'images/*.png',
        ],
    },
    'scripts': [],
    'version': 'v0.5.1',
    'url': 'https://github.com/PeregrineLabs/Ecosystem',
}

# multi-platform custom scripts
if _ON_POSIX:
    data['scripts'] = data.pop('bin')
else:
    data.pop('bin')

setup(**data)