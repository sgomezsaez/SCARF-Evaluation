import workload.constants as cs
import pandas as pd
from workload import WorkloadSummary as ws
import numpy as np
import matplotlib.pyplot as plt

fileName = cs.DATA_LOCAL_PATH + "1-2016_1-2016_hourly_summary.csv"
df = pd.read_csv(fileName, delimiter=' ')

df.columns = [cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP,
               cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ,
               cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES,
               cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
               cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES,
               cs.WORKLOAD_SUMMARY_STAT_STD_REQ,
               cs.WORKLOAD_SUMMARY_STAT_STD_BYTES,
               cs.WORKLOAD_SUMMARY_STAT_MAX_REQ,
               cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES]

df = ws.WorkloadSummary.sortOccurrencesPerTimeStamp(df=df, timestampColName=cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP)

arrayRequests = df.as_matrix(columns=[cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ, cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
                                          cs.WORKLOAD_SUMMARY_STAT_STD_REQ, cs.WORKLOAD_SUMMARY_STAT_MAX_REQ])

arrayBytes = df.as_matrix(columns=[cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES, cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES,
                                          cs.WORKLOAD_SUMMARY_STAT_STD_BYTES, cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES])

coloursArray = ['r', 'g', 'c', 'purple']
labelsArrayRequests = ['Count', 'Mean', 'Std', 'Max.']

# Building X Axis - Timestamps to Date
indentation = df[cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP].tolist()
indentation_date = []
for i in indentation:
    indentation_date.append(ws.WorkloadSummary.getStringTime(i))
bar_width = 0.5

# Adding subplots
f, ax = plt.subplots(2, 1, sharey=True, sharex=True)
f.subplots_adjust(bottom=0.2) #make room for the legend
#plt.yticks(np.arange(0,18,2))
plt.xticks(indentation)
plt.suptitle('Plot of Addresses')

p = [] # list of bar properties


def create_subplot(matrix, colors, axis, title):
    bar_renderers = []
    ind = np.arange(matrix.shape[1])
    bottoms = np.cumsum(np.vstack((np.zeros(matrix.shape[1]), matrix)), axis=0)[:-1]
    for i, row in enumerate(matrix):
        print i
        print row
        r = axis.bar(ind, row, width=0.5, color=colors[i], bottom=bottoms[i])
        bar_renderers.append(r)
    axis.set_title(title)
    return bar_renderers

p.extend(create_subplot(np.transpose(arrayRequests),coloursArray, ax[0], '1'))
p.extend(create_subplot(np.transpose(arrayBytes),coloursArray, ax[1], '2'))
ax[0].set_ylabel('Number of Requests') # add left y label
#ax[0].set_ybound(0, 16) # add buffer at the top of the bars

f.legend(((x[0] for x in p)), # bar properties
         (labelsArrayRequests + labelsArrayRequests),
         bbox_to_anchor=(0.5, 0),
         loc='lower center',
         ncol=4)
plt.show()