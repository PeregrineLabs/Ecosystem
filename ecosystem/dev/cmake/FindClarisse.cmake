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
#  CLARISSE_INCLUDE_DIRS - Location of the 3delight includes
#  CLARISSE_LIBS - Required libraries for all requested bindings
#  CLARISSE_FOUND - true if VRAY was found on the system
#  CLARISSE_LIBRARY_DIRS - the full set of library directories

FIND_PATH ( CLARISSE_ROOT_LOCATION ./clarisse
    "$ENV{CLARISSE_ROOT}"
  )

FIND_PATH ( CLARISSE_SDK_LOCATION include/core_base_object.h
    "$ENV{CLARISSE_SDK_PATH}"
  )

IF ( CLARISSE_ROOT_LOCATION AND CLARISSE_SDK_LOCATION )
	MESSAGE(STATUS "Found Clarisse: ${CLARISSE_ROOT_LOCATION}")
	MESSAGE(STATUS "Found Clarisse SDK: ${CLARISSE_SDK_LOCATION}")
	  	
  	SET ( CLARISSE_INCLUDE_DIRS ${CLARISSE_SDK_LOCATION}/include CACHE STRING "Clarisse include directories")
    
  	SET ( CLARISSE_LIBRARY_DIRS ${CLARISSE_ROOT_LOCATION} CACHE STRING "Clarisse library directories")
    SET ( CLARISSE_LIBS ix_core ix_gmath ix_geometry ix_of ix_module ix_resource ix_poly ix_of ix_app ix_sys )
    
    SET( CLARISSE_DEFINITIONS "-fPIC")
    	
    LINK_DIRECTORIES( ${CLARISSE_LIBRARY_DIRS} )
    MESSAGE(STATUS "Found Clarisse Library Dirs: ${CLARISSE_LIBRARY_DIRS}")    
    
  	SET ( CLARISSE_FOUND TRUE )
ELSE ( CLARISSE_ROOT_LOCATION AND CLARISSE_SDK_LOCATION )
	MESSAGE ( WARNING "Clarisse not found!")
ENDIF ( CLARISSE_ROOT_LOCATION AND CLARISSE_SDK_LOCATION )
