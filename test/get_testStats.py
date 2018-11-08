#!/usr/bin/env python
import csv
import datetime
import subprocess
import json
import update

class statOps:
    def __init__(self, test_name, test_time): # date, #testname #git commit # machinary #hardware config
        self.test_name = test_name
        dt = datetime.datetime.now()
        last_git_commit = 0 # subprocess.Popen(['git','log -n 1','--pretty=format:"%h - %ar"'])
        self.now = dt.strftime("%Y-%B-%d-%I%M%p")
        hardware = 0
        cpu = 0
        hw_mem = 0
        self.common_stat_set = test_name, test_time, self.now, last_git_commit, hardware, cpu, hw_mem
        self.test_results = {}

    def append_test_result(self):
        key = self.now
        if key not in self.test_results:
            self.test_results[key] = []
        self.test_results[key].append(self.common_stat_set) # should append more test result data to dicitonary as lists
        print(self.test_results)
        self.register_time_stats()

    def save_results(self, filename):
    #    print(self.test_name + " is saving.")
        keys = sorted(self.test_results.keys())
        with open("%s" % filename, "wb+") as csv_file:
            writer = csv.writer(csv_file, delimiter = "\t")
            writer.writerows(zip(*[self.test_results[self.now] for self.now in keys]))
        sheet_name = "test-sheet"
        update.main(self.filename, sheet_name)

    # fetch test name and time taken by test
    def register_time_stats(self):
        self.filename = 'TestOverview_{0}.csv'.format(self.now)
        self.save_results(self.filename)

    def register_total_time(final_time): # name # time (end - start)
        #sheet_name = "total-time-IncludeOS-tests"
        print final_time
        # write to csv
        #update.main(self.now, sheet_name)

    # fetch stress test stats for every test in stress test and build_service.
    def register_result_stats(self, test_tag, var_num):
        filename = '{0}{1}'.format(test_tag, self.now)
        print self.test_name, test_tag, var_num
        data = self.test_name, test_tag, var_num
        self.save_results(data, filename)

#class testStats:
#    self.start_time
#    self.end_time
#    self.name

#    def __print__()



#    def duration()
