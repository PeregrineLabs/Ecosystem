# Ecosystem 
![Ecosystem](images/ecosystem.png?raw=true)
## Overview
Ecosystem is a cross-platform environment management system from [Peregrine Labs](http://peregrinelabs.com) originally developed for VFX/Animation production R&D but could be used in any situation where a fine understanding of your working enviornment is important (and it really should be!).  

## Why
Although it may seem like a simple task it's still very common to find that many of the studios we work with don't have control over their environment which is the root of many problems (wrong versions of software being accessed, wrong shared object versions, incompatible versions, etc.).  Our hope is that Ecosystem may be used to not just solve these problems but improve workflow in general.  

The toolset works extremely well in house, but the assumptions we've made may not fit into every workflow or pipeline - our hope is that studios interested in using Ecosystem provide feedback to make it more flexible so it is more general in scope.  

For more information on the design concepts refer to our presentation from the 2012 TDForum conference - [Building and Leveraging a Cross Platform VFX/Animation Development Environment](http://peregrinelabs-share.s3.amazonaws.com/CDoncaster_TDForum2012.pdf)

## Details
There are many situations where you may be required to work on multiple versions of the same software and/or share data between applications that are likely very pedantic about compatibility, most of the time this can all be controlled via environment variables in a shell.  Manually setting the environment variables and/or making sure dependencies are correctly resolved is generally out of the question, this is where Ecosystem comes in.  

Each instance of a tool has a .env file which defines the products base name, version and how the environment should look - "optional" parameters can be included to change the way the environment is resolved if other tools are present. 

With this library of tools and versions the ecosystem.py script is then used within a clean environment (ie. only the bare minimum of variables set) to resolve dependencies and set the environment in a state where the requests tools may be used together. 

For example:

	eneed maya2014,vray3.05,yeti1.3.10

will give me a working environment where **maya** will execute Maya 2014 and both Yeti 1.3.10 and Vray 3.05 will be correctly configured. 

Ecosystem has been developed to be cross platform so the above works on Linux, Osx and Windows.  

Although the intention is for Ecosystem to be used from a shell, the .py source is written in such a way that it would be easy to embed into a GUI application to have a more visual launcher.  

## Getting Started
Once you've cloned the repository all that is left is to create a few environment variables (once!) so Ecosystem knows where to find the .env files and to help resolve some of the dependencies. 

	ECO_ROOT is the root directory of ecosystem
	ECO_ENV is the directory that contains all of the .env tool files (this is very likely $ECO_ROOT/env)
	PATH the Ecosystem /bin directory will need to be added
	PG_SW_BASE is used in the .env tool files and is the mount point for many of the tool installations (so you can have shared or local installations)

We generally have local installations of all our software, so ours look like

	setenv ECO_ROOT ~/dev/ecosystem
	setenv ECO_ENV ${ECO_ROOT}/env
	setenv PATH ${ECO_ROOT}/bin:${PATH}
	setenv PG_SW_BASE /base/sw/

On **Linux** and **Osx** you will also want to 

	source ${ECO_ROOT}/etc/ecosystem.aliases

which provide some functional aliases.  

**Windows** is a slightly different beast, there is a eco.cmd file that wraps ecosystem.py - unlike linux and osx the environment is only temporarily set (if someone has a work around please let us know).  Using the example above one would do 

	eco -t maya2014,vray3.05,yeti1.3.0 -r maya

to start maya with the inteded environment. 

## Tool Environments

Each .env file contains a python dictionary with specific key words to control how Ecosystem resolves the tools needs.  

Here is an example:

	{
	'tool': 'maya', # base name for the tool
	'version': '2014',	# version
	'platforms': [ 'windows', 'linux', 'darwin' ],	# supported platforms
	'requires': [  ],	# a list of requirements, if any
	'environment':	# the environment
		{
		'MAYA_VERSION': '2014',
		'MAYA_LOCATION': { 'darwin': '/Applications/Autodesk/maya${MAYA_VERSION}/Maya.app/Contents', # embeded dictionaries may be used to define platform specific values
							'linux': '/usr/autodesk/maya${MAYA_VERSION}-x64',
							'windows': 'C:/Program Files/Autodesk/Maya${MAYA_VERSION}', },
		'PATH': { 'darwin': '${MAYA_LOCATION}/bin',
					'linux': '${MAYA_LOCATION}/bin',
					'windows': '${MAYA_LOCATION}/bin;C:/Program Files/Common Files/Autodesk Shared/;C:/Program Files (x86)/Autodesk/Backburner/', },
		'DYLD_LIBRARY_PATH': { 'darwin': '${MAYA_LOCATION}/MacOS', },
		},
		'optional': { 'dev':	# optional environment variables based on other tools being requested
						{
		'MAYA_DEV_BUILDS': '${DEV_BUILDS}',
		'PATH': { 'darwin': '${MAYA_DEV_BUILDS}',
					'linux': '${MAYA_DEV_BUILDS}',
					'windows': '${MAYA_DEV_BUILDS}', },
		'MAYA_SCRIPT_PATH': '${MAYA_DEV_BUILDS}/mel',
		'MAYA_SHELF_PATH': '${MAYA_DEV_BUILDS}/shelves',
		'XBMLANGPATH': '${MAYA_DEV_BUILDS}/icons',
		'MAYA_PLUG_IN_PATH': '${MAYA_DEV_BUILDS}',
		'MI_CUSTOM_SHADER_PATH': '${MAYA_DEV_BUILDS}',
						},
					 },
	}

The key words are self explanitory, as you can see each environment file expects the tool to be installed in a specific location.  Some applications (like Maya) are generally installed in common locations (though can be installed on a network) where others are much more flexible.  It is suggested that you review the .env files for the tools you may want to use to review the expected location.  

We've tried hard to keep all off the tools installed under `PG_SW_BASE` using the vendors name and then product version.  Although this may be slightly non-standard the benefits greatly outweigh any downside.

## Directory Assumptions
For Ecosystem to work at your studio you may need to conform to how the .env files have been created (or create your own) thus having software installed in similar locations.  For some tools we assume their default installation location (ie. Maya) and for others we try and install them into a central location with the root being 

	PG_SW_BASE 

thus allowing it to be either a local file system or a network mount.

Please email the list below if it's not completely obvious where Ecosystem is looking for installed software, based on your feedback we can update this introduction to help others.

## Using CMake
We've recently pushed all of our CMake files into the repository with the aim in helping others get started with cross platform VFX development.  This also includes template CMakeList files for various applications. 

## Development
Ecosystem in some form has been used for quite some time within Peregrine Labs though it has been extracted from a much larger system used to manage distributed workflows that wouldn't have leant itself as well to an open source project (remote push/pull from specific servers).  With that said, if there is interest we would love to eventually evolve Ecosystem to create a more generic means of packaging up dependencies and depolying them along with environment management.

There may still be some Peregrine specific cruft in the initial distribution that will need to be resolved, please bear with us! 

Please use the **GitHub** issue tracker to report issues and if you've made fixes/improvements feel free to send us a **Pull Request**.

## Discussion
We have a [ecosystem-env](https://groups.google.com/forum/#!forum/ecosystem-env) discussion list to share feedback and ask questions.
