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
#  VRAYBETA_INCLUDE_DIRS - Location of the 3delight includes
#  VRAYBETA_LIB - Required libraries for all requested bindings
#  VRAYBETA_FOUND - true if VRAY was found on the system
#  VRAYBETA_LIBRARY_DIRS - the full set of library directories

FIND_PATH ( VRAYBETA_LOCATION include/vraycore.h
    "$ENV{VRAYBETA_ROOT}"
    "$ENV{VRAYBETA_ROOT}/vray/"
  )

SET ( MAYA_VERSION $ENV{MAYA_VERSION} )

IF ( VRAYBETA_LOCATION )
	MESSAGE(STATUS "Found VRay: ${VRAYBETA_LOCATION}")
	
  	SET ( VRAYBETA_LIB vray )
  	
  	SET ( VRAYBETA_INCLUDE_DIRS ${VRAYBETA_LOCATION}/include
    	CACHE STRING "VRay include directories")
    
    IF ( WIN32 )
	IF ( MAYA_VERSION EQUAL 2012 )
    SET ( VRAYBETA_LIBRARY_DIRS ${VRAYBETA_LOCATION}/lib/x64/vc91 
    	CACHE STRING "VRay library directories")
	ELSEIF ( MAYA_VERSION EQUAL 2013 )
    SET ( VRAYBETA_LIBRARY_DIRS ${VRAYBETA_LOCATION}/lib/x64/vc101 
    	CACHE STRING "VRay library directories")
	ELSEIF ( MAYA_VERSION EQUAL 2014 )
    SET ( VRAYBETA_LIBRARY_DIRS ${VRAYBETA_LOCATION}/lib/x64/vc101 
    	CACHE STRING "VRay library directories")
	ELSE ( MAYA_VERSION EQUAL 2015 )
    SET ( VRAYBETA_LIBRARY_DIRS ${VRAYBETA_LOCATION}/lib/x64/vc11 
    	CACHE STRING "VRay library directories")
	ENDIF ( MAYA_VERSION EQUAL 2012 )
	MESSAGE(STATUS "VRay Library Dirs: ${VRAYBETA_LIBRARY_DIRS}")
    SET ( VRAYBETA_LIBS plugman_s vray rayserver_s vutils_s )
    ELSE( WIN32 )
    IF ( APPLE )
		FIND_PATH ( VRAYBETA_OSX_LIBRARY_DIRS libplugman_s.a
			${VRAYBETA_LOCATION}/lib/mountain_lion_x64/gcc-4.2
			${VRAYBETA_LOCATION}/lib/snow_leopard_x64/gcc-4.2
		)
  		SET ( VRAYBETA_LIBRARY_DIRS ${VRAYBETA_OSX_LIBRARY_DIRS} CACHE STRING "VRay library directories")
    ELSE ( APPLE )
		FIND_PATH ( VRAYBETA_LINUX_LIBRARY_DIRS libvray.so
			${VRAYBETA_LOCATION}/lib/linux_x64/gcc-4.1
			${VRAYBETA_LOCATION}/lib/linux_x64/gcc-4.4
		)
  		SET ( VRAYBETA_LIBRARY_DIRS ${VRAYBETA_LINUX_LIBRARY_DIRS} CACHE STRING "VRay library directories")
    ENDIF( APPLE )
    SET ( VRAYBETA_LIBS plugman_s rayserver_s vutils_s vray plugman_s rayserver_s vutils_s )
    ENDIF ( WIN32 )
    
    SET( VRAYBETA_DEFINITIONS 
	  "-DREQUIRE_IOSTREAM -DHAVE_EXR -DVRAYBETA_NO_GUI -D__VRAY4MAYA20__ -DBits64_ -D_REENTRANT"
	)
    	
    LINK_DIRECTORIES( ${VRAYBETA_LIBRARY_DIRS} )
	MESSAGE(STATUS "Found VRay BETA Library Dirs: ${VRAYBETA_LIBRARY_DIRS}")    
    
  	SET ( VRAYBETA_FOUND TRUE )
  	
ELSE ( VRAYBETA_LOCATION )
	MESSAGE ( WARNING "VRay BETA not found!")
ENDIF ( VRAYBETA_LOCATION )
