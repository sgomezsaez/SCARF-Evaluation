import csv
import mimetypes
from pylab import *
import os
import ntpath
from datetime import date, timedelta, time
import calendar

#File Utils
import locale
locale.getdefaultlocale()
csv.field_size_limit(sys.maxsize)

def build_file_name(year, month, day, time, count):
    return count + "-" + year + month + day + "-" + time + "0000"

def get_timestamp_from_file_name(fileName):
    splitted = fileName.split('-')
    dateStr = splitted[1]
    timeStr = splitted[2]
    year = dateStr[0:4]
    month = dateStr[4:6]
    day = dateStr[6:8]
    hour = timeStr[0:2]
    d = date(int(year), int(month), int(day))
    t = time(int(hour), 00)
    d = datetime.datetime.combine(d, t)
    return d


def retrieve_files_time_interval(beginYear, beginMonth, beginday, endYear, endMonth, endday, hours, count):
    a = date(beginYear, beginMonth, beginday)
    b = date(endYear, endMonth, endday)

    dd = [a + timedelta(days=x) for x in range((b-a).days + 1)]
    fileList = []
    if dd.__len__() == 0:
        for h in hours:
            fileName = build_file_name(str(beginYear).zfill(2), str(beginMonth).zfill(2), str(beginday).zfill(2), h, count)
            fileList.append(fileName)
    else:
        for d in dd:
            for h in hours:
                fileName = build_file_name(d.isoformat().split('-')[0], d.isoformat().split('-')[1], d.isoformat().split('-')[2], h, count)
                fileList.append(fileName)

    return fileList

def read_csv_file_from_path(file_path, delimiter):
        return csv.reader(open(file_path, 'rb'),
                          delimiter=delimiter, quoting=csv.QUOTE_NONE)

def read_csv_file(file, delimiter):
    return csv.reader(file,
                          delimiter=delimiter, quoting=csv.QUOTE_NONE)

def write_to_csv_file(file_path, delimiter, list):
        resultFile = open(file_path, 'wb')
        writer = csv.writer(resultFile, delimiter=delimiter, dialect='excel')
        writer.writerows(list);

def count_file_lines(file_path):
        return sum(1 for line in open(file_path))

def dict_read_csv_file(file_path, delimiter):
        return csv.DictReader(open(file_path, 'rb'), delimiter=delimiter)

def read_text_file(self, file_path):
        f = open(file_path, 'w')
        return f

def verify_file_type(self, file_path):
        return mimetypes.guess_type(file_path)

def verify_file_extension(self, file_path):
        return os.path.splitext(file_path)[1][1:]

def get_file_name(self, file_path):
        head, tail = ntpath.split(file_path)
        return tail or ntpath.basename(head)

#CSV Utils

def getColumn(reader, column):
        return [result[column] for result in reader]

def getRow(reader, row):
    count = 1
    for i in reader:
        if count == row:
            return i
        else:
            count += 1

def getFromColumn(reader, fromColumn):
    result = []
    for i in reader:
        result.append(i[fromColumn:])
    return result

def getFromRow(reader, fromRow):
    count = 1
    result = []
    for i in reader:
        if count >= fromRow:
            result.append(i)
        else:
            count += 1
    return result;

def convertToMatrix(reader):
    result = []
    for i in reader:
        result.append(i)
    return result

def delete_row(reader, column):
    result = []
    count = 1
    for i in reader:
        if not (count == column):
            result.append(i)
        count += 1
    return result

def getColumnsWithLabel(reader, label):
    result = []
    columnLabel = reader[0]
    index = 0
    for i in columnLabel:
        if i == label:
            result.append(getColumn(reader, index))
        index += 1
    return result

def is_in_list(l, element):
    for i in l:
        if i == element:
            return True

# CSV Calculation Functions
def convertDictToList(dictionary):
    result = []
    if (isinstance(dictionary, dict)):
        for key, value in dictionary.iteritems():
            temp = [key,value]
            result.append(temp)
    return result

def convertToResponseTimeMs(reader):
    result = []
    for i in reader:
        row = []
        for j in i:
            row.append((float(1)/float(j)) * 1000.0)
        result.append(row)

    return result

def calculate_column_average(reader, column):
    l = []
    for i in reader:
        l.append(i[column-1])
    if len(l) > 1:
        return mean(l)
    else:
        return None

def calculate_mean_list(l):
    length = len(l)
    sum = 0.0
    for i in l:
        sum += float(i)
    return sum / length

def calculate_mean_columns(columns, col_label):
    result = {}
    l = []
    for i in columns:
        l.append(calculate_mean_list(i))
    result.update({col_label:l})

    return result

def calculate_median_list(l):
    return median(l)

def calculate_median_columns(columns, col_label):
    result = {}
    l = []
    for i in columns:
        l.append(calculate_median_list(i))
    result.update({col_label:l})
    return result

def convertQueriesAxisSuperindex(queries):
    res = []
    for i in queries:
        spl = i.split(' ')
        res.append('$' + spl[0] + '^{' + spl[1] + '}$')

    return res

def createQuerySuperindex(queriesNumber):
    res = []
    for i in queriesNumber:
        res.append('$Q^{' + i + '}$')

    return res

def convertListToFloat(l):
    res = []
    for i in l:
        res.append(float(i))
    return res

def filter_csv_file_rows(inFilePath, outFilePath, delimiter, filter_values):
    inFile = open(inFilePath, 'rb')
    inReader = csv.reader(inFile, delimiter=delimiter, quoting=csv.QUOTE_NONE)
    outWriter = csv.writer(open(outFilePath, 'wb'), delimiter=delimiter, quoting=csv.QUOTE_NONE, quotechar='')
    for row in inReader:
        for filter_value in filter_values:
            if row[0] == filter_value:
                outWriter.writerow(row)
    inFile.close()
    os.remove(inFilePath)


