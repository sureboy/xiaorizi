#coding:utf-8
from django.template import RequestContext
from django.http import Http404,HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from dahuodong.models import SysCommonDistrict,SysEvent,SysOrder,SysOrderMessage,Crowfunding,CustomPublishEvent,SysSearchKey,SubscribeInfo
from common import *
from django.db.models import Q
import time,datetime
from django.views.decorators.cache import cache_page
from forms import orderForm
from random import randint
from operator import itemgetter
#from django.db import connection
import showlist
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.cache import cache
import random
import  hashlib,cStringIO
import json
from admin_self.common import NewformatEvent
from django.core.urlresolvers import reverse
from admin_self.common import NewCatUrl

cat_lis = ['',u'会议',u'演出',u'旅行',u'公开课',u'会展',u'同城活动']

#@cache_page(60 * 5)
def homePage(request,city_title=False):
    cityId = 45052
    city_name = u'北京'
    title = 'beijing'
    cityObj = None
    if not city_title:#get city obj by ip
        title = request.COOKIES.get('city_py',False)
        city_name = request.COOKIES.get('city',False)
        cityId = request.COOKIES.get('city_id',False)
        if not title or not city_name or not cityId: 
            city_code = getCityNameByIp(request)
            if city_code:
                cityObj = getCityObjFromBaiDuCode(city_code)
                if not cityObj:
                    cityId = 45052
                    city_name = u'北京'
                    title = 'beijing' 
            else:
                cityId = 45052
                city_name = u'北京'
                title = 'beijing'              
        else:
            city_name = city_name.decode('utf-8')
    else:#get city obj by title
        cityObj =  getCityObjFromTitle(city_title)
    if cityObj:
        cityId = cityObj[0]
        city_name = cityObj[1]
        title = cityObj[2]
        
    special_dic_list  = []
    business_dic_list = []
    homec = None
    cc = cache.get(title[0])
    if cc:
        homec = cc.get(title)
        if homec:
            special_dic_list = homec.get('special_dic_list')
            business_dic_list = homec.get('business_dic_list')
    else:
        pass
    if not homec:
        special_list = SysEvent.objects.filter(Q(event_isshow=1)|Q(event_isshow=8),district_id = cityId,event_cat1 = 3).exclude(event_time_expire = 2).order_by('-event_recomend')[0:8]
        if not special_list:
            special_list = SysEvent.objects.filter(Q(event_isshow=1)|Q(event_isshow=8),Q(event_cat1 = 2)|Q(event_cat1 = 6),district_id = cityId).exclude(event_time_expire = 2).order_by('-event_recomend','event_begin_time')[0:8]
        else:
            length = len(special_list)
            if length<8:
                special_list = SysEvent.objects.filter(Q(event_isshow=1)|Q(event_isshow=8),Q(event_cat1 = 2)|Q(event_cat1 = 6)|Q(event_cat1=3),district_id = cityId).exclude(event_time_expire = 2).order_by('-event_recomend','event_begin_time')[0:8]
        business_list = SysEvent.objects.filter(Q(event_isshow=1)|Q(event_isshow=8),Q(event_cat1=1),district_id = cityId).exclude(event_time_expire = 2).order_by('-event_recomend','event_begin_time')[0:8]
        if not business_list:
            business_list = SysEvent.objects.filter(Q(event_isshow=1)|Q(event_isshow=8),event_cat1 = 4,district_id = cityId).exclude(event_time_expire = 2).order_by('-event_recomend','event_begin_time')[0:8]
        else:
            length = len(business_list)
            if length<8:
                business_list = SysEvent.objects.filter(Q(event_isshow=1)|Q(event_isshow=8),Q(event_cat1=1)|Q(event_cat1=5)|Q(event_cat1 = 4),district_id = cityId).exclude(event_time_expire = 2).order_by('-event_recomend','event_begin_time')[0:8]
        
        special_dic_list = [formatEvent(item) for item in special_list]
        business_dic_list = [formatEvent(item) for item in business_list]

    if not city_title:
        head = {'title':u'活动家-亚洲最大的活动聚合平台-全面、安全、快捷、方便_认准活动家官方网站',
              'keywords':u'活动家,网上订票,会议网,活动网,商务会议,活动',
             'description':u'活动家网为您提供海量会议,公开课,会展,极限运动,当地体验,夜生活,演出折扣票,同城活动查询,特色旅游，门票预订,报名,参加活动,每日发布最新活动，发布活动请上活动家！服务热线:400-003-3879'}
    else:
        head = {'title':u'【活动家-HuoDongJia.com】%s站,在线订票平台,活动发布平台,方便,快捷,安全'%city_name,
              'keywords':u'活动家,网上订票,会议网,活动网,商务会议,%s活动'%(city_name),
             'description':u'活动家网为您提供%s地区海量会议,公开课,会展,极限运动,当地体验,夜生活,演出折扣票,同城活动查询,特色旅游，门票预订,报名,参加活动,每日发布最新活动，发布活动请上活动家！服务热线:400-003-3879'%city_name}
    response = render_to_response('home.html',{'city':city_name,
                                           'city_id':cityId,
                                           'city_py':title,
                                           #'list':transport,
                                           'special_list':special_dic_list,
                                           'business_list':business_dic_list,
                                           'head':head,
                                           'background_img':'../images/head_background/header_background.png'},
                                           context_instance=RequestContext(request))
    response.set_cookie('city_id',cityId)
    response.set_cookie('city_py',title)
    response.set_cookie('city',city_name.encode('utf-8'))
    response['Cache-Control'] = 'max-age=300'
    return response

#@cache_page(60*5)
@csrf_exempt
def showEventById(request,eventId=False,template_name='show_event.html'):
    if eventId:
        eventId= int(eventId)
        try:
            event = SysEvent.objects.get(Q(event_isshow=1)|Q(event_isshow=8),event_id=eventId)
        except:
            return render_to_response('base_error.html',{'error_msg':u'没有该活动'})
        event = formatEvent(event,detail = True)
        #catEName = getCatENamefromID(event['event_cat'])
        navigationList = constructNavigationUrl(event['district_title'],event['cat_ename'].encode('utf8'))
        navigationList.append({'catname':event['event_name'],
                               'caturl':'event-%s'%eventId})
        head = getEventHead(event)
        #print event['event_id']
        console_success = False
        if saveConsult(request,event['event_id'],event['event_name']) == True:
            console_success = True
            
        suggestion_success = False
        if saveSuggestion(request,event['event_id'],event['event_name']) == True:
            suggestion_success = True
        
        if cache.has_key('rec_with_cat_%s'%event['event_cat']):
            recommend_list = cache.get('rec_with_cat_%s'%event['event_cat'])
        else:
            recommend_list = SysEvent.objects.filter(Q(event_isshow=1)|Q(event_isshow=8),event_cat=event['event_cat']).exclude(event_id = event['event_id']).exclude(event_time_expire = 2).order_by('event_begin_time')
        randloc = randint(0,len(recommend_list)/2)
        number = 6
        if event['event_cat1'] in [2,3,6]:
            number = 4
        tran_rec_list = [formatEvent(item) for item in recommend_list[randloc:randloc+number]]
        if event['event_price_model'] != 3:
            return render_to_response(template_name,{'head':head,
                                                         'event':event,
                                                         'user_viewed_events':tran_rec_list,
                                                         'city':event['district_name'],
                                                         'console_success':console_success,
                                                         'suggestion_success':suggestion_success,
                                                         'city_py':event['district_title'],
                                                         'navigationList':navigationList},
                                      context_instance=RequestContext(request))
        else:
            try:
                cf = Crowfunding.objects.get(event_id = event['event_id'])
            except:
                return render_to_response('base_error.html',{'error_msg':'id error!'})
            return render_to_response(template_name,{'head':head,
                                                         'event':event,
                                                         'user_viewed_events':tran_rec_list,
                                                         'city':event['district_name'],
                                                         'console_success':console_success,
                                                         'cf':cf,
                                                         'city_py':event['district_title'],
                                                         'navigationList':navigationList},
                                      context_instance=RequestContext(request))
    else:
        return homePage(request)

#@cache_page(60 * 5)
def searchKeyword(request,offset = 15,page = 1,isTag=False):
    #mc = memcache.Client(['127.0.0.1:11211'])

    title = request.COOKIES.get('city_py', '')
    city_name = request.COOKIES.get('city', '')
    cityObj =  getCityObjFromTitle(title)
    district_id = 45052
    if cityObj:
        district_id = cityObj[0]
    if offset < 1 or page < 1:
        return render_to_response('base_error.html',{'error_msg':u'页码错误'},context_instance=RequestContext(request))
    offset = int(offset)
    page = int(page)
    error = u'你什么都没有输入'
    if request.GET.get('keyword',''):
        keyword = request.GET['keyword']
        #keyword = keyword.encode('utf8')
        #print keyword.encode('utf8')


        ##########################################
        ##if tag in tags of categories of <business>
        #### jump to new business list page
        ##########################################
        bs = NewCatUrl()['business']
        for c1 in bs['child']:
            cat = c1['ename']
            if cat in ['expo', 'meeting', 'training']:
                continue
            for tag in c1['tag']:
                if 'name' in tag and keyword in tag['name']:
                    return HttpResponseRedirect("/{cat}/?tag={tag}".format(cat=cat, \
                            tag=keyword.encode('utf-8')))
        ############################

        if keyword:
            if page == 1 and not isTag:
                        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                            ip =  request.META['HTTP_X_FORWARDED_FOR']
                        else:
                            ip = request.META['REMOTE_ADDR']
                        SysSearchKey.objects.create(keyword = keyword,
                                                    ip = ip,
                                                    search_time = time.time()
                                                    )
            if len(keyword) > 20:
                error = u'关键词的字数不能超过20'
            else:
                #events_lis = mc.get(keyword+'_search_lis')
                keyword= keyword.replace('/',' ')
                events_lis = cache.get('_'.join(keyword.split())+'_search_lis')
                if not events_lis:
                    ids = search(keyword)
                    if ids:
                        events_lis = SysEvent.objects.filter(event_id__in = ids)#.order_by('district_id='+str(district_id),'event_begin_time')
                        cache.set('_'.join(keyword.split())+'_search_lis',events_lis,300)
                if events_lis:
                    events_lis = events_lis.extra(select={'is_top':'district_id='+str(district_id)})
                    events_lis = events_lis.extra(order_by=['-is_top'])
                    #print connection.queries
                    count = events_lis.count()
                    if count%offset:
                        page_number = count/offset+1
                    else:
                        page_number = count/offset
                    rlist = [NewformatEvent(False,item.event_id) for item in events_lis[offset*(page-1):offset*page]]
                    if not isTag:
                        url = '/search/'+str(offset)+'/page/?keyword='+keyword
                    else:
                        url = '/tag/'+str(offset)+'/page/?keyword='+keyword
                    #print page_number
                    pageList = []
                    for i in range(1,page_number+1):
                        curPageFlg = False
                        if page == i:
                            curPageFlg = True
                        pageDict = {'page':i, 'pageurl':url.replace('page',str(i)),'flag':curPageFlg}
                        pageList.append(pageDict)
                        
                    if page <= 1:
                        firstPage = False
                        prePage = False
                    else:
                        firstPage = pageList[0]
                        prePage = pageList[page-2]
                        
                    if page >= page_number:
                        lastPage = False
                        nextPage = False
                    else:
                        lastPage = pageList[page_number-1]
                        nextPage = pageList[page]
                    #print pageList
                    
                    head = {'title':u'%s相关热门会议查询与报名_活动家'%(keyword),
              'keywords':u'%s相关会议,%s学术会议,%s工作会议' % \
                      (keyword, keyword, keyword),
             'description':u'找%s方面相关会议信息，就上【活动家www.huodongjia.com】。活动家为您提供全面及时的%s方面的会议、峰会、论坛、年会介绍和查询报名服务，是上万主办方推崇的%s方面会议网站。学习提升，积累人脉，精准标签，个性定制，活动家服务热线:400-003-3879。' % (keyword, keyword, keyword)}
                    return render_to_response('search_results.html',{'list':rlist,
                                                                     'city':city_name,
                                                                     'city_py':title,
                                                                     'keyword':keyword,
                                                                     'firstPage':firstPage,
                                                                     'prePage':prePage,
                                                                     'currentPage':page,
                                                                     'nextPage':nextPage,
                                                                     'lastPage':lastPage,
                                                                     'pageList':pageList,
                                                                     'head':head})
                else:
                    error = u'没能搜索到与"%s"相关的活动，你可以尝试其他搜索'%keyword
                    
                    clist = []
                    for i in [20,21,22,23,89,90]:
                        cl = cache.get('rec_with_cat_%s'%i)
                        if cl:
                            for j in cl:
                                if not random.randint(0,8):
                                    clist.append(j)
                    rlist = [formatEvent(item) for item in clist]
                    
                    if clist:
                        message = u'你可能感兴趣的活动'
                    else:
                        message = ''
                    return render_to_response('search_results.html',{'error_msg':error,'message':message,'city':city_name,'city_py':title,'list':rlist},context_instance=RequestContext(request))

        else:
            error = u'输入不能为空'

    
    return render_to_response('search_results.html',{'error_msg':error,'city':city_name,'city_py':title},context_instance=RequestContext(request))

#@cache_page(60 * 5)
def searchOrder(request):
    city_py = request.COOKIES.get('city_py','')
    city = request.COOKIES.get('city','')
    error = u'请输入手机号或者订单号查询订单'
    if request.GET.get('order_search',''):
        order_search = request.GET['order_search']
        if order_search.isdigit():
            order_list = SysOrder.objects.filter(Q(order_number = order_search.strip())|Q(order_tel = order_search.strip()))
            if order_list:
                for item in order_list:
                    item.order_addtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item.order_addtime))
                    if item.order_paytime:
                        item.order_paytime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item.order_paytime))
                    else:
                        item.order_paytime = ''
                return render_to_response('search_order.html',{'order_list':order_list,'city':city_name,'city_py':title},context_instance=RequestContext(request))
            else:
                error = u'没有找到订单,请确认电话号码和订单号是否正确'
        else:
            error = u'订单号由纯数字组成！'
    head = {'title':u'订单查询_活动网_活动家',
              'keywords':u'订单查询',
             'description':u'订单查询页面,活动家（huodongjia.com）'}
    return render_to_response('search_order.html',{'head':head,'city':city_name,'city_py':title,'error_msg':error },context_instance=RequestContext(request))

@cache_page(60 * 5)
def changeCity(request):
    #cds = SysCommonDistrict.objects.filter(level = 2).exclude(capital_letter = '')
    #res = {}
    #for item in cds:
    #    key = item.capital_letter.strip()
    #    if res.has_key(key):
    #        res[key].append((item.district_name,'/%s/'%item.title))
    #    else:
    #        res[key] = [(item.district_name,'/%s/'%item.title)]
    #res = sorted(res.iteritems(),key=itemgetter(0),reverse=False)*/
    city_py = request.COOKIES.get('city_py','')
    city = request.COOKIES.get('city','')
    head = {'title':u'切换城市',
              'keywords':u'切换城市,城市分站',
             'description':u'切换城市页面,活动家（huodongjia.com）'}
    
    return render_to_response('city_map.html',{'head':head,'city':city_name,'city_py':title,})


@csrf_exempt
def writeOrder(request,event_id):
    #title = request.COOKIES.get('city_py',False)
    #city_name = request.COOKIES.get('city',False)
    if request.method == 'POST':
        eventId= int(event_id)
        event = formatEvent(SysEvent.objects.get(event_id=eventId))
        info = request.POST
        if info.get('price',False) and info.get('cheapMoney',False) and info.get('ticketNum',False):
            currencyDic = {"RMB":1,"HKD":1.24,"TWD":4.84,"USD":0.16,"EUR":0.12,"GBP":0.095,"JPY":16.33,"THB":5.23,"KER":164.46,"SGD":0.2,"VND":3388.90,"MYR":0.52}
            price = '%.2f'%(float(info['price'])/currencyDic[event['event_price_unit']])
            raw_price = info['price']
            cheapMoney = info['cheapMoney']
            ticketNum = info['ticketNum']
            return render_to_response('form.html',{'city':event['district_name'],
                                                   'city_py':event['district_title'],
                                                   'price':price,'cheapMoney':cheapMoney,
                                                   'ticketNum':ticketNum,
                                                   'event':event,
                                                   'raw_price':raw_price,
                                                   'price_unit':event['event_price_unit'],
                                                   'price_unit_name':event['event_price_unit_name'],},context_instance=RequestContext(request))
    return HttpResponseRedirect('/event-%s.html'%event_id)


@csrf_exempt
def writeZhuantiOrder(request,event_id):
    #title = request.COOKIES.get('city_py',False)
    #city_name = request.COOKIES.get('city',False)
    eventId= int(event_id)
    event = formatEvent(SysEvent.objects.get(event_id=eventId),True)
    currencyDic = {"RMB":1,"HKD":1.24,"TWD":4.84,"USD":0.16,"EUR":0.12,"GBP":0.095,"JPY":16.33,"THB":5.23,"KER":164.46,"SGD":0.2,"VND":3388.90,"MYR":0.52}
    pricecontent = ''
    for item in event['event_content']:
        if item[0] == u'会议门票':
            pricecontent = item
    return render_to_response('zhuanti_order.html',{'city':event['district_name'],
                                           'city_py':event['district_title'],
                                           'event':event,
                                           'price_txt':pricecontent,},context_instance=RequestContext(request))


@captcha
def submitOrder(request):
    city_py = request.COOKIES.get('city_py','')
    city = request.COOKIES.get('city','')
    if request.method == 'POST':
        cds = request.POST
        error = False
        if not cds.get('name',''):
            error = True
        if not cds.get('mobilphone',''):
            error = True
        if not cds.get('address',''):
            error = True
        eventId = int(cds.get('event_id','0')) 
        if not eventId:
            error = True
        else:
            try:
                event = SysEvent.objects.get(Q(event_isshow=1)|Q(event_isshow=8),event_id=eventId)
                if event.event_price_model != 2:
                    if event.event_price_model == 1:
                        priceString = event.event_discount_price
                    else:        
                        priceString = event.event_price
                    priceList = priceString.split('/')
                    currencyDic = [1,1,1.24,4.84,0.16,0.12,0.095,16.33,5.23,164.46,0.2,3388.90,0.52]
                    for i in range(len(priceList)):
                        if priceList[i].replace('.','').isdigit():
                            priceList[i] = '%.2f'%(float(priceList[i])/currencyDic[event.event_price_currency])
                    if '%.2f'%float(cds.get('price')) not in priceList:
                        error = True
            except:
                error = True
        if not error:
            city_name = getCityNameById(event.district_id)
            number = '%s%s'%(int(time.time()),random.randint(100,1000))
            totalpay = float(cds['price'])*int(cds['number']) 
            #print cds['payMode']
            try:
                event_id = int(cds['event_id'])
            except:
                return render_to_response('base_error.html',{'city':city_name,'city_py':title,'error_msg':u'下订单时遇到错误,请重新下单'},context_instance=RequestContext(request))
            
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip =  request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            SysOrder.objects.create(
                                    order_number=number,
                                    order_user_name=cds.get('name',''),
                                    order_tel = cds.get('mobilphone',''),
                                    order_email = cds.get('email',''), 
                                    order_totalpay = totalpay,
                                    order_price = cds.get('price',''),
                                    order_amount = cds.get('number',''),
                                    order_address = cds.get('address',''),
                                    order_payment = cds.get('payMode',''),
                                    order_telphone = cds.get('phone',''),
                                    order_pay_status = 0,
                                    order_status = 0,
                                    event_id = int(cds.get('event_id','')),
                                    event_name = cds.get('event_name',''),
                                    city_title = city_name,
                                    order_reg_fields = 0,
                                    order_userid = 0,
                                    order_addtime = time.time(),
                                    order_addip = ip,
                                    order_text = cds.get('remark',''),
                                    )
            subject = '活动家 -新的订单通知.客户:%s,电话:%s'%(cds.get('name','').encode('utf-8'),cds.get('mobilphone','').encode('utf-8'))
            content = '点单号:%s\n总价:%s\n活动链接:http://huodongjia.com/event-%s.html\n'%(number,totalpay,cds.get('event_id','').encode('utf-8'))
            content += dic2text(cds)
            sendMail(subject,content)
            return render_to_response('orderDetails.html',{'city':city_name,'city_py':title,'order_info':cds,'order_number':number,'total_price':totalpay},context_instance=RequestContext(request))

    return render_to_response('base_error.html',{'city':city_name,'city_py':title,'error_msg':u'下订单时遇到错误,请重新下单'},context_instance=RequestContext(request))

#@cache_page(86400)
@csrf_exempt
def list(request,city,cat):
    date = request.GET.get('dat')
    offset = request.GET.get('page')
    
    if not city:
        return render_to_response('base_error.html',{'errorMsg':'Error CityId!' })
    
    if not cat: cat = 'all'
    if not date: date = 'latest'
    if not offset: offset = 1
    
    listDict = showlist.showList(city,cat,date,offset)
    #print connection.queries
    return render_to_response('list.html',listDict,context_instance=RequestContext(request))

#send_mail(u'有新订单%s', u'请到数据库中查看', 'qinchx@163.com',['623707254@qq.com'], fail_silently=False)

@cache_page(60 * 5)
def bankPay(request):
    city_py = request.COOKIES.get('city_py','')
    city = request.COOKIES.get('city','')
    return render_to_response('bankAccount.html',{'city':city_name,'city_py':title})


def subscribePage(request):
    city_py = request.COOKIES.get('city_py','')
    city = request.COOKIES.get('city','')
    head = {'title':u'【活动家-HuoDongJia.com】 活动订阅',
              'keywords':u'活动家活动订阅',
             'description':u'你可以在这里订阅活动'}
    return render_to_response('subscription.html',{'head':head,'city':city_name,'city_py':title},context_instance=RequestContext(request))

#网站使用
@csrf_exempt
@captcha
def subscribe2(request):
    city_py = request.COOKIES.get('city_py','')
    city = request.COOKIES.get('city','')
    if request.method == 'POST':
        cds = request.POST
        email = cds.get('subEmail')
        keywords = cds.get('customerKeywords','')
        import re
        selected = re.sub(',$','',cds.get('selectedSub'))
        selectedList = selected.split(',')
        if keywords:
            selected = keywords+','+selected
        selectedids=[]
        for item in selectedList:
            selectedids.append(str(getCatIdByName(item)))
        SubscribeInfo.objects.create(email=email,cats=';'.join(selectedids),keywords=keywords)
    return render_to_response('subscription.html',{'city':city_name,
                                                   'city_py':title,
                                                   'subscription_success':True,
                                                   'email':email,
                                                   'selected':selected,
                                                   },context_instance=RequestContext(request))

#app订阅
def subscribe(request):
    #title = request.COOKIES.get('city_py',False)
    #city_name = request.COOKIES.get('city',False)
    error = ''
    if request.method == 'GET':
        cds = request.GET
        if not cds.get('phone',False):
            error = u'必须填写电话'
        if not cds.get('keywords',False):
            error = u'至少填写一个感兴趣的关键词'
        if error:
            return HttpResponse(json.dumps({"code":0,"msg":error}), content_type="application/json")
        else:
            if not SubscribeInfo.objects.filter(phone=cds['phone']):
                SubscribeInfo.objects.create(
                                       email = cds.get('email',''),
                                       keywords = cds['keywords'],
                                       phone = cds['phone'],
                                       from_app = 1,
                                       )
            else:
                info = SubscribeInfo.objects.get(phone=cds['phone'])
                info.keywords = cds['keywords']
                info.save()
            return HttpResponse(json.dumps({"code":1,"msg":'subscribe success'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"code":0,"msg":'only GET method is supplied'}), content_type="application/json")

#app订阅
def cancelsubscribe(request):
    error = ''
    if request.method == 'GET':
        cds = request.GET
        if not cds.get('phone',False):
            error = u'必须填写电话'
            return HttpResponse(json.dumps({"code":0,"msg":error}), content_type="application/json")
        
        info = SubscribeInfo.objects.filter(phone=cds['phone'])
        if not info:
            error = u'该号码未订阅'
            return HttpResponse(json.dumps({"code":0,"msg":error}), content_type="application/json")
        info.delete()
        return HttpResponse(json.dumps({"code":1,"msg":'cancel success'}), content_type="application/json")
            
    else:
        return HttpResponse(json.dumps({"code":0,"msg":'only GET method is supplied'}), content_type="application/json")

def publishEvent(request):
    if request.method == 'POST':
        cds = request.POST
        error = {}
        if not cds.get('name',''):
            error['name'] = u'必须填写真实姓名'
        if not cds.get('mobilphone','') and not cds.get('email',''):
            error['mobilphone'] = u'至少填写一种联系方式'
            
        try:
            begin_time = time.mktime(time.strptime(cds.get('begin_time',''),'%Y-%m-%d'))
        except:
            error['begin_time'] = u'时间格式不对'
         
        try:
            end_time = time.mktime(time.strptime(cds.get('end_time',''),'%Y-%m-%d'))
        except:
            error['end_time'] = u'时间格式不对'
                
        if not error:
            addtime = time.time
            CustomPublishEvent.objects.create(
                                              name = cds['name'],
                                              email = cds.get('email',None),
                                              phone = cds.get('mobilephone',None),
                                              event_cat = int(cds.get('cat_id',None)),
                                              event_conent = cds.get('content',None),
                                              venue_name = cds.get('venue',None),
                                              event_begin_time = begin_time,
                                              event_end_time = end_time,
                                              event_price = cds.get('price','')
                                              )
        return

#@cache_page(60 * 5)
def aboutUs(request):
    city_py = request.COOKIES.get('city_py','')
    city = request.COOKIES.get('city','')
    head = {'title':u'活动家介绍_关于活动家-亚洲最大活动网站',
              'keywords':u'活动家,活动网,公司介绍',
             'description':u'找活动，上活动家Huodongjia.com！活动家是亚洲最大活动网站，提供专业商务会议、同城活动的查询与报名服务。服务热线:400-003-3879'}
    return render_to_response('aboutUs.html',{'head':head,'city':city,'city_py':city_py})

@cache_page(60 * 5)
def siteMap(request):
    city_py = request.COOKIES.get('city_py','')
    city = request.COOKIES.get('city','')
    head = {'title':u'网站地图',
              'keywords':u'活动家网站地图',
             'description':u'活动家网站地图'}
    return render_to_response('siteMap.html',{'head':head,'city':city,'city_py':city_py})


@cache_page(60 * 5)
def downloadapp(request, param):
    city_py = request.COOKIES.get('city_py','')
    city = request.COOKIES.get('city','')
    head = {'title':u'活动家客户端_活动家App下载',
              'keywords':u'活动家App下载',
             'description':u'活动家App下载'}
    if 0 != len(param):
        return render_to_response(param,{'head':head,'city':city,'city_py':city_py})
    else:
        return render_to_response('download.html',{'head':head,'city':city,'city_py':city_py})


@csrf_exempt
def get_check_code_image(request):
    from PIL import Image,ImageDraw,ImageFont      
    width = 140
    height = 50
    bgcolor = (255,255,255)
    image = Image.new('RGB',(width,height),bgcolor)
    font = ImageFont.truetype('Carnaval.TTF',20)
    fontcolor = (45,157,169)
    draw = ImageDraw.Draw(image)
    
    mp =  hashlib.md5()    
    mp_src = mp.update(str(datetime.datetime.now()))    
    mp_src = mp.hexdigest()    
    rand_str = mp_src[0:4]
    while '0' in rand_str or 'o' in rand_str or 'O' in rand_str:
        mp_src = mp.update(str(datetime.datetime.now()))    
        mp_src = mp.hexdigest()    
        rand_str = mp_src[0:4]
    rand_str = rand_str.upper()
    draw.text((0,0),rand_str,font=font,fill=fontcolor)
    del draw
    #image.save('1234_1.jpeg')
    newImage = Image.new('RGB',(width,height),bgcolor)
    newPix = newImage.load()
    pix = image.load()
    offset = 0
    for y in range(0,height):
        offset += 1 
        for x in range(0,width):
            newx = x + offset
            if newx < width:                        
                newPix[newx,y] = pix[x,y]         
    #newImage.save('1234_2.jpeg')
    draw = ImageDraw.Draw(newImage)
    linecolor= (134,126,177)
    for i in range(0,3):
        x1 = random.randint(0,width)
        x2 = random.randint(0,width)
        y1 = random.randint(0,height)
        y2 = random.randint(0,height)
        draw.line([(x1, y1), (x2, y2)], linecolor)
    del draw
    buf = cStringIO.StringIO()  
    newImage.save(buf,'GIF')
    request.session['captcha'] = rand_str
    return HttpResponse(buf.getvalue(),'image/gif') 

@csrf_exempt
def verify_captcha(request):
    if request.method == 'POST':
        p = request.POST
        if request.session.get('captcha').upper() == p.get('captcha','false').upper():
            return HttpResponse(json.dumps({'flag':'true'}))
    return HttpResponse(json.dumps({'flag':'false'}))


def theme(request,param):
    return render_to_response('theme/'+param+'.html')

def dispatchsitemap(request,param):
    return render_to_response('xmlsitemap/'+param+'.xml',mimetype="application/xml")

