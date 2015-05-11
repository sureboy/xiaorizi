#coding:utf-8
from version.models import AppVersion,AppVersionCode
from django.http import HttpResponse
import json,re

def update(request):
    if request.method == 'GET':

        cds = request.GET
        if not cds.get('version') or not cds.get('platform'):
            return HttpResponse(json.dumps({"code":0,"msg":"版本号或平台类型缺失"}), content_type="application/json")
        platform = cds.get('platform','')
        if platform == 'life_iOS':
            app_version = AppVersion.objects.get(platform=3)
        elif platform == 'life_Android':
            app_version = AppVersion.objects.get(platform=4)
        else:
            return HttpResponse(json.dumps({"code":0,"msg":"平台类型错误"}), content_type="application/json")
        
        data = {}
        code = 0
        msg = u'已是最新版本'
        version=re.sub(ur"[^\w]", "", app_version.version)
        ver=re.sub(ur"[^\w]", "", cds.get('version'))
        if int(version) > int(ver):
            data = {
                    'must':app_version.must_update,
                    'version':app_version.version,
                    'update':app_version.update_info,
                    'url':app_version.url,
                    }
            code = 1
            msg = u'更新信息'
        return HttpResponse(json.dumps({"code":code,"msg":msg,"data":data}), content_type="application/json")
    
    
def update_test(request):
    if request.method == 'GET':
        cds = request.GET
        if not cds.get('version') or not cds.get('platform'):
            return HttpResponse(json.dumps({"code":0,"msg":"版本号或平台类型缺失"}), content_type="application/json")
        platform = cds.get('platform','')
        if platform == 'iOS':
            app_version = AppVersionCode.objects.get(platform=1)
        elif platform == 'Android':
            app_version = AppVersionCode.objects.get(platform=2)
        else:
            return HttpResponse(json.dumps({"code":0,"msg":"平台类型错误"}), content_type="application/json")
        
        data = {}
        code = 0
        msg = u'已是最新版本'
        version=re.sub(ur"[^\w]", "", app_version.version)
        ver=re.sub(ur"[^\w]", "", cds.get('version'))
        if int(version) > int(ver):
            data = {
                    'must':app_version.must_update,
                    'version':app_version.version,
                    'update':app_version.update_info,
                    'url':app_version.url,
                    }
            code = 1
            msg = u'更新信息'
        return HttpResponse(json.dumps({"code":code,"msg":msg,"data":data}), content_type="application/json")