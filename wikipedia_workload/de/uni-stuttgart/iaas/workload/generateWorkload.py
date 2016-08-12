import workload.constants as cs
import pandas as pd
import hourly_analysis, usersDailyAnalysis
import csvHelper.csvHelper as csvHelper
import numpy as np
from workload import WorkloadSummary as ws
from datetime import datetime

hourly_access_requests_file = cs.DATA_LOCAL_PATH + "1-2016_1-2016_hourly_summary_scaled_factor100Scaling.csv"
users_daily_access_file = cs.DATA_LOCAL_PATH + 'unique_users_monthly_scaled_factor100.csv'
output_workload_file = cs.DATA_LOCAL_PATH + 'workload_hourly_distribution_scaled_factor100.csv'


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