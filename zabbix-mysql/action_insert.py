#coding=utf-8
import json
import urllib2
# based url and required header

import MySQLdb as mdb
import time

index = 1
jifang = 'ALI1'

url = "http://ali-zabbix.cticloud.cn/api_jsonrpc.php"

header = {"Content-Type":"application/json"}
# request json
data = json.dumps(
{
    "jsonrpc": "2.0",
    "method": "action.get",
    "params": {
        "output": "extend",
        "selectOperations": "extend",
        "selectRecoveryOperations": "extend",
        "selectFilter": "extend",
        # "filter": {
        #     "eventsource": 1
        # }
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
   # print response

   conn= mdb.connect(host='127.0.0.1',port = 3306,user='recode',passwd='12345',db ='INFORMATION_RECORD',charset='utf8')
   _time = time.strftime("%Y%m%d",time.localtime(time.time()))

   for i in response['result']:
       guize = ''
       for gz in i['filter']['conditions']:
           guize = guize + str(gz)

       yonghuzu = ''
       for opt in i['operations']:
           # yonghuzu = yonghuzu + str(opt['opmessage_grp']['usrgrpid'])
           if opt.has_key('opmessage_grp'):
               for ug in opt['opmessage_grp']:
                   if ug.has_key('usrgrpid'):
                       yonghuzu = yonghuzu + ug['usrgrpid']
       #
       # print i['name'] + ' , '  \
       #       + u'状态: ' + i['status'] + ' ,' \
       #       + '\n' + u"告警标题" + ': "' + i['def_shortdata'] + '" ' \
       #       + '\n' + u'告警模版' + ':"' + i['def_longdata'] + '"' \
       #       + '\n' + u"恢复标题" + ':"' + i['r_shortdata'] + '"' \
       #       + '\n' + u'恢复模版' + ':"' + i['r_longdata'] + '"' \
       #       + '\n' + u'报警规则:"' + i['filter']['eval_formula'] + '"' \
       #       + '\n' + u'规则明细:"' + guize + '"' \
       #       + '\n' + u'发送用户组:"' + yonghuzu + '"' \
       #       + '\n==================================================='
       try:
           # dic = {'id' : '14' , 'time' : _time , 'type' : '其他' , 'description' : '关闭运营中心王壮vpn，有线网、无线网，邮箱' , 'flag' : '0' , 'reason' : '王壮离职' , 'style' : '其他'}
           conn.autocommit(1)
           cursor = conn.cursor()
           value_List = []
           # tup = (dic['id'] , dic['time'] , dic['type'] , dic['description'] , dic['flag'] , dic['reason'] , dic['style'])
           tup = (index, i['name'], _time, i['status'], jifang, i['def_shortdata'], i['def_longdata'], i['r_shortdata'], i['r_longdata'], i['filter']['eval_formula'], guize, yonghuzu)
           value_List.append(tup)
           sql = "insert into zabbix_action values(%s , %s , %s , %s ,%s , %s , %s , %s , %s , %s ,%s , %s)"
           x = cursor.executemany(sql , value_List)#x为操作行集
           conn.commit()
           cursor.close()
           index = index + 1
       except Exception , e:
           print '操错错误:' + str(e)
   conn.close()



