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
  
PROJECT ( example )

# Product Version
SET( PG_MAJOR_VERSION "0" )
SET( PG_MINOR_VERSION "1" )
SET( PG_PATCH_VERSION "0" )

# Find dependencies
FIND_PACKAGE (Peregrine)
FIND_PACKAGE (Maya)
FIND_PACKAGE (OpenGL)

# includes
INCLUDE_DIRECTORIES ( include )

SET( MAYA_SRC 
	example.cpp
)

SET(MAYA_SCRIPT_FILES
	example.mel
)

# configure other files with verson numbers etc.
configure_file (
  "${CMAKE_SOURCE_DIR}/example.mod.in"
  "${LIBRARY_OUTPUT_PATH}/example.mod"
  )
  
# Build the Maya plugin
ADD_LIBRARY(example MODULE ${MAYA_SRC} )
TARGET_LINK_LIBRARIES(example ${OPENGL_LIBRARIES} Foundation OpenMaya OpenMayaUI OpenMayaFX OpenMayaAnim ${OS_LIBS} )
set_target_properties(example PROPERTIES COMPILE_FLAGS "${MAYA_DEFINITIONS}" )
set_target_properties(example PROPERTIES LINK_FLAGS "${MAYA_LINK_FLAGS}" )
set_target_properties(example PROPERTIES PREFIX "")
set_target_properties(example PROPERTIES SUFFIX "${MAYA_EXTENSION}")

# if it exists
execute_process(COMMAND ${CMAKE_COMMAND} -E copy_directory ${PROJECT_SOURCE_DIR}/mel ${LIBRARY_OUTPUT_PATH}/mel )

#Installation configuration which is used as a basis for packaging
INSTALL(TARGETS example DESTINATION bin)
INSTALL(FILES ${MAYA_SCRIPT_FILES} DESTINATION scripts)
INSTALL(FILES ${LIBRARY_OUTPUT_PATH}/example.mod DESTINATION .)

#CPack configuration for all platforms
INCLUDE(InstallRequiredSystemLibraries)

SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Example")
SET(CPACK_PACKAGE_VENDOR "Some Company")
SET(CPACK_PACKAGE_VERSION_MAJOR "${PG_MAJOR_VERSION}")
SET(CPACK_PACKAGE_VERSION_MINOR "${PG_MINOR_VERSION}")
SET(CPACK_PACKAGE_VERSION_PATCH "${PG_PATCH_VERSION}")

INCLUDE(CPack)