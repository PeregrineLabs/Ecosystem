/*
 *  example.cpp
 *
 */

#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>

#include <sstream>

#ifdef Windows
#define DLLEXPORT __declspec(dllexport)
#else
#define DLLEXPORT __attribute__ ((visibility("default")))
#endif

DLLEXPORT MStatus initializePlugin( MObject obj )
{
	MStatus status;

	std::ostringstream PG_VERSION;
	PG_VERSION << PG_MAJOR_VERSION << "." << PG_MINOR_VERSION << "." << PG_PATCH_VERSION;

	MFnPlugin plugin(obj, "Some Company", PG_VERSION.str().c_str(), "Any");

	// register
	
	return status;
}

DLLEXPORT MStatus uninitializePlugin( MObject obj)
{
	MStatus   status;
	MFnPlugin plugin( obj );
		
	// de-register
	
	return status;
}
