#coding:utf-8

import threading
import urllib2,urllib
import Queue
from models import PostSeoInfo
import time
from django.utils.timezone import now
import re

notIncludeFlag = '如网页存在'
errorFlag = '您的访问出错了'
errorFlag = errorFlag.decode('utf-8','ignore').encode('gbk')

taskqueue=Queue.Queue()

class ParseBase(threading.Thread):
    def __init__(self, proxyhandler=None):
        threading.Thread.__init__(self)
        if proxyhandler:
            self.proxy = proxyhandler
        else:
            self.proxy = 'localhost'
        self.shield=False
        if proxyhandler:
            proxy = urllib2.ProxyHandler({'http':proxyhandler})
            self.opener = urllib2.build_opener(proxy,urllib2.HTTPHandler)
        else:
            self.opener = urllib2.build_opener()   
     
    def run(self):
        while True:
            try:
                #print self.proxy
                if taskqueue.empty():
                    break
                if self.shield:
                    break
                task = taskqueue.get()#task为PostSeoInfo对象
                #print task
                self.isInclude(task)
                time.sleep(5)
            except Exception,e:
                print self.proxy,e
                taskqueue.put(task)
                break
            
    def isInclude(self,task):
        contentUrl = task.site_url
        if not contentUrl:
            task.baidu_include = 2
            task.save()
            return
       
        url='http://www.baidu.com/s?tn=monline_5_dg&rn=20&ie=utf-8&wd=keyword&rsv_sug2=0&inputT=732'
        value={"wd":contentUrl}
        url = url.replace('wd=keyword',urllib.urlencode(value))
        rp = self.opener.open(url).read()
        
        if notIncludeFlag in rp:
            task.baidu_include = 0
            task.save()
            #print u'未收录'
        elif errorFlag in rp:
            taskqueue.put(task)
            self.shield = True
            #print u'被屏蔽了'
        else:
            task.baidu_include = 1
            task.baidu_include_time = now()
            task.save()
            #print url
            

def checkIncludeStatu():
    global taskqueuequeue
    for item in PostSeoInfo.objects.exclude(baidu_include=1):
        taskqueue.put(item)
        
    rp = urllib2.urlopen("http://pachong.org/").read()
    ipre = re.compile(r'<td>(\d+?\.\d+?\.\d+?\.\d+?)</td>[^.]+<td>(\d+?)</td>')
    ips = ipre.findall(rp)
    proxList = []
    for i in ips:
        proxList.append('http://'+i[0]+':'+i[1])
    #print proxList
    threadlist = []
    threadlist.append(ParseBase())
    for thread in threadlist:
        thread.start()
            
    for thread in threadlist:
        thread.join()

if __name__ == '__main__':
    checkIncludeStatu()
        
        
        
        
        
        
        
