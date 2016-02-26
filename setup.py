from setuptools import setup
from pkg_resources import resource_string


data = {
    'name': 'Ecosystem',
    'author': 'Peregrine*Labs',
    'author_email': 'support@peregrinelabs.com',
    'entry_points': [
        "eco = ecosystem.ecosystem:main",
    ],
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
    'version': '0.5.0',
    'url': 'https://github.com/PeregrineLabs/Ecosystem',
}

setup(**data)
