import workload.constants as cs
import pandas as pd
import hourly_analysis, usersDailyAnalysis
import csvHelper.csvHelper as csvHelper
import numpy as np
import random as random
from workload import WorkloadSummary as ws
from datetime import datetime

# Generate the list of files to be read
pageCountFileList = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                   cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

# Adapting file list name with scaled suffix
pageCountFileListSuffix = [(cs.WIKISTATS_GENERATED_WORKLOAD_PREFIX + i + cs.WIKISTATS_FILE_SCALED_SUFFIX + '.csv') for i in pageCountFileList]



# Distributing the requests
count = 0
for pageCountFile in pageCountFileListSuffix:
    print "Processing File: " + pageCountFile
    pageCountDF = pd.read_csv(cs.DATA_LOCAL_PATH + pageCountFile, delimiter=' ')
    # Saving to File
    print "Saving: " + cs.DATA_LOCAL_PATH + cs.WIKISTATS_GENERATED_WORKLOAD_PREFIX + pageCountFileList[count] + cs.WIKISTATS_FILE_SCALED_SUFFIX + ".csv"
    pageCountDF.to_csv(cs.DATA_LOCAL_PATH + cs.WIKISTATS_GENERATED_WORKLOAD_PREFIX + pageCountFileList[count] + cs.WIKISTATS_FILE_SCALED_SUFFIX + ".csv", sep=',', index=False)
    count += 1