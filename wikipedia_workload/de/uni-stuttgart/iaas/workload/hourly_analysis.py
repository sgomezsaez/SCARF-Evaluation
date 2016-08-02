import workload.constants as cs
import pandas as pd
import csvHelper.csvHelper as csvHelper
import workload.WorkloadSummary as ws


fileList = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                   cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)


# Create the Workload Summary for the set of files

w = ws.WorkloadSummary(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH, cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_HOURS[0],
                       cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH, cs.WIKISTATS_END_DAY,
                       cs.WIKISTATS_HOURS[len(cs.WIKISTATS_HOURS)-1], cs.WORKLOAD_SUMMARY_COL)

for i in fileList:
    fileName = cs.DATA_LOCAL_PATH + i + cs.DATA_LOCAL_FILE_FILTERED + '.csv'
    print "### Processing File: %s" % fileName
    print csvHelper.get_time_from_file_name(i)
    timeInterval = csvHelper.get_time_from_file_name(i)
    # Append each workload file to a data frame
    df = pd.read_csv(fileName, delimiter=' ')

    w.addWorkloadHourStatSummary(df, int(timeInterval[0]), int(timeInterval[1]),
                                 int(timeInterval[2]), int(timeInterval[3]))
    print "### Processed File: %s" % fileName

#print w.workloadHourSummary

workloadSummary = pd.DataFrame(columns=[cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP, cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ,
                                        cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES, cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
                                        cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES, cs.WORKLOAD_SUMMARY_STAT_STD_REQ,
                                        cs.WORKLOAD_SUMMARY_STAT_STD_BYTES, cs.WORKLOAD_SUMMARY_STAT_MAX_REQ,
                                        cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES])


for i in w.workloadHourSummary:
    print "Processing Timestamp " + str(i)
    workloadSummary = workloadSummary.append(w.getDataFrameHourlyReport(i), ignore_index=True)

path = cs.DATA_LOCAL_PATH + str(cs.WIKISTATS_BEGIN_MONTH) + '-'+ str(cs.WIKISTATS_BEGIN_YEAR) + '_' + \
           str(cs.WIKISTATS_END_MONTH) + '-' + str(cs.WIKISTATS_END_YEAR) + cs.DATA_LOCAL_FILE_HOURLY_SUMMARY + '.csv'
print "Saving to File: " + path
workloadSummary.to_csv(path_or_buf=path, sep=' ', columns=[cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP,
                                                           cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ,
                                                           cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES,
                                                           cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
                                                           cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES,
                                                           cs.WORKLOAD_SUMMARY_STAT_STD_REQ,
                                                           cs.WORKLOAD_SUMMARY_STAT_STD_BYTES,
                                                           cs.WORKLOAD_SUMMARY_STAT_MAX_REQ,
                                                           cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES],
                       index=False)

