#!/usr/bin/env python
#coding=utf-8
import urllib2
import json
#定义URL账户密码
url = 'http://192.168.168.147/zabbix/api_jsonrpc.php'
username = 'Admin'
password = 'omygad911'
#定义通过HTTP方式访问API地址的函数，后面每次请求API的各个方法都会调用这个函数
def requestJson(url,values):
    data = json.dumps(values)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
    response = urllib2.urlopen(req, data)
    output = json.loads(response.read())
#    print output
    try:
        message = output['result']
    except:
        message = output['error']['data']
        print message
        quit()

    return output['result']

#API接口认证的函数，登录成功会返回一个Token
def authenticate(url, username, password):
    values = {'jsonrpc': '2.0',
              'method': 'user.login',
              'params': {
                  'user': username,
                  'password': password
              },
              'id': '0'
              }
    idvalue = requestJson(url,values)
    return idvalue

print authenticate(url,username,password)