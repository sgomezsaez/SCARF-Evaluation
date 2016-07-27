import RequestSummary as rs
import pandas as pd
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
        #TODO: verify if the page already exists in the summary. Then, just update its value and find the one in the list

        for row in df.itertuples():
            #each row is a tuple of (index,project, page, num_requests, bytes)
            page = row[2]
            #Request already exists
            if self.requests.has_key(page):
                request = self.requests.get(page)
                request.addOccurence(row[2], row[3], row[4], year, month, day, hour)

                # Update Entry in Workload Summary
                index = self.workload_summary[self.workload_summary[cs.WORKLOAD_SUMMARY_COL_PAGE] ==
                                    page].index.tolist()[0]
                self.workload_summary.set_value(index, cs.WORKLOAD_SUMMARY_COL_TOTAL_REQUESTS,
                                                request.getNumberRequests() + row[3])
                self.workload_summary.set_value(index, cs.WORKLOAD_SUMMARY_COL_TOTAL_BYTES,
                                                request.getNumberRequests() * request.getSizeContentBytes())

            else:
                request = rs.RequestSummary(row[1], row[2], row[3], row[4], year, month, day, hour)

                 # Create Entry in Workload Summary
                requestOccurrence = pd.DataFrame([[row[1], page, row[3], row[4], row[4],
                                                   request.getDateTimeStamp(self.beginYear, self.beginMonth, self.beginDay,self.beginHour),
                                                   request.getDateTimeStamp(self.endYear, self.endMonth, self.endDay, self.endHour)]],
                                                 columns=cs.WORKLOAD_SUMMARY_COL)
                self.workload_summary = self.workload_summary.append(requestOccurrence, ignore_index=True)

            self.requests[page] = request




