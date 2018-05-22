#coding=utf-8
import json
import urllib2
# based url and required header
#url = "http://192.168.168.147/zabbix/api_jsonrpc.php"
url = "http://172.16.0.219/api_jsonrpc.php"
header = {"Content-Type":"application/json"}
# request json
data = json.dumps(
{
    "jsonrpc": "2.0",
    "method": "graph.get",
    "params": {
        "output": "extend",
        "hostids": 10112,
        "sortfield": "name"
    },
    "auth": "04547204e1b83122ee66d4897b16f936",
    "id": 1
}
)
# create request object
request = urllib2.Request(url,data)
for key in header:
   request.add_header(key,header[key])
# get host list

result = urllib2.urlopen(request)
response = json.loads(result.read())
# print response['result']
for i in response['result']:
    print i['name'] , i['graphid']
    # for x in i.keys():
    #     print i['name'] , i['graphid']
