#coding:utf-8
from django.template import RequestContext
#from django.http import Http404
from django.shortcuts import render_to_response
#from django.views.decorators.cache import cache_page
#from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from BeautifulSoup import BeautifulSoup

import  datetime
from common import getEventHead
from models import SysSpotInfo

#@cache_page(60 * 15)
@csrf_exempt
def index(request,spotId=False):
    if spotId:
        spotId= int(spotId)
        try:
            spot = SysSpotInfo.objects.get(id=spotId)       
        except:
            return render_to_response('base_error.html',{'error_msg': spotId}) 
        
        
        try:
            img=spot.spot_img.order_by('end_time')[0]
            spot_img_url=img.urls
        except:        
            spot_img_url='';
        
 
        try:
            city_info=spot.spot_city.order_by('district_id')[0]
            district_name=city_info.district_name
            title=city_info.title
        except:
             
            title = request.COOKIES.get('city_py',False)
            district_name = request.COOKIES.get('city',False)
            if not title:
                title = 'beijing'
            city_info=False
            if not district_name:
                district_name='切换城市'
            
        nav={}  
        nav_arr=[]
        nav_name=()
        
        desc=u'在现场'
           
          
        #nav[desc]=[{'txt':spot.spot_desc}]        
        #nav_arr.append(nav[desc])
        try:          
            for tab in spot.spot_txt.all():
                if not tab.cat_name :
                    if not nav.has_key(desc) : 
                        nav[desc]=[]
                        nav_name = nav_name+(desc,)
                        nav_arr.append(nav[desc])
                    nav[desc].append(tab)
                else:   
                
                    if not nav.has_key(tab.cat_name) :                                       
                        nav[tab.cat_name]=[]  
                        nav_name= nav_name+  (tab.cat_name , ) 
                        nav_arr.append(nav[tab.cat_name])
                                     
                    nav[tab.cat_name].append(tab)  
        except:     
            nav={}    
        #nav['现场报告']=[{'txt':spot.spot_desc}]     
        spot.spot_desc =  BeautifulSoup(spot.spot_desc).text[0:100]
        
        spot.spot_begin_time =datetime.datetime.strftime(spot.spot_begin_time,'%Y-%m-%d')
        spot.spot_end_time =datetime.datetime.strftime(spot.spot_end_time,'%Y-%m-%d')    
          
      
            
            
        try:
            cat_info=spot.spot_cat.order_by('-cat_id')[0]
            if cat_info.cat_ename:
                cat_t=cat_info.cat_ename
            else:
                cat_t=cat_info.cat_id 
        except:
            cat_info=[]  
            cat_t=None         
        
        head = getEventHead(spot,cat_info,city_info)
        from  common import constructNavigationUrl
        
        navigationList = constructNavigationUrl(cat_t)
        navigationList.append({'catname':spot.spot_name,
                               'caturl':'spot-%s.html'%spotId})
        
        #spot = formatSpot(spot)  
        #print title
        #print district_name
        return render_to_response('show_spot.html',{'head':head,
                                                    'spot':spot,
                                                    'city':district_name,
                                                    'city_py':title,
                                                    'spot_img_url':spot_img_url,
                                                    'spot_tab_arr':nav_arr,
                                                    'nav_name':nav_name,
                                                    'navigationList':navigationList
                                                    },context_instance=RequestContext(request))
        
    else:
        #return homePage(request)
        return False
 
    
        