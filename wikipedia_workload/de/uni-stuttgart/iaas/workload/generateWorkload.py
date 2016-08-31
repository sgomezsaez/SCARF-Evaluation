import workload.constants as cs
import pandas as pd
import hourly_analysis, usersDailyAnalysis
import csvHelper.csvHelper as csvHelper
import numpy as np
import random as random
from workload import WorkloadSummary as ws
from datetime import datetime


def generateRequestsDfFromNumber(project, page, request_number, bytes):
    df = pd.DataFrame(columns=[cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE, cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE])

    for i in range(1, request_number):
        df = df.append(pd.DataFrame(data=[[project, page, 1, bytes, 0]], columns=[cs.WIKISTATS_COL_PROJECT,
                                                                        cs.WIKISTATS_COL_PAGE,
                                                                        cs.WIKISTATS_COL_REQUESTS,
                                                                        cs.WIKISTATS_COL_SIZE,
                                                                        cs.WIKISTATS_COL_DELAY]), ignore_index=True)
    return df

def shuffle_data_frame(df):
    index = list(df.index)
    random.shuffle(index)
    df = df.ix[index]
    df.reset_index()
    return df

hourly_access_requests_file = cs.DATA_LOCAL_PATH + "1-2016_1-2016_hourly_summary_scaled_factor1000Scaling.csv"
users_daily_access_file = cs.DATA_LOCAL_PATH + 'unique_users_monthly_scaled_factor1000.csv'
output_workload_file = cs.DATA_LOCAL_PATH + 'workload_hourly_distribution_scaled_factor1000.csv'


month_total_number_requests = hourly_analysis.calculate_total_number_requests(hourly_access_requests_file)
month_average_number_requests = hourly_analysis.calculate_average_number_requests(hourly_access_requests_file)
day_total_number_requests = hourly_analysis.calculate_daily_total_number_requests(hourly_access_requests_file)
hour_total_number_requests = hourly_analysis.calculate_hourly_total_number_requests(hourly_access_requests_file)
day_workload_probability = hourly_analysis.calculate_daily_probability(hourly_access_requests_file)

users_per_day = np.asarray(usersDailyAnalysis.users_per_day(users_daily_access_file)) / 24
donations_per_day = usersDailyAnalysis.donations_per_day(users_daily_access_file)



# Calculating the proportion of the hourly request w.r.t. the total number of requests per day
hour_total_number_requests_list = hour_total_number_requests[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ].tolist()
day_total_number_requests_list = day_total_number_requests.tolist()
#print hour_total_number_requests_list
#print day_total_number_requests_list

hourly_proportion_wrt_daily_total_requests = []
for day in day_total_number_requests_list:
    for hour in range(0,24):
        proportion = hour_total_number_requests_list[day_total_number_requests_list.index(day) * 24 + hour] / day
        hourly_proportion_wrt_daily_total_requests.append(hour_total_number_requests_list[day_total_number_requests_list.index(day) * 24 + hour] / day)


df = pd.DataFrame({cs.GENERATED_WORKLOAD_COL_DAILY_PROPORTION_REQS : hourly_proportion_wrt_daily_total_requests}, index=hour_total_number_requests.index.values)
hour_total_number_requests[cs.GENERATED_WORKLOAD_COL_DAILY_PROPORTION_REQS ] = df[cs.GENERATED_WORKLOAD_COL_DAILY_PROPORTION_REQS]

# Distributing daily amount of users among the hours. num_users_hour = users_per_day * daily_proportion

users_per_day_list = users_per_day.tolist()
day_count = 0
users_per_hour_list = []
for users in users_per_day_list:
    for hours in range(0,24):
        users_per_hour = users * hourly_proportion_wrt_daily_total_requests[users_per_day_list.index(users) * 24 + hours]
        users_per_hour_list.append(int(round(users_per_hour)))

df = pd.DataFrame({cs.GENERATED_WORKLOAD_COL_HOURLY_CONCURRENT_USERS : users_per_hour_list}, index=hour_total_number_requests.index.values)
hour_total_number_requests[cs.GENERATED_WORKLOAD_COL_HOURLY_CONCURRENT_USERS ] = df[cs.GENERATED_WORKLOAD_COL_HOURLY_CONCURRENT_USERS]

hour_total_number_requests.to_csv(path_or_buf=output_workload_file, sep=' ', index=False)

# Calculating the delay between requests, Uniformely distributed among each hour (3600 sec.) and modifying the original wikipedia page counts workload with the delay

# Generate the list of files to be read
pageCountFileList = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                   cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

# Adapting file list name with scaled suffix
pageCountFileListSuffix = [(i + cs.WIKISTATS_FILE_SCALED_SUFFIX + '.csv') for i in pageCountFileList]


# Distributing the requests
count = 0
for pageCountFile in pageCountFileListSuffix:
    print "Processing File: " + pageCountFile
    pageCountDF = pd.read_csv(cs.DATA_LOCAL_PATH + pageCountFile, delimiter=' ')
    outDataFrame = pd.DataFrame(columns=[cs.WIKISTATS_COL_PROJECT,
                                         cs.WIKISTATS_COL_PAGE,
                                         cs.WIKISTATS_COL_REQUESTS,
                                         cs.WIKISTATS_COL_SIZE,
                                         cs.WIKISTATS_COL_DELAY])

    pageCountDF.columns = cs.WIKISTATS_COLUMNS

    for index,row in pageCountDF.iterrows():
        requests_number = row[cs.WIKISTATS_COL_REQUESTS]
        if requests_number > 1:
            requestsDF = generateRequestsDfFromNumber(row[cs.WIKISTATS_COL_PROJECT],
                                        row[cs.WIKISTATS_COL_PAGE],
                                         row[cs.WIKISTATS_COL_REQUESTS],
                                         row[cs.WIKISTATS_COL_SIZE])
            outDataFrame = outDataFrame.append(requestsDF, ignore_index=True)
        else:
            dfAux = pd.DataFrame(data=[[row[cs.WIKISTATS_COL_PROJECT], row[cs.WIKISTATS_COL_PAGE], int(row[cs.WIKISTATS_COL_REQUESTS]), int(row[cs.WIKISTATS_COL_SIZE]), int(0)]],
                                 columns= [cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE, cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE, cs.WIKISTATS_COL_DELAY])

            outDataFrame = outDataFrame.append(dfAux, ignore_index=True)


    # Shuffling elements

    outDataFrame = shuffle_data_frame(outDataFrame)

    # Saving to File
    print "Saving: " + cs.DATA_LOCAL_PATH + cs.WIKISTATS_GENERATED_WORKLOAD_PREFIX + \
          pageCountFileList[count] + cs.WIKISTATS_FILE_SCALED_SUFFIX + ".csv"
    outDataFrame.to_csv(cs.DATA_LOCAL_PATH + cs.WIKISTATS_GENERATED_WORKLOAD_PREFIX +
                        pageCountFileList[count] + cs.WIKISTATS_FILE_SCALED_SUFFIX + ".csv", sep=' ', index=False)
    count += 1


    # Calculating and filling the delays





