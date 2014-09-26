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
#  GLOG_INCLUDES - Location of the GLOG includes
#  GLOG_LIBRARIES - Required libraries for all requested bindings
#  GLOG_FOUND - true if GLOG was found on the system

FIND_PATH ( GLOG_INCLUDES 
  $ENV{GLOG_PATH}/include/
  /usr/include
  /usr/local/include
  /sw/include
  /opt/local/include )

FIND_LIBRARY(GLOG_LIBRARIES
  NAMES glog
  PATHS
  $ENV{GLOG_PATH}/lib/
  /usr/lib64
  /usr/lib
  /usr/local/lib64
  /usr/local/lib
  /sw/lib
  /opt/local/lib
  DOC "The Glog library")

if(GLOG_INCLUDES AND GLOG_LIBRARIES)
  set(GLOG_FOUND TRUE)
  if (VERBOSE)
      message(STATUS "Found Glog library ${GLOG_LIBRARIES}")
      message(STATUS "Found Glog includes ${GLOG_INCLUDES}")
  endif ()
else()
  set(GLOG_FOUND FALSE)
  message(STATUS "Glog not found. Specify GLOG_PATH to locate it")
endif()

