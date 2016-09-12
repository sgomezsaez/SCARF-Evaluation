import pandas as pd
import utils as ut
import constants as cs
import matplotlib.pyplot as plt
import numpy as np
import datetime
import calendar
import time

# Create list of files to analyze

def createFileList(results_path, scenario_list, scenario_file):
    fileList = []
    for i in scenario_list:
        fileList.append(results_path + i[0] + '/' + scenario_file)
    return fileList


def line_plot_summary_hourly_analysis(file_list, scenario_list, plot_parameter, plot_output_file, plot_title):
    scenario_count = 0
    scenario_colors = ['lightblue', 'lightgreen', 'lightgrey', 'cyan', 'magenta', 'darkgrey', 'khaki', 'limegreen']


    # Creating Plot
    fig1 = plt.figure(figsize=(7, 6))
    plt.suptitle(plot_title, fontsize=20)
    ax1 = plt.subplot(111)

    for i in file_list:
        scenario = scenario_list[scenario_count][0]

        df = pd.read_csv(i, delimiter=',')

        x_axis_data = range(1, len(df) + 1)
        y_axis_data = df[plot_parameter].tolist()

        print y_axis_data

        l1 = ax1.plot(x_axis_data, y_axis_data, color=scenario_colors[scenario_count], label=scenario, linewidth=1.5)
        scenario_count += 1

    ax1.grid(True)
    handles, labels = ax1.get_legend_handles_labels()
    plt.legend(ut.flip(handles, 2), ut.flip(labels, 2), bbox_to_anchor=(0.5, 1.12), loc=9, ncol=4, prop={'size':15})
    ax1.set_xlabel('Hourly Interval', fontsize=20)
    ax1.set_ylabel(plot_parameter, fontsize=20)
    fig1.savefig(plot_output_file, format='pdf')
    print "Saving to %s" %(plot_output_file)
    #plt.show()


def bar_plot_average_hourly_analysis(file_list, scenario_list, plot_parameter, plot_output_file, plot_title):
    scenario_patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
    scenario_count = 0

    # Creating Plot
    fig1 = plt.figure(figsize=(7, 6))
    plt.suptitle(plot_title, fontsize=20)
    ax1 = fig1.add_subplot(111)

    # Create X Axis
    x_axis_list = []
    for i in scenario_list:
        x_axis_list.append(i[0])

    x_axis_list = x_axis_list

    y_axis_list = []

    for i in file_list:
        scenario = scenario_list[scenario_count][0]

        df = pd.read_csv(i, delimiter=',')
        if (plot_parameter == cs.HOUR_SUMMARY_SUM_REQS_SUCCESS or plot_parameter == cs.HOUR_SUMMARY_AVG_LATENCY):
            y_axis_data = df[plot_parameter].describe().iloc[1]
            if plot_parameter == cs.HOUR_SUMMARY_AVG_LATENCY:
                y_axis_data = y_axis_data / 1000

        if (plot_parameter == cs.HOUR_SUMMARY_SUM_BYTES_TRANSFERRED or plot_parameter == cs.HOUR_SUMMARY_TIMESTAMP_DURATION or plot_parameter == cs.HOUR_SUMMARY_SUM_RESP_500):
            y_axis_data = df[plot_parameter].sum()

        if (plot_parameter == cs.HOUR_SUMMARY_TIMESTAMP_DURATION):
            y_axis_data = df[plot_parameter].sum() / 3600


        if (plot_parameter == cs.HOUR_SUMMARY_ERROR_RATE):
            y_axis_data = (1 - (float(df[cs.HOUR_SUMMARY_SUM_REQS_SUCCESS].sum()) / float(df[cs.HOUR_SUMMARY_SUM_ALL_REQS].sum())))

        y_axis_list.append(y_axis_data)


    x_axis_num = np.arange(1, len(x_axis_list) + 1)
    ax1.bar(x_axis_num, y_axis_list, align='center', color='grey', edgecolor='black', alpha=0.85)
    ax1.set_xticks(x_axis_num)
    ax1.set_xticklabels(x_axis_list, fontsize=20)
    if (plot_parameter == cs.HOUR_SUMMARY_TIMESTAMP_DURATION):
        ax1.set_ylabel('duration_hour', fontsize=20)
    if (plot_parameter == cs.HOUR_SUMMARY_AVG_LATENCY):
        ax1.set_ylabel('avg_latency (s)', fontsize=20)
    else:
        ax1.set_ylabel(plot_parameter, fontsize=20)
    #ax1.set_xlabel('$T^{\mu}_{i}$', fontsize=15)
    ax1.grid(True)
    fig1.savefig(plot_output_file, format='pdf')
    print "Saving to %s" %(plot_output_file)
    #plt.show()



file_list = createFileList(cs.EXP_RESULTS_DATA_PATH, cs.EXP_RESULTS_DATA_SCENARIOS, cs.SUMMARY_HOURLY_RESULTS_OUTPUT_FILE_NAME + '.csv')

print file_list

#line_plot_summary_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_SUM_REQS_SUCCESS,
#                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_REQ_SUCCESS_FILE, '')

bar_plot_average_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_SUM_REQS_SUCCESS,
                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_REQ_SUCCESS_FILE, cs.PLOT_RESULTS_TITLE_REQ_SUCCESS)

bar_plot_average_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_AVG_LATENCY,
                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_LATENCY_FILE, cs.PLOT_RESULTS_TITLE_LATENCY)

bar_plot_average_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_TIMESTAMP_DURATION,
                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_EXP_DURATION_FILE, cs.PLOT_RESULTS_TITLE_DURATION)

bar_plot_average_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_SUM_BYTES_TRANSFERRED,
                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_BYTES_TRANSFERRED_FILE, cs.PLOT_RESULTS_TITLE_BYTES_TRANSFERRED)

bar_plot_average_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_SUM_RESP_500,
                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_SERVER_FAILURE_FILE, cs.PLOT_RESULTS_TITLE_REQ_SERVER_FAILURE)

bar_plot_average_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_ERROR_RATE,
                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_TRANSACTION_ERROR_RATE_FILE, cs.PLOT_RESULTS_TITLE_TRANSACTION_ERROR_RATE)
