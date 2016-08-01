import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import workload.constants as cs

########### PLOTTING #############

#fileName = cs.DATA_LOCAL_PATH + str(cs.WIKISTATS_BEGIN_MONTH) + '-'+ str(cs.WIKISTATS_BEGIN_YEAR) + '_' + \
#           cs.WIKISTATS_END_MONTH + '-' + cs.WIKISTATS_END_YEAR + cs.DATA_LOCAL_FILE_MONTHLY

fileName = cs.DATA_LOCAL_PATH + "pagecounts-20160102-040000_filtered.csv"
df = pd.read_csv(fileName, delimiter=' ')

print df.describe()

df.columns = [cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE, cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]
df[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]] = df[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]].astype(float)

df_requests = pd.DataFrame(df.as_matrix(columns=[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]),
                                 index=df[cs.WIKISTATS_COL_PAGE],
                                 columns=[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE])

# Plotting individually the number of requests and the size of the requests
data_requests = df_requests.as_matrix(columns=[cs.WIKISTATS_COL_REQUESTS])
data_bytes = df_requests.as_matrix(columns=[cs.WIKISTATS_COL_SIZE])
labels = df_requests.index.values

print data_requests.shape

fig = plt.figure(1)
ax1 = plt.subplot(211)
ax1.plot(data_requests, 'r^')
ax1.set_xlabel('Requests')
ax1.set_ylabel('Number of Requests')
#ax1.set_xscale('log')
ax1.set_yscale('log', basex=2)
plt.grid(True)

ax2 = plt.subplot(212)
ax2.plot(data_bytes, 'g^')
ax2.set_xlabel('Requests')
ax2.set_ylabel('Bytes Per Request')
#ax2.set_xscale('log')
ax2.set_yscale('log', basex=2)
plt.grid(True)

plt.show()

# Plotting number of requests and bytes per requests together
data_bytes_requests = df_requests.as_matrix(columns=[cs.WIKISTATS_COL_SIZE, cs.WIKISTATS_COL_REQUESTS])
print data_bytes_requests.shape

fig = plt.figure(1)
ax1 = plt.subplot(111)
ax1.scatter(data_bytes, data_requests, s=10, alpha=0.5)
#ax1.plot(data_bytes_requests, 'g^')
ax1.set_xlabel('Request Size')
ax1.set_ylabel('Number of Requests')
#ax1.set_xscale('log', basex=2)
ax1.set_yscale('log', basex=2)
plt.grid(True)
#plt.show()
################################