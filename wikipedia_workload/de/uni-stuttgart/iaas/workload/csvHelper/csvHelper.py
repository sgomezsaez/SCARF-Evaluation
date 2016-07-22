import csv
import mimetypes
from pylab import *
import os.path
import ntpath

#File Utils

def read_csv_file(file_path, delimiter):
        return csv.reader(open(file_path, 'rb'),
                          delimiter=delimiter)

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

def getColumn(self, reader, column):
        return [result[column] for result in reader]

def getRow(self, reader, row):
    count = 1
    for i in reader:
        if count == row:
            return i
        else:
            count += 1

def getFromColumn(self, reader, fromColumn):
    result = []
    for i in reader:
        result.append(i[fromColumn:])
    return result

def getFromRow(self, reader, fromRow):
    count = 1
    result = []
    for i in reader:
        if count >= fromRow:
            result.append(i)
        else:
            count += 1
    return result;

def convertToMatrix(self, reader):
    result = []
    for i in reader:
        result.append(i)
    return result

def delete_row(self, reader, column):
    result = []
    count = 1
    for i in reader:
        if not (count == column):
            result.append(i)
        count += 1
    return result

def getColumnsWithLabel(self, reader, label):
    result = []
    columnLabel = reader[0]
    index = 0
    for i in columnLabel:
        if i == label:
            result.append(self.getColumn(reader, index))
        index += 1
    return result

def is_in_list(self, l, element):
    for i in l:
        if i == element:
            return True

# CSV Calculation Functions
def convertDictToList(self, dictionary):
    result = []
    if (isinstance(dictionary, dict)):
        for key, value in dictionary.iteritems():
            temp = [key,value]
            result.append(temp)
    return result

def convertToResponseTimeMs(self, reader):
    result = []
    for i in reader:
        row = []
        for j in i:
            row.append((float(1)/float(j)) * 1000.0)
        result.append(row)

    return result

def calculate_column_average(self, reader, column):
    l = []
    for i in reader:
        l.append(i[column-1])
    if len(l) > 1:
        return mean(l)
    else:
        return None

def calculate_mean_list(self, l):
    length = len(l)
    sum = 0.0
    for i in l:
        sum += float(i)
    return sum / length

def calculate_mean_columns(self, columns, col_label):
    result = {}
    l = []
    for i in columns:
        l.append(self.calculate_mean_list(i))
    result.update({col_label:l})

    return result

def calculate_median_list(self,l):
    return median(l)

def calculate_median_columns(self, columns, col_label):
    result = {}
    l = []
    for i in columns:
        l.append(self.calculate_median_list(i))
    result.update({col_label:l})
    return result

def convertQueriesAxisSuperindex(self, queries):
    res = []
    for i in queries:
        spl = i.split(' ')
        res.append('$' + spl[0] + '^{' + spl[1] + '}$')

    return res

def createQuerySuperindex(self, queriesNumber):
    res = []
    for i in queriesNumber:
        res.append('$Q^{' + i + '}$')

    return res

def convertListToFloat(self, l):
    res = []
    for i in l:
        res.append(float(i))
    return res