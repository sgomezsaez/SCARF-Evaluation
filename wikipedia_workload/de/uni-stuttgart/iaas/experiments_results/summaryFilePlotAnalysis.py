import pandas as pd
import utils as ut
import constants as cs
import matplotlib.pyplot as plt
import numpy as np
import datetime
import calendar
import time
import math

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
            print df[plot_parameter].tolist()
            y_axis_data = df[plot_parameter].sum() / 3600



        if (plot_parameter == cs.HOUR_SUMMARY_ERROR_RATE):
            y_axis_data = (1 - (float(df[cs.HOUR_SUMMARY_SUM_REQS_SUCCESS].sum()) / float(df[cs.HOUR_SUMMARY_SUM_ALL_REQS].sum())))


        y_axis_list.append(y_axis_data)

    # Calculating Percentages
    if (plot_parameter == cs.HOUR_SUMMARY_ERROR_RATE):
        min_error_rate = min(y_axis_list)
        percent_diff_t4 = (1 - (min_error_rate / y_axis_list[3])) * 100
        percent_diff_t5 = (1 - (min_error_rate / y_axis_list[4])) * 100

        print min_error_rate
        print y_axis_list

        print percent_diff_t4
        print percent_diff_t5

    if (plot_parameter == cs.HOUR_SUMMARY_AVG_LATENCY):
        print y_axis_list

        # Average when distributing the stack in two VMs and one VM
        # avg T1,T3,T6
        avg_t16 = (y_axis_list[0] + y_axis_list[5]) / 2
        # avg T2,T7
        avg_t27 = (y_axis_list[1] + y_axis_list[6]) / 2

        print "Analysis between full stack vm and separate vms"
        print 1 - (avg_t27 / avg_t16)

        # Analysis between separate vms and database as a service
        print "Analysis separate vms and database as a service"
        avg_t1 = y_axis_list[0]
        avg_t3 = y_axis_list[2]

        print 1 - (avg_t1 / avg_t3)

        # Analysis between container (azure) and separate vms and DBaaS
        print "Analysis between container (azure) and separate vms and DBaaS"
        avg_t8 = y_axis_list[7]
        avg_t6 = y_axis_list[5]

        print 1 - (avg_t6 / avg_t8)

        print "Provider Comparison"

        print "VMs distributed"
        avg_t1 = y_axis_list[0]
        avg_t6 = y_axis_list[5]

        print 1 - (avg_t1 / avg_t6)

        print "VMs full stack"
        avg_t2 = y_axis_list[1]
        avg_t7 = y_axis_list[6]

        print 1 - (avg_t2 / avg_t7)

    if (plot_parameter == cs.HOUR_SUMMARY_SUM_BYTES_TRANSFERRED):
        print y_axis_list
        gb_list = [i / math.pow(2,30) for i in y_axis_list]
        print gb_list


    x_axis_num = np.arange(1, len(x_axis_list) + 1)
    ax1.bar(x_axis_num, y_axis_list, align='center', color='grey', edgecolor='black', alpha=0.85)
    ax1.set_xticks(x_axis_num)
    ax1.set_xticklabels(x_axis_list, fontsize=20)
    if (plot_parameter == cs.HOUR_SUMMARY_TIMESTAMP_DURATION):
        ax1.set_ylabel('Experiment Duration (h)', fontsize=20)
    elif (plot_parameter == cs.HOUR_SUMMARY_AVG_LATENCY):
        ax1.set_ylabel('Average Latency (s)', fontsize=20)
    elif (plot_parameter == cs.HOUR_SUMMARY_ERROR_RATE):
        ax1.set_ylabel('Average Error Rate', fontsize=20)
    elif (plot_parameter == cs.HOUR_SUMMARY_SUM_BYTES_TRANSFERRED):
        ax1.set_ylabel('Total Bytes Transferred', fontsize=20)
    else:
        ax1.set_ylabel(plot_parameter, fontsize=20)
    #ax1.set_xlabel('$T^{\mu}_{i}$', fontsize=15)
    ax1.grid(True)
    #fig1.savefig(plot_output_file, format='pdf')
    #print "Saving to %s" %(plot_output_file)
    #plt.show()



file_list = createFileList(cs.EXP_RESULTS_DATA_PATH, cs.EXP_RESULTS_DATA_SCENARIOS, cs.SUMMARY_HOURLY_RESULTS_OUTPUT_FILE_NAME + '.csv')

print file_list

#line_plot_summary_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_SUM_REQS_SUCCESS,
#                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_REQ_SUCCESS_FILE, '')

#bar_plot_average_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_SUM_REQS_SUCCESS,
#                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_REQ_SUCCESS_FILE, cs.PLOT_RESULTS_TITLE_REQ_SUCCESS)

bar_plot_average_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_AVG_LATENCY,
                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_LATENCY_FILE, cs.PLOT_RESULTS_TITLE_LATENCY)

bar_plot_average_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_TIMESTAMP_DURATION,
                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_EXP_DURATION_FILE, cs.PLOT_RESULTS_TITLE_DURATION)

bar_plot_average_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_SUM_BYTES_TRANSFERRED,
                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_BYTES_TRANSFERRED_FILE, cs.PLOT_RESULTS_TITLE_BYTES_TRANSFERRED)

#bar_plot_average_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_SUM_RESP_500,
#                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_SERVER_FAILURE_FILE, cs.PLOT_RESULTS_TITLE_REQ_SERVER_FAILURE)

bar_plot_average_hourly_analysis(file_list, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, cs.HOUR_SUMMARY_ERROR_RATE,
                             cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_RESULTS_TRANSACTION_ERROR_RATE_FILE, cs.PLOT_RESULTS_TITLE_TRANSACTION_ERROR_RATE)
