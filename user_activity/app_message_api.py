#coding:utf-8
 
from django.utils import simplejson as json
from django.http import HttpResponse

from  user_activity.functions import ip_Filter,save_message,black_message,admin_black_message,\
find_event_message,find_user_time_message,find_user_collect


def get_user_collect(request):
 
    p=find_user_collect(request,request.GET.get('userid',False))
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
#留言
def get_message(request):
    cds = request.GET
    eventId = cds['eventid']
    question = cds['question']
    userid = cds['userid']   

 

    p=save_message(eventId,question,None,userid)
 
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

        
    
    
    
#回复留言
def get_an_message(request,messageid,question,date,userid,username,userfrom):
    
 
    if ip_Filter(request,50,userid):
    
        p=black_message(messageid,question,date,userid,username,userfrom) 
    else:
        p={'code':-10,'message':u"频繁请求，请稍后再试"}
           
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def get_admin_message(request,messageid,question,date,userid,username,userfrom,examine=False):
 
    try:
        if int(examine)==0:
            examine=False
        else:
            examine=True
    except:
        examine=False
    
    p=admin_black_message(messageid,question,date,userid,username,userfrom,examine) 
 
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

    
def get_event_message(request):
    
    
    
    cds = request.GET
    eventid = cds['eventid']
    offset = cds.get('offset',5)
    page = cds.get('page',1)
    p=find_event_message(eventid,int(offset) ,int(page) )

    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json") 
def get_user_message(request):
    
    cds = request.GET
    userid = cds['userid']
    date = cds.get('time',0)
    p=find_user_time_message(userid,date ) 
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json") 


def test_ip(request):
    p=ip_Filter(request)
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json") 
    
    


