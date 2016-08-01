import workload.constants as cs
import pandas as pd
import csvHelper.csvHelper as csvHelper
import workload.WorkloadSummary as ws
import os


fileList = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                   cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)


# Create the Workload Summary for the set of files

w = ws.WorkloadSummary(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH, cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_HOURS[0],
                       cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH, cs.WIKISTATS_END_DAY,
                       cs.WIKISTATS_HOURS[len(cs.WIKISTATS_HOURS)-1], cs.WORKLOAD_SUMMARY_COL)

print fileList[0]
print csvHelper.get_timestamp_from_file_name(fileList[0])


for i in fileList:
    fileName = cs.DATA_LOCAL_PATH + i + cs.DATA_LOCAL_FILE_FILTERED + '.csv'
    print "### Processing File: %s" % fileName
    # Append each workload file to a data frame
    df = pd.read_csv(fileName, delimiter=' ')
    df.columns = [cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE, cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]
    df[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]] = df[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]].astype(float)

    # Cleaning Sample. Deleting Entries that Number of Requests < mean number of requests
    description = df.describe()
    mean_requests = description.iloc[1][cs.WIKISTATS_COL_REQUESTS]
    mean_bytes = description.iloc[1][cs.WIKISTATS_COL_SIZE]

    df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] < mean_requests].index)
    # Sorting Data Sample - Ordering Number of Requests Descending
    #df = w.sortOccurrencePerNumberOfRequests(df)

    w.addWorkloadHourStatSummary(df, csvHelper.get_timestamp_from_file_name(i).year,
                        csvHelper.get_timestamp_from_file_name(i).month,
                        csvHelper.get_timestamp_from_file_name(i).day,
                        csvHelper.get_timestamp_from_file_name(i).hour)
    w.addWorkloadSample(df, csvHelper.get_timestamp_from_file_name(i).year,
                        csvHelper.get_timestamp_from_file_name(i).month,
                        csvHelper.get_timestamp_from_file_name(i).day,
                        csvHelper.get_timestamp_from_file_name(i).hour)

    print "Processed Workload Summaries: "
    print w.workloadHourSummary
    print "### Processed File: %s" % fileName
    print "### Deleting File: %s" % fileName
    os.remove(fileName)


# Dumping dataframe to CSV File
if w.workload_summary.size > 0:
    path = cs.DATA_LOCAL_PATH + str(cs.WIKISTATS_BEGIN_MONTH) + '-'+ str(cs.WIKISTATS_BEGIN_YEAR) + '_' + \
           str(cs.WIKISTATS_END_MONTH) + '-' + str(cs.WIKISTATS_END_YEAR) + cs.DATA_LOCAL_FILE_MONTHLY + '.csv'
    print "Writing DataFrame to: " + path
    w.workload_summary.to_csv(path_or_buf=path, sep=' ', columns=cs.WORKLOAD_SUMMARY_COL, index=False)









