#coding:utf-8
from django.http import HttpResponseRedirect,HttpResponse
#from app_manage.common import get_app_list
from app_manage.models import app_table
from django.shortcuts import render_to_response
from django.template import RequestContext
from LifeApi.common import NewAppEvent
import json,re

'''
def app_manage(request,app=0,template_name='app_list.html'):   
    list_s=get_app_list(app,request.GET.get('new',None)) 
    return render_to_response(template_name,{'list':list_s,'len_list':len(list_s),'page':1,'offset':20},context_instance=RequestContext(request))

def app_manage_api(request,app=0):
    return HttpResponse(json.dumps({"code":0,"msg":"keyword Fail","list":get_app_list(app,request.GET.get('new',None))}), content_type="application/json")

'''
def update(request):
    #return HttpResponse(json.dumps({"code":0,"msg":'',"data":''}), content_type="application/json")
    if request.method == 'GET':
        cds = request.GET
        if not cds.get('version') or not cds.get('platform'):
            return HttpResponse(json.dumps({"code":0,"msg":"版本号或平台类型缺失"}), content_type="application/json")
        platform = cds.get('platform','')
        try:
            app_version = app_table.objects.get(md5=platform)
        except:
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
                    'update':app_version.update_text,
                    'url':app_version.link,
                    }
            code = 1
            msg = u'更新信息'
        return HttpResponse(json.dumps({"code":code,"msg":msg,"data":data}), content_type="application/json")
def downApp(request):
    if request.method == 'GET':
        try:
            app=app_table.objects.get(id=request.GET.get('app_id'))
            app.hot+=1
            url=app.link
            app.save()
            if url:
                return HttpResponseRedirect(url)
        except:
            pass
    
    return HttpResponse(json.dumps({"code":0,"msg":"err"}), content_type="application/json")
        
def downAppPage(request,param):
    #6,7
    #app_table.objects.filter(id__in=[6,7])
    p={}
    p['android']='/app/?app_id=%s' % (6,)
    p['iOS']='/app/?app_id=%s' % (7,)
    if 0 != len(param):
        return render_to_response(param,p)
    else:
        return render_to_response('download.html',p)

def showQ(request,query=False,template_name='q_showEvent.html'):
    event={}
    if query.isdigit():
        event= NewAppEvent(False,int(query),request.GET.get('new',False))        

    if not event.has_key('isshow'):
        return render_to_response('not.html',{'error_msg':u'没有该活动  '  })
  
    else:
        if not event['isshow'] in [1,8]:
            return render_to_response('not.html',{'error_msg':u'活动没有发布' })       


        note=None
        for con in event['event_content']:
            if con[0] in [u'购买须知']:
                note=con
                break

                
 
        body={'note':note,
              'event_id':event['event_id']
             }
        return render_to_response(template_name,body,context_instance=RequestContext(request))
def showCont(request,query=False,template_name='s_showEvent.html'):
    event={}
    if query.isdigit():
        event= NewAppEvent(False,int(query),request.GET.get('new',False))        
    '''
    if not event.has_key('isshow'):
        return render_to_response('not.html',{'error_msg':u'没有该活动  '  })
  
    else:
    
        if not event['isshow'] in [1,8]:
            return render_to_response('not.html',{'error_msg':u'活动没有发布' })       

    '''

    note=[]
    
    for i in range(len(event['event_content'])):

        if i is 0:    
            cont=event['event_content'][i][1].replace('<br>','').replace('<br />','')
            cont=re.sub(ur"[\u200b]", "", cont)
            i=repr(cont).find('200b')
            if i>0:
                break
            cont=eval(repr(cont).replace('\u200b','').replace('200B',''))
            #event['event_content'][i]=(event['event_content'][i][0],cont)            
            
            note.append((event['event_content'][i][0],cont))
        elif event['event_content'][i][0] in  [u'行程安排']:
            note.append(event['event_content'][i])
    
            

    body={'note':note,
          'event_id':event['event_id'],
          'event_name':event['title'],
          'event_tag':' '.join(event['event_tag']),
          'event_img':event['event_img'],          
         }
    return render_to_response(template_name,body,context_instance=RequestContext(request))

