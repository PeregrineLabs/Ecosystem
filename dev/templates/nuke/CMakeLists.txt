#
# (c) 2010 Peregrine Labs a division of Peregrine Visual Storytelling Ltd.
# All rights reserved.
#
# The coded instructions, statements, computer programs, and/or related
# material (collectively the "Data") in these files contain unpublished
# information proprietary to Peregrine Visual Storytelling Ltd. ("Peregrine") 
# and/or its licensors, which is protected by U.S. and Canadian federal 
# copyright law and by international treaties.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. PEREGRINE
# DOES NOT MAKE AND HEREBY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES
# INCLUDING, BUT NOT LIMITED TO, THE WARRANTIES OF NON-INFRINGEMENT,
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, OR ARISING FROM A COURSE 
# OF DEALING, USAGE, OR TRADE PRACTICE. IN NO EVENT WILL PEREGRINE AND/OR ITS
# LICENSORS BE LIABLE FOR ANY LOST REVENUES, DATA, OR PROFITS, OR SPECIAL,
# DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES, EVEN IF PEREGRINE AND/OR ITS
# LICENSORS HAS BEEN ADVISED OF THE POSSIBILITY OR PROBABILITY OF SUCH DAMAGES.
#
#

CMAKE_MINIMUM_REQUIRED( VERSION 2.8 )

set( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR}/cmake $ENV{PG_CMAKE_MODULE_PATH} )
  
PROJECT ( Example )

# Product Version
SET( PG_MAJOR_VERSION "0" )
SET( PG_MINOR_VERSION "1" )
SET( PG_PATCH_VERSION "0" )

FIND_PACKAGE (Peregrine)
FIND_PACKAGE (Nuke)
FIND_PACKAGE (OpenGL)

INCLUDE_DIRECTORIES ( include )

ADD_DEFINITIONS ( -DUSE_GLEW )

IF ( WIN32 )
	INCLUDE_DIRECTORIES ( external )
	set( PLATFORM_SRC external/stdafx.cpp )
ELSE ( WIN32 )
	ADD_DEFINITIONS ( -msse3 -fno-math-errno )
ENDIF ( WIN32 )

# you need to make sure you're building against OSX10.7's SDK
IF ( APPLE )
    set(CMAKE_OSX_SYSROOT /base/sw/darwin/MacOSX10.7.sdk)
    set(CMAKE_OSX_DEPLOYMENT_TARGET 10.7)
ENDIF( APPLE )
  
ADD_LIBRARY ( example SHARED Add.cpp )
IF ( WIN32 )
	set_target_properties( example PROPERTIES LINK_FLAGS "/NODEFAULTLIB:LIBCMT" )
ENDIF( WIN32 )
TARGET_LINK_LIBRARIES ( example ${NUKE_LIBRARIES} ${RLM_LIBRARIES} )
SET_TARGET_PROPERTIES ( example PROPERTIES PREFIX "")

execute_process(COMMAND ${CMAKE_COMMAND} -E copy_directory ${PROJECT_SOURCE_DIR}/py ${LIBRARY_OUTPUT_PATH} )
execute_process(COMMAND ${CMAKE_COMMAND} -E copy_directory ${PROJECT_SOURCE_DIR}/icons ${LIBRARY_OUTPUT_PATH} )

