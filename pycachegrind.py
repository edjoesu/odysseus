#!/usr/bin/env python
"""
Profile a script using hotshot and kcachegrind.

This program runs a script under the control of the Python hotshot profiler and
converts the hotshot results into the Kcachegrind format.  It finally calls
kcachegrind to visualize the output.


Usage:

  pycachegrind.py script.py [script args]

Any arguments after your script name are passed directly to the script in
sys.argv.

This program leaves two files on disk:

  - script.py.prof: hotshot profile results.

  - script.py.cgrind: hotshot results converted to cachegrind format.
  

Requirements:

  - kcachegrind.  Used to visualize the results.  It includes hotshot2calltree,
    the default converter from hotshot to cachegrind format.

Optional:
    
  - hotshot2cachegrind.py.  This is hotshot2calltree's ancestor, and if you
  experience any problems with h2ctree, you may want to test this script
  instead (I'm not sure, but I've seen a few minor problems that /might/ be
  bugs in h2ctree).  I've put up a copy of hotshot2cachegrind on the net, since
  it is not easy to find:

      http://amath.colorado.edu/faculty/fperez/python/profiling

  You'll need to modify a global constant in the source if you wish to use
  hotshot2cachegrind instead of hotshot2calltree.

    
Acknowledgements:

  This code is heavily inspired in scripts written by Arnd Baecker and Nikolai
  Hlubek, and posted to the SciPy mailing lists.
"""

#*****************************************************************************
#     Copyright (C) 2006 Fernando Perez. <Fernando.Perez@colorado.edu>
#
#             Distributed under the terms of the BSD License.
#
#*****************************************************************************

__author__ = 'Fernando Perez <Fernando.Perez@colorado.edu>'
__url__ =  'http://amath.colorado.edu/faculty/fperez/python/profiling'
__license__ = 'BSD'

# Tweak any constants you may want here

# Select the converter from hotshot format to callgrind format
HOTSHOT2CG = 'hotshot2calltree'

#HOTSHOT2CG = 'hotshot2cachegrind.py'
#HOTSHOT2CG = '/home/ralf/data/analysis/python/hotshot2cachegrind.py'


#############################################################################
# No user-serviceable parts below.
#############################################################################

# Stdlib imports
import hotshot
import os
import sys

# Main code starts.  The run() routine is as simple as possible so that it
# produces the least amount of extraneous information in the profile results.

def run(code):
    loc = locals()
    loc['__name__'] = '__main__'
    loc['__file__'] = sys.argv[0]
    exec code in loc

def main():
    # Simple args processing
    try:
        fname = sys.argv[1]
    except IndexError:
        print __doc__
        sys.exit(1)

    # Read and compile source
    f = file(fname,'r')
    source = f.read()
    f.close()

    # Precompile the source so we don't see compilation times in the profile.
    # Let any generated exceptions propagate out.
    code = compile(source,fname,'exec')

    # Build filenames for outputs
    base_fname = os.path.basename(fname)
    prof_fname = base_fname+'.prof'
    cgr_fname = base_fname+'.cgrind'

    # Build the profiler object
    prof = hotshot.Profile(prof_fname, lineevents=1)
    # Modify sys.argv so the executed code sees it as if it were running
    # standalone
    sys.argv[:] = sys.argv[1:]
    try:
        prof.runcall(run,code)
    finally:
        prof.close()

    # Post-process the hotshot output so it can be read by kcachegrind
    os.system('%s -o %s %s' % (HOTSHOT2CG,cgr_fname,prof_fname))
    os.system('kcachegrind %s &' % cgr_fname)

if __name__ == '__main__':
    main()
