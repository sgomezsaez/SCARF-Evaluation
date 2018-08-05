import constants as cs
import file_processing as fp
import pandas as pd
import constants
import math
import os

def calculate_avg_revenue_user():
    avg_travel_time = (constants.CUSTOMER_AVG_TRAVEL_KMS / constants.CUSTOMER_MAX_TRAVEL_TIME_PER_MINUTE_PER_KM) + \
                      (constants.CUSTOMER_AVG_NUMBER_OF_CHANGES * constants.CUSTOMER_AVG_WAITING_TIME_CHANGE)

    if avg_travel_time < constants.CUSTOMER_TICKET_PRICE_TIME:
        return constants.CUSTOMER_TICKET_PRICE
    else:
        return math.ceil(avg_travel_time / constants.CUSTOMER_TICKET_PRICE_TIME) * constants.CUSTOMER_TICKET_PRICE

def workload_probability():
    return constants.WORKLOAD_PROBABILITY

def avg_transactions_user(df):
    return df['total_requests'] / (constants.TOTAL_NUMBER_USERS * 2)

def avg_error_rate(df):
    return df['count_requests_unsuccessful'] / df['total_requests']

def avg_user_satisfaction(df):
    total_reqs_latency_greater_twenty = df['total_req_latency_greater_20_s']
    total_reqs_error = df['count_requests_unsuccessful']
    total_reqs = df['total_requests']

    return 1 - ((total_reqs_latency_greater_twenty + total_reqs_error) / total_reqs)

def calculate_revenue(row):
    workload_probability_value = workload_probability()
    avg_error_rate_value = avg_error_rate(row)
    avg_transactions_per_user_value = avg_transactions_user(row)
    time_interval = constants.TIME_INTERVAL
    revenue_per_user_value = calculate_avg_revenue_user()
    users = constants.TOTAL_NUMBER_USERS
    availability = constants.AWS_AVAILABILITY_SLA / 100.0

    # print 'Revenue Calculation: '
    # print 'workload probability: ' + str(workload_probability_value)
    # print 'avg error rate: ' + str(avg_error_rate_value)
    # print 'avg transactions per user: ' + str(avg_transactions_per_user_value)
    # print 'time interval: ' + str(time_interval)
    # print 'revenue per user: ' + str(revenue_per_user_value)
    # print 'users: ' + str(users)
    # print 'availability: ' + str(availability)


    return workload_probability_value * (1 - avg_error_rate_value) * time_interval * \
           avg_transactions_per_user_value * revenue_per_user_value * users * availability


def calculate_utility(df):

    df['utility'] = 0.0
    for index, row in df.iterrows():
        revenue = calculate_revenue(row)
        satisfaction = avg_user_satisfaction(row)
        cost = row['price'] * constants.TIME_INTERVAL

        df.set_value(index, 'utility', (revenue * satisfaction) - cost)

    return df

print 'Calculating Utility...'
print 'Starting File Processing...'
print 'Creating a Summary of all Evaluation Results...'

summary_all_data_frame = pd.DataFrame(columns=constants.JMETER_SUMMARY_RESULTS_CSV_COLUMNS)

for zeta_topology in os.listdir(constants.ARGUMENTS_JMETER_RESULTS_PATH_VAR):
    if os.path.isdir(constants.ARGUMENTS_JMETER_RESULTS_PATH_VAR + zeta_topology):
        merged_results = fp.merge_load_test_results(constants.ARGUMENTS_JMETER_RESULTS_PATH_VAR + zeta_topology)

        filtered_results_data_frame = fp.clean_data_frame(merged_results, constants.ARGUMENTS_JMETER_LABEL, 'BeanShell Sampler')
        summary_data_frame = fp.create_summary_from_dataframe(zeta_topology, filtered_results_data_frame)
        summary_all_data_frame = summary_all_data_frame.append(summary_data_frame)

summary_all_data_frame = summary_all_data_frame.reset_index()
fp.attach_price_to_dataframe(summary_all_data_frame, constants.ZETA_TOPOLOGIES)

#print summary_all_data_frame

print calculate_utility(summary_all_data_frame).sort_values(by=['utility'], ascending=False)[['zeta_topology', 'utility']]
