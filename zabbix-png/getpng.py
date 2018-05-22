#coding=utf-8
import sys
import datetime
import cookielib, urllib2,urllib
# class ZabbixGraph(object):
def getoper(url,name,password):
    #初始化的时候生成cookies
    cookiejar = cookielib.CookieJar()
    urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    values = {"name":name,'password':password,'autologin':1,"enter":'Sign in'}
    data = urllib.urlencode(values)
    print data
    request = urllib2.Request(url, data)
    try:
        urlOpener.open(request,timeout=10)
        return urlOpener
        # self.urlOpener=urlOpener
    except urllib2.HTTPError, e:
        print e


# def __init__(self,url,name,password):
#     self.url=url
#     self.name=name
#     self.password=password
#     #初始化的时候生成cookies
#     cookiejar = cookielib.CookieJar()
#     urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
#     values = {"name":self.name,'password':self.password,'autologin':1,"enter":'Sign in'}
#     data = urllib.urlencode(values)
#     request = urllib2.Request(url, data)
#     try:
#         urlOpener.open(request,timeout=10)
#         self.urlOpener=urlOpener
#     except urllib2.HTTPError, e:
#         print e

def GetGraph(s ,url,values,image_dir):
    key=values.keys()
    if "graphid"  not in key:
        print u"请确认是否输入graphid"
        sys.exit(1)
    #以下if 是给定默认值
    if  "period" not in key :
        #默认获取一天的数据，单位为秒
        values["period"]=86400
    if "stime" not in key:
        #默认为当前时间开始
        values["stime"]=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if "width" not in key:
        values["width"]=800
    if "height" not in key:
        values["height"]=200
    data=urllib.urlencode(values)
    request = urllib2.Request(url,data)
    url = s.open(request)
    image = url.read()
    imagename="%s/%s.png" % (image_dir, values["graphid"])
    f=open(imagename,'wb')
    f.write(image)

#此url是获取图片是的，请注意饼图的URL 和此URL不一样，请仔细观察！
#gr_url="http://192.168.168.147/zabbix/chart2.php"
gr_url="http://172.16.0.219/chart2.php"
#登陆URL
indexURL="http://172.16.0.219/index.php"
username="Admin"
password="zabbix"
#用于图片存放的目录
image_dir="png"
#图片的参数，该字典至少传入graphid。
values={"graphid":"649","period":3600,"stime":20180415150000,"width":800,"height":200}
# b=ZabbixGraph(indexURL,username,password)
b=getoper(indexURL,username,password)
GetGraph(b,gr_url,values,image_dir)