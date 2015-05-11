#coding:utf-8
from django.http import HttpResponse
import json
import hashlib
import time

def islogin(func): 
    def _islogin(request,*arg):
        if request.session.get('islogin'):
            return func(request,*arg)
        else:
            return HttpResponse(json.dumps({"code":0,"msg":u'请登陆后进行此操作'}), content_type="application/json")
    return _islogin

def isAPP(func):
    def _isAPP(request,*p,**arg):
        if request.method == 'POST':
            cds = request.POST
        if request.method == 'GET':
            cds = request.GET
        token =  cds.get('app_token')
        app_time = cds.get('token_time')
        if token and app_time:
            #return func(request,*p,**arg)
            if int(app_time) > time.time() - 60*10:
                m = hashlib.md5()
                m.update('%scqdeveloper' % app_time)
                md = m.hexdigest().upper()
                ms = [md[i] for i in range(len(md)) if i%2]
                if token == ''.join(ms):
                    return func(request,*p,**arg)
        return HttpResponse(json.dumps({"code":0,"msg":u'无权访问'}), content_type="application/json")
    return _isAPP

def queryset2list(queryset):
    res = []
    for item in queryset:
        res.append(item)
    return res

def make_password(pwd):
    m = hashlib.md5()
    m.update(pwd)
    return m.hexdigest()

def check_password(pw1,pw2):
    m = hashlib.md5()
    m.update(pw1)
    if m.hexdigest() == pw2:
        return True
    else:
        return False
    

    