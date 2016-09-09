import pandas as pd
import utils as ut
import constants as cs
import matplotlib.pyplot as plt
import datetime
import calendar
import time

# Create list of files to analyze

def createFileList(results_path, scenario_list, scenario_file):
    fileList = []
    for i in scenario_list:
        fileList.append(results_path + i + '/' + scenario_file)
    return fileList


def plot_summary_hourly_analysis(file_list, scenario_list, plot_parameter, plot_output_file, plot_title):
    scenario_count = 0
    scenario_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']


    # Creating Plot
    fig1 = plt.figure(figsize=(8, 6))
    plt.suptitle(plot_title, fontsize=20)
    ax1 = plt.subplot(111)

    for i in file_list:
        scenario = scenario_list[scenario_count]

        df = pd.read_csv(i, delimiter=',')

        x_axis_data = range(1, len(df) + 1)
        y_axis_data = df[plot_parameter].tolist()

        print y_axis_data

        l1 = ax1.plot(x_axis_data, y_axis_data, color=scenario_colors[scenario_count], label=scenario, linewidth=1.5)
        scenario_count += 1

    ax1.grid(True)
    plt.legend()
    ax1.set_xlabel('Hourly Interval', fontsize=20)
    ax1.set_ylabel(plot_parameter, fontsize=20)
    #fig1.savefig(plot_output_file, format='pdf')
    plt.show()




print createFileList(cs.EXP_RESULTS_DATA_PATH, cs.EXP_RESULTS_DATA_SCENARIOS, cs.SUMMARY_HOURLY_RESULTS_OUTPUT_FILE_NAME + '.csv')

plot_summary_hourly_analysis(['/Users/gomezsso/Documents/dissertation_evaluation/SCARF-Evaluation/wikipedia_workload/experiments_results/T1/summary_results_hourly.csv',
                              '/Users/gomezsso/Documents/dissertation_evaluation/SCARF-Evaluation/wikipedia_workload/experiments_results/T2/summary_results_hourly.csv',
                              '/Users/gomezsso/Documents/dissertation_evaluation/SCARF-Evaluation/wikipedia_workload/experiments_results/T3/summary_results_hourly.csv',
                              #'/Users/gomezsso/Documents/dissertation_evaluation/SCARF-Evaluation/wikipedia_workload/experiments_results/T5/summary_results_hourly.csv',
                              '/Users/gomezsso/Documents/dissertation_evaluation/SCARF-Evaluation/wikipedia_workload/experiments_results/T6/summary_results_hourly.csv',
                              '/Users/gomezsso/Documents/dissertation_evaluation/SCARF-Evaluation/wikipedia_workload/experiments_results/T7/summary_results_hourly.csv'],
                             ['T1', 'T2', 'T3', 'T6', 'T7'], cs.HOUR_SUMMARY_TIMESTAMP_DURATION, cs.PLOT_RESULTS_LATENCY_FILE, 'Successful Requests per Distribution')
