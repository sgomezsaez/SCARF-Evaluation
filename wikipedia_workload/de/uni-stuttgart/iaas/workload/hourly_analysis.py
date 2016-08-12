import workload.constants as cs
import pandas as pd
import csvHelper.csvHelper as csvHelper
import workload.WorkloadSummary as ws
from datetime import datetime, timedelta
import workloadDistFitting as wdf
from scipy.stats import dweibull

def create_hourly_analysis(fileList=[], outPutFilePath= ''):


    # Create the Workload Summary for the set of files

    w = ws.WorkloadSummary(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH, cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_HOURS[0],
                           cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH, cs.WIKISTATS_END_DAY,
                           cs.WIKISTATS_HOURS[len(cs.WIKISTATS_HOURS)-1], cs.WORKLOAD_SUMMARY_COL)

    for i in fileList:
        fileName = cs.DATA_LOCAL_PATH + i
        print "### Processing File: %s" % fileName
        print csvHelper.get_time_from_file_name(i)
        timeInterval = csvHelper.get_time_from_file_name(i)
        # Append each workload file to a data frame
        df = pd.read_csv(fileName, delimiter=' ')
        df.columns = [cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE, cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]

        # Cleaning Sample. Deleting Entries that Number of Requests = 0
        df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] == 0].index)

        # Cleaning Sample. Deleting Entries that Number of Requests < mean number of requests
        description = df.describe()
        mean_requests = description.iloc[1][cs.WIKISTATS_COL_REQUESTS]
        mean_bytes = description.iloc[1][cs.WIKISTATS_COL_SIZE]

        #df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] < mean_requests].index)
        #df = df.drop(df[df[cs.WIKISTATS_COL_SIZE] < mean_bytes].index)

        w.addWorkloadHourStatSummary(df, int(timeInterval[0]), int(timeInterval[1]),
                                     int(timeInterval[2]), int(timeInterval[3]))
        print "### Processed File: %s" % fileName

    #print w.workloadHourSummary

    workloadSummary = pd.DataFrame(columns=[cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP, cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ,
                                            cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES, cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
                                            cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES, cs.WORKLOAD_SUMMARY_STAT_STD_REQ,
                                            cs.WORKLOAD_SUMMARY_STAT_STD_BYTES, cs.WORKLOAD_SUMMARY_STAT_MAX_REQ,
                                            cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES, cs.WORKLOAD_SUMMARY_STAT_SUM_REQ,
                                                cs.WORKLOAD_SUMMARY_STAT_SUM_BYTES])



    for i in w.workloadHourSummary:
        print "Processing Timestamp " + str(i)
        workloadSummary = workloadSummary.append(w.getDataFrameHourlyReport(i), ignore_index=True)


    print "Saving to File: " + outPutFilePath
    workloadSummary.to_csv(path_or_buf=outPutFilePath, sep=' ', columns=[cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP,
                                                               cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ,
                                                               cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES,
                                                               cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
                                                               cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES,
                                                               cs.WORKLOAD_SUMMARY_STAT_STD_REQ,
                                                               cs.WORKLOAD_SUMMARY_STAT_STD_BYTES,
                                                               cs.WORKLOAD_SUMMARY_STAT_MAX_REQ,
                                                               cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES,
                                                               cs.WORKLOAD_SUMMARY_STAT_SUM_REQ,
                                                                cs.WORKLOAD_SUMMARY_STAT_SUM_BYTES],
                           index=False)

def calculate_total_number_requests(summary_file):
    df = pd.read_csv(summary_file, delimiter=' ')
    df = ws.WorkloadSummary.sortOccurrencesPerTimeStamp(df=df, timestampColName=cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP)
    df.columns = [cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP,
                   cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES,
                   cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES,
                   cs.WORKLOAD_SUMMARY_STAT_STD_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_STD_BYTES,
                   cs.WORKLOAD_SUMMARY_STAT_MAX_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES,
                    cs.WORKLOAD_SUMMARY_STAT_SUM_REQ,
                    cs.WORKLOAD_SUMMARY_STAT_SUM_BYTES]

    return (df.as_matrix(columns=[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ])).sum()

def calculate_average_number_requests(summary_file):
    df = pd.read_csv(summary_file, delimiter=' ')
    df = ws.WorkloadSummary.sortOccurrencesPerTimeStamp(df=df, timestampColName=cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP)
    df.columns = [cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP,
                   cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES,
                   cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES,
                   cs.WORKLOAD_SUMMARY_STAT_STD_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_STD_BYTES,
                   cs.WORKLOAD_SUMMARY_STAT_MAX_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES,
                    cs.WORKLOAD_SUMMARY_STAT_SUM_REQ,
                    cs.WORKLOAD_SUMMARY_STAT_SUM_BYTES]

    return ((df.as_matrix(columns=[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ])).sum()) / len(df)


def calculate_daily_total_number_requests(summary_file):
    df_requests_summary = pd.read_csv(summary_file, delimiter=' ')
    df_requests_summary = ws.WorkloadSummary.sortOccurrencesPerTimeStamp(df=df_requests_summary, timestampColName=cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP)
    df_requests_summary.columns = [cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP,
                   cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES,
                   cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES,
                   cs.WORKLOAD_SUMMARY_STAT_STD_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_STD_BYTES,
                   cs.WORKLOAD_SUMMARY_STAT_MAX_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES,
                    cs.WORKLOAD_SUMMARY_STAT_SUM_REQ,
                    cs.WORKLOAD_SUMMARY_STAT_SUM_BYTES]

    timeStampToDateTime = lambda x: datetime.fromtimestamp(
            int(x)
        ).strftime('%Y-%m-%d %H:%M:%S')

    df_requests_summary[cs.WIKISTATS_UNIQUE_DEVICES_TIMESTAMP] = \
        df_requests_summary[cs.WIKISTATS_UNIQUE_DEVICES_TIMESTAMP].map(timeStampToDateTime)


    df_grouped = df_requests_summary[[cs.WIKISTATS_UNIQUE_DEVICES_TIMESTAMP, cs.WORKLOAD_SUMMARY_STAT_SUM_REQ]].groupby(
            df_requests_summary[cs.WIKISTATS_UNIQUE_DEVICES_TIMESTAMP].map(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').day)).sum()

    return df_grouped[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ]

def calculate_hourly_total_number_requests(summary_file):
    df_requests_summary = pd.read_csv(summary_file, delimiter=' ')
    df_requests_summary = ws.WorkloadSummary.sortOccurrencesPerTimeStamp(df=df_requests_summary, timestampColName=cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP)
    df_requests_summary.columns = [cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP,
                   cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES,
                   cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES,
                   cs.WORKLOAD_SUMMARY_STAT_STD_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_STD_BYTES,
                   cs.WORKLOAD_SUMMARY_STAT_MAX_REQ,
                   cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES,
                    cs.WORKLOAD_SUMMARY_STAT_SUM_REQ,
                    cs.WORKLOAD_SUMMARY_STAT_SUM_BYTES]

    return df_requests_summary[[cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP, cs.WORKLOAD_SUMMARY_STAT_SUM_REQ]]

# Assumption that distribution is fitted to the Weibull Distribution
def calculate_daily_probability(summary_file):
    daily_requests_sum = calculate_daily_total_number_requests(summary_file)
    daily_requests_sum.columns = [cs.WORKLOAD_SUMMARY_STAT_SUM_REQ]

    #print daily_requests_sum.to_frame()
    prob_dist = wdf.best_fit_distribution(daily_requests_sum, bins=15)
    #wdf.load_and_fit_data(df=daily_requests_sum.to_frame(), bins=15)

    daily_probability = []

    for i in daily_requests_sum.tolist():
        daily_probability.append(dweibull.pdf(i, prob_dist[1][0], loc=prob_dist[1][1], scale=prob_dist[1][2]) * 1000)

    return daily_probability


fileList = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                   cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

#path = cs.DATA_LOCAL_PATH + str(cs.WIKISTATS_BEGIN_MONTH) + '-'+ str(cs.WIKISTATS_BEGIN_YEAR) + '_' + \
#               str(cs.WIKISTATS_END_MONTH) + '-' + str(cs.WIKISTATS_END_YEAR) + cs.DATA_LOCAL_FILE_HOURLY_SUMMARY + '_' + cs.DATA_LOCAL_FILE_NO_CLEAN + '.csv'

path = cs.DATA_LOCAL_PATH + str(cs.WIKISTATS_BEGIN_MONTH) + '-'+ str(cs.WIKISTATS_BEGIN_YEAR) + '_' + \
               str(cs.WIKISTATS_END_MONTH) + '-' + str(cs.WIKISTATS_END_YEAR) + cs.DATA_LOCAL_FILE_HOURLY_SUMMARY + '.csv'

fileListFiltered = []

for i in fileList:
    fileListFiltered.append(i + cs.DATA_LOCAL_FILE_FILTERED + '.csv')

#create_hourly_analysis(fileList=fileListFiltered, outPutFilePath=path)

file_name = cs.DATA_LOCAL_PATH + "1-2016_1-2016_hourly_summary_scaled_factor100Scaling.csv"

#print calculate_total_number_requests(file_name)
#print calculate_average_number_requests(file_name)
#print calculate_daily_total_number_requests(file_name)
#print calculate_hourly_total_number_requests(file_name)
#print calculate_daily_probability(file_name)

