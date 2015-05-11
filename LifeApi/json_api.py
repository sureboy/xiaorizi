#coding:utf-8
from django.http import HttpResponse
from django.utils import simplejson as json
from LifeApi.common import NewformatEvent,get_event_list,event_city_cat,NewCity,get_str_singers,NewCatUrl,get_site_links,get_str_event



     

def NewformatEvent_json(request,eventid=False,new=False):
    
    try:
        if int(new) is 0:
            new=False
    except:
        if not new:
            new=False

    ev=NewformatEvent(False,eventid,new)
    response = json.dumps(ev)
    return HttpResponse(response, mimetype="application/json")



def get_event_list_json(request,cat=False,city=False,date=False,page=False,offset=False,order=False,new=False):

    city_ids=city.split("_")
    if len(city_ids)>1:
        city_ids=tuple(city_ids)
    else:
        city_ids=int(city)
        
    try:
        if int(new) is 0:
            new=False
    except:
        if not new:
            new=False
    
    ev=get_event_list( cat  ,  city_ids  ,  date, int(page) , int(offset) ,  order  ,new )
    response = json.dumps(ev)
    return HttpResponse(response, mimetype="application/json")

def event_city_cat_json(request,city_id=None,cat_id=None, new=False,cou=False):
    city_ids=city_id.split("_")
    if len(city_ids)>1:
        city_ids=tuple(city_ids)
    else:
        city_ids=int(city_id)
        
    cat_ids=cat_id.split("_")
    if len(cat_ids)>1:
        cat_ids=tuple(cat_ids)
    else:
        cat_ids=int(cat_id)
        
    try:
        if int(new) is 0:
            new=False
    except:
        if not new:
            new=False
        
    try:
        if int(cou) is 0:
            cou=False
    except:
        if not cou:
            cou=False
        
    ev=event_city_cat(city_ids , cat_ids , new ,  cou  )
     
    response = json.dumps(ev)
    return HttpResponse(response, mimetype="application/json")


def NewCity_json(request,type=0,new=False):
    try:
        if int(new) is 0:
            new=False
    except:
        if not new:
            new=False
 
    ev=NewCity(int(type),new)
    response = json.dumps(ev)
    return HttpResponse(response, mimetype="application/json")

def NewCatUrl_json(request,type=0,city='',new=False ):
    try:
        if int(new) is 0:
            new=False
    except:
        if not new:
            new=False
    ev=NewCatUrl(int(type),city ,new  )
    response = json.dumps(ev)
    return HttpResponse(response, mimetype="application/json")

def get_site_links_json(request,new=False):
    try:
        if int(new) is 0:
            new=False
    except:
        if not new:
            new=False
    ev=get_site_links(new)
    response = json.dumps(ev)
    return HttpResponse(response, mimetype="application/json")
 
 
def get_str_event_json(request,new=False):
    try:
        if int(new) is 0:
            new=False
    except:
        if not new:
            new=False
    ev=get_str_event(new)
    response = json.dumps(ev)
    return HttpResponse(response, mimetype="application/json")

def get_str_singers_json(request,new=False):
    try:
        if int(new) is 0:
            new=False
    except:
        if not new:
            new=False
    
    ev=get_str_singers(new)
    response = json.dumps(ev)
    return HttpResponse(response, mimetype="application/json")