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
#  WM_INCLUDE_DIRS - Location of the WildMagic includes
#  WM_LIBRARIES - [TODO] Required libraries for all requested bindings
#  WM_FOUND - true if WildMagic was found on the system
#  WM_LIBRARY_DIRS - the full set of library directories

FIND_PATH ( WM_Base_Dir SDK/Include/Wm5Core.h
  ENV WM_ROOT
  )

IF ( WM_Base_Dir )

MESSAGE(STATUS "Found Wild Magic: ${WM_Base_Dir}")
  SET ( WM_INCLUDE_DIRS
    ${WM_Base_Dir}/SDK/Include
    CACHE STRING "WildMagic include directories")
  SET ( WM_LIBRARY_DIRS ${WM_Base_Dir}/SDK/Library/${CMAKE_BUILD_TYPE}
    CACHE STRING "WildMagic library directories")
  SET ( WM_FOUND TRUE )

	INCLUDE_DIRECTORIES( ${WM_INCLUDE_DIRS} )
	LINK_DIRECTORIES( ${WM_LIBRARY_DIRS} )
	
	IF( WildMagic_FIND_COMPONENTS )
	  FOREACH( component ${WildMagic_FIND_COMPONENTS} )
	    SET(WM_${component}_LIBRARY_RELEASE "Wm5${component}")
	    SET(WM_${component}_LIBRARY_DEBUG "Wm5${component}d")
	    
	    SET(WM_${component}_LIBRARY       optimized ${WM_${component}_LIBRARY_RELEASE} debug ${WM_${component}_LIBRARY_DEBUG}) 
	    SET( WM_LIBRARIES ${WM_LIBRARIES} ${WM_${component}_LIBRARY} )
	  ENDFOREACH( component )
	
	ENDIF( WildMagic_FIND_COMPONENTS )
	MESSAGE(STATUS "Found Wild Magic Components: ${WM_LIBRARIES}")
ELSE ( WM_Base_Dir )
	MESSAGE ( FATAL_ERROR "WildMagic not found!")
ENDIF ( WM_Base_Dir )
