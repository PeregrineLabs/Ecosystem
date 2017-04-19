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
#  VRAY_INCLUDE_DIRS - Location of the 3delight includes
#  VRAY_LIB - Required libraries for all requested bindings
#  VRAY_FOUND - true if VRAY was found on the system
#  VRAY_LIBRARY_DIRS - the full set of library directories

FIND_PATH ( VRAY_LOCATION include/vraycore.h
    "$ENV{VRAY_ROOT}"
    "$ENV{VRAY_ROOT}/vray/"
  )

SET ( MAYA_VERSION $ENV{MAYA_VERSION} )

IF ( VRAY_LOCATION )
	MESSAGE(STATUS "Found VRay: ${VRAY_LOCATION}")
	
  	SET ( VRAY_LIB vray )
  	
  	SET ( VRAY_INCLUDE_DIRS ${VRAY_LOCATION}/include
    	CACHE STRING "VRay include directories")
    
    IF ( WIN32 )
	IF ( MAYA_VERSION EQUAL 2012 )
    SET ( VRAY_LIBRARY_DIRS ${VRAY_LOCATION}/lib/x64/vc91 
    	CACHE STRING "VRay library directories")
	ELSEIF ( MAYA_VERSION EQUAL 2013 )
    SET ( VRAY_LIBRARY_DIRS ${VRAY_LOCATION}/lib/x64/vc101 
    	CACHE STRING "VRay library directories")
	ELSEIF ( MAYA_VERSION EQUAL 2014 )
    SET ( VRAY_LIBRARY_DIRS ${VRAY_LOCATION}/lib/x64/vc101 
    	CACHE STRING "VRay library directories")
	ELSE ( MAYA_VERSION EQUAL 2015 )
    SET ( VRAY_LIBRARY_DIRS ${VRAY_LOCATION}/lib/x64/vc11 
    	CACHE STRING "VRay library directories")
	ENDIF ( MAYA_VERSION EQUAL 2012 )
	MESSAGE(STATUS "VRay Library Dirs: ${VRAY_LIBRARY_DIRS}")
    SET ( VRAY_LIBS plugman_s vray rayserver_s vutils_s )
    ELSE( WIN32 )
    IF ( APPLE )
		FIND_PATH ( VRAY_OSX_LIBRARY_DIRS libplugman_s.a
			${VRAY_LOCATION}/lib/mavericks_x64/gcc-4.2-cpp
			${VRAY_LOCATION}/lib/mavericks_x64/gcc-4.2
			${VRAY_LOCATION}/lib/mountain_lion_x64/gcc-4.2
			${VRAY_LOCATION}/lib/snow_leopard_x64/gcc-4.2
		)
  		SET ( VRAY_LIBRARY_DIRS ${VRAY_OSX_LIBRARY_DIRS} CACHE STRING "VRay library directories")
    ELSE ( APPLE )
		FIND_PATH ( VRAY_LINUX_LIBRARY_DIRS libvray.so
			${VRAY_LOCATION}/lib/linux_x64/gcc-4.1
			${VRAY_LOCATION}/lib/linux_x64/gcc-4.4
		)
  		SET ( VRAY_LIBRARY_DIRS ${VRAY_LINUX_LIBRARY_DIRS} CACHE STRING "VRay library directories")
    ENDIF( APPLE )
    SET ( VRAY_LIBS plugman_s rayserver_s vutils_s vray plugman_s rayserver_s vutils_s )
    ENDIF ( WIN32 )
    
    SET( VRAY_DEFINITIONS 
	  "-DREQUIRE_IOSTREAM -DHAVE_EXR -DVRAY_NO_GUI -D__VRAY4MAYA20__ -DBits64_ -D_REENTRANT"
	)
    	
    LINK_DIRECTORIES( ${VRAY_LIBRARY_DIRS} )
	MESSAGE(STATUS "Found VRay Library Dirs: ${VRAY_LIBRARY_DIRS}")    
    
  	SET ( VRAY_FOUND TRUE )
  	
ELSE ( VRAY_LOCATION )
	MESSAGE ( WARNING "VRay not found!")
ENDIF ( VRAY_LOCATION )
