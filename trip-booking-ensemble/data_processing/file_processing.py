import csvHelper
import constants
import os
import pandas as pd
import numpy

def merge_load_test_results(directory_path):
    summary_data_frame = pd.DataFrame(columns=constants.JMETER_RESULTS_CSV_COLUMNS)
    if os.path.isdir(directory_path):
        for file_name in os.listdir(directory_path):
            file_data_frame = csvHelper.data_frame_from_csv(directory_path + '/' + file_name,
                                                           constants.JMETER_RESULTS_CSV_COLUMNS)
            summary_data_frame = summary_data_frame.append(file_data_frame, ignore_index=True)
    return summary_data_frame

def clean_data_frame(df, column_name, filter_out_value):
    return df[df[column_name] != filter_out_value]

def create_summary_from_dataframe(zeta_topology, df):
    summary_data_frame = pd.DataFrame(columns=constants.JMETER_SUMMARY_RESULTS_CSV_COLUMNS)

    mean_elapsed = df[df[constants.ARGUMENTS_JMETER_RESPONSE_CODE] == '200'][constants.ARGUMENTS_JMETER_ELAPSED].mean()
    count_req_successful = df[df[constants.ARGUMENTS_JMETER_RESPONSE_CODE] == '200'][constants.ARGUMENTS_JMETER_RESPONSE_CODE].count()
    count_req_unsuccessful = df[df[constants.ARGUMENTS_JMETER_RESPONSE_CODE] != '200'][constants.ARGUMENTS_JMETER_RESPONSE_CODE].count()
    mean_latency = df[df[constants.ARGUMENTS_JMETER_RESPONSE_CODE] == '200'][constants.ARGUMENTS_JMETER_LATENCY].mean()
    total_requests = df[constants.ARGUMENTS_JMETER_ELAPSED].count()
    avg_requests_per_user = total_requests / constants.TOTAL_NUMBER_USERS
    topology_availability = constants.AWS_AVAILABILITY_SLA
    total_req_latency_greater_twenty = df[df[constants.ARGUMENTS_JMETER_LATENCY] >= 20000][constants.ARGUMENTS_JMETER_LATENCY].count()

    df2 = pd.DataFrame([[zeta_topology, topology_availability, mean_elapsed,
                         count_req_successful, count_req_unsuccessful, mean_latency,
                         total_requests, total_req_latency_greater_twenty, avg_requests_per_user, 0.0]],
                              columns=constants.JMETER_SUMMARY_RESULTS_CSV_COLUMNS)

    summary_data_frame = summary_data_frame.append(df2, ignore_index=True)

    return summary_data_frame

def attach_price_to_dataframe(df, prices):
    for index, row in df.iterrows():
        zeta_topology = row['zeta_topology']
        df.set_value(index, 'price', prices[zeta_topology])