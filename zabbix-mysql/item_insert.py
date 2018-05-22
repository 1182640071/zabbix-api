#coding=utf-8
import json
import urllib2

import MySQLdb as mdb
import time

index = 1
jifang = 'ALI1'


def get_item(hostid, id ):
    global index
    #net.if.in[eth0]  net.if.out[eth0]
    # based url and required header
    url = "http://ali-zabbix.cticloud.cn/api_jsonrpc.php"
    header = {"Content-Type":"application/json"}
    # request json
    data = json.dumps(
    {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": hostid,
            "search": {
                # "key_": "system"
            },
            "sortfield": "name"
        },
        "auth": "9a9bc92f1ef917ae74bd7c550b2e506b",
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

       conn= mdb.connect(host='127.0.0.1',port = 3306,user='recode',passwd='12345',db ='INFORMATION_RECORD',charset='utf8')
       _time = time.strftime("%Y%m%d",time.localtime(time.time()))

       print len(response['result'])
       for i in response['result']:
           # print 'itemid: ' + i['itemid'] \
           # +'\n'+'name: ' + i['name'] \
           # +'\n'+'key_: ' + i['key_'] \
           # +'\n'+'status: ' + i['status'] \
           # +'\n'+'hostid: ' + i['hostid'] \
           # +'\n'+'Update interval: ' + i['delay'] \
           # +'\n'+'history: ' + i['history'] \
           # +'\n'+'Trend storage period: ' + i['trends'] \
           # +'\n'+'templateid: ' + i['templateid'] \
           # +'\n'+'type: ' + i['type'] \
           # +'\n'+'description: ' + i['description'] \
           # +'\n' + '========================================'

            try:
               # dic = {'id' : '14' , 'time' : _time , 'type' : '其他' , 'description' : '关闭运营中心王壮vpn，有线网、无线网，邮箱' , 'flag' : '0' , 'reason' : '王壮离职' , 'style' : '其他'}
               conn.autocommit(1)
               cursor = conn.cursor()
               value_List = []
               # tup = (dic['id'] , dic['time'] , dic['type'] , dic['description'] , dic['flag'] , dic['reason'] , dic['style'])
               tup = (index,_time,i['name'],i['itemid'],i['key_'],i['status'],i['hostid'],i['delay'],i['history'],i['trends'],i['templateid'],i['type'],jifang,i['description'])
               value_List.append(tup)
               sql = "insert into zabbix_item values(%s , %s , %s , %s ,%s , %s,%s , %s , %s , %s ,%s , %s,%s , %s)"
               x = cursor.executemany(sql , value_List)#x为操作行集
               conn.commit()
               cursor.close()
               index = index + 1
            except Exception , e:
               print '操错错误:' + str(e)
       conn.close()



#获得 mysql 查询的链接对象
con = mdb.connect('127.0.0.1',port = 3306,user='recode',passwd='12345',db ='INFORMATION_RECORD',charset='utf8')
with con:
#获取连接上的字典 cursor，注意获取的方法，
#每一个 cursor 其实都是 cursor 的子类
    cur = con.cursor(mdb.cursors.DictCursor)
    sql = "SELECT DISTINCT name , hostid FROM zabbix_host where source_addres='"+ jifang  +"'"
    #执行语句不变
    cur.execute(sql)
    #获取数据方法不变
    rows = cur.fetchall()
    #遍历数据也不变（比上一个更直接一点）
    # print len(rows)
    for i in rows:
    #     print i['id'] , i['groupid']
        get_item(i['hostid'] , '1')
    #     index = index + len(rows)

con.close()
