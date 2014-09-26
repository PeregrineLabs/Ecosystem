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
#  RLM_INCLUDE_DIRS - Location of the RLM includes
#  RLM_LIBRARIES - [TODO] Required libraries for all requested bindings
#  RLM_FOUND - true if RLM was found on the system
#  RLM_LIBRARY_DIRS - the full set of library directories

FIND_PATH ( RLM_Base_Dir src/license_to_run.h
  ENV RLM_ROOT
  )

IF ( RLM_Base_Dir )

MESSAGE(STATUS "Found RLM: ${RLM_Base_Dir}")
	IF( WIN32 )
		SET( RLM_LIBRARIES rlmclient Ws2_32 )
		SET( RLM_PLATFORM x64_w3 )
	ELSE( WIN32 )
		IF ( APPLE )
			SET( RLM_PLATFORM x64_m1 )
			SET( RLM_LIBRARIES rlm )
		ELSE( APPLE )
			SET( RLM_PLATFORM x64_l1 )	
			SET( RLM_LIBRARIES ${RLM_Base_Dir}/${RLM_PLATFORM}/rlm.a )
		ENDIF( APPLE )
	ENDIF( WIN32 )
	
	

  SET ( RLM_INCLUDE_DIRS
    ${RLM_Base_Dir}/src
    CACHE STRING "RLM include directories")
  SET ( RLM_LIBRARY_DIRS ${RLM_Base_Dir}/${RLM_PLATFORM}
    CACHE STRING "RLM library directories")
  SET ( RLM_FOUND TRUE )

	INCLUDE_DIRECTORIES( ${RLM_INCLUDE_DIRS} )
	LINK_DIRECTORIES( ${RLM_LIBRARY_DIRS} )
ELSE ( RLM_Base_Dir )
	MESSAGE ( FATAL_ERROR "RLM not found!")
ENDIF ( RLM_Base_Dir )
