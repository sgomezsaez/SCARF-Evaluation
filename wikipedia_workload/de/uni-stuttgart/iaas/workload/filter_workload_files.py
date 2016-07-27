import os

import constants.constants as cs

import csvHelper.csvHelper as csvHelper
import http.httpHelper as httpHelper
import workload.RequestSummary as rs

#import threading
#import datetime
#from datetime import date, timedelta
#from random import randint
#from time import sleep


w = rs.RequestSummary("a","b","b", 300, 22, 2016, 7, 21, 13)
w.addOccurence("b", 200, 22, 2016, 7, 21, 13)
w.addOccurence("b", 200, 22, 2016, 7, 23, 17)
w.addOccurence("b", 100, 22, 2016, 7, 23, 13)

#print "unordered list of keys"
#print w.getOccurrences().keys()
#print "ordered list of keys"
#print sorted(w.getOccurrences().keys())
#print w.getOcurrences()

print "Initial Workload Occurrences "
print w.getOccurrences()

print "group workload per day"
print w.groupWorkloadPerDay(w.getOccurrences())
print "group workload per month"
print w.groupWorkloadPerMonth(w.getOccurrences())

print "sortOcurrencePerTimeStamp"
print w.sortOccurrencesPerTimeStamp(w.getOccurrences())

print "sortOcurrencePerNumberOfRequests"
print w.sortOccurrencePerNumberOfRequests(w.getOccurrences())

urlList = httpHelper.retrieve_urls_time_interval(cs.WIKISTATS_URL, cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

fileList = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                   cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

#Create 23 threads for each day.

#def retrieve_number_of_days(beginYear, beginMonth, beginday, endYear, endMonth, endday):
#    a = date(beginYear, beginMonth, beginday)
#    b = date(endYear, endMonth, endday)

#    return len([a + timedelta(days=x) for x in range((b-a).days + 1)])

#def worker(url, filePath):
#    print "Retrieving File from url " + url
#    sleep(randint(5,50))
#    httpHelper.retrieve_and_save_package_async(url, cs.DATA_LOCAL_PATH)
#    print "Filtering File " +  os.path.join(cs.DATA_LOCAL_PATH, filePath) + ".csv"
#    csvHelper.filter_csv_file_rows(os.path.join(cs.DATA_LOCAL_PATH, filePath + ".csv"),
#                                   os.path.join(cs.DATA_LOCAL_PATH, filePath + cs.DATA_LOCAL_FILE_FILTERED + ".csv"),
#                                   cs.WIKISTATS_DELIMITER, cs.WIKISTATS_FILTER_VALUES)

#threads = []

#for day in range(retrieve_number_of_days(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
#                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
#                                                cs.WIKISTATS_END_DAY)):
#    print "#Day %s" % day
#    for hour in range(cs.THREAD_NUMBER):
#        print "#Hour %s" % hour
#        if day == 0:
#            url = urlList[day * cs.THREAD_NUMBER + hour]
#            filePath = fileList[day * cs.THREAD_NUMBER + hour]
#            t = threading.Thread(target=worker, args=(url, filePath))
#        else:
#            url = urlList[day * cs.THREAD_NUMBER + (hour + 1)]
#            filePath = fileList[day * cs.THREAD_NUMBER + (hour + 1)]
#            t = threading.Thread(target=worker, args=(url, filePath))
#        threads.append(t)
#        t.start()

def download_and_filter_workload_files():
    for url in urlList:
        print "Retrieving File " + url
        httpHelper.retrieve_and_save_package(url, cs.DATA_LOCAL_PATH)
        print "Filtering File " +  os.path.join(cs.DATA_LOCAL_PATH, fileList[urlList.index(url)]) + ".csv"
        csvHelper.filter_csv_file_rows(os.path.join(cs.DATA_LOCAL_PATH, fileList[urlList.index(url)] + ".csv"),
                                       os.path.join(cs.DATA_LOCAL_PATH, fileList[urlList.index(url)] + cs.DATA_LOCAL_FILE_FILTERED + ".csv"),
                                     cs.WIKISTATS_DELIMITER, cs.WIKISTATS_FILTER_VALUES)


download_and_filter_workload_files()

