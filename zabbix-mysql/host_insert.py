#coding=utf-8
import json
import urllib2
# based url and required header

import MySQLdb as mdb
import time

index = 1
jifang = 'ALI1'


# def get_host(groupid, id ):
#     global index
url = "http://ali-zabbix.cticloud.cn/api_jsonrpc.php"
header = {"Content-Type":"application/json"}
# request json
data = json.dumps(
{
   "jsonrpc":"2.0",
   "method":"host.get",
   "params":{
       # "output":["hostid","name"],
       # "groupids":groupid,
   },
   "auth":"944403ac5983b711ef785eb2cd24324f", # theauth id is what auth script returns, remeber it is string
   "id":2,
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
   # print response

   conn= mdb.connect(host='127.0.0.1',port = 3306,user='recode',passwd='12345',db ='INFORMATION_RECORD',charset='utf8')
   _time = time.strftime("%Y%m%d",time.localtime(time.time()))

   for host in response['result']:
       print "Host ID:",host['hostid'],"HostName:",host['name'] , "state:",host['available']

       try:
           # dic = {'id' : '14' , 'time' : _time , 'type' : '其他' , 'description' : '关闭运营中心王壮vpn，有线网、无线网，邮箱' , 'flag' : '0' , 'reason' : '王壮离职' , 'style' : '其他'}
           conn.autocommit(1)
           cursor = conn.cursor()
           value_List = []
           # tup = (dic['id'] , dic['time'] , dic['type'] , dic['description'] , dic['flag'] , dic['reason'] , dic['style'])
           tup = (index , host['name'] , _time , jifang , id , host['hostid']) #fixme id可以随便设一个值
           value_List.append(tup)
           sql = "insert into zabbix_host values(%s , %s , %s , %s ,%s , %s)"
           x = cursor.executemany(sql , value_List)#x为操作行集
           conn.commit()
           cursor.close()
           index = index + 1
       except Exception , e:
           print '操错错误:' + str(e)
   conn.close()



# #获得 mysql 查询的链接对象
# con = mdb.connect('127.0.0.1',port = 3306,user='recode',passwd='12345',db ='INFORMATION_RECORD',charset='utf8')
# with con:
# #获取连接上的字典 cursor，注意获取的方法，
# #每一个 cursor 其实都是 cursor 的子类
#     cur = con.cursor(mdb.cursors.DictCursor)
#     sql = "SELECT id ,groupid  FROM zabbix_hostgroup where source_addres='"+ jifang  +"'"
#     #执行语句不变
#     cur.execute(sql)
#     #获取数据方法不变
#     rows = cur.fetchall()
#     #遍历数据也不变（比上一个更直接一点）
#     print rows
#     for i in rows:
#         print i['id'] , i['groupid']
#         get_host(i['groupid'],i['id'])
#         index = index + len(rows)
#
# con.close()