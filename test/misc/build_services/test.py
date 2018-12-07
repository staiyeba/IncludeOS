#! /usr/bin/env python3
# test/misc/build_services/test.py

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
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1) # line buffering
sys.path.insert(0, ".")
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

from get_testStats import statOps
from get_testStats import subTestStats

test_name = "build_services"
tmpfile = "/tmp/build_test"
skip_tests = "demo_service"
count = 0
count_build = 0
examples = []
path_to_examples = os.path.join(includeos_src,'examples')
path_to_starbase = os.path.join(includeos_src,'lib/uplink')
sub_test_stats = subTestStats()
sub_stat_results = {}

def starbase():
    print(">>>Building starbase")
    sub_test_tag = subdir
    print(sub_test_tag + " " + test_name)
    for find_starbase in next(os.walk(path_to_starbase))[1]:
        if "starbase" in find_starbase:
            starbase_dir = os.path.join(includeos_src, path_to_starbase, find_starbase)

    run_test(stabase_dir)

def build_service(subdir):
    print(">>>Building service:" + subdir)
    sub_test_tag = subdir
    print(sub_test_tag + " " + test_name)
    service_dir = os.path.join(includeos_src,'examples', subdir)
    run_test(service_dir, sub_test_tag)

def run_test(run_dir, sub_test_tag):
    os.chdir(run_dir)
    subprocess.call(["git", "submodule", "update", "--init", "--recursive"])

    if os.path.exists("prereq.sh"):
        print("Installing Prereq")
        subprocess.call("./prereq.sh")

    run_boot_path=os.path.join(includeos_prefix,'bin/boot')
    clean_build = '-cb'
    dot = '.'
    if not subprocess.call(['/bin/bash', run_boot_path,clean_build, dot,'&>',tmpfile ]):
        print("[ PASS ]")
        status = "PASS"
    else:
        print("[ FAIL ]")
        status = "FAIL"

    print(">>> Saving test to csv ...")
    sub_test_stats.append_sub_stats(test_name, sub_test_tag, None, status)

print(">>>Building all examples")

for subdir in next(os.walk(path_to_examples))[1]:
    if skip_tests in subdir:
        continue

    examples.append(subdir)
    count = count + 1

p = Pool(count)
p.map(build_service, examples)
#sub_test_stats.save_sub_stats_csv("build_services", sub_stat_results)
starbase
