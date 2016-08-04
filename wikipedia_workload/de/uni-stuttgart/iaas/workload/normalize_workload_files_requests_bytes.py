import workload.constants as cs
import pandas as pd
import csvHelper.csvHelper as csvHelper
from sklearn import preprocessing
import hourly_analysis as hs


def scale_workload_files_requests(inputFileList=[], scaleMin=0, scaleMax=1000):

    df_processed = pd.DataFrame(columns=[cs.WIKISTATS_COL_PROJECT, cs.WIKISTATS_COL_PAGE,
                                         cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE])
    fileList = inputFileList


    for i in fileList:
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
        df = df.drop(df[df[cs.WIKISTATS_COL_REQUESTS] < mean_requests].index)
        df = df.drop(df[df[cs.WIKISTATS_COL_SIZE] < mean_bytes].index)

        # Scaling workload distribution (Num of Requests) between 1 and 1000
        x = df.as_matrix(columns=[cs.WIKISTATS_COL_REQUESTS]) #returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(scaleMin, scaleMax))
        x_scaled = min_max_scaler.fit_transform(x)
        df_scaled = pd.DataFrame(x_scaled, columns=[cs.WIKISTATS_COL_REQUESTS], index=df.index.values)
        df[[cs.WIKISTATS_COL_REQUESTS]] = df_scaled[[cs.WIKISTATS_COL_REQUESTS]]
        df[[cs.WIKISTATS_COL_REQUESTS]] = df[[cs.WIKISTATS_COL_REQUESTS]].round(decimals=0)
        df[[cs.WIKISTATS_COL_REQUESTS]] = df[cs.WIKISTATS_COL_REQUESTS].astype(int)

        # Saving Workload
        path = cs.DATA_LOCAL_PATH + i + cs.DATA_LOCAL_FILE_SCALED + '.csv'
        df.to_csv(path_or_buf=path, sep=' ', index=False, header=False)


print "starting"
non_scaled_file_list = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                    cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                       cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

scaled_file_list = []
for i in non_scaled_file_list:
    scaled_file_list.append(i + cs.DATA_LOCAL_FILE_SCALED + '.csv')

scaled_file_summary_path = cs.DATA_LOCAL_PATH + str(cs.WIKISTATS_BEGIN_MONTH) + '-'+ str(cs.WIKISTATS_BEGIN_YEAR) + '_' + \
               str(cs.WIKISTATS_END_MONTH) + '-' + str(cs.WIKISTATS_END_YEAR) + cs.DATA_LOCAL_FILE_HOURLY_SUMMARY + \
                           cs.DATA_LOCAL_FILE_SCALED + '.csv'

print scaled_file_list

scale_workload_files_requests(non_scaled_file_list, 0, 1000)
hs.create_hourly_analysis(scaled_file_list, scaled_file_summary_path)

