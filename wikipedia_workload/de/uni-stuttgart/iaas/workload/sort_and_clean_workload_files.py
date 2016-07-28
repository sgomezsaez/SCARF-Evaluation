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

print fileList[0]
print csvHelper.get_timestamp_from_file_name(fileList[0])

for i in fileList:
    fileName = cs.DATA_LOCAL_PATH + i + cs.DATA_LOCAL_FILE_FILTERED + '.csv'
    print "### Processing File: %s" % i
    # Append each workload file to a data frame
    df = pd.read_csv(fileName, delimiter=' ')
    df.columns = [cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE, cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]


    print w.sortOccurrencePerNumberOfRequests(df)

    #w.addWorkloadSample(df, csvHelper.get_timestamp_from_file_name(i).year,
    #                    csvHelper.get_timestamp_from_file_name(i).month,
    #                    csvHelper.get_timestamp_from_file_name(i).day,
    #                    csvHelper.get_timestamp_from_file_name(i).hour)


#print w.workload_summary
