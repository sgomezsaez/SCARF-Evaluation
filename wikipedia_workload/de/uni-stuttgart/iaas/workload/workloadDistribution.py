import matplotlib.pyplot as plt
from workload import constants as cs
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, DayLocator, HourLocator, MinuteLocator
import datetime
import matplotlib.mlab as mlab
import pandas as pd
from workload import WorkloadSummary as ws


def plot_workload_distribution_summary(fileSummaryPath=''):
    fileName = fileSummaryPath
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
    fig1.subplots_adjust(hspace=.3)
    plt.suptitle('Distribution of Requests/hour - January 2016', fontsize=13)

    # Plotting Request Count
    ax1 = fig1.add_subplot(211)
    countRequests = df[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ].tolist()
    n, bins, patches = ax1.hist(countRequests, 50, normed=True, facecolor='black', alpha=0.5)
    bincenters = 0.5*(bins[1:]+bins[:-1])
    mu, sigma = 100, 15
    y = mlab.normpdf( bincenters, mu, sigma)
    ## l1 = ax1.plot(bincenters, y, 'r--', linewidth=10)
    #ax1.xaxis.set_visible(False)
    ax1.set_title("Number of Requests")
    #ax1.set_yscale('log', basex=10)
    ax1.grid(True)
    plt.xticks(rotation=5)

    # Plotting Bytes Count
    ax1 = fig1.add_subplot(212)
    countBytes = df[cs.WORKLOAD_SUMMARY_STAT_SUM_BYTES].tolist()
    mu, sigma = 100, 15
    n, bins, patches = ax1.hist(countBytes, 50, normed=True, facecolor='black', alpha=0.5)
    bincenters = 0.5*(bins[1:]+bins[:-1])
    y = mlab.normpdf( bincenters, mu, sigma)
    #l2 = ax1.plot(bincenters, y, 'r--', linewidth=10)
    ax1.set_title("Size of Requests")
    #ax1.set_yscale('log', basex=10)
    ax1.grid(True)

    #ax1.xaxis.set_visible(False)
    #ax2.set_yscale('log')
    #ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    #plt.xticks(rotation=70)
    #ax1.xaxis.set_major_locator(HourLocator(interval=25))
    #ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))
    #plt.xticks(rotation=80)
    #ax1.grid(True)
    #ax1.set_title("Bytes Distribution")


    plt.show()

fileName = cs.DATA_LOCAL_PATH + "1-2016_1-2016_hourly_summary.csv"
plot_workload_distribution_summary(fileName)