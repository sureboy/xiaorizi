#coding:utf-8
from BeautifulSoup import BeautifulSoup
import  datetime
import HTMLParser
from django.core.cache import cache
from models import  SysSpotCatInfo 


def formatSpot(item):
    try:
        cat_id=item.spot_cat.order_by('cat_id')[0].cat_id
    except:
        cat_id=4
    
    try:
        img=item.spot_img.order_by('end_time')[0]
        if img:
            spot_img_url=img.urls.replace('pic1.qkan.com','pic.huodongjia.com')
        else:
            spot_img_url='http://pic.huodongjia.com/' + 'images/default%d.jpg' %cat_id;

    except:
        spot_img_url='http://pic.huodongjia.com/' + 'images/default%d.jpg' %cat_id;

    spot_id=item.id
    spot_txt = item.spot_txt 
    spot_hcode = item.spot_hcode  
    spot_img = item.spot_img  
    spot_event = item.spot_event  
    spot_name = item.spot_name
    spot_city=  item.spot_city 
    spot_addr = item.spot_addr
    spot_cat = item.spot_cat
    spot_begin_time =datetime.datetime.strftime(item.spot_begin_time,'%Y-%m-%d')
    spot_end_time =datetime.datetime.strftime(item.spot_end_time,'%Y-%m-%d')
    spot_isshow =item.spot_isshow
    spot_edit = item.spot_edit
    #spot_desc = item.spot_desc
    spot_desc =  BeautifulSoup(item.spot_desc).text[0:100]
    '''
    try:
        arr=[]
        spot_event=[]
        for event in item.spot_event.all():        
            arr.extend(event.event_cat_tag.split(','))
            #event['url']='/event-%s' % (event.event_id)
            #spot_event.append(event)       
            
        spot_tag = set(arr)
    except:
        spot_tag=[]
        #spot_event=[]
    '''
    return locals()
def find_cat_fid(cat_arr={},cat_str=''):
    navigationList=[]
    
    try:
        if cat_arr.has_key(cat_str):
            
            cat_k=cat_arr[cat_str]
            
        elif cat_arr.has_key(int(cat_str)):
            cat_k=cat_arr[int(cat_str)]
        else:
            cat_k=None
    except:
        cat_k=None
  
    if cat_k:
        navigationDict = dict()
        navigationDict['catname'] = cat_k['catname']
        navigationDict['caturl'] = '/spot/%s/'%(cat_str)
        navigationList.append(navigationDict)    
           
        for key,cat_a in cat_arr.items():        
            if cat_k['fid']==cat_a['id']:
                navigationList.extend(find_cat_fid(cat_arr ,key  ) ) 
                break
                 

    
    return navigationList
def constructNavigationUrl( catt):
 
    navigationList = []
    
    navigationList.extend(find_cat_fid(spotcatUrl(True),catt))
    
    navigationDict = dict()
    navigationDict['catname'] = '在现场'
    navigationDict['caturl'] = '/spot/'
    navigationList.append(navigationDict)
    navigationList.reverse()
    return navigationList

    
def getEventHead(spot,cat_info,city_info):
     
    #cat_info=spot.spot_cat.order_by('cat_id')[0]
    try:
        catId = cat_info.cat_id
        cat_name = cat_info.cat_name
    except:
        catId =7
        cat_name = ''
    #city_info=spot.spot_city.order_by('district_id')[0]
    des =  BeautifulSoup(spot.spot_desc).text[0:100]
 
    h = HTMLParser.HTMLParser()
    des = h.unescape(des)  
           
    try:        
        district_name=city_info.district_name        
    except:
        district_name=u'全国'
        
   
        
    if catId == 1:
        head = {'title':u'%s-ppt-讲义-活动家'% spot.spot_name,
                 'keywords':u'%s,会议门票,会议注册,会议报名,会议日程,会议资料,会议网'%spot.spot_name,
                 'description':u'%s-%s'% (spot.spot_name,des),
                 }
    elif catId == 2:
        head = {'title':u'%s-活动家'% spot.spot_name,
                 'keywords':u'%s,%s,订票,打折,%s%s'%(spot.spot_name,cat_name,district_name,cat_name),
                 'description':u'%s-%s'% (spot.spot_name,des),
                 }
    elif catId == 3:
        head = {'title':u'%s-活动家'% spot.spot_name,
                 'keywords':u'%s,%s,门票预订,特色旅游,%s%s'%(spot.spot_name,cat_name,district_name,cat_name),
                 'description':u'%s-%s'% (spot.spot_name,des),
                 }
    elif catId == 4:
        head = {'title':u'%s-活动家'% spot.spot_name,
                 'keywords':u'%s,公开课培训,培训报名,'%spot.spot_name,
                 'description':u'%s-%s'% (spot.spot_name,des),
                 }
    elif  catId == 5:
        head = {'title':u'%s-展商-会刊-活动家'% spot.spot_name,
                 'keywords':u'%s_参展_展位预订_会议网_%s会展_%s展览'%(spot.spot_name,district_name,spot.spot_name),
                 'description':u'%s-%s'% (spot.spot_name,des),
                 }
    elif catId == 6:
        head = {'title':u'%s-活动家'% spot.spot_name,
                 'keywords':u'%s_活动网_%s沙龙_讲座_画展_展览'%(spot.spot_name,district_name),
                 'description':u'%s-%s'% (spot.spot_name,des),
                 }
    else:
        head = {'title':u'%s-活动家'% spot.spot_name,
                 'keywords':u'%s_活动网_%s沙龙_讲座_画展_展览'%(spot.spot_name,district_name),
                 'description':u'%s-%s'% (spot.spot_name,des),
                 }
    return head

 
def spotcatUrl(type=False):
    f_cat = cache.get('cat_spot_map') 
    x_cat=cache.get('cat_spot_list') 
    if not f_cat or not x_cat:
        f_cat=[]
        x_cat={}
        id_cat={}
        catinfo = SysSpotCatInfo.objects.all() 
        catinfo.query.group_by = ['syscat_id']  
 
        cat_list=[]
 
        for val in catinfo:
            cat_x={}
            cat_x['catname']= val.syscat.cat_name
            if val.syscat.cat_ename: 
                cat_x['caturl']= '/spot/'+val.syscat.cat_ename  
            else:
                cat_x['caturl']= '/spot/'+str(val.syscat.cat_id)
            cat_x['fid']=val.syscat.cat_fid
            cat_x['id']=val.syscat.cat_id
            cat_x['ename']=val.syscat.cat_ename
            cat_x['child']= []
            cat_list.append(cat_x)
            id_cat[val.syscat.cat_id]=cat_x
            #cat_id_li[val.syscat.cat_id]=cat_x
            
        #cat_list=get_cat_map(cat_list)

        #catinfo1 = catinfo[:]
        for cat in cat_list:
            if id_cat.has_key(cat['fid']):
                id_cat[cat['fid']]['child'].append(cat)
            else:
                f_cat.append(id_cat[cat['id']])
                
                #catinfo.remove(cat)
            if cat['ename']:
                x_cat[cat['ename']]=id_cat[cat['id']]
            else:
                x_cat[cat['id']]=id_cat[cat['id']]
        
        cache.set('cat_spot_map',f_cat,86400)
        cache.set('cat_spot_list',x_cat,86400)

        
    
    if type:
        return x_cat
    else:         
        return f_cat


