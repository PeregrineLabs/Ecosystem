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
#  RMS_INCLUDE_DIRS - Location of the RenderManStudio includes
#  RMS_LIB - Required libraries for all requested bindings
#  RMS_FOUND - true if RMS was found on the system
#  RMS_LIBRARY_DIRS - the full set of library directories

IF ( WIN32 )
SET ( RMSLIBFULL libprman.dll )
ELSE ( WIN32 )
	IF ( APPLE )
		SET ( RMSLIBFULL libprman.dylib )
	ELSE ( APPLE )
		SET ( RMSLIBFULL libprman.so )
	ENDIF ( APPLE )
ENDIF ( WIN32 )

FIND_PATH ( RMS_Base_Dir rmantree/lib/${RMANLIBFULL}
  ENV RMSTREE
  )
  
IF ( RMS_Base_Dir AND PRMAN_Base_Dir )

MESSAGE(STATUS "Found Render Man Studio ( and compatible Prman headers ): ${RMS_Base_Dir}, Headers: ${PRMAN_Base_Dir}/include}")

	SET ( RMS_INCLUDE_DIRS ${PRMAN_Base_Dir}/include
    	CACHE STRING "RenderManStudio include directories")
    
	IF ( WIN32 )	
 		SET ( RMS_LIBRARY_DIRS ${RMS_Base_Dir}/lib
    		CACHE STRING "RenderManStudio library directories")
 		SET ( RMS_LIB RenderMan_for_Maya )
	ELSE ( WIN32 )
 		SET ( RMS_LIBRARY_DIRS ${RMS_Base_Dir}/rmantree/lib
    		CACHE STRING "RenderManStudio library directories")
 		SET ( RMS_LIB prman )
	ENDIF ( WIN32 )

	SET ( RMS_FOUND TRUE )
  
ELSE ( RMS_Base_Dir AND PRMAN_Base_Dir )
	MESSAGE ( WARNING "Render Man Studio not found!")
ENDIF ( RMS_Base_Dir AND PRMAN_Base_Dir )
