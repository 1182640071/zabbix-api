#coding=utf-8
import zabbixFunction
import xlwt
from wtiteXsl.WriteXls import getDiff

url = "http://124.251.7.6:40000/zabbix/api_jsonrpc.php"  #http://221.179.172.66:40000/zabbix Admin g2u6d5c4
user='Admin'
password='xxxxx'
token = 'b5056dcbcb5b0aea65ca282e432cf5d7'
zf = zabbixFunction.ZabbixFunction(url , {"Content-Type":"application/json"} , user , password , "" , "" , '' , 0)
token = zf.getToken()
groupList = zf.getGroupList( token,url,{"Content-Type":"application/json"})


#将zabbix的监控清单写入xls
# wb = xlwt.Workbook()
# style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',num_format_str='#,##0.00')
# style1 = xlwt.easyxf('font: name Times New Roman, color-index blue, bold on',num_format_str='#,##0.00')
# for gl in groupList.keys():
#     height=0
#     ws = wb.add_sheet(gl,cell_overwrite_ok=True)
#     # ws.write(height, 0, gl, style0)
#     hostList = zf.getHostList( groupList[gl] ,token,url,{"Content-Type":"application/json"})
#     for hl in hostList.keys():
#         ws.write(height, 0, hl, style0)
#         height=height+1
#         print gl + ' ==> ' + hl + " :"
#         itemList = zf.getItemList('value', hostList[hl] ,token,url,{"Content-Type":"application/json"})
#         for item in itemList.keys():
#             ws.write(height, 1, item)
#             height=height+1
#         ws.write(height, 0, '')
#         height = height+1
#
# wb.save('zabbixSjHl.xls')


x=[]
for gl in groupList.keys():
    height=0
    hostList = zf.getHostList( groupList[gl] ,token,url,{"Content-Type":"application/json"})
    for host in hostList.keys():
        if host not in x:
            x.append(host)

getDiff(x , 'cmdb_sjhl.xlsx')
# print x




# ws.write(0, 0, 1234.56, style0)
# ws.write(1, 0, datetime.now(), style1)
# ws.write(2, 0, 1)
# ws.write(2, 1, 1)
# ws.write(2, 2, 3)
#
# wb.save('zabbix.xls')
