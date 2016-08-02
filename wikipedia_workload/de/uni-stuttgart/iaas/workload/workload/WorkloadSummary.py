import RequestSummary as rs
import locale
locale.getdefaultlocale()
from datetime import datetime, date, time
import pandas as pd
import calendar
import constants as cs
from multiprocessing import Lock

lock = Lock()

class WorkloadSummary:

    def __init__(self, beginYear, beginMonth, beginDay, beginHour,
                 endYear, endMonth, endDay, endHour, summary_col_names=[],
                 workload_summary= None, numberRequests= 0, sizeContentBytes= 0, workloadHourSummary={}):
        self.beginYear = int(beginYear)
        self.beginMonth = int(beginMonth)
        self.beginDay = int(beginDay)
        self.beginHour = int(beginHour)
        self.endYear = int(endYear)
        self.endMonth = int(endMonth)
        self.endDay = int(endDay)
        self.endHour = int(endHour)
        self.numberRequest = numberRequests
        self.sizeContentBytes = sizeContentBytes


        if summary_col_names.__len__() > 0:
            self.summary_col_names = summary_col_names
        else:
            self.summary_col_names = cs.WORKLOAD_SUMMARY_COL

        if workload_summary:
            self.workload_summary = workload_summary
        else:
            self.workload_summary = None

        # Dict of dataFrames describing each hourly workload file
        if workloadHourSummary.__len__() > 0:
            self.hour_summary = workloadHourSummary
        else:
            self.workloadHourSummary = {}

    def addWorkloadHourStatSummary(self, df, year, month, day, hour):
        # Adding Hourly Summary
        print "Adding Workload Hour Stats Summary"
        timeStamp = self.getDateTimeStamp(year, month, day, hour)
        statDescriptionDF = df.describe()
        statDescriptionDF[cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP] = timeStamp
        statDescriptionDF.columns= [cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE, cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP]
        sum_requests = df[cs.WIKISTATS_COL_REQUESTS].sum()
        sum_bytes = df[cs.WIKISTATS_COL_SIZE].sum()
        sumDF = pd.DataFrame([[sum_requests, sum_bytes, timeStamp]], index=['sum'], columns=[cs.WIKISTATS_COL_REQUESTS,
                                                                              cs.WIKISTATS_COL_SIZE,
                                                                              cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP])
        sumDF[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]] = sumDF[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]].astype(float)
        statDescriptionDF = statDescriptionDF.append(sumDF)
        self.workloadHourSummary[timeStamp] = statDescriptionDF

    def addWorkloadSample(self, df, year, month, day, hour):
        message = "Adding Workload Sample for " + str(year) + str(month) + str(day) + str(hour)
        print "Adding Workload Sample for " + message
        df[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]] = df[[cs.WIKISTATS_COL_REQUESTS, cs.WIKISTATS_COL_SIZE]].astype(float)
        for row in df.itertuples():
            # each row is a tuple of (index,project, page, num_requests, bytes)
            #print "Processing Row " + str(row[0])
            page = row[2]
            # Workload summary does not exist for this timestamp
            if self.workload_summary is not None:
                # Update Entry in Workload Summary if page (request) already exists
                if not self.workload_summary.loc[self.workload_summary[cs.WORKLOAD_SUMMARY_COL_PAGE] == page].empty:
                    index = self.workload_summary[self.workload_summary[cs.WORKLOAD_SUMMARY_COL_PAGE] ==
                                    page].index.tolist()[0]


                    #print "Acquiring lock"
                    lock.acquire()
                    self.workload_summary.set_value(index, cs.WORKLOAD_SUMMARY_COL_TOTAL_REQUESTS,
                                            self.workload_summary.loc[[index]][cs.WORKLOAD_SUMMARY_COL_TOTAL_REQUESTS]
                                                + row[3])
                    self.workload_summary.set_value(index, cs.WORKLOAD_SUMMARY_COL_TOTAL_BYTES,
                                                self.workload_summary.loc[[index]][cs.WORKLOAD_SUMMARY_COL_TOTAL_REQUESTS] *
                                                self.workload_summary.loc[[index]][cs.WORKLOAD_SUMMARY_COL_BYTES_PER_REQUEST])
                    self.workload_summary.set_value(index, cs.WORKLOAD_SUMMARY_COL_FREQUENCY,
                                                self.workload_summary.loc[[index]][cs.WORKLOAD_SUMMARY_COL_FREQUENCY] + 1)
                    lock.release()
                    #print "Releasing lock"
                else:
                    # Create Entry in Workload Summary
                    requestOccurrence = pd.DataFrame([[row[1], page, row[3], row[4], row[4],
                                                 self.getDateTimeStamp(self.beginYear, self.beginMonth, self.beginDay,self.beginHour),
                                                 self.getDateTimeStamp(self.endYear, self.endMonth, self.endDay, self.endHour), 1]],
                                               columns=cs.WORKLOAD_SUMMARY_COL)
                    #print "Acquiring lock"
                    lock.acquire()
                    self.workload_summary = self.workload_summary.append(requestOccurrence, ignore_index=True)
                    lock.release()
                    #print "Releasing lock"
            else:
                # Create DataFrame if Null
                #print "Acquiring lock"
                lock.acquire()
                self.workload_summary = pd.DataFrame([[row[1], page, row[3], row[4], row[4],
                                               self.getDateTimeStamp(self.beginYear, self.beginMonth, self.beginDay,self.beginHour),
                                               self.getDateTimeStamp(self.endYear, self.endMonth, self.endDay, self.endHour), 1]], columns=cs.WORKLOAD_SUMMARY_COL)
                lock.release()
                #print "Releasing lock"

    @staticmethod
    def getDateTimeStamp(year, month, day, hour):
       d = date(year, month, day)
       t = time(hour, 00)
       d = datetime.combine(d, t)
       return calendar.timegm(d.timetuple())

    @staticmethod
    def sortOccurrencesPerTimeStamp(df, timestampColName):
        dfCopy = df.copy(deep=True);
        return dfCopy.sort_index(by=[timestampColName], ascending=True)

    @staticmethod
    def sortOccurrencePerNumberOfRequests(df):
        dfCopy = df.copy(deep=True);
        return dfCopy.sort_index(by=[cs.WIKISTATS_COL_REQUESTS], ascending=False)

    @staticmethod
    def sortOccurrencePerHourlyFrequency(df):
        dfCopy = df.copy(deep=True);
        return dfCopy.sort_index(by=[cs.WORKLOAD_SUMMARY_COL_FREQUENCY], ascending=False)

    @staticmethod
    def getStringTime(timestamp):
       return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def getDataFrameHourlyReport(self, timestamp):
        count_requests = self.workloadHourSummary.get(timestamp).iloc[0][cs.WIKISTATS_COL_REQUESTS]
        count_bytes = self.workloadHourSummary.get(timestamp).iloc[0][cs.WIKISTATS_COL_SIZE]
        mean_requests = self.workloadHourSummary.get(timestamp).iloc[1][cs.WIKISTATS_COL_REQUESTS]
        mean_bytes = self.workloadHourSummary.get(timestamp).iloc[1][cs.WIKISTATS_COL_SIZE]
        std_requests = self.workloadHourSummary.get(timestamp).iloc[2][cs.WIKISTATS_COL_REQUESTS]
        std_bytes = self.workloadHourSummary.get(timestamp).iloc[2][cs.WIKISTATS_COL_SIZE]
        max_requests = self.workloadHourSummary.get(timestamp).iloc[7][cs.WIKISTATS_COL_REQUESTS]
        max_bytes = self.workloadHourSummary.get(timestamp).iloc[7][cs.WIKISTATS_COL_SIZE]
        timeStamp = self.workloadHourSummary.get(timestamp).iloc[1][cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP]
        sum_requests = self.workloadHourSummary.get(timestamp).iloc[8][cs.WIKISTATS_COL_REQUESTS]
        sum_bytes = self.workloadHourSummary.get(timestamp).iloc[8][cs.WIKISTATS_COL_SIZE]

        df = pd.DataFrame([[timeStamp, count_requests, count_bytes, mean_requests, mean_bytes, std_requests,
                                   std_bytes, max_requests, max_bytes, sum_requests, sum_bytes]],
                                 columns=[cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP, cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ,
                                            cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES, cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
                                            cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES, cs.WORKLOAD_SUMMARY_STAT_STD_REQ,
                                            cs.WORKLOAD_SUMMARY_STAT_STD_BYTES, cs.WORKLOAD_SUMMARY_STAT_MAX_REQ,
                                            cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES, cs.WORKLOAD_SUMMARY_STAT_SUM_REQ,
                                            cs.WORKLOAD_SUMMARY_STAT_SUM_BYTES])
        return df