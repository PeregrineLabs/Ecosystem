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
#  PLATEAU_INCLUDE_DIRS - Location of the ilmbase includes
#  PLATEAU_LIBRARIES - [TODO] Required libraries for all requested bindings
#  PLATEAU_FOUND - true if ILMBASE was found on the system
#  PLATEAU_LIBRARY_DIRS - the full set of library directories

MESSAGE(STATUS "Found Build: ${CMAKE_BUILD_TYPE}")

FIND_PATH ( Plateau_Base_Dir include/pgUtils.h
  $ENV{DEV_BASE}/build/${CMAKE_SYSTEM_NAME}/${CMAKE_BUILD_TYPE}
	NO_DEFAULT_PATH
  )

IF ( Plateau_Base_Dir )
MESSAGE(STATUS "Found Plateau: ${Plateau_Base_Dir}")

    FIND_LIBRARY(PLATEAU_LIBRARIES pgPlateau
      ${Plateau_Base_Dir}
    )
    if( PLATEAU_LIBRARIES )
    MESSAGE(STATUS "Plateau Libraries: ${PLATEAU_LIBRARIES}")

  SET ( PLATEAU_INCLUDE_DIRS ${Plateau_Base_Dir}/include
    CACHE STRING "Plateau include directories")
  SET ( PLATEAU_LIBRARY_DIRS ${Plateau_Base_Dir}
    CACHE STRING "Plateau library directories")

MESSAGE(STATUS "Plateau Includes: ${PLATEAU_INCLUDE_DIRS}")
	
  SET ( PLATEAU_FOUND TRUE )

	INCLUDE_DIRECTORIES( ${PLATEAU_INCLUDE_DIRS} )
	LINK_DIRECTORIES( ${PLATEAU_LIBRARY_DIRS} )
ELSE ( Plateau_Base_Dir )
	MESSAGE ( FATAL_ERROR "Couldn't find Plateau!")
	    endif( PLATEAU_LIBRARIES )
ENDIF ( Plateau_Base_Dir )
