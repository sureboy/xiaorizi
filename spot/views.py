#coding:utf-8
from models import SysSpotImg,SysSpotEvent,SysCity,SysSpotHcode,SysSpotTxt,SysCat
from django.utils import simplejson as json
from django.http import HttpResponse
from django.db.models import Q 
import datetime


def get_json(request,type, query):
    ty= {'img':SysSpotImg,'event':SysSpotEvent,'city':SysCity,'code':SysSpotHcode,'txt':SysSpotTxt,'cat':SysCat}
    try:
        arr = ty[type].objects.filter()
        if type == 'img':
            arr = arr.filter(name__icontains=query)
            arr = arr.filter(cat_name__icontains=query)
            arr = arr.filter(urls__icontains=query)[:20]
            p = [ {"name":k.name, "id":k.id,'url':k.urls } for k in arr ]
        elif type == 'code':
            arr = arr.filter(name__icontains=query)
            arr = arr.filter(cat_name__icontains=query)[:20]
            p = [ {"name":k.name, "id":k.id, } for k in arr ]
        elif type == 'txt':   
            arr = arr.filter(name__icontains=query)
            arr = arr.filter(cat_name__icontains=query)[:20]
            p = [ {"name":k.name, "id":k.id, } for k in arr ] 
        elif type == 'event':  
            arr = arr.filter(event_name__icontains=query) 
            arr = arr.filter(event_id__icontains=query)[:20]
            p = [ {"name":k.event_name, "id":k.event_id, } for k in arr ]
        elif type == 'city':
            arr = arr.filter(district_name__icontains=query) 
            arr = arr.filter(title__icontains=query)[:20]
            p = [ {"name":k.district_name, "id":k.district_id, } for k in arr ]
        elif type == 'cat':
            arr = arr.filter(cat_name__icontains=query) 
            arr = arr.filter(cat_id__icontains=query)[:20]
            p = [ {"name":k.cat_name, "id":k.cat_id, } for k in arr ]
        
            
    except:
        p=[]
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
def Txt_data_list(request,query):
    try: 
        query= query.split(',')
        diss=SysSpotTxt.objects.filter(id__in=query).order_by('-txt_order').order_by('-id')
        p=[ {"name":"%s" % (dis) , "id":dis.id ,"txt":dis.txt,"tag":dis.tag,'img':[{'urls':imgs.urls,'name':imgs.name} for imgs in dis.txt_img.all()] } for dis in diss ]
 
    except:
        p=[]    
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def get_json_event_id(request, query):
    query= query.split(',')
    events=SysSpotEvent.objects.filter(event_id__in=query) 
     
    
    p = [ {"name":event.event_name, "id":event.event_id, } for event in events ]
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def img_data(request,query):
    try: 
        query= query.split(',')
        diss=SysSpotImg.objects.filter(id__in=query) 
        p=[ {"name":dis.name, "id":dis.id,"url":dis.urls   } for dis in diss ]
    except:
        p=[]   
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def get_json_img(request, query):
    photos = SysSpotImg.objects.order_by('-end_time').filter(Q(name__icontains=query) | Q(cat_name__name__contains=query) | Q(urls__icontains=query))[:20]
    p = [ {"name":photo.name, "id":photo.id,"urls":photo.urls } for photo in photos ]
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def get_json_code(request, query):
    codes = SysSpotHcode.objects.filter(Q(name__icontains=query) |Q(cat_name__name__icontains=query))[:20]
    #codes = codes.filter(cat_name__name__contains=query)[:20]
    p = [ {"name":code.name, "id":code.id,"code":code.hcode } for code in codes ]
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def get_json_txt(request, query):
    if query.isdigit():
        txts = SysSpotTxt.objects.filter(id=query)[:20]
    else:
        txts = SysSpotTxt.objects.filter(Q(tag__icontains=query) |Q(txt__icontains=query) |Q(name__icontains=query) |Q(cat_name__name__icontains=query))[:20]
    #txts = txts.filter(cat_name__name__icontains=query)[:20]
    p = [ {"name":txt.name, "id":txt.id,"txt":txt.txt } for txt in txts ]
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def get_json_event(request, query):
    
    events=SysSpotEvent.objects.order_by('-event_begin_time').filter( event_isshow=1)
    
    if query.isdigit():
        events = events.filter(event_id=query)[:20]
    else:
        events = events.filter(event_name__icontains=query) [:20]
    
    p = [ {"name":event.event_name, "id":event.event_id,"img":event.event_img } for event in events ]
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def get_json_city(request, query):
    citys = SysCity.objects.filter(Q(district_name__icontains=query)|Q(title__icontains=query)) [:20]
    #citys = citys.filter(title__icontains=query)[:20]
    p = [ {"name":city.district_name, "id":city.district_id, } for city in citys ]
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def get_json_cat(request, query):
    
    cats = SysCat.objects.filter(Q(cat_name__icontains=query)|Q(cat_id__icontains=query)) 
    cats = cats.exclude(cat_ename='')[:20]
    p = [ {"name":cat.cat_name, "id":cat.cat_id, } for cat in cats ]
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")