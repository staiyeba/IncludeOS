#!/usr/bin/env python
import csv
import datetime
import subprocess
import json
import update
import re
import ntpath

class statOps:
    def __init__(self): # date, #testname #git commit # machinary #hardware config
        dt = datetime.datetime.now()
        self.now = dt.strftime("%Y-%B-%d-%I%M%p")
        self.last_git_commit = subprocess.check_output(['git','log','-n 1','--pretty=format: %h, %ar']).strip()
        self.test_results = {}
        self.final_time = None

    def append_test_result(self, test_name, test_time, test_status, cpu_usage):
        key = ntpath.basename(test_name)
        if key not in self.test_results:
            self.test_results[key] = []

        result_list = test_name, test_time[-2:-1], self.now, test_status, cpu_usage
        self.test_results[key].append('%s' % ', '.join(map(str, result_list)))

    def save_results(self, filename):
        keys = sorted(self.test_results.keys())
        with open("%s" % filename, "wb+") as csv_file:
            writer = csv.writer(csv_file, delimiter="\t", quoting = csv.QUOTE_NONE)
            writer.writerows(self.test_results.values())

        sheet_name = "test-sheet"
        update.main(filename, sheet_name)

    # fetch and register test name and time taken by test
    def register_time_stats(self):
        filename = 'TestOverview_{0}.csv'.format(self.now)
        self.save_results(filename)
        subprocess.call(["rm %s" % filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    def register_total_time(self, final_time, test_description, skipped, test_status): # name # time (end - start)
        sheet_name = "IncludeOS-testing-stats"
        filename = "TestStats.csv"
        total_test_data = [self.now, final_time[:-1], test_description, skipped, test_status, ''.join(self.last_git_commit)]
        with open("%s" % filename,'wb+') as csv_file:
            writer = csv.writer(csv_file,lineterminator='\n')
            writer.writerow(total_test_data)
        update.main(filename, sheet_name)
        subprocess.call(["rm %s" % filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)


    # fetch stress test stats for every test in stress test and build_service.
    def register_result_stats(self, test_tag, var_num):
        filename = '{0}{1}'.format(test_tag, self.now)
        data = self.test_name, test_tag, var_num
        self.save_results(data, filename)
        subprocess.call(["rm %s" % filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)


#class testStats:
#    self.start_time
#    self.end_time
#    self.name

#    def __print__()



#    def duration()
