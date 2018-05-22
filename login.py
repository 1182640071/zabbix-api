#coding=utf-8
import json
import urllib2
# based url and required header
url = "http://172.16.22.25/zabbix/api_jsonrpc.php"
# url = "http://172.16.0.219/api_jsonrpc.php"
header = {"Content-Type":"application/json"}
# auth user and password
data = json.dumps(
{
   "jsonrpc": "2.0",
   "method": "user.login",
   "params": {
   "user": "Admin",
   "password": "zabbix"
},
"id": 0
})
# create request object
request = urllib2.Request(url,data)
for key in header:
   request.add_header(key,header[key])
# auth and get authid
try:
   result = urllib2.urlopen(request)
except Exception:
   print "Auth Failed, Please Check Your Name AndPassword:",Exception.code
else:
   response = json.loads(result.read())
   result.close()
print"Auth Successful. The Auth ID Is:",response['result']


# ce959d06b406108dd303f451f410fd2e