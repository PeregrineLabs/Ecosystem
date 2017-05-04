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
#  REDSHIFT_INCLUDE_DIRS - Location of the 3delight includes
#  REDSHIFT_LIBS - Required libraries for all requested bindings
#  REDSHIFT_FOUND - true if VRAY was found on the system
#  REDSHIFT_LIBRARY_DIRS - the full set of library directories

FIND_PATH ( REDSHIFT_LOCATION include/RS.h
    "$ENV{REDSHIFT_SDK_PATH}"
  )

SET ( MAYA_VERSION $ENV{MAYA_VERSION} )

IF ( REDSHIFT_LOCATION )
	 MESSAGE(STATUS "Found Redshift: ${REDSHIFT_LOCATION}")
	  	
  	SET ( REDSHIFT_INCLUDE_DIRS ${REDSHIFT_LOCATION}/include CACHE STRING "Redshift include directories")
    
    IF ( WIN32 )
      SET ( REDSHIFT_LIBRARY_DIRS ${REDSHIFT_LOCATION}/lib/x64 CACHE STRING "Redshift library directories")
      SET ( REDSHIFT_LIBS redshift-core-vc100 )
    ELSE( WIN32 )
  		SET ( REDSHIFT_LIBRARY_DIRS ${REDSHIFT_LOCATION}/lib CACHE STRING "Redshift library directories")
      SET ( REDSHIFT_LIBS redshift-core )
    ENDIF ( WIN32 )
    
    SET( REDSHIFT_DEFINITIONS "-fPIC")
    	
    LINK_DIRECTORIES( ${REDSHIFT_LIBRARY_DIRS} )
    MESSAGE(STATUS "Found Redshift Library Dirs: ${REDSHIFT_LIBRARY_DIRS}")    
    
  	SET ( REDSHIFT_FOUND TRUE )
ELSE ( REDSHIFT_LOCATION )
	MESSAGE ( WARNING "Redshift not found!")
ENDIF ( REDSHIFT_LOCATION )
