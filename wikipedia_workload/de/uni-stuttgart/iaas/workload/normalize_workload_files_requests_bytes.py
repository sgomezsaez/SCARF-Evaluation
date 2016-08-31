import workload.constants as cs
import pandas as pd
import csvHelper.csvHelper as csvHelper
from sklearn import preprocessing
import hourly_analysis as hs
from sklearn.preprocessing import RobustScaler
import numpy as np


def min_max_scale_workload_files_requests(inputFileList=[], scaled_file_list=[], scaleMin=0, scaleMax=1000):

    df_processed = pd.DataFrame(columns=[cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE,
                                         cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE])
    fileList = inputFileList


    for n, i in enumerate(fileList):
        fileName = cs.DATA_LOCAL_PATH + i + cs.DATA_LOCAL_FILE_FILTERED + '.csv'
        print "### Processing File: %s" % fileName
        print csvHelper.get_time_from_file_name(i)
        timeInterval = csvHelper.get_time_from_file_name(i)
        # Append each workload file to a data frame
        df = pd.read_csv(fileName, delimiter=' ')
        df.columns = [cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE, cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]

        # Cleaning Sample. Deleting Entries that Number of Requests < mean number of requests and bytes < mean bytes
        description = df.describe()
        mean_requests = description.iloc[1][cs.WIKISTATS_COL_REQUESTS]
        mean_bytes = description.iloc[1][cs.WIKISTATS_COL_SIZE]
        #df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] < mean_requests].index)
        #df = df.drop(df[df[cs.WIKISTATS_COL_SIZE] < mean_bytes].index)

        # Cleaning Sample. Deleting Entries that Number of Requests = 0
        df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] == 0].index)

        # Scaling workload distribution (Num of Requests) between 1 and 1000
        x = df.as_matrix(columns=[cs.WIKISTATS_COL_REQUESTS]) #returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(scaleMin, scaleMax))
        x_scaled = min_max_scaler.fit_transform(x)
        df_scaled = pd.DataFrame(x_scaled, columns=[cs.WIKISTATS_COL_REQUESTS], index=df.index.values)
        df[[cs.WIKISTATS_COL_REQUESTS]] = df_scaled[[cs.WIKISTATS_COL_REQUESTS]]
        #df[[cs.WIKISTATS_COL_REQUESTS]] = df[[cs.WIKISTATS_COL_REQUESTS]].round(decimals=0)
        #df[[cs.WIKISTATS_COL_REQUESTS]] = df[cs.WIKISTATS_COL_REQUESTS].astype(int)

        # Deleting Entries that Number of Requests = 0
        #print df.describe()
        df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] < 1].index)
        #print df.describe()
        #print df

        # Saving Workload
        print "Saving Workload to " + scaled_file_list[n]
        path = cs.DATA_LOCAL_PATH + scaled_file_list[n]
        df.to_csv(path_or_buf=path, sep=' ', index=False, header=False)


def robust_scale_workload_files_requests(inputFileList=[], scaled_file_list=[]):

    df_processed = pd.DataFrame(columns=[cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE,
                                         cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE])
    fileList = inputFileList


    for n, i in enumerate(fileList):
        fileName = cs.DATA_LOCAL_PATH + i + cs.DATA_LOCAL_FILE_FILTERED + '.csv'
        print "### Processing File: %s" % fileName
        print csvHelper.get_time_from_file_name(i)
        timeInterval = csvHelper.get_time_from_file_name(i)
        # Append each workload file to a data frame
        df = pd.read_csv(fileName, delimiter=' ')
        df.columns = [cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE, cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]

        # Cleaning Sample. Deleting Entries that Number of Requests < mean number of requests and bytes < mean bytes
        description = df.describe()
        mean_requests = description.iloc[1][cs.WIKISTATS_COL_REQUESTS]
        mean_bytes = description.iloc[1][cs.WIKISTATS_COL_SIZE]
        #df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] < mean_requests].index)
        #df = df.drop(df[df[cs.WIKISTATS_COL_SIZE] < mean_bytes].index)

        # Cleaning Sample. Deleting Entries that Number of Requests = 0
        df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] == 0].index)

        # Scaling workload distribution (Num of Requests) between 1 and 1000
        x = df.as_matrix(columns=[cs.WIKISTATS_COL_REQUESTS]) #returns a numpy array

        robust_scaler = RobustScaler()
        x_scaled = robust_scaler.fit_transform(x)
        df_scaled = pd.DataFrame(x_scaled, columns=[cs.WIKISTATS_COL_REQUESTS], index=df.index.values)
        df[[cs.WIKISTATS_COL_REQUESTS]] = df_scaled[[cs.WIKISTATS_COL_REQUESTS]]
        # Deleting Entries that Number of Requests = 0
        #print df.describe()
        df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] < 1].index)
        #print df.describe()
        #print df
        # Saving Workload
        print "Saving Workload to " + scaled_file_list[n]
        path = cs.DATA_LOCAL_PATH + scaled_file_list[n]
        df.to_csv(path_or_buf=path, sep=' ', index=False, header=False)

def factor_scale_workload_files_requests(inputFileList=[], scaled_file_list=[], factor=100000):

    df_processed = pd.DataFrame(columns=[cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE,
                                         cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE])
    fileList = inputFileList


    for n, i in enumerate(fileList):
        fileName = cs.DATA_LOCAL_PATH + i + cs.DATA_LOCAL_FILE_FILTERED + '.csv'
        print "### Processing File: %s" % fileName
        print csvHelper.get_time_from_file_name(i)
        timeInterval = csvHelper.get_time_from_file_name(i)
        # Append each workload file to a data frame
        df = pd.read_csv(fileName, delimiter=' ')
        df.columns = [cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE, cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]

        # Cleaning Sample. Deleting Entries that Number of Requests < mean number of requests and bytes < mean bytes
        description = df.describe()
        mean_requests = description.iloc[1][cs.WIKISTATS_COL_REQUESTS]
        mean_bytes = description.iloc[1][cs.WIKISTATS_COL_SIZE]
        #df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] < mean_requests].index)
        #df = df.drop(df[df[cs.WIKISTATS_COL_SIZE] < mean_bytes].index)

        # Cleaning Sample. Deleting Entries that Number of Requests = 0
        df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] == 0].index)

        # Scaling workload distribution (Num of Requests) between 1 and 1000
        x = df.as_matrix(columns=[cs.WIKISTATS_COL_REQUESTS]) #returns a numpy array
        x_scaled = x / factor
        df_scaled = pd.DataFrame(x_scaled, columns=[cs.WIKISTATS_COL_REQUESTS], index=df.index.values)
        df[[cs.WIKISTATS_COL_REQUESTS]] = df_scaled[[cs.WIKISTATS_COL_REQUESTS]]
        # Deleting Entries that Number of Requests = 0
        #print df.describe()
        df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] < 1].index)
        #print df.describe()
        #print df
        # Saving Workload
        print "Saving Workload to " + scaled_file_list[n]
        path = cs.DATA_LOCAL_PATH + scaled_file_list[n]
        df.to_csv(path_or_buf=path, sep=' ', index=False, header=False)



non_scaled_file_list = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                    cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                       cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

scaled_file_list = []
for i in non_scaled_file_list:
    #scaled_file_list.append(i + cs.DATA_LOCAL_FILE_SCALED + '_RobustScaler' + '.csv')
    scaled_file_list.append(i + cs.DATA_LOCAL_FILE_SCALED + '_factor1000Scaling' + '.csv')

#scaled_file_summary_path = cs.DATA_LOCAL_PATH + str(cs.WIKISTATS_BEGIN_MONTH) + '-'+ str(cs.WIKISTATS_BEGIN_YEAR) + '_' + \
#               str(cs.WIKISTATS_END_MONTH) + '-' + str(cs.WIKISTATS_END_YEAR) + cs.DATA_LOCAL_FILE_HOURLY_SUMMARY + \
#                           cs.DATA_LOCAL_FILE_SCALED + '_RobustScaler' + '.csv'

scaled_file_summary_path = cs.DATA_LOCAL_PATH + str(cs.WIKISTATS_BEGIN_MONTH) + '-'+ str(cs.WIKISTATS_BEGIN_YEAR) + '_' + \
               str(cs.WIKISTATS_END_MONTH) + '-' + str(cs.WIKISTATS_END_YEAR) + cs.DATA_LOCAL_FILE_HOURLY_SUMMARY + \
                           cs.DATA_LOCAL_FILE_SCALED + '_factor1000Scaling' + '.csv'


#min_max_scale_workload_files_requests(non_scaled_file_list, scaled_file_list, 0, 10000)
#robust_scale_workload_files_requests(non_scaled_file_list, scaled_file_list)
#factor_scale_workload_files_requests(non_scaled_file_list, scaled_file_list, 1000)

hs.create_hourly_analysis(scaled_file_list, scaled_file_summary_path)

