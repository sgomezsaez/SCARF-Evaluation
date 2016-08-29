import os

import workload.constants as cs
import workload.WorkloadSummary as ws
import csvHelper.csvHelper as csvHelper
import http.httpHelper as httpHelper
import csv






def download_and_filter_workload_files(urllist=[], filelist=[]):
    for url in urllist:
        print "Retrieving File " + url
        httpHelper.retrieve_and_save_package(url, cs.DATA_LOCAL_PATH)
        print "Filtering File " +  os.path.join(cs.DATA_LOCAL_PATH, filelist[urllist.index(url)]) + ".csv"
        csvHelper.filter_csv_file_rows(os.path.join(cs.DATA_LOCAL_PATH, filelist[urllist.index(url)] + ".csv"),
                                       os.path.join(cs.DATA_LOCAL_PATH, filelist[urllist.index(url)] + cs.DATA_LOCAL_FILE_FILTERED + ".csv"),
                                     cs.WIKISTATS_DELIMITER, cs.WIKISTATS_FILTER_VALUES)

def download_and_filter_users(urllist=[]):
    summary = []
    for url in urllist:
        print "Retrieving File " + url

        decompressedFile = httpHelper.retrieve_package(url)
        print "Reading file " + decompressedFile.name
        s = decompressedFile.read()
        csvreader = csv.reader(s.splitlines(), delimiter='\t', quotechar='|')

        filtered_csv = csvHelper.filter_csv_file_rows(csvreader, ['en.wikipedia.org', 'en.m.wikipedia.org'])
        row_output = [httpHelper.get_file_timestamp_from_url(url), filtered_csv[0][1], filtered_csv[1][1], int(filtered_csv[0][1]) + int(filtered_csv[1][1])]

        summary.append(row_output)

    outFile = open(cs.DATA_LOCAL_PATH + "unique_users_monthly.csv", 'wb')
    wr = csv.writer(outFile, quoting=csv.QUOTE_ALL, delimiter=' ')
    for i in summary:
        wr.writerow(i)



pageCountUrlList = httpHelper.retrieve_urls_time_interval(cs.WIKISTATS_URL, cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

pageCountFileList = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                   cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

uniqueDevicesUrlList = httpHelper.retrieve_urls_unique_devices(cs.WIKISTATS_UNIQUE_DEVICES_URL, cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                cs.WIKISTATS_END_DAY)

print uniqueDevicesUrlList
#download_and_filter_workload_files(pageCountUrlList, pageCountFileList)
download_and_filter_users(uniqueDevicesUrlList)

