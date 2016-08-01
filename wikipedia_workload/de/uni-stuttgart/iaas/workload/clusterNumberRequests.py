from sklearn.cluster import KMeans
import plotHelper.colorGeneration as colorGeneration
import pylab
import pandas as pd
import workload.constants as cs

fileName = cs.DATA_LOCAL_PATH + str(cs.WIKISTATS_BEGIN_MONTH) + '-'+ str(cs.WIKISTATS_BEGIN_YEAR) + '_' + \
           cs.WIKISTATS_END_MONTH + '-' + cs.WIKISTATS_END_YEAR + cs.DATA_LOCAL_FILE_MONTHLY

df = pd.read_csv(fileName, delimiter=' ')

df_requests = pd.DataFrame(df.as_matrix(columns=[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]),
                                 index=df[cs.WIKISTATS_COL_PAGE],
                                 columns=[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE])

# Plotting individually the number of requests and the size of the requests
data_requests = df_requests.as_matrix(columns=[cs.WIKISTATS_COL_REQUESTS])
data_bytes = df_requests.as_matrix(columns=[cs.WIKISTATS_COL_SIZE])
labels = df_requests.index.values

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
