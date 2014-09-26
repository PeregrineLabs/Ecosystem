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

# This module will define the following variables:
#  GMAGICK_INCLUDE_DIRS - Location of the GMAGICK includes
#  GMAGICK_LIBRARIES - [TODO] Required libraries for all requested bindings
#  GMAGICK_FOUND - true if GMAGICK was found on the system
#  GMAGICK_LIBRARY_DIRS - the full set of library directories

IF ( WIN32 )
FIND_PATH ( GMAGICK_Base_Dir include/magick/magick.h
  ENV GMAGICK_ROOT
  )
ELSE ( WIN32 )
FIND_PATH ( GMAGICK_Base_Dir include/GraphicsMagick/magick/magick.h
  ENV GMAGICK_ROOT
  /opt/local
  )
ENDIF(WIN32)

IF ( GMAGICK_Base_Dir )

MESSAGE(STATUS "Found Graphics Magick: ${GMAGICK_Base_Dir}")
IF ( WIN32 )
SET ( GMAGICK_INCLUDE_DIRS
  ${GMAGICK_Base_Dir}/include
  CACHE STRING "GMAGICK include directories")
ELSE ( WIN32 )
  SET ( GMAGICK_INCLUDE_DIRS
    ${GMAGICK_Base_Dir}/include/GraphicsMagick
    CACHE STRING "GMAGICK include directories")
ENDIF ( WIN32 )
  SET ( GMAGICK_LIBRARY_DIRS ${GMAGICK_Base_Dir}/lib
    CACHE STRING "GMAGICK library directories")
IF ( WIN32 )
  SET ( GMAGICK_LIBRARIES CORE_RL_magick_ )
ELSE ( WIN32 )
  SET ( GMAGICK_LIBRARIES GraphicsMagick++ GraphicsMagick lcms tiff freetype jpeg png bz2 xml2 z m gomp pthread ltdl )
ENDIF ( WIN32 )
  SET ( GMAGICK_FOUND TRUE )

	INCLUDE_DIRECTORIES( ${GMAGICK_INCLUDE_DIRS} )
	LINK_DIRECTORIES( ${GMAGICK_LIBRARY_DIRS} )
ELSE ( GMAGICK_Base_Dir )
	MESSAGE ( FATAL_ERROR "Graphics Magick not found!")
ENDIF ( GMAGICK_Base_Dir )
