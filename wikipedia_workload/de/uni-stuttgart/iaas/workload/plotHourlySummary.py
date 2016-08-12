import workload.constants as cs
import pandas as pd
from workload import WorkloadSummary as ws
import numpy as np
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, DayLocator, HourLocator, MinuteLocator
from matplotlib import rc
import seaborn as sns

rc('font', **cs.font)

def plot_hourly_summary_workload(filePath='', outputFigureSummaryRequests='.'):
    df = pd.read_csv(filePath, delimiter=' ')
    df.columns = [cs.GENERATED_WORKLOAD_COL_TIMESTAMP,
                  cs.GENERATED_WORKLOAD_COL_SUM_REQS,
                  cs.GENERATED_WORKLOAD_COL_DAILY_PROPORTION_REQS,
                  cs.GENERATED_WORKLOAD_COL_HOURLY_CONCURRENT_USERS]

    df = ws.WorkloadSummary.sortOccurrencesPerTimeStamp(df=df, timestampColName=cs.GENERATED_WORKLOAD_COL_TIMESTAMP)

    # Getting TimeStamp for X-Axis
    timeStamp_list = df[cs.GENERATED_WORKLOAD_COL_TIMESTAMP].tolist()
    date_list = []
    for i in timeStamp_list:
        date_list.append(datetime.datetime.fromtimestamp(i))

    years = YearLocator()   # every year
    months = MonthLocator()  # every month
    yearsFmt = DateFormatter('%Y')
    days = DayLocator()
    daysFmt = DateFormatter('%D')
    minutes = MinuteLocator()
    hours = HourLocator()


    # Creating Figure for the Requests Analysis
    fig1 = plt.figure(figsize=(8, 6))
    plt.suptitle('Workload Summary - Jan. 2016', fontsize=13)

    # Plotting Request Count
    ax1 = plt.subplot(211)
    countRequests = df[cs.GENERATED_WORKLOAD_COL_SUM_REQS].tolist()
    print countRequests
    l1 = ax1.plot(date_list, countRequests, color='b')
    ax1.xaxis.set_visible(False)
    ax1.set_title("Requests - Hourly Distribution")
    ax1.grid(True)

    # Plotting Request Mean
    ax1 = plt.subplot(212)
    concurrent_users = df[cs.GENERATED_WORKLOAD_COL_HOURLY_CONCURRENT_USERS].tolist()
    l2 = ax1.plot(date_list, concurrent_users, color='g')
    ax1.set_title("Concurrent Users - Hourly Distribution")
    #ax1.xaxis.set_visible(False)
    ax1.grid(True)

    # Plotting Request Standard Deviation

    #ax1 = plt.subplot(313)
    #countStd = df[cs.WORKLOAD_SUMMARY_STAT_STD_REQ].tolist()
    #l3 = ax1.plot(date_list, countStd, color='g')
    #ax1.set_title("Standard Deviation")

    # Axis
    ax1.xaxis.set_major_locator(DayLocator())
    ax1.xaxis.set_major_formatter(DateFormatter('%a %Y-%m-%d %H:%M'))
    plt.xticks(rotation=80)
    ax1.grid(True)

    plt.gcf().subplots_adjust(bottom=0.26)
    # Saving Figure to PDF
    fig1.savefig(outputFigureSummaryRequests, format='pdf')





def plot_hourly_summary(filePath='', outputFigureSummaryRequests='.', outputFigureSummaryBytes='.'):
    fileName = filePath

    df = pd.read_csv(fileName, delimiter=' ')

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

    df = ws.WorkloadSummary.sortOccurrencesPerTimeStamp(df=df, timestampColName=cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP)

    arrayRequests = df.as_matrix(columns=[cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ, cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
                                              cs.WORKLOAD_SUMMARY_STAT_STD_REQ, cs.WORKLOAD_SUMMARY_STAT_MAX_REQ,
                                          cs.WORKLOAD_SUMMARY_STAT_SUM_REQ])

    arrayBytes = df.as_matrix(columns=[cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES, cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES,
                                              cs.WORKLOAD_SUMMARY_STAT_STD_BYTES, cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES,
                                       cs.WORKLOAD_SUMMARY_STAT_SUM_BYTES])


    df_non_scaled = pd.read_csv('/Users/gomezsso/Documents/dissertation_evaluation/SCARF-Evaluation/wikipedia_workload/data/1-2016_1-2016_hourly_summary_no_clean.csv', delimiter=' ')
    df_non_scaled.columns = [cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP,
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

    print df_non_scaled[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ].sum()
    print df[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ].sum()
    print df_non_scaled[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ].sum() - df[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ].sum()
    #print df.as_matrix(columns=[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ])

    years = YearLocator()   # every year
    months = MonthLocator()  # every month
    yearsFmt = DateFormatter('%Y')
    days = DayLocator()
    daysFmt = DateFormatter('%D')
    minutes = MinuteLocator()
    hours = HourLocator()

    # Getting TimeStamp for X-Axis
    timeStamp_list = df[cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP].tolist()
    date_list = []
    for i in timeStamp_list:
        date_list.append(datetime.datetime.fromtimestamp(i))

    # Creating Figure for the Requests Analysis
    fig1 = plt.figure(figsize=(8, 6))
    plt.suptitle('Number of Requests - Jan. 2016 Hourly Analysis', fontsize=13)

    # Plotting Request Count
    ax1 = plt.subplot(211)
    countRequests = df[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ].tolist()
    print countRequests
    l1 = ax1.plot(date_list, countRequests, color='b')
    ax1.xaxis.set_visible(False)
    ax1.set_title("Sum")
    ax1.grid(True)


    # Plotting Request Mean
    ax1 = plt.subplot(212)
    countMean = df[cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ].tolist()
    l2 = ax1.plot(date_list, countMean, color='r')
    #ax1.xaxis.set_visible(False)
    ax1.grid(True)

    # Plotting Request Standard Deviation

    #ax1 = plt.subplot(313)
    #countStd = df[cs.WORKLOAD_SUMMARY_STAT_STD_REQ].tolist()
    #l3 = ax1.plot(date_list, countStd, color='g')
    #ax1.set_title("Standard Deviation")

    # Axis
    ax1.xaxis.set_major_locator(DayLocator())
    ax1.xaxis.set_major_formatter(DateFormatter('%a %Y-%m-%d %H:%M'))
    plt.xticks(rotation=80)
    #ax1.grid(True)


    plt.gcf().subplots_adjust(bottom=0.26)




    # Creating Figure for the Requests Analysis
    fig2 = plt.figure(figsize=(8, 6))
    plt.suptitle('Bytes per Request - Jan. 2016 Hourly Analysis', fontsize=13)

    # Plotting Bytes Count

    ax2 = plt.subplot(211)
    countBytes = df[cs.WORKLOAD_SUMMARY_STAT_SUM_BYTES].tolist()
    print countBytes
    ax2.plot(date_list, countBytes, color='b')
    ax2.xaxis.set_visible(False)
    ax2.set_title("Sum")
    ax2.grid(True)

    # Plotting Bytes Mean

    ax2 = plt.subplot(212)
    bytesMean = df[cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES].tolist()
    ax2.plot(date_list, bytesMean, color='r')
    #ax2.xaxis.set_visible(False)
    ax2.grid(True)
    ax2.set_title("Mean")

    # Plotting Bytes Standard Deviation

    #ax2 = plt.subplot(313)
    #bytesStd = df[cs.WORKLOAD_SUMMARY_STAT_STD_BYTES].tolist()
    #ax2.plot(date_list, bytesStd, color='g')
    #ax2.set_title("Standard Deviation")

    # Axis
    #ax2.xaxis.set_major_locator(HourLocator(interval=25))
    ax2.xaxis.set_major_locator(DayLocator())
    ax2.xaxis.set_major_formatter(DateFormatter('%a %Y-%m-%d %H:%M'))
    plt.xticks(rotation=80)
    ax2.grid(True)


    plt.gcf().subplots_adjust(bottom=0.26)


    # Plotting Bytes Max

    # Saving Figure to PDF
    fig1.savefig(outputFigureSummaryRequests, format='pdf')
    fig2.savefig(outputFigureSummaryBytes, format='pdf')
    #plt.show()


#fileName = cs.DATA_LOCAL_PATH + "1-2016_1-2016_hourly_summary.csv"
#fileName = cs.DATA_LOCAL_PATH + "1-2016_1-2016_hourly_summary_scaled_RobustScaler.csv"
#fileName = cs.DATA_LOCAL_PATH + "1-2016_1-2016_hourly_summary_scaled0-1000.csv"
#fileName = cs.DATA_LOCAL_PATH + "1-2016_1-2016_hourly_summary_scaled0-10000.csv"
#fileName = cs.DATA_LOCAL_PATH + "1-2016_1-2016_hourly_summary_scaled_factor100Scaling.csv"
fileNameWorkload = cs.DATA_LOCAL_PATH + "workload_hourly_distribution_scaled_factor100.csv"
outputFiguresPath = cs.FIGURES_LOCAL_PATH + '/'
#outputFigureSummaryRequests = outputFiguresPath + "hourlySummaryRequests_scaleRobustScaler.pdf"
#outputFigureSummaryBytes = outputFiguresPath + "hourlySummaryBytes_scaled_scaleRobustScaler.pdf"
#outputFigureSummaryRequests = outputFiguresPath + "hourlySummaryRequests_scale0-1000.pdf"
#outputFigureSummaryBytes = outputFiguresPath + "hourlySummaryBytes_scaled_scale0-1000.pdf"
#outputFigureSummaryRequests = outputFiguresPath + "hourlySummaryRequests_scalefactor100.pdf"
#outputFigureSummaryBytes = outputFiguresPath + "hourlySummaryBytes_scaled_scalefactor100.pdf"
#plot_hourly_summary(fileName, outputFigureSummaryRequests, outputFigureSummaryBytes)
plot_hourly_summary_workload(filePath=fileNameWorkload, outputFigureSummaryRequests=outputFiguresPath + 'workload_hourly_distribution_scaled_factor100.pdf')


