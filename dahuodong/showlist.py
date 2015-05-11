#coding:utf-8
#
#list.html
#
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from dahuodong.models import SysCommonDistrict,SysEvent,SysEventCat,PubEventCat,SysOrder
from common import formatEvent,getListHead
from django.db.models import Q
import time
import logging
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from forms import orderForm
from django.db import connection
from dateutil.relativedelta import relativedelta,MO,SU
import datetime
from common import *

def constructDatUrl(city,cat,date):
    datList = []
    ddc = ['本周','下周','下月','最新']
    dde = ['thisweek','nextweek','nextmonth','new']
    for i in range(0,len(dde)):
        url = '/'+city
        url = url + '/'+cat+'/'
        datDict = dict()
        datDict['daturl'] = url + '?dat='+dde[i]
        datDict['datname'] = ddc[i]
        datDict['flag'] = 'false'
        if date == dde[i]:
            datDict['flag'] = 'true'
        datList.append(datDict)
    return datList

def constructSliceUrl(city,cat,date,amountPages,curpage):
    if curpage > amountPages:
        curpage =  amountPages
    if curpage <= 0 or False == curpage:
        curpage = 1
    pageList = []
    url = '/'+city+'/'+cat+'/?'+'dat='+date
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
        pageDict = {'page':i, 'pageurl':url+'&page='+str(i),'flag':curPageFlg}
        pageList.append(pageDict)
    #first last page
    firstPage = 'false'
    lastPage = 'false'
    if curpage != 1:
        firstPage = url+'&page='+'1'
    if curpage != amountPages:
        lastPage = url+'&page='+str(amountPages)
    #prepage nextpage
    prePage = 'false'
    nextPage = 'false'
    if 1 < curpage:
        prePage = url+'&page='+str(curpage-1)
    if curpage < amountPages and 1 < amountPages:
        nextPage = url+'&page='+str(curpage+1)
    return (firstPage,lastPage,prePage,nextPage,pageList)


def constructLiveUrl(city):
    liveList = []
    liveDict = {'livename':'测试','liveurl':'#','flg':'true'}
    liveList.append(liveDict)
    return liveList

#sql date query condition
def getDateQueryCondition(date):
    if not date:
        return ()
    now = datetime.datetime.now()
    today = datetime.date.today()
    startTime = 0
    endTime = 0
    if 'thisweek' == date:
        #this week monday
        startTime = today+relativedelta(weekday=MO(-1))
        #next week monday
        endTime = today+relativedelta(days=+1,weekday=MO)
        #this week SUNDAY
        #endTime = today+relativedelta(weekday=SU(+1))
    elif 'nextweek' == date:
        #next week monday
        startTime = today+relativedelta(days=+1,weekday=MO)
        #after next week monday
        endTime = startTime+relativedelta(days=+1,weekday=MO)
        #next week SUNDAY
        #endTime = today+relativedelta(days=+7,weekday=SU)
    elif 'nextmonth' == date:
        thisMonthStart = now.strftime('%Y-%m-1')
        tmp = thisMonthStart.split('-')
        thisMonthStart = datetime.datetime(int(tmp[0]), int(tmp[1]),int(tmp[2]))
        startTime = thisMonthStart+relativedelta(months=+1)
        endTime = thisMonthStart+relativedelta(months=+2)
    else:
        return ()
    startTime = time.mktime(startTime.timetuple())
    endTime = time.mktime(endTime.timetuple())
    #args = (Q(event_begin_time__gte=startTime)&Q(event_begin_time__lte=endTime))|\
    #(Q(event_end_time__gte=startTime)&Q(event_end_time__lte=endTime))#|\
    #(Q(event_begin_time__lt=startTime)&Q(event_end_time__lt=endTime))
    args = (Q(event_begin_time__lte=startTime)&Q(event_end_time__gte=endTime))|\
    (Q(event_begin_time__gte=startTime)&Q(event_begin_time__lte=endTime))|\
    (Q(event_end_time__gte=startTime)&Q(event_end_time__lte=endTime))
    return args

#sql cat query condition
def getCatQueryCondition(cat, args):
    if not cat:
        return args
    try:
        if 'business' == cat:
            catArgs = Q(event_cat1__in=[1,4,5])
        elif 'fun' == cat:
            catArgs = Q(event_cat1__in=[2,6])
        elif 'all' == cat:
            return args
        else:
            catArgs = ()
            catObj = getCatObjByEName(cat)
            if catObj:
                catId = catObj[2]
                fid = catObj[3]
            else:
                cat_list = SysEventCat.objects.filter(cat_ename=cat)[0]
                catId = cat_list.cat_id
                fid = cat_list.cat_fid
            if 0 == fid:
                catArgs = Q(event_cat1=catId)
            else:
                catArgs = Q(event_cat=catId)
    except Exception,e:
        pass
    
    if not args:
        args = catArgs
    else:
        args = (args)&catArgs
    return  args


def showList(city, cat, date, offset):
    #translate city character to city digit
    cityObj = getCityObjFromTitle(city)
    if cityObj:
        cityId = cityObj[0]
        cityName = cityObj[1]
        cityPy = cityObj[2]
    else:
        district_list = SysCommonDistrict.objects.filter(title=city,level=2)
        if 0 == district_list.count():
            return render_to_response('base_error.html',{'errorMsg':'Error CityId!' })
        cityId = district_list[0].district_id
        cityName = district_list[0].district_name
        cityPy = district_list[0].title
    
    #get sql query condition
    args = getDateQueryCondition(date)
    args = getCatQueryCondition(cat,args)
    #calculate slice page
    perpage=10
    offset = int(offset)
    cout = perpage*(offset-1)

    if 0 == len(args):
        count = SysEvent.objects.filter(Q(event_isshow=1)|Q(event_isshow=8),district_id=cityId).exclude(event_time_expire=2).count()
    else:
        count = SysEvent.objects.filter(Q(event_isshow=1)|Q(event_isshow=8),args,district_id=cityId).exclude(event_time_expire=2).count()
    #print connection.queries
    pages = count/perpage
    if 0 != (count%perpage):
        pages = pages + 1
    
    #get date
    #[30:45]  offset:limit
    #return count = limit-offset
    orderStr = 'event_end_time'
    if 'new' == date:
        orderStr = '-crawl_time'
    if 0 == len(args):
        mlist = SysEvent.objects.filter(Q(event_isshow=1)|Q(event_isshow=8),district_id=cityId).exclude(event_time_expire=2).order_by("-event_recomend",orderStr)[cout:cout+perpage]
    else:
        mlist = SysEvent.objects.filter(Q(event_isshow=1)|Q(event_isshow=8),args,district_id=cityId,).exclude(event_time_expire=2).order_by("-event_recomend",orderStr)[cout:cout+perpage]
    #print connection.queries
    id = ''
    
    #format data
    tmp = []
    for item in mlist:
        tmp.append(formatEvent(item))
    
    #list page: dat url,cat url,navigation url,slice page url
    datList = constructDatUrl(city,cat,date)
    catUrlLv1 = constructCatUrl(city,cat,date)
    navigationList = constructNavigationUrl(city,cat)
    firstPage,lastPage,prePage,nextPage,pageList = constructSliceUrl(city,cat,date,pages,offset)
    
    head = getListHead(cityName,cat,date)
    
    listDict = {'city':cityName,
                'city_py':cityPy,
                 'list':tmp,
                 'datList':datList,
                 'catUrlLv1':catUrlLv1,
                 'allcat':'/'+city+'/all/',
                 'navigationList':navigationList,
                 'firstPage':firstPage,
                 'lastPage':lastPage,
                 'prePage':prePage,
                 'nextPage':nextPage,
                 'countpage':pages,
                 'pageList':pageList,
                 'head':head,
                               }
    return listDict

