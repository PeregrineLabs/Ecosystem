#
# (c) 2010-Present Peregrine Labs a division of Peregrine Visual Storytelling Ltd.
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
  
MESSAGE( STATUS "*********** Building ${CMAKE_BUILD_TYPE} version ${PG_MAJOR_VERSION}.${PG_MINOR_VERSION}.${PG_PATCH_VERSION} for ${CMAKE_SYSTEM_NAME}..." )

GET_FILENAME_COMPONENT(LIBRARY_OUTPUT_PATH "${CMAKE_BINARY_DIR}/$ENV{DEV_BUILDS}" ABSOLUTE)
GET_FILENAME_COMPONENT(EXECUTABLE_OUTPUT_PATH "${CMAKE_BINARY_DIR}/$ENV{DEV_BUILDS}" ABSOLUTE)

# Add version definitions
ADD_DEFINITIONS("-DPG_MAJOR_VERSION=${PG_MAJOR_VERSION}")
ADD_DEFINITIONS("-DPG_MINOR_VERSION=${PG_MINOR_VERSION}")
ADD_DEFINITIONS("-DPG_PATCH_VERSION=${PG_PATCH_VERSION}")
ADD_DEFINITIONS("-DPG_DISTRIBUTION_VERSION=\"${PG_DISTRIBUTION_VERSION}\"")

IF( CMAKE_BUILD_TYPE )
STRING(TOUPPER ${CMAKE_BUILD_TYPE} PEREGRINE_BUILD_TYPE)
ADD_DEFINITIONS("-D_${PEREGRINE_BUILD_TYPE}_")
ENDIF( CMAKE_BUILD_TYPE )

IF ( NOT WIN32 )
	SET( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
ENDIF ( NOT WIN32 )

STRING(TOLOWER "$ENV{OSNAME}" PEREGRINE_PLATFORM)
