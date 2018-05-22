#coding=utf-8
import xlrd

def getDiff(list , path ):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows
    # ncols = table.ncols
    for i in xrange(1,nrows):
        rowValues= table.row_values(i)
        if not rowValues[0] in list:
            print rowValues[0]
        # for item in rowValues:
        #     print item