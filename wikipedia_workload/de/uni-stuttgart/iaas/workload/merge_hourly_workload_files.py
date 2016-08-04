import workload.constants as cs
import pandas as pd
import csvHelper.csvHelper as csvHelper
import workload.WorkloadSummary as ws
import numpy as np

from multiprocessing import Process, Lock
from datetime import date, timedelta
from random import randint
from time import sleep
import os

#os.system("taskset -p 0xff %d" % os.getpid())

#lock = Lock()

def merge_hourly_workload_files(fileList, outputFilePath, beginYear, beginMonth, beginDay, endYear, endMonth, endDay):

    w = ws.WorkloadSummary(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH, cs.WIKISTATS_BEGIN_DAY,
                           cs.WIKISTATS_HOURS[0], cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                           cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS[len(cs.WIKISTATS_HOURS)-1],
                           cs.WORKLOAD_SUMMARY_COL)

    for i in range(retrieve_number_of_days(beginYear, beginMonth, beginDay, endYear, endMonth, endDay)):
        filePath = cs.DATA_LOCAL_PATH + fileList[i] + '.csv'
        print "Processing File " + filePath
        w = worker(filePath, fileList[i], w)
        os.remove(filePath)

    print "Processed Workload Summaries: Writing to file to " + outputFilePath
    w.workload_summary.to_csv(path_or_buf=outputFilePath, sep=' ', columns=cs.WORKLOAD_SUMMARY_COL, index=False)



#for day in range(retrieve_number_of_days(beginYear, beginMonth, beginDay, endYear, endMonth, endDay)):
#for day in range(1):
#    print "#Day %s" % day
#    for hour in range(cs.THREAD_NUMBER):
#        print "#Hour %s" % hour
#        if day == 0:
#            filePath = cs.DATA_LOCAL_PATH + fileList[day * cs.THREAD_NUMBER + hour] + cs.DATA_LOCAL_FILE_FILTERED + '.csv'
#            fileName = fileList[day * cs.THREAD_NUMBER + hour]

#        else:
#            if day * cs.THREAD_NUMBER + (hour + 1) < len(fileList):
#                filePath = cs.DATA_LOCAL_PATH + fileList[day * cs.THREAD_NUMBER + (hour + 1)] + cs.DATA_LOCAL_FILE_FILTERED + '.csv'
#                fileName = fileList[day * cs.THREAD_NUMBER + hour]
#        print filePath
#        t = Process(target=worker, args=(filePath, fileName))
#        processes.append(t)

#print processes


def retrieve_number_of_days(beginYear, beginMonth, beginday, endYear, endMonth, endday):
    a = date(beginYear, beginMonth, beginday)
    b = date(endYear, endMonth, endday)
    return len([a + timedelta(days=x) for x in range((b-a).days + 1)])


def worker(filePath, fileName, w):
    print "### Worker Processing File: %s" % filePath
    # Append each workload file to a data frame
    df = pd.read_csv(filePath, delimiter=' ')
    df.columns = [cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE, cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]
    df[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]] = df[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]].astype(float)

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

    return w



fileList = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                   cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

fileListFiltered = []
for i in fileList:
    fileListFiltered.append(i + cs.DATA_LOCAL_FILE_FILTERED)

fileListScaled = []

for i in fileList:
    fileListScaled.append(i + cs.DATA_LOCAL_FILE_SCALED)

outputFilePath = cs.DATA_LOCAL_PATH + str(cs.WIKISTATS_BEGIN_MONTH) + '-'+ str(cs.WIKISTATS_BEGIN_YEAR) + '_' + \
           str(cs.WIKISTATS_END_MONTH) + '-' + str(cs.WIKISTATS_END_YEAR) + cs.DATA_LOCAL_FILE_MONTHLY + \
                 '_' + cs.DATA_LOCAL_FILE_SCALED + '_Merged' + '.csv'


merge_hourly_workload_files(fileListScaled, outputFilePath, cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                            cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR,
                            cs.WIKISTATS_END_MONTH, cs.WIKISTATS_END_DAY)

