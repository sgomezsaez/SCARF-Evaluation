from datetime import date, timedelta, time
import datetime
import calendar

timeStampToDateTime = lambda x: datetime.fromtimestamp(
            int(x)
        ).strftime('%Y-%m-%d %H:%M:%S')

def retrieve_files_time_interval(beginYear, beginMonth, beginday, endYear, endMonth, endday, hours, count, suffix=''):
    a = date(beginYear, beginMonth, beginday)
    b = date(endYear, endMonth, endday)

    dd = [a + timedelta(days=x) for x in range((b-a).days + 1)]
    fileList = []
    if dd.__len__() == 0:
        for h in hours:
            fileName = build_file_name(str(beginYear).zfill(2), str(beginMonth).zfill(2), str(beginday).zfill(2), h, count)
            if suffix != '':
                fileName = fileName + suffix
            fileList.append(fileName)
    else:
        for d in dd:
            for h in hours:
                fileName = build_file_name(d.isoformat().split('-')[0], d.isoformat().split('-')[1], d.isoformat().split('-')[2], h, count)
                if suffix != '':
                    fileName = fileName + suffix
                fileList.append(fileName)

    return fileList

def build_file_name(year, month, day, time, count):
    return year + month + day + "-" + time + "0000"

def get_timestamp_from_file_name(fileName):
    splitted = fileName.split('-')
    dateStr = splitted[0]
    timeStr = splitted[1]
    year = dateStr[0:4]
    month = dateStr[4:6]
    day = dateStr[6:8]
    hour = timeStr[0:2]
    d = date(int(year), int(month), int(day))
    t = time(int(hour), 00)
    d = datetime.datetime.combine(d, t)
    return calendar.timegm(d.timetuple())



def get_time_from_file_name(fileName):
    splitted = fileName.split('-')
    dateStr = splitted[1]
    timeStr = splitted[2]
    year = dateStr[0:4]
    month = dateStr[4:6]
    day = dateStr[6:8]
    hour = timeStr[0:2]
    return [year, month, day, hour]
