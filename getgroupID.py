#coding=utf-8
import json
import urllib2
# based url and required header
url = "http://192.168.168.147/zabbix/api_jsonrpc.php"
id = '09cd56f8958c999be22c1569f6587a82'
header = {"Content-Type":"application/json"}
# request json
data = json.dumps(
{
   "jsonrpc":"2.0",
   "method":"hostgroup.get",
   "params":{
       # "output":["groupid","name"],
   },
   "auth":id, # theauth id is what auth script returns, remeber it is string
   "id":1,
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
   print response
   for group in response['result']:
       print "Group ID:",group['groupid'],"\tGroupName:",group['name']
