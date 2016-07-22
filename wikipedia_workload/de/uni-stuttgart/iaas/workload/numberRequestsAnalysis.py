import workload.workloadOcurrence, workload.workloadSummary as wl
import http.httpHelper as httpHelper
import constants.constants as cs
import csvHelper.csvHelper

import datetime

w = wl.workloadSummary("a","b","b", 300, 22, 2016, 7, 21, 13)
w.addOccurence("b", 200, 22, 2016, 7, 22, 13)
w.addOccurence("b", 100, 22, 2016, 7, 23, 13)

print "unordered list of keys"
print w.getOcurrences().keys()
print "ordered list of keys"
print sorted(w.getOcurrences().keys())
#print w.getOcurrences()

print "group workload per day"
print w.groupWorkloadPerDay()
print "group workload per month"
print w.groupWorkloadPerMonth()

#d1 = datetime.datetime.fromtimestamp(w.getDateTimeStamp(2016, 07, 22, 05 - 1))
#d2 = datetime.datetime.fromtimestamp(w.getDateTimeStamp(2016, 07, 22, 04 - 1))
#print d1.day == d2.day

print "sortOcurrencePerTimeStamp"
print w.sortOcurrencePerTimeStamp(w.getOcurrences())

print "sortOcurrencePerNumberOfRequests"
print w.sortOcurrencePerNumberOfRequests(w.getOcurrences())

print httpHelper.retrieve_package_time_interval(cs.WIKISTATS_URL, cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_MONTH, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

