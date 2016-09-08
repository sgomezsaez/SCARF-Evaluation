import pandas as pd
import utils as ut
import constants as cs
import datetime
import calendar
import time

def calculate_total_concurrent_users(df):
    thread_labels = df.as_matrix(columns=[cs.EXP_RESULTS_LABEL]).flatten()
    max_num_threads = 0

    for i in thread_labels:
        thread_num = int(i.split(' ')[len(i.split(' ')) - 1])
        if thread_num >= max_num_threads:
            max_num_threads = thread_num

    return max_num_threads


def create_df_summary_hour_from_file(file_path=''):
    print "# Creating DF Hourly Summary for File: %s" % file_path
    df = pd.read_csv(file_path, delimiter=',')

    fileName = file_path.split('/')[len(file_path.split('/')) - 1]

    hour_timestamp = ut.get_timestamp_from_file_name(fileName)

    # Change Data Type of Column Response Code
    df[[cs.EXP_RESULTS_RESP_CODE]] = df[[cs.EXP_RESULTS_RESP_CODE]].astype(str)

    description = df.describe()
    mean_elapsed = description.iloc[1][cs.EXP_RESULTS_ELAPSED]
    total_reqs_resp_200 = len(df[df[cs.EXP_RESULTS_RESP_CODE] == '200'])
    total_reqs_resp_404 = len(df[df[cs.EXP_RESULTS_RESP_CODE] == '404'])
    total_reqs_resp_500 = len(df[(df[cs.EXP_RESULTS_RESP_CODE] == '500') | (df[cs.EXP_RESULTS_RESP_CODE] == '502') | (df[cs.EXP_RESULTS_RESP_CODE] == '504')])
    total_reqs_success = len(df[df[cs.EXP_RESULTS_SUCCESS] == True])
    total_reqs = len(df)
    mean_bytes = description.iloc[1][cs.EXP_RESULTS_BYTES]
    mean_latency = description.iloc[1][cs.EXP_RESULTS_LATENCY]
    total_concurrent_users = calculate_total_concurrent_users(df)
    mean_reqs_per_sec = 1 / (description.iloc[1][cs.EXP_RESULTS_LATENCY] / 1000)
    total_bytes = df[cs.EXP_RESULTS_BYTES].sum()

    sorted_df_timestamp = df.sort_index(by=[cs.EXP_RESULTS_TIMESTAMP], ascending=True)

    start_timestamp = time.mktime(datetime.datetime.strptime(sorted_df_timestamp.iloc[0][cs.EXP_RESULTS_TIMESTAMP], "%Y/%m/%d %H:%M:%S").timetuple())
    end_timestamp = time.mktime(datetime.datetime.strptime(sorted_df_timestamp.iloc[len(sorted_df_timestamp) - 1][cs.EXP_RESULTS_TIMESTAMP], "%Y/%m/%d %H:%M:%S").timetuple())
    duration_sec = (datetime.datetime.strptime(df.iloc[len(sorted_df_timestamp) - 1][cs.EXP_RESULTS_TIMESTAMP], "%Y/%m/%d %H:%M:%S") -
                    datetime.datetime.strptime(df.iloc[0][cs.EXP_RESULTS_TIMESTAMP], "%Y/%m/%d %H:%M:%S")).seconds

    data = [[hour_timestamp, mean_elapsed, total_reqs_resp_200, total_reqs_resp_404, total_reqs_resp_500, total_reqs_success, total_reqs,
            mean_bytes, mean_latency, total_concurrent_users, mean_reqs_per_sec, total_bytes, start_timestamp,
            end_timestamp, duration_sec]]
    return pd.DataFrame(data, columns=cs.SUMMARY_HOURLY_RESULTS_INPUT_COLUMNS_LIST)


def create_df_summary_experiment_scenario_round(dir_path, scenarioID, scenarioRound, outputFileName):
    scenario_path = dir_path + scenarioID
    file_list = ut.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH, cs.WIKISTATS_BEGIN_DAY,
                                            cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH, cs.WIKISTATS_END_DAY,
                                            cs.WIKISTATS_HOURS, '', suffix='_'+ scenarioRound + '.jtl')
    df = None

    for i in file_list:
        print "### Processing File %s" % (scenario_path + '/' + i)
        if file_list.index(i) > 0 :
            df = df.append(create_df_summary_hour_from_file(file_path=scenario_path + '/' + i), ignore_index=True)
        else:
            df = create_df_summary_hour_from_file(file_path=scenario_path + '/' + i)

    df.to_csv(path_or_buf=scenario_path + '/' + outputFileName + '.csv', sep=',', index=False, header=True)











file_list = ut.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH, cs.WIKISTATS_BEGIN_DAY,
                                            cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH, cs.WIKISTATS_END_DAY,
                                            cs.WIKISTATS_HOURS, '', suffix='_'+ cs.EXP_RESULTS_DATA_ROUND + '.jtl')

#print create_df_summary_hour_from_file(file_path=cs.EXP_RESULTS_DATA_PATH + 'T1/' + file_list[0])

create_df_summary_experiment_scenario_round(cs.EXP_RESULTS_DATA_PATH, cs.EXP_RESULTS_DATA_SCENARIOS[0],
                                            cs.EXP_RESULTS_DATA_ROUND, cs.SUMMARY_HOURLY_RESULTS_OUTPUT_FILE_NAME)