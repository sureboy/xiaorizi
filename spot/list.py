#coding:utf-8
from django.template import RequestContext
#from django.http import Http404 getCityObjFromTitle
from django.shortcuts import render_to_response
#from django.views.decorators.cache import cache_page

from django.views.decorators.csrf import csrf_exempt
 
from django.db.models import Q 
#import time,datetime
#from dateutil.relativedelta import relativedelta,MO,SU
from dahuodong.models import   PubEventCat
from models import SysSpotInfo  
from dahuodong.common import getCityObjFromTitle

from common import *

@csrf_exempt
def index(request,cat,offset):
    city = request.GET.get('city')
    #cat = request.GET.get('cat')
    date = request.GET.get('dat')
    #offset = request.GET.get('page')  
    if not cat: cat = 'all'
    if not date: date = 'latest'
    if not offset: offset = 1
    if not city: city=''   
 
    
    
    listDict = showList(request,city,cat,date,offset)
    return render_to_response('spot_list.html',listDict,context_instance=RequestContext(request))
    #return render_to_response('list.html',listDict,context_instance=RequestContext(request))

def get_spot_list(event,cat,city,date,page,offset,order):
    #args=Q(spot_isshow=1)
    args=SysSpotInfo.objects.filter(spot_isshow=True)
  
    if event:
        args = args.filter(Q(spot_event=event))
    
    if cat !='all':
        
        cat_id_li=spotcatUrl(True)
        tmp=[]
        try:
            if cat_id_li.has_key(cat):
                
                tmp.append(cat_id_li[cat]['id'])
                
            elif cat_id_li.has_key(int(cat)):
                cat=int(cat)
                tmp.append(cat_id_li[cat]['id'])
            
            for ch in cat_id_li[cat]:
                tmp.append(ch['id'])            
        except: 
            pass
        
        if len(tmp)>0:
            args = args.filter(spot_cat__in=tmp)
    
        
    #return render_to_response('base_error.html',{'error_msg':str(cat)})
    
    if city and  city != 0:  
        args =args.filter(Q(spot_city=city))
        #args = args&Q(spot_city=city)
        
       
        
     
    if not offset:
        #return SysSpotInfo.objects.filter(args).count()
        return args.distinct().count()
        
        
    else:
        #return SysSpotInfo.objects.filter(args).order_by(order)[page:offset]
        return args.order_by(order).distinct()[page:offset]
    
     
def showList(request,city, cat, date, offset):
    #translate city character to city digit
    #if city and  city != 'home' and  city != '':  
        
    cityObj = getCityObjFromTitle(city)
    if cityObj:
        cityId = cityObj[0]
        cityName = cityObj[1]
        cityPy = cityObj[2]
    else:
 
        cityId=False
        cityPy = request.COOKIES.get('city_py',False)
        cityName = request.COOKIES.get('city',False)
        if not cityPy:
            cityPy = 'beijing'
        city_info=False
        if not cityName:
            cityName=u'切换城市'
        
     
        
    #get sql query condition
    #date_url = getDateQueryCondition(date)
    #args = getCatQueryCondition(cat,args)
    
    #calculate slice page
    perpage=3
    offset = int(offset)
    cout = perpage*(offset-1)
    
    
    count =   get_spot_list(False,cat,cityId,date ,False,False,False)      
    
    
    pages = count/perpage
    if 0 != (count%perpage):
        pages = pages + 1
    
    #get date
    #[30:45]  offset:limit
    #return count = limit-offset
    orderStr = '-spot_end_time'
    catList = spotcatUrl()
        
    mlist =  get_spot_list(False,cat,cityId,date, cout,cout+perpage,orderStr)
        

    #id = ''
    
    #format data
    tmp = []
    
    for item in mlist:
        tmp.append(formatSpot(item))
    
    #list page: dat url,cat url,navigation url,slice page url
    #datList = constructDatUrl(city,cat,date)
    #constructCatUrl(city,cat,date)
    #catUrlLv1 = constructCatUrl(city,cat,date)
    
    navigationList =constructNavigationUrl (cat)
    firstPage,lastPage,prePage,nextPage,pageList = constructSliceUrl(city,cat,date,pages,offset)
    #liveList = constructLiveUrl(city)
    if cat == 'meeting':
        head =  {'title':u'会议报告,会议简报_活动家在现场',
              'keywords':u'会议现场回顾,会议纪要,现场图片,嘉宾精彩言论,参会者评论,网友评论,在现场',
              'description':u'会议报告（会议介绍,现场图片,嘉宾精彩言论,参会观众评论,网友评论）帮助参会和未能参会的您通过该场会议全面了解行业动态。',
              }
    elif cat == 'expo':
        head =  {'title':u'会展简报_展会简报_在现场_活动家',
              'keywords':u'展会介绍,展会现场回顾,展商介绍,同行点评,观众点评,网友点评,在现场,展会简报',
              'description':u'会展简报（展会现场回顾,展商介绍,同行点评,观众点评,网友点评,在现场,展会简报）帮助参展和未能参展的商家和消费者通过在现场及时掌握行业动态。',
              }
    else:
        if cat=='all' or  not cat:    
            head =  {'title':u'探讨业界问题,交流成功经验与观点-活动家在现场频道',
                      'keywords':u'会议简报,会展简报,现场回顾,现场图片,嘉宾精彩言论,网友评论',
                      'description':u'在现场频道为您提供会议、会展、公开课、讲座沙龙等优质活动的现场图片、嘉宾精彩言论,网友评论等舆情报告。帮助参加活动的和未参加活动的您全面了解该场活动和行业动态。'
                      }
        else:
       
            cats =getCats(cat)
 
            if cats:
                catName = cats['catname']
                title = u'%s,会议报告,舆情报告,活动家在现场'%catName
 
            else:
                catName = u'精彩活动'
                title = u'%s,会议报告,舆情报告,活动家在现场'%catName
            head =  {'title':title,
                      'keywords':u'%s,互联网大会,现场回顾,会议纪要,现场图片,嘉宾精彩言论,参会者评论,网友评论,在现场'%(catName) ,
                      'description':u'%s,在现场频道为您提供会议、会展、同城活动现场图片、嘉宾精彩言论,网友评论等舆情报告。帮助参加活动的和未参加活动的您全面了解该场活动和行业动态。'%(catName) 
                      }
    listDict = {'city':cityName,
                'city_py':cityPy,
                 'list':tmp,
                 #'datList':datList,
                 'catUrlLv1':catList,
                 'allcat':'/spot/',
                 'navigationList':navigationList,
                 #'liveList':liveList,
                 'liveParent':'#',
                 'firstPage':firstPage,
                 'lastPage':lastPage,
                 'prePage':prePage,
                 'nextPage':nextPage,
                 'countpage':pages,
                 'pageList':pageList,
                 'head':head,
                 'cat':cat,
                 
                               }
    return listDict
 
    
def consNavigationUrl(cat):
    
    cat=getCats(cat)
    
    return cat 

def findCatFid(cat,nav=[]):

    
    cat_id_li=spotcatUrl(True)
    cats={}
    navs=[]
    try:
        cats =cat_id_li[cat]
    except:
        cats =cat_id_li[int(cat)]
    f_cats={}    
    for v in cat_id_li.values():
        if v['id']==cats['fid']:
            f_cats=v
            break
    if  f_cats:
        navs.extend=findCatFid(f_cats,nav)
        
    
        
    
        
    
    
    
    
def getCats(cat):
    cat_id_li=spotcatUrl(True)
    cats={}
    try:
        cats =cat_id_li[cat]
    except:
        try:
            cats =cat_id_li[int(cat)]
        except:
            cats={}
        
    return cats;
    
   
'''

def constructNavigationUrl(city,catt):
    navigationList = []
    cat_list = PubEventCat.objects.filter(cat_ename__icontains=catt)
    
    for cat in cat_list:
        navigationDict = dict()
        navigationDict['catname'] = cat.cat_name
        navigationDict['caturl'] = '/spot/' + cat.cat_ename
        navigationList.append(navigationDict)
        if 0 == cat.cat_fid:
            break
        tmp_list = PubEventCat.objects.filter(cat_id = cat.cat_fid)
        for tmp in tmp_list:
            navigationDict = dict()
            navigationDict['catname'] = tmp.cat_name
            navigationDict['caturl'] = '/spot/' + tmp.cat_ename
            navigationList.append(navigationDict)
            break
        break
    navigationDict = dict()
    navigationDict['catname'] = u'首页'
    navigationDict['caturl'] = '/'
    navigationList.append(navigationDict)
    navigationList.reverse()
    return navigationList
'''

def constructSliceUrl(city,cat,date,amountPages,curpage):
    if curpage > amountPages:
        curpage =  amountPages
    if curpage <= 0 or False == curpage:
        curpage = 1
    pageList = []
    url = '/spot/'+cat 
    #construct section page
    startPage = 1
    endPage = amountPages
    if 3 <= curpage:
        startPage = curpage-2
    if 2 <= amountPages - curpage:
        endPage =  curpage+2
    
    for i in range(startPage,endPage+1):
        curPageFlg = 'false'
        if curpage == i:
            curPageFlg = 'true'
        pageDict = {'page':i, 'pageurl':url+'/'+str(i),'flag':curPageFlg}
        pageList.append(pageDict)
    #first last page
    firstPage = 'false'
    lastPage = 'false'
    if curpage != 1:
        firstPage = url+'/'+'1'
    if curpage != amountPages:
        lastPage = url+'/'+str(amountPages)
    #prepage nextpage
    prePage = 'false'
    nextPage = 'false'
    if 1 < curpage:
        prePage = url+'/'+str(curpage-1)
    if curpage < amountPages and 1 < amountPages:
        nextPage = url+'/'+str(curpage+1)
    return (firstPage,lastPage,prePage,nextPage,pageList)
 