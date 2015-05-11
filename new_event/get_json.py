#coding:utf-8
from django.utils import simplejson as json
import urllib2
from django.core.cache import cache



def get_get_str_singers_json(new=False):
    
    locApiUrl = 'http://admin5.huodongjia.com/api/get_str_singers_json/'   
    if new:
        locApiUrl += '%s/' % new   
    
    #print locApiUrl
    try:
        rp = urllib2.urlopen(locApiUrl).read()
        
        jsondic = json.loads(rp)
        return jsondic
    except:
        return []  
    
def get_get_str_event_json(new=False):
    
    locApiUrl = 'http://admin5.huodongjia.com/api/get_str_event_json/'   
    if new:
        locApiUrl += '%s/' % new   
    
    #print locApiUrl
    try:
        rp = urllib2.urlopen(locApiUrl).read()
        
        jsondic = json.loads(rp)
        return jsondic
    except:
        return {}  

def get_get_site_links_json(new=False):
    
    locApiUrl = 'http://admin5.huodongjia.com/api/get_site_links_json/'   
    if new:
        locApiUrl += '%s/' % new   
    
    #print locApiUrl
    try:
        rp = urllib2.urlopen(locApiUrl).read()
        
        jsondic = json.loads(rp)
        return jsondic
    except:
        return []    

def get_NewCatUrl_json(type=0,city='',new=False):
    if not type:
        type='0'
    if not city:
        city='0'
 
 
    
            
    locApiUrl = 'http://admin5.huodongjia.com/api/newcaturl_json/%s/%s/%s/' % (type,city,new)
    if new:
        locApiUrl += '%s/' % new    
    #print locApiUrl
    try:
        rp = urllib2.urlopen(locApiUrl).read()
        
        jsondic = json.loads(rp)
        
          
 
 
        return jsondic
    except:
        return {}



def get_NewCity_json(type=0,new=False):        
    locApiUrl = 'http://admin5.huodongjia.com/api/newcity_json/%s/' % type   
    if new:
        locApiUrl += '%s/' % new   
    
    #print locApiUrl
    try:
        rp = urllib2.urlopen(locApiUrl).read()
        
        jsondic = json.loads(rp)
        
          
 
 
        return jsondic
    except:
        return {}
 
    
def get_NewformatEvent_json(eventid=False,new=False):        
    locApiUrl = 'http://admin5.huodongjia.com/api/newformatevent_json/%s/' % eventid   
    if new:
        locApiUrl += '%s/' % new   
    
    try:
        rp = urllib2.urlopen(locApiUrl).read()
        #print rp
        jsondic = json.loads(rp)
        cache.set('event_%s' % eventid,jsondic,86400)
        #print jsondic
        return jsondic
    except:
        return {}
 
   
    
def get_get_event_list_json(cat=False,city=False,date=False,page=False,offset=False,order=False,new=False ):        
    if not cat:
        cat='0'
    if not city:
        city='0'
         
    elif type(city) in [tuple,list] :
        str=''
        for ci in city:
            if str:
                str+='_'
            str+='%s'% ci
            
        
        city=str
     
    if not date:
        date='0'
    if not page:
        page='0'
    if not offset:
        offset='0'
    if not order:
        order='0'
    
        
    
    locApiUrl = 'http://admin5.huodongjia.com/api/get_event_list_json/%s/%s/%s/%s/%s/%s/' % (cat,city,date,page,offset,order )
    if new:
        locApiUrl += '%s/' % new   
    
    print locApiUrl.encode("utf8")
    try:
        rp = urllib2.urlopen(locApiUrl.encode("utf8")).read()
         
        jsondic = json.loads(rp)
        
        
       
 
        return jsondic
    except Exception,e:
 
        return []
    
def get_event_city_cat(city_id=None,cat_id=None, new=False,cou=False):
    city=city_id
    city_s=city_id
    if  type(city_id) == tuple :
        
        city_s='_'.join(tuple(map(str, city_id)))
        
        city=str(city_id).replace('(','').replace( ',' ,'').replace(')' ,'').replace(' ' ,'')  
        #city_s=str(city_id).replace('(','').replace(')' ,'').replace(' ' ,'').replace( ',' ,'_')
    cats=cat_id
    cat_s=cat_id
    if  type(cat_id) == tuple :
        cats= str(cat_id).replace('(','').replace( ',' ,'').replace(')' ,'').replace(' ' ,'')  
        cat_s='_'.join(tuple(map(str, cat_id)))
        #cat_s= str(cat_id).replace('(','').replace(')' ,'').replace(' ' ,'').replace( ',' ,'_')  
    if not city_s:
        city_s='0'
    if not cat_s:
        cat_s='0'
        
    if not new:
        new='0'  
    if not cou:
        cou1='0'  
    else:
        cou1=cou    
        
        
    locApiUrl = 'http://admin5.huodongjia.com/api/event_city_cat_json/%s/%s/%s/%s/' % (city_s,cat_s,new,cou1)
    #print locApiUrl
    
    
    try:
        rp = urllib2.urlopen(locApiUrl).read()
        jsondic = json.loads(rp)
        
        
        if cou:
            if not jsondic:
                jsondic=0
            else:
                cache.set('event_%s_%s_con' % (city,cats),jsondic ,86400)
        else:
            if not jsondic:
                jsondic=[]
            else:
                
                cache.set('event_%s_%s' % (city,cats),jsondic ,86400)
                

 
        return jsondic
    except:
        return []


    
    
    
    