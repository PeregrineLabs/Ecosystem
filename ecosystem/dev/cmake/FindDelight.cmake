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
#  DELIGHT_INCLUDE_DIRS - Location of the 3delight includes
#  DELIGHT_LIB - Required libraries for all requested bindings
#  DELIGHT_FOUND - true if DELIGHT was found on the system
#  DELIGHT_LIBRARY_DIRS - the full set of library directories

FIND_PATH ( Delight_Base_Dir include/delight.h
  ENV DELIGHT
  )

IF ( Delight_Base_Dir )
	MESSAGE(STATUS "Found 3Delight: ${Delight_Base_Dir}")
  	SET ( DELIGHT_LIB 3delight )
  	SET ( DELIGHT_INCLUDE_DIRS ${Delight_Base_Dir}/include
    	CACHE STRING "Delight include directories")
  	SET ( DELIGHT_LIBRARY_DIRS ${Delight_Base_Dir}/lib
    	CACHE STRING "Delight library directories")
  	SET ( DELIGHT_FOUND TRUE )
ELSE ( Delight_Base_Dir )
	MESSAGE ( WARNING "3Delight not found!")
ENDIF ( Delight_Base_Dir )
