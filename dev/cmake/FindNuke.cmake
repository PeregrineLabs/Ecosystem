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
#
# NUKE_FOUND            set if Nuke is found.
# NUKE_INCLUDE_DIR      Nuke's include directory
# NUKE_LIBRARY_DIR      Nuke's library directory
# NUKE_LIBRARIES        all nuke libraries

SET( NUKE_FOUND "NO" )

##
## Obtain Nuke install location
##

FIND_PATH( NUKE_LOCATION include/DDImage/NukeWrapper.h
  $ENV{NUKE}
  /usr/local
  /usr
)

IF (NUKE_LOCATION)
  MESSAGE ( STATUS "Found Nuke: ${NUKE_LOCATION}" )
  SET( NUKE_FOUND "YES" )
ENDIF (NUKE_LOCATION)

SET( NUKE_VERSION "$ENV{NUKE_VERSION}" )
IF (NUKE_VERSION)
  MESSAGE ( STATUS "Found Nuke Version: ${NUKE_VERSION}" )
  SET( NUKE_MAJOR_VERSION "$ENV{NUKE_MAJOR_VERSION}" )
  SET( NUKE_MINOR_VERSION "$ENV{NUKE_MINOR_VERSION}" )
ELSE (NUKE_VERSION)
	MESSAGE( FATAL_ERROR "Nuke Version not defined!" )
ENDIF (NUKE_VERSION)

SET( NUKE_INCLUDE_DIR       "${NUKE_LOCATION}/include" )
SET( NUKE_LIBRARY_DIR       "${NUKE_LOCATION}" )
FIND_LIBRARY( NUKE_nuke_LIBRARY DDImage
  ${NUKE_LIBRARY_DIR}
  NO_DEFAULT_PATH
  )

  MESSAGE ( STATUS "Found Nuke Libraries: ${NUKE_nuke_LIBRARY}" )

IF ( WIN32 )
  SET( NUKE_LIBRARIES 
    ${NUKE_nuke_LIBRARY}
    )
ELSE (WIN32 )
  IF (CMAKE_BUILD_TYPE MATCHES Debug)
    SET ( GCOV_LIB "gcov" )
  ENDIF (CMAKE_BUILD_TYPE MATCHES Debug)
  SET( NUKE_LIBRARIES 
    ${NUKE_nuke_LIBRARY} dl
    )
STRING ( REGEX MATCH "[/a-zA-Z0-9.]*/"
  NUKE_LIBRARY_DIR "${NUKE_nuke_LIBRARY}")
 
ENDIF ( WIN32 ) 
  

INCLUDE_DIRECTORIES( ${NUKE_INCLUDE_DIR} )
LINK_DIRECTORIES( ${NUKE_LIBRARY_DIR} )
