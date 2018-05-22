#coding=utf-8
import MySQLdb

class MysqlFunction(object):

    def getConnection(self , **kwargs):
        '''
        获取数据连接
        :param kwargs:
        :return:
        '''
        conn= MySQLdb.connect(host=kwargs['host'],port=kwargs['port'],user=kwargs['user'],passwd=kwargs['passwd'],db =kwargs['db'],charset=kwargs['charset'])
        return conn

    def closeConnection(self , conn):
        '''
        关闭数据库连接
        :param conn: 数据库连接
        :return:
        '''
        try:
            conn.close()
        except Exception , e:
            print Exception
            print e


    def selectExcute(self , connection , sql , *args , **kwargs):
        '''
        mysql select 语句执行方法
        :param connection: 数据库连接
        :param sql: sql语句
        :param args: 条件参数
        :param kwargs: 条件参数
        :return: 由各行数据组成的元组
        '''
        cur = connection.cursor(MySQLdb.cursors.DictCursor)
        if len(args) > 0:
            cur.execute(sql , args)
        else:
            cur.execute(sql)
        rows = cur.fetchall()
        return rows

