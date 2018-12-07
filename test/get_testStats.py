#! /usr/bin/env python3
# test/get_testStats.py

import csv
import datetime
import subprocess
import json
import update
import re
import ntpath
import multiprocessing
import os

#sub_test_stats = subTestStats()

class statOps:
    def __init__(self): # date, #testname #git commit # machinary config
        dt = datetime.datetime.utcnow()
        self.now = dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.last_git_commit = subprocess.check_output(['git','log', '--date=iso-strict-local','-n 1','--pretty=format: %h, %ad']).strip()
        self.latest_git_tag = subprocess.check_output(['git', 'describe', '--abbrev=0', '--tags']).strip()
        # git describe --tags $(git rev-list --tags --max-count=1)
        self.test_results = {}
        self.final_time = None

    def clean_csv(self, filename):
        subprocess.call(["rm %s" % filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    def append_stat_to_list(self, test_name, test_time, test_status, cpu_usage, memory_usage, machine):
        key = ntpath.basename(test_name) + os.path.split(test_name)[0]
        if key not in self.test_results:
            self.test_results[key] = []

        result_list = test_name, test_time[-2:-1], self.now, test_status, cpu_usage, memory_usage, machine
        self.test_results[key].append('%s' % ', '.join(map(str, result_list)))

    def register_all_test_stats(self, filename):
        keys = sorted(self.test_results.keys())
        with open("%s" % filename, "wb+") as csv_file:
            writer = csv.writer(csv_file, delimiter="\t", quoting=csv.QUOTE_NONE)
            writer.writerows(self.test_results.values())

        sheet_name = "Includeos-Sub-Test-Stats"
        update.main(filename, sheet_name)

    # fetch and register test name and time taken by test
    def save_stats_csv(self):
        filename = 'TestOverview_{0}.csv'.format(self.now)
        self.register_all_test_stats(filename)
        self.clean_csv(filename)

    def register_final_stats(self, final_time, test_description, skipped, test_status, fail_count): # name # time (end - start)
        sheet_name = "IncludeOS-Test-Stats" #"IncludeOS-testing-stats"
        filename = "TestStats.csv"
    #    sheet_choice = "sh.sheet1"
        num_cpus = int(multiprocessing.cpu_count())
        machine = os.uname()[3]#.replace(" ", "_")
        total_test_data = [self.now, final_time[:-1], test_description, skipped, test_status, self.latest_git_tag, "%s" % ''.join(self.last_git_commit), num_cpus, machine, fail_count]
        with open("%s" % filename,'wb+') as csv_file:
            writer = csv.writer(csv_file,lineterminator='\n')
            writer.writerow(total_test_data)
        update.main(filename, sheet_name)
        self.clean_csv(filename)

class subTestStats(statOps):

    def __init__(self):
        statOps.__init__(self)
        dt = datetime.datetime.utcnow()
        self.now = dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.sub_stat_results = {}
        self.sub_csv_file = None

    # fetch stress test stats for every test in stress test and build_service.
    def append_sub_stats(self, name_tag, test_tag, var_num, count):
        key = test_tag #ntpath.basename(name_tag)
        if key not in self.sub_stat_results:
            self.sub_stat_results[key] = []

        stat_list = test_tag, var_num, count
        self.sub_stat_results[key].append('%s' % ', '.join(map(str, stat_list)))
        print("SUB STAT RESULTS")
        print(self.sub_stat_results)


    def save_sub_stats_csv(self, test_name):
        print("************** SAVING TO CSV " + test_name + ".csv  **************")
    #    print(self.sub_stat_results)
        self.register_sub_stats(test_name)
        subfilename = '{0}.csv'.format(test_name)
        print(subfilename)
        self.register_sub_stats_gsheet(subfilename)
        # clear after save

    def register_sub_stats(self, test_name):
        keys = sorted(self.sub_stat_results.keys())
        print(test_name)
        full_path = os.path.realpath(__file__)
        print(self.sub_stat_results)
        dirpath = os.path.dirname(full_path)
        filepath  = '{0}/{1}.csv'.format(dirpath, test_name)
        print(filepath)
        with open("%s" % filepath, "wb+") as sub_csv_file:
            print(sub_csv_file)
            writer = csv.writer(sub_csv_file, delimiter="\t", quoting = csv.QUOTE_NONE)
            writer.writerows(self.sub_stat_results.values())

    def register_sub_stats_gsheet(self, sub_filename):
        sheet_name = "Includeos-Sub-Test-Stats"
    #    if test_name == "stress":
    #    sheet_choice = '1' #if stress test
#        elif test_name == "misc":
#            sheet_choice = "sheet3"
    #    sub_filename = ""
        #sheet_choice = "sh-sheet3" #if build services
        subcsv_filename = sub_filename
        print(subcsv_filename)
        update.main(subcsv_filename, sheet_name)
    #    statOps.register_all_test_stats(data, sub_filename)
    #    self.clean_csv(sub_filename)


    #    self.clean_csv(sub_filename)

    #    self.start_time
    #    self.end_time
    #    self.name

    #    def __print__()
    #    def duration()
