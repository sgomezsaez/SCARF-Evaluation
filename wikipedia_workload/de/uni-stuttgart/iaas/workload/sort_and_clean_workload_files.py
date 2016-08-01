import workload.constants as cs
import pandas as pd
import csvHelper.csvHelper as csvHelper
import workload.WorkloadSummary as ws
import os

import threading
from thread import start_new_thread
import datetime
from datetime import date, timedelta
from random import randint
from time import sleep

fileList = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                   cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

# Create the Workload Summary for the set of files

w = ws.WorkloadSummary(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH, cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_HOURS[0],
                       cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH, cs.WIKISTATS_END_DAY,
                       cs.WIKISTATS_HOURS[len(cs.WIKISTATS_HOURS)-1], cs.WORKLOAD_SUMMARY_COL)

#print fileList[0]
#print csvHelper.get_timestamp_from_file_name(fileList[0])


def retrieve_number_of_days(beginYear, beginMonth, beginday, endYear, endMonth, endday):
    a = date(beginYear, beginMonth, beginday)
    b = date(endYear, endMonth, endday)
    return len([a + timedelta(days=x) for x in range((b-a).days + 1)])


def worker(filePath, fileName):
    print "### Processing File: %s" % filePath
    # Append each workload file to a data frame
    df = pd.read_csv(filePath, delimiter=' ')
    df.columns = [cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE, cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]
    df[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]] = df[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]].astype(float)

    # Cleaning Sample. Deleting Entries that Number of Requests < mean number of requests
    description = df.describe()
    mean_requests = description.iloc[1][cs.WIKISTATS_COL_REQUESTS]
    mean_bytes = description.iloc[1][cs.WIKISTATS_COL_SIZE]

    df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] < mean_requests].index)
    # Sorting Data Sample - Ordering Number of Requests Descending
    df = w.sortOccurrencePerNumberOfRequests(df)

    w.addWorkloadHourStatSummary(df, csvHelper.get_timestamp_from_file_name(fileName).year,
                        csvHelper.get_timestamp_from_file_name(fileName).month,
                        csvHelper.get_timestamp_from_file_name(fileName).day,
                        csvHelper.get_timestamp_from_file_name(fileName).hour)
    w.addWorkloadSample(df, csvHelper.get_timestamp_from_file_name(fileName).year,
                        csvHelper.get_timestamp_from_file_name(fileName).month,
                        csvHelper.get_timestamp_from_file_name(fileName).day,
                        csvHelper.get_timestamp_from_file_name(fileName).hour)

    print "Processed Workload Summaries: "
    print w.workloadHourSummary
    print "### Processed File: %s" % filePath
    print "### Deleting File: %s" % filePath
    os.remove(filePath)

threads = []

for day in range(retrieve_number_of_days(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                cs.WIKISTATS_END_DAY)):
    print "#Day %s" % day
    for hour in range(cs.THREAD_NUMBER):
        print "#Hour %s" % hour
        if day == 0:
            filePath = cs.DATA_LOCAL_PATH + fileList[day * cs.THREAD_NUMBER + hour] + cs.DATA_LOCAL_FILE_FILTERED + '.csv'
            fileName = fileList[day * cs.THREAD_NUMBER + hour]

        else:
            if day * cs.THREAD_NUMBER + (hour + 1) < len(fileList):
                filePath = cs.DATA_LOCAL_PATH + fileList[day * cs.THREAD_NUMBER + (hour + 1)] + cs.DATA_LOCAL_FILE_FILTERED + '.csv'
                fileName = fileList[day * cs.THREAD_NUMBER + hour]
        print filePath
        t = threading.Thread(target=worker, args=(filePath, fileName))
        threads.append(t)

print threads

# Starting 23 Threads
#for i in range(cs.THREAD_NUMBER):
#    print "starting thread " + str(i)
#    threads[i].start()

# Starting 24..endDays threads that will join when the 23 first threads finish
#for j in range(24, retrieve_number_of_days(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
#                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
#                                                cs.WIKISTATS_END_DAY)):
#    print "join thread " + str(j)
#    threads[j].join()

[t.start() for t in threads]
[t.join() for t in threads]


# Dumping dataframe to CSV File
#if w.workload_summary.size > 0:
#    path = cs.DATA_LOCAL_PATH + str(cs.WIKISTATS_BEGIN_MONTH) + '-'+ str(cs.WIKISTATS_BEGIN_YEAR) + '_' + \
#           str(cs.WIKISTATS_END_MONTH) + '-' + str(cs.WIKISTATS_END_YEAR) + cs.DATA_LOCAL_FILE_MONTHLY + '.csv'
#    print "Writing DataFrame to: " + path
#    w.workload_summary.to_csv(path_or_buf=path, sep=' ', columns=cs.WORKLOAD_SUMMARY_COL, index=False)









