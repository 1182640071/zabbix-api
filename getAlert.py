#coding=utf-8
import json
import urllib2
# based url and required header
# url = "http://192.168.168.147/zabbix/api_jsonrpc.php"
url = "http://ali-zabbix.cticloud.cn/api_jsonrpc.php"
header = {"Content-Type":"application/json"}
# request json
data = json.dumps(
{
    "jsonrpc": "2.0",
    "method": "alert.get",
    "params": {
        "output": "extend",
        "actionids": "1"
    },
    "auth": "b74c1bfb1e3d0f301bfc7a4d7b88df1d",
    "id": 1
}
)
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
   print response
   # for host in response['result']:
   #     print host
       # print "Host ID:",host['hostid'],"HostName:",host['name'] , "state:",host['available']
