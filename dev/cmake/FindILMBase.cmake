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
#  ILMBASE_INCLUDE_DIRS - Location of the ilmbase includes
#  ILMBASE_LIBRARIES - [TODO] Required libraries for all requested bindings
#  ILMBASE_FOUND - true if ILMBASE was found on the system
#  ILMBASE_LIBRARY_DIRS - the full set of library directories

FIND_PATH ( Ilmbase_Base_Dir include/OpenEXR/IlmBaseConfig.h
  ENV ILMBASE_ROOT
  )

IF ( Ilmbase_Base_Dir )

MESSAGE(STATUS "Found ILM Base: ${Ilmbase_Base_Dir}")

  SET ( ILMBASE_INCLUDE_DIRS
    ${Ilmbase_Base_Dir}/include
    ${Ilmbase_Base_Dir}/include/OpenEXR
    CACHE STRING "ILMBase include directories")
  SET ( ILMBASE_LIBRARY_DIRS ${Ilmbase_Base_Dir}/lib
    CACHE STRING "ILMBase library directories")
  SET ( ILMBASE_FOUND TRUE )

	INCLUDE_DIRECTORIES( ${ILMBASE_INCLUDE_DIRS} )
	LINK_DIRECTORIES( ${ILMBASE_LIBRARY_DIRS} )
ELSE ( Ilmbase_Base_Dir )
	MESSAGE ( FATAL_ERROR "ILM Base not found!")
ENDIF ( Ilmbase_Base_Dir )
