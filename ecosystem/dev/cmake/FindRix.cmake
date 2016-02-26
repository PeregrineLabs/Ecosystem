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
#  RIX_INCLUDE_DIRS - Location of the RIX includes
#  RIX_LIB - Required libraries for all requested bindings
#  RIX_FOUND - true if ILMBASE was found on the system
#  RIX_LIBRARY_DIRS - the full set of library directories

FIND_PATH ( RIX_Base_Dir include/prmanapi.h
  ENV LIBRIX
  )

IF ( RIX_Base_Dir )

	MESSAGE(STATUS "Found RIX: ${RIX_Base_Dir}")

	IF ( WIN32 )	
		SET ( RIX_LIB librix )
	ELSE ( WIN32 )
		SET ( RIX_LIB rix )
	ENDIF ( WIN32 )

  	SET ( RIX_INCLUDE_DIRS ${RIX_Base_Dir}/include
    	CACHE STRING "RIX include directories")
  	SET ( RIX_LIBRARY_DIRS ${RIX_Base_Dir}/lib
    	CACHE STRING "RIX library directories")

    LINK_DIRECTORIES( ${RIX_LIBRARY_DIRS} )

  	SET ( RIX_FOUND TRUE )
ELSE ( RIX_Base_Dir )
	MESSAGE ( WARNING "RIX not found!")
ENDIF ( RIX_Base_Dir )
