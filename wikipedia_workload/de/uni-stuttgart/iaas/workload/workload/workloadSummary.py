#Definition of the Workload: https://dumps.wikimedia.org/other/pagecounts-raw/

from datetime import datetime, date, time
from collections import OrderedDict
import calendar
import workloadOcurrence

class workloadSummary:

   def __init__(self, project, language, titlePage, numberRequests, sizeContentBytes, year, month, day, hour):
       self.project = project
       self.language = language
       self.titlePage = titlePage
       self.totalNumberRequests = numberRequests
       self.totalSizeContentBytes = sizeContentBytes

       self.ocurrences = {self.getDateTimeStamp(year, month, day, hour - 1):
           workloadOcurrence.WorkloadOcurrence(
                   self.getDateTimeStamp(year, month, day, hour - 1), numberRequests, sizeContentBytes)}

   def getProject(self):
       return self.project

   def getLanguage(self):
       return self.language

   def getTitlePage(self):
       return self.titlePage

   def getNumberRequests(self):
       return self.totalNumberRequests

   def getSizeContentBytes(self):
       return self.totalSizeContentBytes

   def getOcurrences(self):
       return self.ocurrences

   def getDateTimeStamp(self, year, month, day, hour):
       d = date(year, month, day)
       t = time(hour, 00)
       d = datetime.combine(d, t)
       return calendar.timegm(d.timetuple())

   def getStringTime(self, timestamp):
       return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

   def addOccurence(self, titlePage, numberRequests, sizeContentBytes, year, month, day, hour):
       if self.ocurrences.__len__() > 0:
           self.totalNumberRequests += numberRequests
           self.ocurrences[self.getDateTimeStamp(year, month, day, hour - 1)] = \
               workloadOcurrence.WorkloadOcurrence(
                   self.getDateTimeStamp(year, month, day, hour - 1), numberRequests, sizeContentBytes)

       else:
           self.ocurrences = {self.getDateTimeStamp(year, month, day, hour - 1):
           workloadOcurrence.WorkloadOcurrence(
                   self.getDateTimeStamp(year, month, day, hour - 1), numberRequests, sizeContentBytes)}

   def groupWorkloadPerDay(self):
       sortedTimeStamps = sorted(self.ocurrences.keys())
       w = {}
       timestamp = 0
       workloadGroupedOcurrence = None
       for i in sortedTimeStamps:
           if sortedTimeStamps.index(i) == 0 or (datetime.fromtimestamp(i).day != datetime.fromtimestamp(timestamp).day\
                   or datetime.fromtimestamp(i).month != datetime.fromtimestamp(timestamp).month
                                                 or datetime.fromtimestamp(i).year != datetime.fromtimestamp(timestamp).year):
               timestamp = i
               workloadGroupedOcurrence = workloadOcurrence.WorkloadOcurrence(i, self.ocurrences[i].getNumberRequests(),
                                                                        self.ocurrences[i].getSizeContentBytes())
               w[timestamp] = workloadGroupedOcurrence
           else:
               workloadGroupedOcurrence = w.pop(timestamp)
               workloadOccurrence = self.ocurrences[i]
               workloadGroupedOcurrence.addNumberRequests(workloadOccurrence.getNumberRequests())
               w[timestamp] = workloadGroupedOcurrence
       return w

   def groupWorkloadPerMonth(self):
       sortedTimeStamps = sorted(self.ocurrences.keys())
       w = {}
       timestamp = 0
       workloadGroupedOcurrence = None
       for i in sortedTimeStamps:
           if sortedTimeStamps.index(i) == 0 or (datetime.fromtimestamp(i).month != datetime.fromtimestamp(timestamp).month\
                   or datetime.fromtimestamp(i).year != datetime.fromtimestamp(timestamp).year):
               timestamp = i
               workloadGroupedOcurrence = workloadOcurrence.WorkloadOcurrence(i, self.ocurrences[i].getNumberRequests(),
                                                                        self.ocurrences[i].getSizeContentBytes())
               w[timestamp] = workloadGroupedOcurrence
           else:
               workloadGroupedOcurrence = w.pop(timestamp)
               workloadOccurrence = self.ocurrences[i]
               workloadGroupedOcurrence.addNumberRequests(workloadOccurrence.getNumberRequests())
               w[timestamp] = workloadGroupedOcurrence
       return w

   def sortOcurrencePerTimeStamp(self, workloadOcurrence):
       return OrderedDict(sorted(workloadOcurrence.items(), key=lambda t: t[0]))

   def sortOcurrencePerNumberOfRequests(self, workloadOcurrence):
       return OrderedDict(sorted(workloadOcurrence.items(), key=lambda t: t[1].numberRequests))

   def __str__(self):
       return self.project + ' ' + self.titlePage + ' ' + str(self.totalNumberRequests) + ' ' + str(self.totalSizeContentBytes)







