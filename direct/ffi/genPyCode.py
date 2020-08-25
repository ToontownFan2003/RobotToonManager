#! /usr/bin/env python
### Generated automatically by ppremake 1.22 from genPyCode.pp.
################################ DO NOT EDIT ###########################

import os
import sys
import glob

# This script was generated while the user was using the ctattach
# tools.  That had better still be the case.

def deCygwinify(path):
    if os.name in ['nt'] and path[0] == '/':
        # On Windows, we may need to convert from a Cygwin-style path
        # to a native Windows path.

        # Check for a case like /i/ or /p/: this converts
        # to i:/ or p:/.

        dirs = path.split('/')
        if len(dirs) > 2 and len(dirs[1]) == 1:
            path = '%s:\%s' % (dirs[1], '\\'.join(dirs[2:]))

        else:
            # Otherwise, prepend $PANDA_ROOT and flip the slashes.
            pandaRoot = os.getenv('PANDA_ROOT')
            if pandaRoot:
                path = os.path.normpath(pandaRoot + path)

    return path

ctprojs = os.getenv('CTPROJS')
if not ctprojs:
    print "You are no longer attached to any trees!"
    sys.exit(1)

directDir = os.getenv('DIRECT')
if not directDir:
    print "You are not attached to DIRECT!"
    sys.exit(1)

directDir = deCygwinify(directDir)

# Make sure that direct.showbase.FindCtaPaths gets imported.
parent, base = os.path.split(directDir)

if parent not in sys.path:
    sys.path.append(parent)

import direct.showbase.FindCtaPaths

from direct.ffi import DoGenPyCode
from direct.ffi import FFIConstants

# The following parameters were baked in to this script at the time
# ppremake was run in Direct.

DoGenPyCode.interrogateLib = r'libdtoolconfig'
DoGenPyCode.codeLibs = r'libpandaexpress libpanda libpandaphysics libdirect libpandafx libpandafx libpandaegg libpandaode'.split()
DoGenPyCode.native = 1

# The user is expected to be using ctattach, so don't bake in the
# following four; these instead come from the dynamic settings set by
# ctattach.

DoGenPyCode.directDir = directDir
DoGenPyCode.outputCodeDir = os.path.join(directDir, 'built', 'lib', 'pandac')
DoGenPyCode.outputHTMLDir = os.path.join(directDir, 'built', 'shared', 'doc')
DoGenPyCode.extensionsDir = os.path.join(directDir, 'src', 'extensions_native')
DoGenPyCode.etcPath = []
DoGenPyCode.pythonSourcePath = []

# Look for additional packages (other than the basic three)
# that the user might be dynamically attached to.
packages = []
for proj in ctprojs.split():
    projName = proj.split(':')[0]
    packages.append(projName)
packages.reverse()

for package in packages:
    packageDir = os.getenv(package)
    if packageDir:
        packageDir = deCygwinify(packageDir)
        etcDir = os.path.join(packageDir, 'etc')
        try:
            inFiles = glob.glob(os.path.join(etcDir, 'built', '*.in'))
        except:
            inFiles = []
        if inFiles:
            DoGenPyCode.etcPath.append(etcDir)

        if package not in ['WINTOOLS', 'DTOOL', 'DIRECT', 'PANDA']:
	    DoGenPyCode.pythonSourcePath.append(packageDir)

            libDir = os.path.join(packageDir, 'built', 'lib')
            try:
                files = os.listdir(libDir)
            except:
                files = []
            for file in files:
                if os.path.isfile(os.path.join(libDir, file)):
                    basename, ext = os.path.splitext(file)

                    # Try to import the library.  If we can import it,
                    # instrument it.
                    try:
                        __import__(basename, globals(), locals())
                        isModule = 1
                    except:
                        isModule = 0

                    #
                    # RHH.... hack OPT2 .. py debug libraries...
                    #
                    if not isModule:
                        # debug py library magin naming in windows..
                        basename = basename.replace('_d','')
                        try:
                            __import__(basename, globals(), locals())
                            isModule = 1
                        except:
                            isModule = 0

                    if isModule:
                        if basename not in DoGenPyCode.codeLibs:
                            DoGenPyCode.codeLibs.append(basename)

DoGenPyCode.run()

