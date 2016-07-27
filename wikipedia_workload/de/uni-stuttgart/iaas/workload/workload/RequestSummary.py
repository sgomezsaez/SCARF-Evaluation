#Definition of the Workload: https://dumps.wikimedia.org/other/pagecounts-raw/
#
import locale
locale.getdefaultlocale()
from datetime import datetime, date, time
import pandas as pd
import calendar

class RequestSummary:

   def __init__(self, project, titlePage, numberRequests, sizeContentBytes, year, month, day, hour):
       self.project = project
       self.titlePage = titlePage
       self.totalNumberRequests = numberRequests
       self.totalSizeContentBytes = sizeContentBytes

       self.occurrences = pd.DataFrame({'date':[self.getDateTimeStamp(year, month, day, hour)], 'requests':[numberRequests]})

   def getProject(self):
       return self.project

   def getTitlePage(self):
       return self.titlePage

   def getNumberRequests(self):
       return self.totalNumberRequests

   def getSizeContentBytes(self):
       return self.totalSizeContentBytes

   def getOccurrences(self):
       return self.occurrences

   def getDateTimeStamp(self, year, month, day, hour):
       d = date(year, month, day)
       t = time(hour, 00)
       d = datetime.combine(d, t)
       return calendar.timegm(d.timetuple())

   def getStringTime(self, timestamp):
       return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

   def addOccurence(self, titlePage, numberRequests, sizeContentBytes, year, month, day, hour):
       workloadOccurrence = self.occurrences.loc[self.occurrences['date'] == self.getDateTimeStamp(year, month, day, hour)]

       if workloadOccurrence.empty:
           workloadOccurrence = pd.DataFrame([[self.getDateTimeStamp(year, month, day, hour), numberRequests]], columns=['date', 'requests'])
           self.occurrences = self.occurrences.append(workloadOccurrence, ignore_index=True)
       else:
           index = self.occurrences[self.occurrences['date'] ==
                                    self.getDateTimeStamp(year, month, day, hour)].index.tolist()[0]
           self.occurrences.set_value(index, 'requests', numberRequests + workloadOccurrence['requests'])

   def groupWorkloadPerDay(self, df):
       dfCopy = df.copy(deep=True);
       dfCopy['date'] = pd.to_datetime(dfCopy['date'],unit='s')
       groupedFrame = dfCopy.groupby(pd.DatetimeIndex(dfCopy['date']).normalize()).sum()
       groupedFrame.columns = ['date']
       return groupedFrame

   def groupWorkloadPerMonth(self, df):
       dfCopy = df.copy(deep=True);
       dfCopy['date'] = pd.to_datetime(dfCopy['date'],unit='s')
       groupedFrame = dfCopy.groupby(pd.DatetimeIndex(dfCopy['date']).normalize().month).sum()
       groupedFrame.columns = ['date']
       return groupedFrame

   def sortOccurrencesPerTimeStamp(self, wO):
       dfCopy = wO.copy(deep=True);
       return dfCopy.sort_index(by=['date'], ascending=True)

   def sortOccurrencePerNumberOfRequests(self, wO):
       dfCopy = wO.copy(deep=True);
       return dfCopy.sort_index(by=['requests'], ascending=True)

   def __str__(self):
       return self.project + ' ' + self.titlePage + ' ' + str(self.totalNumberRequests) + ' ' + str(self.totalSizeContentBytes)