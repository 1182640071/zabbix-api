#coding=utf-8
import json
import urllib2

import MySQLdb as mdb
import time
import string

index = 1
jifang = 'ALI1'


#net.if.in[eth0]  net.if.out[eth0]
# based url and required header
url = "http://ali-zabbix.cticloud.cn/api_jsonrpc.php"
header = {"Content-Type":"application/json"}
# request json
data = json.dumps(
{
    "jsonrpc": "2.0",
    "method": "application.get",
    "params": {
        "output": "extend",
        "selectItems": "extend",
        # "selectHost": "extend",
        # "hostids": "10001",
        # "sortfield": "name"
    },
    "auth": "92fd90e2ec1e194d08df8e193800b183",
    "id": 1
})
# create request object
request = urllib2.Request(url,data)
for key in header:
   request.add_header(key,header[key])
# get host list
try:
   result = urllib2.urlopen(request)
except Exception as e:
   if hasattr(e, 'reason'):
       print 'We failed to reach a server.'
       print 'Reason: ', e.reason
   elif hasattr(e, 'code'):
       print 'The server could not fulfill the request.'
       print 'Error code: ', e.code
else:
   response = json.loads(result.read())
   result.close()
   print "Number Of Hosts: ", len(response['result'])
   # print response['result']

   conn= mdb.connect(host='127.0.0.1',port = 3306,user='recode',passwd='12345',db ='INFORMATION_RECORD',charset='utf8')
   _time = time.strftime("%Y%m%d",time.localtime(time.time()))

   for i in response['result']:

       # print i['name']

       for item in i['items']:
           # print item['itemid']


           try:
               conn.autocommit(1)
               cursor = conn.cursor()
               value_List = []
               tup = (i['applicationid'], i['name'],  _time, jifang , item['itemid'])
               value_List.append(tup)
               sql = "insert into zabbix_application_itemid values(%s , %s , %s , %s ,%s)"
               x = cursor.executemany(sql , value_List)#x为操作行集
               conn.commit()
               cursor.close()
               index = index + 1
           except Exception , e:
               print '操错错误:' + str(e)
   conn.close()




