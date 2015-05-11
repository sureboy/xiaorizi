#coding:utf-8
#from mptt.models import MPTTModel
from new_event.models import NewDistrict,NewEventCat,NewEventTag,NewVenue,NewEventParagraph,NewEventImg,\
                            NewEventFrom,NewEventTable,NewEventParagraphTag
from django.http import HttpResponse
from django.utils import simplejson as json
from django.db import models
from django.db import connection
import operator
import re
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt 

def show_city_json(request,offset = None,page = 1):

    
    try: 
        if offset:
            count = NewDistrict.objects.count()
            offset=int(offset)
            page=int(page)
            if count%offset:
                page_number = count/offset+1
            else:
                page_number = count/offset 
            diss=NewDistrict.objects.all()[offset*(page-1):offset*page]
        else:
            diss=NewDistrict.objects.all()
        p=[ {"name":dis.district_name, "id":dis.id  } for dis in diss ]
    except:
        p=[]    
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")    

def show_from_json(request,offset = 15,page = 1):
   
    try: 
        if offset:
            count = NewEventFrom.objects.count()
            offset=int(offset)
            page=int(page)
            if count%offset:
                page_number = count/offset+1
            else:
                page_number = count/offset 
            diss=NewEventFrom.objects.all()[offset*(page-1):offset*page]
        else:
            diss=NewEventFrom.objects.all()[:20]
        p=[ {"id":dis.id,"f_Class":dis.f_Class.name,"Website":dis.Website,"email":dis.email,"tel":dis.tel,"content":dis.content,"type":dis.type,"edit":dis.edit } for dis in diss ]
    except:
        p=[]    
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")  
 
def show_img_json(request,offset = 15,page = 1):
   
    try: 
        if offset:
            count = NewEventImg.objects.count()
            offset=int(offset)
            page=int(page)
            if count%offset:
                page_number = count/offset+1
            else:
                page_number = count/offset 
            diss=NewEventImg.objects.all().order_by('-order')[offset*(page-1):offset*page]
        else:
            diss=NewEventImg.objects.all().order_by('-order')[:20]
        p=[ {"id":dis.id,"name":dis.name,"url":dis.url,"order":dis.order } for dis in diss ]
    except:
        p=[]    
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")  
  
        