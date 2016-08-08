import workload.constants as cs
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import workload.WorkloadSummary as ws
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import datasets, linear_model
import matplotlib

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
ax1.scatter(array_user_access, array_requests, s=20, alpha=0.5)
plt.title('Correlation Number of Users vs. Wikipedia Requests', fontsize=15)
plt.xlabel('Users', fontsize=15)
plt.ylabel('Requests', fontsize=15)
ax1.plot(array_user_access, regr.predict(array_user_access), color='red', linewidth=2, label='Linear Regression')

pearson_legend = 'pearson correlation= '+ str(format(pearson_correlation[0], '.3f'))

plt.text(50, 50, r'$\mu=100,\ \sigma=15$')
plt.annotate(pearson_legend, xy=(600000, 250000), xytext=(600000, 250000), fontsize = 15
            )
plt.show()