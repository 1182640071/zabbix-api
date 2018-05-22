#coding=utf-8
import json
import urllib2
#net.if.in[eth0]  net.if.out[eth0]
# based url and required header
url = "http://192.168.168.147/zabbix/api_jsonrpc.php"
header = {"Content-Type":"application/json"}
# request json
data = json.dumps(
{
   "jsonrpc":"2.0",
   "method":"item.get",
   "params":{
       "output":["itemids","key_"],
       "hostids":"10114", #10123  234   local_centos6-2  10117
   },
   "auth":"eb9c2a73493243deef3b8de155bc13d6", # theauth id is what auth script returns, remeber it is string
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
       print host
       #print "Host ID:",host['hostid'],"HostName:",host['name']



