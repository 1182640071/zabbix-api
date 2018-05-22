#coding=utf-8
#create by wml
#date 2017.09.14

import json , urllib2
# from getValues import getPNG
from httpPost import HttpPost

class ZabbixFunction:
    '''
    zabbix包含zabbix各种操作的类,通过init传参进行构造,或得ZabbixFunction类对象,进而使用此类的其他方法
    '''

    def __init__(self , url='' , header={"Content-Type":"application/json"} , user='' , password='' , urlpng="http://192.168.168.147/zabbix/chart2.php" , urlvalue="http://192.168.168.147/zabbix/index.php" , token='' , size=0):
        '''
        ZabbixFunction类的构造方法
        :param url:zabbix地址
        :param header:http请求的消息头
        :param user:zabbix用户名
        :param password:zabbix密码
        :return:返回ZabbixFunction类对象
        '''
        self.url=url
        self.urlvalue=urlvalue
        self.header=header
        self.user=user
        self.password=password
        self.urlpng=urlpng
        self.token=token
        self.size=0

    def getToken(self):
        '''
        zabbix登录方法,类对象加载token值,对zabbix的所有操作,查询都需要带有此token值
        :param user:zabbix用户名
        :param password:zabbix密码
        :return:None
        '''
        data = json.dumps(
        {
           "jsonrpc": "2.0",
           "method": "user.login",
           "params": {
           "user": self.user,
           "password": self.password
        },
        "id": 0
        })
        self.token = HttpPost().post(self.url , data , self.header)
        return self.token



    def getValue(self , itemID , type , path='' , period='' , starttime='' , width=800 , height=200):
        '''
        获取监控项信息(图片,或者数据)
        :param type: 获取数据类型 'png'图片 其他为数据
        :param path: 图片保存目录
        :param period: 数据持续时间
        :param starttime: 数据开始时间
        :param width: 图片横长
        :param height: 图片纵长
        :return:None
        '''
        if itemID == '':
            print '监控项id为空,没有要查询的监控项'
        searchValue=self.instantiation(type , path , period , starttime , width=800 , height=200)
        if searchValue is not None:
            return searchValue.getPng(itemID)


    #
    # def instantiation(self , type , path , period , starttime , width=800 , height=200):
    #     '''
    #     简单工厂模式进行实例化,通过type进行区分
    #     :param type: 获取数据类型 'png'图片 其他为数据
    #     :param path: 图片保存目录
    #     :param period: 数据持续时间
    #     :param starttime: 数据开始时间
    #     :param width: 图片横长
    #     :param height: 图片纵长
    #     :return:获取图片类对象
    #     '''
    #     if type == '':
    #         return None
    #     elif type == 'png':
    #         return getPNG(self , period , starttime , path, width , height)
    #     else:
    #         #FIXME 获取数据的类对象
    #         return ZabbixFunction(self.url , self.header , self.user , self.password , self.urlpng , self.urlvalue , self.token)
    #


    def getGroupList(self , token='',url='',header=''):
        '''
        获取监控中的主机组信息
        :param token:token值
        :return:group数据字典{'groupname':'groupid'}
        '''
        if token == '' or url == '':
            print '[ERROR]token or url is null'
            return []

        if header == '' or type(header) != dict:
            header = {"Content-Type":"application/json"}
        data = json.dumps(
        {
           "jsonrpc":"2.0",
           "method":"hostgroup.get",
           "params":{
               "output":["groupid","name"],
           },
           "auth":token,
           "id":1,
        })
        list = HttpPost().post(url , data , header)
        dic = {}
        if len(list) <= 0:
            print "[ERROR]group is empty!"
            return dic
        else:
            for dc in list:
                dic[dc['name']]=dc['groupid']
            return dic

    def getHostList(self , groupid ,token='',url='',header=''):
        '''
        获取监控中的主机信息
        :param token:token值
        :return:group数据字典{'hostname':'hostid'}
        '''
        if header == '' or type(header) != dict:
            header = {"Content-Type":"application/json"}
        data = json.dumps(
        {
           "jsonrpc":"2.0",
           "method":"host.get",
           "params":{
               "output":["hostid","name"],
               "groupids":groupid,
           },
           "auth":token, # theauth id is what auth script returns, remeber it is string
           "id":2,
        })
        list = HttpPost().post(url , data , header)
        dic = {}
        if len(list) <= 0:
            print "[ERROR]group is empty!"
            return dic
        else:
            for dc in list:
                dic[dc['name']]=dc['hostid']
            return dic



    def getItemList(self , type, hostid ,token='',url='',header={"Content-Type":"application/json"}):
        '''
        获取监控项信息
        :param token:token值
        :return:group数据字典{'itemname':'itemid'}
        '''
        # if header == '' or type(header) != dict:
        #     header = {"Content-Type":"application/json"}

        if type =='png':
            data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "graph.get",
                "params": {
                    "output": "extend",
                    "hostids": hostid,
                    "sortfield": "name"
                },
                "auth": token,
                "id": 1
            })
        elif type == "value":
            data = json.dumps(
            {
               "jsonrpc":"2.0",
               "method":"item.get",
               "params":{
                   "output":["itemids","key_"],
                   "hostids":hostid, #10123  234   local_centos6-2  10117
               },
               "auth":token, # theauth id is what auth script returns, remeber it is string
               "id":2,
            })
        else:
            print "[ERROR]type类型错误"
            return {}
        list = HttpPost().post(url , data , header)
        dic = {}
        if len(list) <= 0:
            print "[ERROR]group is empty!"
            return dic
        else:
            for dc in list:
                if type == "png":
                    dic[dc['name']]=dc['graphid']
                if type == "value":
                    dic[dc['key_']]=dc['itemid']
            return dic


    def getPng(self , itemId , header={"Content-Type":"application/json"}):
        '''
        获取监控项信息
        :param token:token值
        :return:group数据字典{'itemname':'itemid'}
        '''
        if self.token== '':
            print '[ERROR]token不能为空!'
            return None

        data = json.dumps(
        {
           "jsonrpc":"2.0",
           "method":"history.get",
            # history参数可能的取值
            # 0 - float;
            # 1 - string;
            # 2 - log;
            # 3 - integer;
            # 4 - text.
           "params":{
               "output":"extend",
               "history":3,
               "sortfield":"clock",
               "itemids":itemId,
               "sortorder":"DESC",
               "limit":self.size
           },
           "auth":self.token, # theauth id is what auth script returns, remeber it is string
           "id":1,
        })
        list = HttpPost().post(self.url , data , header)
        dic = {}
        if len(list) <= 0:
            print "[ERROR]result is empty!"
            return dic
        else:
            for dc in list:
                dic[dc['clock']]=dc['value']
            return dic
