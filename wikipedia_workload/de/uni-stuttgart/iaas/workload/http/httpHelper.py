#Helper functions to retrieve the wikipedia workload data through http
#https://dumps.wikimedia.org/other/pagecounts-raw/
#Sample URL https://dumps.wikimedia.org/other/pagecounts-raw/2015/2015-11/pagecounts-20151101-000000.gz
#Sample URL https://dumps.wikimedia.org/other/pagecounts-raw/2015/2015-7/pagecounts-201577-000000.gz

import urllib2, gzip, StringIO
from datetime import date, timedelta

def build_url(url_base, year, month, day, time, count):
    return url_base + "/" + year + "/" + year + "-" + month + "/" + count + "-" + year + month + day + "-" + time + "0000.gz"

def retrieve_package(url):
    response = urllib2.urlopen(url)
    compressedFile = StringIO.StringIO()
    compressedFile.write(response.read())
    compressedFile.seek(0)
    return gzip.GzipFile(fileobj=compressedFile, mode='rb')

def retrieve_package_time_interval(url_base, beginYear, beginMonth, beginday, endYear, endMonth, endday, hours, count):
    a = date(beginYear, beginMonth, beginday)
    b = date(endYear, endMonth, endday)

    dd = [a + timedelta(days=x) for x in range((b-a).days + 1)]
    urlList = []
    if dd.__len__() == 0:
        for h in hours:
            url = build_url(url_base, str(beginYear).zfill(2), str(beginMonth).zfill(2), str(beginday).zfill(2), h, count)
            urlList.append(url)
    else:
        for d in dd:
            for h in hours:
                url = build_url(url_base, d.isoformat().split('-')[0], d.isoformat().split('-')[1], d.isoformat().split('-')[2], h, count)
                urlList.append(url)

    print urlList
    for url in urlList:
        retrieve_package(url)