import workload.constants as cs
import pandas as pd
from workload import WorkloadSummary as ws
import numpy as np
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, DayLocator, HourLocator, MinuteLocator
from matplotlib import rc
import seaborn as sns


def plot_daily_access_summary(filePath='', outputFigureSummaryAccess='.'):
    fileName = filePath

    df = pd.read_csv(fileName, delimiter=' ')

    df.columns = cs.WIKISTATS_UNIQUE_DEVICES_COL_LIST

    array_mobile = df.as_matrix(columns=[cs.WIKISTATS_UNIQUE_DEVICES_EN_WIKI_MOBILE]) / 100
    array_computer = df.as_matrix(columns=[cs.WIKISTATS_UNIQUE_DEVICES_EN_WIKI]) / 100
    array_total = df.as_matrix(columns=[cs.WIKISTATS_UNIQUE_DEVICES_EN_WIKI_TOTAL]) / 100

    years = YearLocator()   # every year
    months = MonthLocator()  # every month
    yearsFmt = DateFormatter('%Y')
    days = DayLocator()
    daysFmt = DateFormatter('%D')
    minutes = MinuteLocator()
    hours = HourLocator()


    # Getting TimeStamp for X-Axis
    timeStamp_list = df[cs.WIKISTATS_UNIQUE_DEVICES_TIMESTAMP].tolist()
    date_list = []
    for i in timeStamp_list:
        date_list.append(datetime.datetime.fromtimestamp(i))

    # Creating Figure for the Requests Analysis
    fig1 = plt.figure(figsize=(8, 6))
    plt.suptitle('Daily Access - Jan. 2016', fontsize=15)

    # Plotting Request Count
    ax1 = plt.subplot(111)
    ax1.plot(date_list, array_mobile, "r.-", label=cs.WIKISTATS_UNIQUE_DEVICES_EN_WIKI_MOBILE)
    ax1.plot(date_list, array_computer, "gv-.",label=cs.WIKISTATS_UNIQUE_DEVICES_EN_WIKI)
    ax1.plot(date_list, array_total, "b^-",label=cs.WIKISTATS_UNIQUE_DEVICES_EN_WIKI_TOTAL)
    plt.ylabel('Devices', fontsize=15)
    #plt.xlabel('Day', fontsize=15)
    ax1.grid(True)
    ax1.xaxis.set_major_locator(DayLocator())
    ax1.xaxis.set_major_formatter(DateFormatter('%a %Y-%m-%d %H:%M'))
    plt.xticks(rotation=80)
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00),
          ncol=3, fancybox=True, shadow=True, fontsize=12)

    plt.gcf().subplots_adjust(bottom=0.26)
    #plt.show()
    # Saving Figure to PDF
    fig1.savefig(outputFigureSummaryAccess, format='pdf')

fileName = cs.WIKISTATS_UNIQUE_DEVICES_FILE_PATH
outputFiguresPath = cs.FIGURES_LOCAL_PATH + '/' + "dailySummaryAccesses_scaled100.pdf"
outputFigureSummaryAccesses = outputFiguresPath
plot_daily_access_summary(fileName, outputFiguresPath)
