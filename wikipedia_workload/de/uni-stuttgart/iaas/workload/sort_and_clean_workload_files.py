import workload.constants as cs
import pandas as pd
import csvHelper.csvHelper as csvHelper
import workload.WorkloadSummary as ws
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import plotHelper.colorGeneration as colorGeneration
import pylab


fileList = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                   cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)


# Create the Workload Summary for the set of files

w = ws.WorkloadSummary(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH, cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_HOURS[0],
                       cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH, cs.WIKISTATS_END_DAY,
                       cs.WIKISTATS_HOURS[len(cs.WIKISTATS_HOURS)-1], cs.WORKLOAD_SUMMARY_COL)

print fileList[0]
print csvHelper.get_timestamp_from_file_name(fileList[0])


for i in fileList:
    fileName = cs.DATA_LOCAL_PATH + i + cs.DATA_LOCAL_FILE_FILTERED + '.csv'
    print "### Processing File: %s" % i
    # Append each workload file to a data frame
    df = pd.read_csv(fileName, delimiter=' ')
    df.columns = [cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE, cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]
    df[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]] = df[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]].astype(float)

    # Cleaning Sample. Deleting Entries that Number of Requests < mean number of requests
    description = df.describe()
    mean_requests = description.iloc[1][cs.WIKISTATS_COL_REQUESTS]
    mean_bytes = description.iloc[1][cs.WIKISTATS_COL_SIZE]

    df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] < mean_requests].index)
    # Sorting Data Sample - Ordering Number of Requests Descending
    df = w.sortOccurrencePerNumberOfRequests(df)

#    w.addWorkloadHourStatSummary(df, csvHelper.get_timestamp_from_file_name(i).year,
#                        csvHelper.get_timestamp_from_file_name(i).month,
#                        csvHelper.get_timestamp_from_file_name(i).day,
#                        csvHelper.get_timestamp_from_file_name(i).hour)
#    w.addWorkloadSample(df, csvHelper.get_timestamp_from_file_name(i).year,
#                        csvHelper.get_timestamp_from_file_name(i).month,
#                        csvHelper.get_timestamp_from_file_name(i).day,
#                        csvHelper.get_timestamp_from_file_name(i).hour)

#    print w.workload_summary


    df_requests = pd.DataFrame(df.as_matrix(columns=[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]),
                                     index=df[cs.WIKISTATS_COL_PAGE],
                                     columns=[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE])

    ########### PLOTTING #############

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

    #plt.show()

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
    plt.show()
    ################################

    ####### CLUSTERING - KMEANS #######
    # Retrieve the column col_requests and assign as index the column col_page

    #kmeans_centroids,_ = kmeans(data, 100)
    #idx,_ = vq(data, kmeans_centroids)

    kmean = KMeans(n_clusters=100)
    kmean.fit(data_requests)

    # centers of the clusters
    print kmean.cluster_centers_
    # to which cluster each element belongs to
    print len(kmean.labels_)

    #print kmean

    #fig = pyplot.figure()
    #ax = fig.add_subplot(1,1,1)
    #ax.plot(data, 'b^')

    #ax.plot(kmeans_centroids,'rs',markersize=15)
    #ax.set_yscale('log')
    #pyplot.show()
    ##########################

