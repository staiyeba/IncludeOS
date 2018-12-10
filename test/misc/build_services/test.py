#! /usr/bin/env python3

import sys
import os
import subprocess
import multiprocessing
from multiprocessing import Pool

includeos_src = os.environ.get('INCLUDEOS_SRC',
                               os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))).split('/test')[0])
sys.path.insert(0,includeos_src)

includeos_prefix = os.environ.get('INCLUDEOS_PREFIX',
                               os.path.realpath(os.path.join(os.getcwd())))
sys.path.insert(0,includeos_prefix)

sys.path.insert(0, ".")
sys.path.insert(0, "../..")

#from vmrunner import vmrunner
#from vmrunner.prettify import color

count = 0
count_build = 0
examples = []
tmpfile="/tmp/build_test"
skip_tests="demo_service"

path_to_examples = os.path.join(includeos_src,'examples')
path_to_starbase = os.path.join(includeos_src,'lib/uplink')

passed = 0
failed = 0

def starbase():
    print(">>>Building starbase")
    for find_starbase in next(os.walk(path_to_starbase))[1]:
    #    print(find_starbase)
        if "starbase" in find_starbase:
            starbase_dir = os.path.join(includeos_src, path_to_starbase, find_starbase)
            examples.append(find_starbase)




def build_service(subdir):

    print(">>>Building service: " + subdir)

    if subdir == 'starbase':
        service_dir = os.path.join(includeos_src,'lib/uplink', subdir)
        print(service_dir)
    else:
        service_dir = os.path.join(includeos_src,'examples', subdir)
        print(service_dir)

    run_test(service_dir)

def run_test(run_dir):

    global passed
    global failed

    os.chdir(run_dir)
    subprocess.call(["git", "submodule", "update", "--init", "--recursive"])

    if os.path.exists("prereq.sh"):
        print("Installing Prereq")
        subprocess.call("./prereq.sh")

    run_boot_path=os.path.join(includeos_prefix,'bin/boot')
    clean_build = '-cb'
    dot = '.'

    subprocess.call(['/bin/bash', run_boot_path,clean_build, dot,'&>',tmpfile ], stderr=subprocess.STDOUT)

#    try:
#        command = ['/bin/bash', run_boot_path,clean_build, dot,'&>',tmpfile ]
    #    print color.DATA(" ".join(command))
#        subprocess.call(command)
#        passed = passed + 1
#        print(" [ PASS ] ")
#    except Exception as e:
#        print(" [ FAIL ] ")
    #    print color.FAIL("<Test.py> FAILED Process threw exception:")
#        print(">>> Printing ERROR EXCEPTION: ")
#        print(e)
#        failed = failed + 1


def main():
    global count
    for subdir in next(os.walk(path_to_examples))[1]:
        if skip_tests in subdir:
            continue

        examples.append(subdir)
        count = count + 1

    starbase()
    count = count + 1

    #p = Pool(count)

    # to create thread based on the number of cpus available
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    result = p.map(build_service, examples)
    p.close()
    p.join

#    p.map(build_service, examples) as pool:


    print(">>> PASSED: ")
    print(passed)
    print(">>> FAILED: ")
    print(failed)


if __name__ == '__main__':
    main()
