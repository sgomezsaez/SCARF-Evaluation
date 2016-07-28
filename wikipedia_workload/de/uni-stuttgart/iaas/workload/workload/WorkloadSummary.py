import RequestSummary as rs
import locale
locale.getdefaultlocale()
from datetime import datetime, date, time
import pandas as pd
import calendar
import constants as cs

class WorkloadSummary:

    def __init__(self, beginYear, beginMonth, beginDay, beginHour,
                 endYear, endMonth, endDay, endHour, summary_col_names=[],
                 workload_summary= None, numberRequests= 0, sizeContentBytes= 0, requests={}):
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
            self.workload_summary = pd.DataFrame(self.summary_col_names)

        if requests.__len__() > 0:
            self.requests = requests
        else:
            self.requests = {}



    def addWorkloadSample(self, df, year, month, day, hour):

        for row in df.itertuples():
            #each row is a tuple of (index,project, page, num_requests, bytes)
            print "Processing Row %s" % row[0]
            page = row[2]
            #Request already exists
            if self.requests.has_key(page):
                #request = self.requests.get(page)
                #request.addOccurence(row[2], row[3], row[4], year, month, day, hour)

                # Update Entry in Workload Summary
                index = self.workload_summary[self.workload_summary[cs.WORKLOAD_SUMMARY_COL_PAGE] ==
                                    page].index.tolist()[0]
                self.workload_summary.set_value(index, cs.WORKLOAD_SUMMARY_COL_TOTAL_REQUESTS,
                                                self.workload_summary.loc[[index]][cs.WORKLOAD_SUMMARY_COL_TOTAL_REQUESTS] + row[3])
                self.workload_summary.set_value(index, cs.WORKLOAD_SUMMARY_COL_TOTAL_BYTES,
                                                self.workload_summary.loc[[index]][cs.WORKLOAD_SUMMARY_COL_TOTAL_REQUESTS] *
                                                self.workload_summary.loc[[index]][cs.WORKLOAD_SUMMARY_COL_BYTES_PER_REQUEST])

            else:
                #request = rs.RequestSummary(row[1], row[2], row[3], row[4], year, month, day, hour)

                 # Create Entry in Workload Summary
                requestOccurrence = pd.DataFrame([[row[1], page, row[3], row[4], row[4],
                                                   self.getDateTimeStamp(self.beginYear, self.beginMonth, self.beginDay,self.beginHour),
                                                   self.getDateTimeStamp(self.endYear, self.endMonth, self.endDay, self.endHour)]],
                                                 columns=cs.WORKLOAD_SUMMARY_COL)
                self.workload_summary = self.workload_summary.append(requestOccurrence, ignore_index=True)

            #self.requests[page] = request

    def getDateTimeStamp(self, year, month, day, hour):
       d = date(year, month, day)
       t = time(hour, 00)
       d = datetime.combine(d, t)
       return calendar.timegm(d.timetuple())

    def sortOccurrencesPerTimeStamp(self, wO):
        dfCopy = wO.copy(deep=True);
        return dfCopy.sort_index(by=['date'], ascending=True)

    def sortOccurrencePerNumberOfRequests(self, wO):
        dfCopy = wO.copy(deep=True);
        return dfCopy.sort_index(by=[cs.WIKISTATS_COL_REQUESTS], ascending=False)

