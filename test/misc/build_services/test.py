#! /usr/bin/env python3

import sys
import os
import subprocess
from multiprocessing import Pool

includeos_src = os.environ.get('INCLUDEOS_SRC',
                               os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))).split('/test')[0])
sys.path.insert(0,includeos_src)

includeos_prefix = os.environ.get('INCLUDEOS_PREFIX',
                               os.path.realpath(os.path.join(os.getcwd())))
sys.path.insert(0,includeos_prefix)


tmpfile="/tmp/build_test"
skip_tests="demo_service"
examples = []
count = 0
path_to_examples = os.path.join(includeos_src,'examples')
#def getScriptAbsoluteDir:


def build_service(subdir):
    
    examples_dir = os.path.join(includeos_src,'examples', subdir)
    os.chdir(examples_dir)
    subprocess.call("ls")
    subprocess.call(["git", "submodule", "update", "--init", "--recursive"])


    if os.path.exists("prereq.sh"):
        print("Installing Prereq")
        subprocess.call("./prereq.sh")


    run_boot_path=os.path.join(includeos_prefix,'bin/boot')
    print(run_boot_path)
    clean_build = '-cb'
    dot = '.'
    print(dot)
    subprocess.call(['/bin/bash', run_boot_path,clean_build, dot,'&>',tmpfile ])
    print("[ PASS ]")
#    exec(run_boot_path + dot)

print(">>>Building all examples")

for subdir in next(os.walk(path_to_examples))[1]:
    if skip_tests not in subdir:
        examples.append(subdir)
        print(examples)
        count = count + 1

print(count)
p = Pool(count)
p.map(build_service, examples)
