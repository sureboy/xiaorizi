#coding:utf-8
from django.http import HttpResponse
from django.utils import simplejson as json
from django.core.cache import cache
from admin_self.common import event_city_cat

     

def save_img(request):
    p=[]
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")  

def show_cache(request):
    name=request.GET.get('name',None) 
    p=[]
    if name:    
        #p = cache.get('%s' % (name)) 
        p=event_city_cat(101,69,True  )   
        response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")  