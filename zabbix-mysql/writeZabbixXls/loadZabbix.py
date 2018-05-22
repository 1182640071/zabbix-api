#coding=utf-8
import threading
from mysqlFunction import MysqlFunction

class LoadZabbixMysql(object):

    #单例模式
    _instance_lock = threading.Lock()

    def __init__(self):
        self.mysql_function = MysqlFunction()
        # pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(LoadZabbixMysql, "_instance"):
            with LoadZabbixMysql._instance_lock:
                if not hasattr(LoadZabbixMysql, "_instance"):
                    LoadZabbixMysql._instance = object.__new__(cls)
        return LoadZabbixMysql._instance


    #加载template_application表
    def Load_template_application(self):
        try:
            conn = self.mysql_function.getConnection(host='127.0.0.1',port = 3306,user='recode',passwd='12345',db ='INFORMATION_RECORD',charset='utf8')
        except Exception ,e :
            print '数据库连接获取失败:'
            print Exception , e
            return {}
        sql = 'select templateid,name , applicationid from zabbix_template_application where source_addres = %s'
        sql = "select t.`name` as template_name , t.`templateid` , t.`applicationid` , f.`applicationid` , f.`name` as application_name , f.`itemid` from  " \
              "zabbix_template_application t,zabbix_application_itemid f " \
              "where t.`applicationid` = f.`applicationid`"
        try:
            rs = self.mysql_function.selectExcute(conn , sql)
        except Exception , e:
            print 'sql语句执行错误: ' + sql
            print Exception , e
            rs = {}
        finally:
            self.mysql_function.closeConnection(conn)

        data = {}
        for row in rs:
            keys = []
            dt = {}
            if not data.has_key(row['template_name']):
                data[row['template_name']] = []
                # dt[row['applicationid']] = row['application_name']
                dt['applicationid'] = row['applicationid']
                dt['application_name'] = row['application_name']
                dt['itemids']=[]
                dt['itemids'].append(row['itemid'])
                data[row['template_name']].append(dt)
            else:
                print row['template_name']
                print data[row['template_name']]
                for i in range(0,len(data[row['template_name']])):
                    print data[row['template_name']][i]
                    print row['template_name'] , row['itemid'] , row['applicationid'] , row['application_name']
                    print keys

                    if row['applicationid'] == data[row['template_name']][i]['applicationid']:
                        data[row['template_name']][i]['itemids'].append(row['itemid'])
                        continue
                    applicationid = data[row['template_name']][i]['applicationid']
                    keys.append(applicationid)
                if not row['applicationid'] in keys:
                    for i in range(0,len(data[row['template_name']])-1):
                        if row['applicationid'] == data[row['template_name']][i]['applicationid']:
                            data[row['template_name']][i]['itemids'].append(row['itemid'])
                # print row['applicationid']
                # print keys


        print data
                # print row


    #加载application_itemid表
    def Load_application_itemid(self):
        print 222

x = LoadZabbixMysql()
x.Load_template_application()