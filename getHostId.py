#coding=utf-8
import json
import urllib2
# based url and required header
# url = "http://192.168.168.147/zabbix/api_jsonrpc.php"
url = "http://aws-6-zabbix.cticloud.cn/api_jsonrpc.php"
header = {"Content-Type":"application/json"}
# request json
data = json.dumps(
{
   "jsonrpc":"2.0",
   "method":"host.get",
   "params":{
       "selectParentTemplates": "extend",
       "selectGroups": "extend"
       # "output":["hostid","name"],
       # "groupids":"2",
   },
   "auth":"ce959d06b406108dd303f451f410fd2e", # theauth id is what auth script returns, remeber it is string
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
   for host in response['result']:
       if host['name'] == "VB_AWS6_CTI_LINK_AGENT-GATEWAY_DATA_CDR1_172.31.0.107" :
           print host
       # print host
       # print "Host ID:",host['hostid'],"HostName:",host['name'] , "state:",host['available']
