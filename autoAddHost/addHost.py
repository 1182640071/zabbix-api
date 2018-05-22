#coding=utf-8
import json
import urllib2 , sys
import socket
import fcntl
import struct


url = "http://172.16.22.25:8010/zabbix/api_jsonrpc.php"
header = {"Content-Type":"application/json"}


def getToken():
    '''
    获取token
    :return: token
    '''
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
        exit(1)
    else:
        response = json.loads(result.read())
        result.close()
    print"Auth Successful. The Auth ID Is:",response['result']
    return response['result']


def getModeHost(token , modle):
    '''
    获取模版信息
    :param token: token
    :param modle: 模版名称
    :return: 模版信息{'templete': [], 'group': [], 'jmxstatus': u''}
    '''
    groups = []
    templetes = []
    modeinfo = {}
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
        "auth":token, # theauth id is what auth script returns, remeber it is string
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
        for host in response['result']:
            if host['name'] == modle:
                for group in host['groups']:
                    groups.append(group["groupid"])
                modeinfo['group'] = groups
                for temp in host["parentTemplates"]:
                    templetes.append(temp['templateid'])
                modeinfo['templete'] = templetes
                modeinfo['jmxstatus'] = host['jmx_available']
    return modeinfo

def addHost(hostname , interface , token , group , templates):
    '''
    添加主机
    :param hostname: 主机名
    :param hostip: 主机ip
    :param params: data
    :param token: token
    :param group: 主机组id列表
    :param templates: 模版列表
    :return:
    '''
    data = json.dumps({
        "jsonrpc":"2.0",
        "method":"host.create",
        "params":{
             "host": hostname,
             "interfaces": interface,
           "groups": group,
           "templates": templates,
             },
        "auth": token,
        "id":1
        })
    request = urllib2.Request(url, data)
    for key in header:
        request.add_header(key, header[key])

    try:
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()
        print "add host : %s" % (hostname)
    except KeyError as e:
        print "\033[041m 主机添加有误，请检查模板正确性或主机是否添加重复 !\033[0m",e
        print response


def get_ip_address(ifname):
    '''
    获取本机内网ip,指定网卡
    :param ifname:
    :return: ip
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

# mode = sys.argv[1]
# hostname = sys.argv[2]
mode = 'VB_AWS6_CTI_LINK_ELK_1_172.31.1.112'
hostname = 'testtest'
hostIp = get_ip_address('en0')
interface = []
token = getToken()
modeinfo = getModeHost(token , mode)
if modeinfo == {}:
    exit(1)

if modeinfo["jmxstatus"] == '1':
    interface = [{
             "type": 1,
             "main": 1,
             "useip": 1,
             "ip": hostIp,
             "dns": "",
             "port": "10050"
              },
        {
             "type": 4,
             "main": 1,
             "useip": 1,
             "ip": hostIp,
             "dns": "",
             "port": "30000"
              },]
else:
    interface = [{
             "type": 1,
             "main": 1,
             "useip": 1,
             "ip": hostIp,
             "dns": "",
             "port": "10050"
              },]

print hostname+hostIp
print interface
print token
print modeinfo['group']
print modeinfo['templete']

addHost(hostname+hostIp , interface , token , modeinfo['group'] , modeinfo['templete'])

