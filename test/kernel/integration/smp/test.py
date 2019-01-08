#! /usr/bin/env python

import sys
import os

includeos_src = os.environ.get('INCLUDEOS_SRC',
                               os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))).split('/test')[0])
sys.path.insert(0,includeos_src)

from vmrunner import vmrunner

if len(sys.argv) > 1:
    vmrunner.vms[0].boot(20,image_name=str(sys.argv[1]))
else:
    vmrunner.vms[0].cmake().boot(20).clean()
#vm.cmake(["-Dsingle_threaded=OFF"]).boot(20).clean()
