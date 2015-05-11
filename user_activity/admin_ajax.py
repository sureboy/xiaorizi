#coding:utf-8
from user_activity.models import UserEventMessage
from django.utils import simplejson as json
from django.http import HttpResponse
from  user_activity.functions import admin_black_message
import time

'''
def get_json_img(request, query):
    photos = SysSpotImg.objects.order_by('-end_time').filter(Q(name__icontains=query) | Q(cat_name__name__contains=query) | Q(urls__icontains=query))[:20]
    p = [ {"name":photo.name, "id":photo.id,"urls":photo.urls } for photo in photos ]
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
    
'''

def save_json_blackmessage(request):
    msg_id=request.POST.get("msg_id",'') 
    content=request.POST.get("content",'')  
    
    p=admin_black_message(msg_id,content,int(time.time()),99999,'活动家艾艾','活动小管家',True)
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
    