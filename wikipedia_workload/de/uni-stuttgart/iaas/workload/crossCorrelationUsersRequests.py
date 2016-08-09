import workload.constants as cs
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import workload.WorkloadSummary as ws
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import datasets, linear_model
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, DayLocator, HourLocator, MinuteLocator
import matplotlib
from scipy import optimize as opt



def correlate_users_requests():


    requests_summary_file = cs.DATA_LOCAL_PATH + "1-2016_1-2016_hourly_summary_scaled_factor100Scaling.csv"
    users_access_file = cs.WIKISTATS_UNIQUE_DEVICES_FILE_PATH
    df_requests_summary = pd.read_csv(requests_summary_file, delimiter=' ')
    df_users_access = pd.read_csv(users_access_file, delimiter=' ')

    df_requests_summary = ws.WorkloadSummary.sortOccurrencesPerTimeStamp(df=df_requests_summary, timestampColName=cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP)

    timeStampToDateTime = lambda x: datetime.fromtimestamp(
            int(x)
        ).strftime('%Y-%m-%d %H:%M:%S')

    df_requests_summary[cs.WIKISTATS_UNIQUE_DEVICES_TIMESTAMP] = \
        df_requests_summary[cs.WIKISTATS_UNIQUE_DEVICES_TIMESTAMP].map(timeStampToDateTime)

    df_grouped = df_requests_summary[[cs.WIKISTATS_UNIQUE_DEVICES_TIMESTAMP, cs.WORKLOAD_SUMMARY_STAT_SUM_REQ]].groupby(
            df_requests_summary[cs.WIKISTATS_UNIQUE_DEVICES_TIMESTAMP].map(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').day)).sum()

    array_requests = df_grouped.as_matrix(columns=[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ])
    array_user_access = df_users_access.as_matrix(columns=[cs.WIKISTATS_UNIQUE_DEVICES_EN_WIKI_TOTAL]) / 100

    base = datetime.fromtimestamp(int(df_users_access.iloc[0][cs.WIKISTATS_UNIQUE_DEVICES_TIMESTAMP]))
    date_list = [(base + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(0, 31)]

    correlation_array = np.correlate(array_user_access.flatten(), array_requests.flatten(), mode='same')
    pearson_correlation = stats.pearsonr(array_user_access.flatten(), array_requests.flatten())

    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Train the model using the training sets
    regr.fit(array_user_access, array_requests)

    # Creating Figure for the Requests Analysis
    fig1 = plt.figure(figsize=(8, 6))
    # Plotting Request Count
    ax1 = plt.subplot(111)
    #ax1.plot(df_grouped.as_matrix(columns=[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ]), "r.-")
    ax1.scatter(array_user_access, array_requests, s=20, alpha=0.5, color='black')
    plt.title('Daily Users Access vs. Wikipedia Requests', fontsize=15)
    plt.xlabel('Users', fontsize=15)
    plt.ylabel('Requests', fontsize=15)
    ax1.plot(array_user_access, regr.predict(array_user_access), color='blue', linewidth=2, label='Linear Regression')

    pearson_legend = 'pearson correlation= '+ str(format(pearson_correlation[0], '.3f'))

    plt.text(50, 50, r'$\mu=100,\ \sigma=15$')
    plt.annotate(pearson_legend, xy=(600000, 250000), xytext=(600000, 250000), fontsize = 15
                )
    plt.show()


def correlate_users_donations(unique_access_users_file):
    df_users_access = pd.read_csv(unique_access_users_file, delimiter=' ')

    array_user_access = df_users_access.as_matrix(columns=[cs.WIKISTATS_UNIQUE_DEVICES_EN_WIKI_TOTAL])
    array_donations = df_users_access.as_matrix(columns=[cs.WIKISTATS_DAILY_DONATIONS]) / 100

    pearson_correlation = stats.pearsonr(array_user_access.flatten(), array_donations.flatten())

    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Train the model using the training sets
    regr.fit(array_user_access, array_donations)

    # Creating Figure for the Requests Analysis
    fig1 = plt.figure(figsize=(8, 6))
    # Plotting Request Count
    ax1 = plt.subplot(111)
    #ax1.plot(df_grouped.as_matrix(columns=[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ]), "r.-")
    ax1.scatter(array_user_access, array_donations, s=20, alpha=0.5)
    plt.title('Correlation Users Daily Access vs. Donations', fontsize=15)
    plt.xlabel('Users', fontsize=15)
    plt.ylabel('Donations', fontsize=15)
    ax1.plot(array_user_access, regr.predict(array_user_access), color='red', linewidth=2, label='Linear Regression')

    pearson_legend = 'pearson correlation= '+ str(format(pearson_correlation[0], '.3f'))

    plt.text(50, 50, r'$\mu=100,\ \sigma=15$')
    plt.annotate(pearson_legend, xy=(600000, 250000), xytext=(600000, 250000), fontsize = 15
                )
    plt.show()

def average_revenue_per_user(array_users_access, array_users_donations):
    return array_users_donations / array_users_access

#We define the eponential function used afterwards to get the fitted curve
def exponential(x, a, b, c):
    return a*np.exp(-b*x)+c

def average_revenue_plot(unique_access_users_file):
    df_users_access = pd.read_csv(unique_access_users_file, delimiter=' ')

    array_user_access = df_users_access.as_matrix(columns=[cs.WIKISTATS_UNIQUE_DEVICES_EN_WIKI_TOTAL]).flatten()
    array_donations = (df_users_access.as_matrix(columns=[cs.WIKISTATS_DAILY_DONATIONS])).flatten()
    array_timestamp = df_users_access.as_matrix(columns=[cs.WIKISTATS_UNIQUE_DEVICES_TIMESTAMP]).flatten()

    array_dates = []
    for i in array_timestamp:
        array_dates.append(datetime.fromtimestamp(int(i)))

    average_revenue_user = average_revenue_per_user(array_user_access, array_donations)

    years = YearLocator()   # every year
    months = MonthLocator()  # every month
    yearsFmt = DateFormatter('%Y')
    days = DayLocator()
    daysFmt = DateFormatter('%D')
    minutes = MinuteLocator()
    hours = HourLocator()

    # Creating Figure s
    fig1 = plt.figure(figsize=(8, 6))
    # Plotting
    ax1 = plt.subplot(111)
    ax1.bar(array_dates, average_revenue_user, width=1, alpha=0.5, color='black')

    # Axis
    ax1.xaxis.set_major_locator(DayLocator())
    ax1.xaxis.set_major_formatter(DateFormatter('%a %Y-%m-%d'))
    plt.xticks(rotation=80)
    ax1.set_ylabel('Average Revenue / User ($)', fontsize=15)
    ax1.set_yscale('log', basex=2)
    ax1.xaxis.label.set_size(15)


    plt.gcf().subplots_adjust(bottom=0.26)

    #Fitting to Exponential function
    x_data = np.linspace(1, len(array_dates), len(array_dates))

    popt, pcov = opt.curve_fit(exponential, x_data, average_revenue_user)


    fitting_exp = exponential(x_data, *popt)
    ax1.plot(ax1.get_xticks(), popt[0] * np.exp(-popt[1] * x_data) + popt[2], 'b--', linewidth=3.0, label='Fitted Curve' + '\n y=' + str(round(popt[0], 2)) + '*exp(-' + str(round(popt[1], 2)) + '*x)+' + str(round(popt[2], 2)))
    plt.legend()

    plt.show()


def user_donation_analysis(scaled_users_daily_access_file):
    df_users_access = pd.read_csv(scaled_users_daily_access_file, delimiter=' ')
    array_user_access = df_users_access.as_matrix(columns=[cs.WIKISTATS_UNIQUE_DEVICES_EN_WIKI_TOTAL])
    array_donations = df_users_access.as_matrix(columns=[cs.WIKISTATS_DAILY_DONATIONS])

    print array_user_access.sum()
    print array_donations.sum()

scaled_users_daily_access_file = cs.DATA_LOCAL_PATH + 'unique_users_monthly_scaled_factor100.csv'
correlate_users_requests()
#correlate_users_donations(scaled_users_daily_access_file)
#average_revenue_plot(scaled_users_daily_access_file)
#user_donation_analysis(scaled_users_daily_access_file)