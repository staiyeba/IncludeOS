#!/usr/bin/env python
import csv
import datetime
import subprocess

class statOps:
    def __init__(self, test_name, test_time): # date, #testname #git commit # machinary #hardware config
        dt = datetime.datetime.now()
        self.now = dt.strftime("%Y_%B_%d_%I%M%p")
        self.test_name = test_name  #gets test name from testrunner
        self.test_time = test_time
        self.git_commit = 0 # subprocess.Popen(['git','log -n 1','--pretty=format:"%h - %ar"'])
        self.hardware = 0
        self.cpu = 0
        self.hw_mem = 0

    #    self.results = [["name", "duration"],["name2", "duration2"]]
    #    self.results2 = [test1, test2, test3]
    #    test1.duration()
    #    print test1

    def save_results(self, data, filename):
        print(self.test_name + " is saving restults.")
        with open("%s.csv" % filename, "wb+") as csv_file:
            writer = csv.writer(csv_file)
            for line in data:
                writer.writerow(line)

    # fetch test name and time taken by test
    def register_time_stats(self): # name # time (end - start) then append to list
        filename = 'TestOverview_{0}'.format(self.now)
        print filename, self.now, self.test_name, self.test_time #, self.git_commit
        data = [self.now, self.test_name, self.test_time]
        self.save_results(data, filename) # data and filename


    # fetch stress test stats for every test in stress test.
    def register_result_stats(self, test_tag, var_num):
        filename = "{0}{1}".format(test_tag, self.now)
        print self.test_name, test_tag, var_num
        data = [self.test_name, test_tag, var_num]
        self.save_results(data, filename)

#class testStats:
#    self.start_time
#    self.end_time
#    self.name

#    def __print__()



#    def duration()
