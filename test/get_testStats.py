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
        last_git_commit = 0 # subprocess.Popen(['git','log -n 1','--pretty=format:"%h - %ar"'])

    #    self.common_stat_set = [] #test_name, test_time[:-1], self.now, last_git_commit, hardware, cpu, hw_mem, self.status
        self.test_results = {}
        self.final_time = None
        # pass or fail?

    def append_test_result(self, test_name, test_time, test_status): # test name, time , status
    #    key = self.test_name
        key = ntpath.basename(test_name)
    #    print key
        if key not in self.test_results:
            self.test_results[key] = []

        result_list = test_name, test_time[-2:-1], self.now, test_status
        self.test_results[key].append('%s' % ', '.join(map(str, result_list)))
    #    result_list = "%s, %s, %s, %s" % (test_name, test_time[-2:-1], self.now, test_status)
        print result_list
    #    self.test_results[key].append(result_list) #append test result to dicitonary as lists
        print('\n'.join("{}: {}".format(k, v) for k, v in self.test_results.items()))

    #    print self.test_results

    def save_results(self, filename):
        keys = sorted(self.test_results.keys())
        with open("%s" % filename, "wb+") as csv_file:
        #    for line in self.test_results:
        #        line_data = re.split(',', line)
        #        print(line_data)
            writer = csv.writer(csv_file, delimiter="\t", quoting = csv.QUOTE_NONE)
            writer.writerows(self.test_results.values())

        sheet_name = "test-sheet"
        update.main(self.filename, sheet_name)

    # fetch and register test name and time taken by test
    def register_time_stats(self):
        self.filename = 'TestOverview_{0}.csv'.format(self.now)
        self.save_results(self.filename)

    def register_total_time(self, final_time, test_description, test_status): # name # time (end - start)
        sheet_name = "IncludeOS-testing-stats"
        filename = "TestStats.csv"
        total_test_data = [self.now, final_time[:-1], test_description, test_status]
        with open("%s" % filename,'wb+') as csv_file:
            writer = csv.writer(csv_file,lineterminator='\n')
            writer.writerow(total_test_data)
        update.main(filename, sheet_name)

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
