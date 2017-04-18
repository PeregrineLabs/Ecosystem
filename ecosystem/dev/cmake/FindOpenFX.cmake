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
#  OPENFX_INCLUDE_DIRS - Location of the 3delight includes
#  OPENFX_FOUND - true if ARNOLD was found on the system

FIND_PATH ( OPENFX_BASE_DIR include/ofxCore.h
  ENV OPENFX_SDK
  )

IF ( OPENFX_BASE_DIR )
	MESSAGE(STATUS "Found OpenFX: ${OPENFX_BASE_DIR}")
  	SET ( OPENFX_INCLUDE_DIR ${OPENFX_BASE_DIR}/include CACHE STRING "OpenFX include directories")
	SET( OPENFX_EXTENSION ".ofx" )
  	SET ( OPENFX_FOUND TRUE )
ELSE ( OPENFX_BASE_DIR )
	MESSAGE ( WARNING "OpenFX not found!")
ENDIF ( OPENFX_BASE_DIR )

INCLUDE_DIRECTORIES( ${OPENFX_INCLUDE_DIR} )
