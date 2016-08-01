import workload.constants as cs
import pandas as pd

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

print df


