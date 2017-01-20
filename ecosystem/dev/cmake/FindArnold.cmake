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
#  ARNOLD_INCLUDE_DIRS - Location of the 3delight includes
#  ARNOLD_LIB - Required libraries for all requested bindings
#  ARNOLD_FOUND - true if ARNOLD was found on the system
#  ARNOLD_LIBRARY_DIRS - the full set of library directories

FIND_PATH ( ARNOLD_BASE_DIR include/ai.h
  ENV ARNOLD
  )

IF ( ARNOLD_BASE_DIR )
	MESSAGE(STATUS "Found Arnold: ${ARNOLD_BASE_DIR}")
  	SET ( ARNOLD_LIBS ai )
  	SET ( ARNOLD_INCLUDE_DIRS ${ARNOLD_BASE_DIR}/include
    	CACHE STRING "Arnold include directories")
    IF ( WIN32 )
  	SET ( ARNOLD_LIBRARY_DIRS ${ARNOLD_BASE_DIR}/lib
    	CACHE STRING "Arnold library directories")
    ELSE ( WIN32 )
  	SET ( ARNOLD_LIBRARY_DIRS ${ARNOLD_BASE_DIR}/bin
    	CACHE STRING "Arnold library directories")
    ENDIF ( WIN32 )
	MESSAGE(STATUS "Found Arnold Libs: ${ARNOLD_LIBRARY_DIRS}")
  	SET ( ARNOLD_FOUND TRUE )
  	
  	LINK_DIRECTORIES( ${ARNOLD_LIBRARY_DIRS} )
ELSE ( ARNOLD_BASE_DIR )
	MESSAGE ( WARNING "Arnold not found!")
ENDIF ( ARNOLD_BASE_DIR )

FIND_PATH ( MTOA_BASE_DIR include/extension/Extension.h
  ENV MTOA
  )

IF ( MTOA_BASE_DIR )
	MESSAGE(STATUS "Found MTOA: ${MTOA_BASE_DIR}")
  	SET ( MTOA_LIBS mtoa_api )
  	SET ( MTOA_INCLUDE_DIRS ${MTOA_BASE_DIR}/include
    	CACHE STRING "MTOA include directories")
    IF ( WIN32 )
  	SET ( MTOA_LIBRARY_DIRS ${MTOA_BASE_DIR}/lib
    	CACHE STRING "MTOA library directories")
    ELSE ( WIN32 )
  	SET ( MTOA_LIBRARY_DIRS ${MTOA_BASE_DIR}/bin
    	CACHE STRING "MTOA library directories")
    ENDIF ( WIN32 )
  	SET ( MTOA_FOUND TRUE )
  	LINK_DIRECTORIES( ${MTOA_LIBRARY_DIRS} )
ELSE ( MTOA_BASE_DIR )
	MESSAGE ( WARNING "MTOA not found!")
ENDIF ( MTOA_BASE_DIR )
