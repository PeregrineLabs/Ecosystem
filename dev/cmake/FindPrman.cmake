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
#  PRMAN_INCLUDE_DIRS - Location of the Prman includes
#  PRMAN_LIB - Required libraries for all requested bindings
#  PRMAN_FOUND - true if ILMBASE was found on the system
#  PRMAN_LIBRARY_DIRS - the full set of library directories

FIND_PATH ( PRMAN_Base_Dir include/prmanapi.h
  ENV RMANTREE
  )

IF ( PRMAN_Base_Dir )

	MESSAGE(STATUS "Found Prman: ${PRMAN_Base_Dir}")

	IF ( WIN32 )	
		SET ( PRMAN_LIB libprman )
	ELSE ( WIN32 )
		SET ( PRMAN_LIB prman )
	ENDIF ( WIN32 )

  	SET ( PRMAN_INCLUDE_DIRS ${PRMAN_Base_Dir}/include
    	CACHE STRING "Prman include directories")
  	SET ( PRMAN_LIBRARY_DIRS ${PRMAN_Base_Dir}/lib
    	CACHE STRING "Prman library directories")
  	SET ( PRMAN_FOUND TRUE )
ELSE ( PRMAN_Base_Dir )
	MESSAGE ( WARNING "Prman not found!")
ENDIF ( PRMAN_Base_Dir )
