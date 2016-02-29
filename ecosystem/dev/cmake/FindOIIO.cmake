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
#  OIIO_INCLUDES - Location of the OIIO includes
#  OIIO_LIBRARIES - [TODO] Required libraries for all requested bindings
#  OIIO_FOUND - true if OIIO was found on the system

FIND_PATH ( OIIO_INCLUDES OpenImageIO/imageio.h
  $ENV{OIIO_PATH}/include/
  /usr/include
  /usr/local/include
  /sw/include
  /opt/local/include
  DOC "The directory where OpenImageIo/imageio.h resides")

FIND_LIBRARY(OIIO_LIBRARIES
  NAMES OpenImageIO
  PATHS
  $ENV{OIIO_PATH}/lib/
  /usr/lib64
  /usr/lib
  /usr/local/lib64
  /usr/local/lib
  /sw/lib
  /opt/local/lib
  DOC "The OIIO library")

if(OIIO_INCLUDES AND OIIO_LIBRARIES)
  set(OIIO_FOUND TRUE)
  if (VERBOSE)
      message(STATUS "Found OIIO library ${OIIO_LIBRARIES}")
      message(STATUS "Found OIIO includes ${OIIO_INCLUDES}")
  endif ()
else()
  set(OIIO_FOUND FALSE)
  message(STATUS "OIIO not found. Specify OIIO_PATH to locate it")
endif()

