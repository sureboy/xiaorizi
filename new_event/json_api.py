#coding:utf-8
from django.http import HttpResponse
from django.utils import simplejson as json
from admin_self.common import NewformatEvent,get_event_list,event_city_cat



     

def NewformatEvent_json(request,eventid=False,new=False):

    ev=NewformatEvent(False,eventid,new)
    response = json.dumps(ev)
    return HttpResponse(response, mimetype="application/json")



def get_event_list_json(request,cat=False,city=False,date=False,page=False,offset=False,order=False,new=False):

    ev=get_event_list(int(cat) , int(city) , int(date) , int(page) , int(offset) , int(order) ,new )
    response = json.dumps(ev)
    return HttpResponse(response, mimetype="application/json")

def event_city_cat_json(request,city_id=None,cat_id=None, new=False,cou=False):
    city_ids=city_id.split("_")
    if len(city_ids)>1:
        city_ids=tuple(city_ids)
    else:
        city_ids=city_id
        
    cat_ids=cat_id.split("_")
    if len(cat_ids)>1:
        cat_ids=tuple(cat_ids)
    else:
        cat_ids=cat_id
        
    ev=event_city_cat(city_ids , cat_ids , new , int(cou)  )
     
    response = json.dumps(ev)
    return HttpResponse(response, mimetype="application/json")