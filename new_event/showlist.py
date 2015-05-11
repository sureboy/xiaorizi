#coding:utf-8
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from admin_self.common import NewCatUrl, NewCity,NewformatEvent,event_city_cat,get_event_list,get_site_links,get_site_hot_links
 
from new_event.common import constructNavigationUrl,find_from_city
from new_event.list_cal import list_page
from new_event.models import NewEventParagraph
import spot.list
from dateutil.relativedelta import relativedelta ,MO

from django.core.cache import cache
from sponsor.common import get_image_ads
#from dahuodong.common import getListHead
import datetime
import logging
log = logging.getLogger('XieYin.app')  

def homePage(request,city_title=False):
    #cityId = 45052
    #city_name = u'北京'
    #title = 'beijing'
    if not city_title:
        cityObj=(None, 0, '')
    else:
        cityObj = find_from_city(request,city_title)
    left=event_city_cat(cityObj[0], 69, True)     
    #right=event_city_cat(cityObj[0],(19,70)  )    
    #return render_to_response('base_error.html',{'error_msg':left}) 
    #special_dic_list  = right [:12]
    business_dic_list = left [:12]
    
    '''
    r= len(special_dic_list)-8
    if r<0:  
        rb = event_city_cat(cityObj[0],70  )  
        special_dic_list.extend(rb[:abs(r)] )
        
        
    l= len(business_dic_list)-8
    if l<0:  
        b = event_city_cat(cityObj[0],(19,69)  )  
        business_dic_list.extend(b[:abs(l)] )
        #return render_to_response('base_error.html',{'error_msg':b}) 
    '''
    # 获取视频，按照end_time排序，只取6个
    video = NewEventParagraph.objects.filter(cat_name_id=17543).order_by('-end_time')
    def setUrl(v):
        v.video_url = '/video-' + str(v.id) + '.html'
        return v
    video_list = map(setUrl, video[:7])

    #return render_to_response('base_error.html',{'error_msg':special_dic_list}) 


    head = {'title':u'活动家-亚洲最大的活动网聚合平台-全面、安全、快捷、方便_认准活动家官方网站' ,
            'keywords':u'活动家,网上订票,会议网,活动网,亲子活动,活动,同城活动' ,
            'description':u'活动网为您提供海量会议,公开课,会展,极限运动,当地体验,夜生活,演出折扣票,同城活动查询,特色旅游，门票预订,报名,参加活动,每日发布最新活动，发布活动请上活动家！服务热线:400-003-3879'
            }
    hot_links=get_site_hot_links()
    hot_links_new=[]
    for ev in hot_links:
        try:
            if   datetime.datetime.strptime(ev[5],'%Y-%m-%d %H:%M:%S')<datetime.datetime.now():
                continue 
        except:
            pass
        try:
            if  datetime.datetime.strptime(ev[4],'%Y-%m-%d %H:%M:%S')> datetime.datetime.now():
                continue
        except:
            pass
        #ev[0]='%s%s' % (ev[0],ev[5])
        hot_links_new.append(ev)
    
   
        
    ###########

    def judge(string):
        for c in string:
            if c.isdigit():
                return False
        return True
    
    meetings = NewCatUrl(0,'',True)['business']
    
    i = 0
    length = len(meetings['child'])
    while i < length:
        nav = meetings['child'][i]
        if not judge(nav['caturl']) or meetings['child'][i]['ename'] in ['meeting','training','expo']:
            del  meetings['child'][i]
            #nav['caturl'] += 'del'
            length -= 1
        else:
            i += 1
    ###########

    if city_title:
        cn = cityObj[1]
        head = {'title':u'%s商务会议网_%s同城活动网_%s活动家' % (cn, cn, cn),
            'keywords':u'%s会议网,%s同城活动,%s商务活动,%s活动' % (cn, \
                cn, cn, cn),
            'description':u'找%s会议、活动，上活动家Huodongjia.com！活动家是%s最大商务活动网站，提供%s地区专业商务会议、同城活动的查询与报名服务，涵盖IT、医疗、金融财经、能源化工、农业林业等行业优质商务会议，美食体验、极限运动、亲子活动、娱乐演出等优质同城活动，在线订票，免费发布活动，全面、安全、快捷、方便，认准活动家官方网站！服务热线:400-003-3879' % \
                    (cn, cn, cn)

            }
    else:
        head = {'title':u'活动家-专业商务会议网-亚洲最大活动网站' ,
            'keywords':u'活动网,会议网,商务活动,商务会议,活动家' ,
            'description':u'找会议，上活动家Huodongjia.com！活动家是亚洲最大商务活动网站，提供专业商务会议、同城活动的查询与报名服务，涵盖IT、医疗、金融财经、能源化工、农业林业等行业优质商务会议，美食体验、极限运动、亲子活动、娱乐演出等优质同城活动，在线订票，免费发布活动，全面、安全、快捷、方便，认准活动家官方网站！服务热线:400-003-3879'
            }

    ##########
    bay={'city':cityObj[1],
       'city_id':cityObj[0],
       'city_py':cityObj[2],
       'hot_links':hot_links_new[:5],
       #'special_list':special_dic_list,
       'business_list':business_dic_list,
       'video_list': video_list,
       'meeting': meetings,

       'head':head,
       'background_img':'../images/head_background/header_background.png'}
    
    links=get_site_links()
    
    bay['site_links']=[]
    for li in range(len(links)):
        #####
        ####
        ###
        try:
            if 0 < len(links[li][4]):
                for l in links[li][4]:
                    if l == city_title:
                        bay['site_links'].append(links[li])
                        break
                    
            else:
                #pass
                #无城市信息就显示没有设置城市的友情链接
                #有城市信息就显示设置有该城市的友情链接
                if not city_title:
                    bay['site_links'].append(links[li])
        except:
            #pass
            bay['site_links'].append(links[li])
    
    #
    bay['list'] = spot.list.showList(request, False, 'all', 'latest', 1)['list'] \
                    + spot.list.showList(request, False, 'all', 'latest', 2)['list']
    for item in bay['list'][:6]:
        item['spot_name'] = item['spot_name'].replace(u'会议报告：', '')
         
    #
    ############
    # 读取广告
    ############
    
    ads_pos_1 = get_image_ads(1)
    ads_pos_2 = get_image_ads(2)
    ads_pos_3 = get_image_ads(3)
    def set_url(ia):
        try:
            ia.pic_url = ia.pic.server.name + ia.pic.urls
        except AttributeError:
            if ia.pic is not None:
                ia.pic_url = "http://pic.huodongjia.com/" + ia.pic.urls
            else:
                ia.pic_url = ""

        return ia
    
    ads_in_1 = map(set_url, ads_pos_1)
    ads_in_2 = map(set_url, ads_pos_2)
    ads_in_3 = map(set_url, ads_pos_3)
    
    bay['ads1'] = ads_in_1
    bay['ads2'] = ads_in_2
    bay['ads3'] = ads_in_3
    
    response = render_to_response('home.html',bay,
                                           context_instance=RequestContext(request))
    '''
    response.set_cookie('city_id',cityObj[0])
    response.set_cookie('city_py',cityObj[2])
    response.set_cookie('city',cityObj[1].encode('utf-8'))
    response['Cache-Control'] = 'max-age=300'
    '''
    return response


@csrf_exempt
def list(request,city=None,cat=None,date=None,offset=1):
    
    
    #log.debug('get list')
              
    date = request.GET.get('dat')
    offset = request.GET.get('page')
    ''' 
    if not date and not cat:    
        return homePage(request,city)
        #return False
    '''
    ##router to homePage when host/<city> requested
    if not cat and city:
        #if city is a real <city> identifier
        titleDict = NewCity(3)
        if city in titleDict:
            return homePage(request, city)
        #else do nothing
    

    ##if <cat> in meeting -> views.list_page
    cat_url = NewCatUrl()
    meetings = cat_url['meeting']
    business = cat_url['business']
    
    tags_set = ['meeting', 'business']

    for nav in meetings['child']:
        tags_set.append(nav['ename'])
    for nav in business['child']:
        tags_set.append(nav['ename'])
        for nav2 in nav['child']:
            tags_set.append(nav2['ename'])

    #when url is host/<cat> the variable 'city' is <cat>
    if city in tags_set:
        return list_page(request, cat = city)
    if cat in tags_set:
        return list_page(request, city = city, cat = cat)
    ###

    if cat_url.has_key(city):
        cat=city
        city='';
    if not cat: cat = 'all'
    if not date: date = 'latest'
    if not offset: 
        offset = 1 
    else: 
        offset = int(offset)
 
    
    
    listDict = showList(request,city,cat,date,offset)
    
    
    links=get_site_links()
    
    site_link_city=[]
    for li in range(len(links)):
        try:
            if 0 < len(links[li][4]):
                for l in links[li][4]:
                    if l == city:                         
                        site_link_city.append(links[li])
                        break
                    
            else:
                pass
                #listDict['site_links'].append(links[li])
        except:
            pass
            #listDict['site_links'].append(links[li])
    
    site_link_cat=[]
    for li in range(len(site_link_city)):
        try:
            if 0 < len(site_link_city[li][5]):
                for l in site_link_city[li][5]:
                    if str(l) == str(cat):                         
                        site_link_cat.append(site_link_city[li])
                        break
                    
            else:
                pass
                #site_link_cat.append(listDict['site_links'][li])
        except:
            pass
            #site_link_cat.append(listDict['site_links'][li])  
    listDict['site_links']=site_link_cat
    
    #print connection.queries
    return render_to_response('list.html',listDict,context_instance=RequestContext(request))
def constructDatUrl( city,cat , date):
    datList = []
    ddc = ['本周','下周','下月','最新']
    dde = ['thisweek','nextweek','nextmonth','new']
    url = '/'+city + '/'+cat  if city else '/'+cat
        
        
    for i in range(0,len(dde)):
         
        #url = url + '/'+cat+'/'
        datDict = dict()    
 
        datDict['daturl'] = url + '?dat='+dde[i] 
        #datDict['daturl'] =url + '/'+dde[i] + '/'
        datDict['datname'] = ddc[i]
        datDict['flag'] = 'false'
        if date == dde[i]:
            datDict['flag'] = 'true'
        datList.append(datDict)
    return datList
'''
def find_cat_ch(cat_id_li={},cat_id=0,tmp=[]):
    #cat_id_li=NewCatUrl(False,city)
    
    try:
        if cat_id_li.has_key(cat_id):            
            tmp.append(cat_id_li[cat_id]['id'])
        
        if cat_id_li[cat_id]['child']:
            for ch in cat_id_li[cat_id]['child']:
                #tmp.append(ch['id'])
                 
                find_cat_ch(cat_id_li,ch['id'],tmp)
           
    except: 
        pass
 
    
def get_event_list( cat,city,date,page,offset,order,new=False):
    
    
    #args=Q(spot_isshow=1)
    args=NewEventTable.objects.filter( isshow__in=(1,8)).filter(end_time__gt=datetime.date.today())
    if date and date != 'latest':
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

        if startTime and endTime:
            args =args.filter( (Q( begin_time__lte=startTime)&Q( end_time__gte=endTime))|\
            (Q( begin_time__gte=startTime)&Q( begin_time__lte=endTime))|\
            (Q( end_time__gte=startTime)&Q(end_time__lte=endTime)))
    
    
    if cat !='all':
        
        cat_id_li=NewCatUrl(0,city[2])
        tmps=[]
        cat_id=None
        try:
            cat_id=cat_id_li[cat]['id']
        except:
            try:
                cat_id=cat_id_li[int(cat)]['id']
            except:
                pass
            
        if cat_id:
            find_cat_ch(NewCatUrl(2,city[2]),cat_id,tmp=tmps)
        
        if len(tmps)>0:
            args = args.filter(cat__in=tmps)
        else:
            return None
        
    #return render_to_response('base_error.html',{'error_msg':str(cat)})
    
    if city and  city != 0:  
        args =args.filter( city=city[0] )
        #args = args&Q(spot_city=city)
        
       
        
     
    if not offset:
        #return SysSpotInfo.objects.filter(args).count()
        return args.distinct().count()
        
        
    else:
        #return SysSpotInfo.objects.filter(args).order_by(order)[page:offset]
        return args.order_by("-order").order_by(order).distinct()[page:offset]
''' 
def getListHeadNew(city ,cat ,date):
    city_name=city[1]
    cat_id_li=NewCatUrl(False,city[2])
    if cat.isdigit():
        cat=int(cat)
        
    data_str=''
    if 'thisweek' == date:
        startTime = datetime.date.today()+relativedelta(weekday=MO(-1))
        #next week monday
        endTime = datetime.date.today()+relativedelta(days=+1,weekday=MO)
        
        data_str=u'%s年%s月%s-%s日' % (startTime.year,startTime.month,startTime.day,endTime.day)
        #data_str=datetime.datetime.strftime(startTime,'%Y年%m月%d')
        #data_str+=datetime.datetime.strftime(endTime,'-%d')
        #data_str+=u"日"
    elif 'nextweek' == date:
        #next week monday
        startTime = datetime.date.today()+relativedelta(days=+1,weekday=MO)
        #after next week monday
        endTime = startTime+relativedelta(days=+1,weekday=MO)
        #next week SUNDAY
        #endTime = today+relativedelta(days=+7,weekday=SU)datetime
        datetime.date.year
        data_str=u'%s年%s月%s-%s日' % (startTime.year,startTime.month,startTime.day,endTime.day)
        #data_str=datetime.datetime.strftime(startTime,'%Y年%m月%d')
        #data_str+=datetime.datetime.strftime(endTime,'-%d')
        #data_str+=u"日"
    elif 'nextmonth' == date:
        thisMonthStart = datetime.datetime.now().strftime('%Y-%m-1')
        tmp = thisMonthStart.split('-')
        thisMonthStart = datetime.datetime(int(tmp[0]), int(tmp[1]),int(tmp[2]))
        startTime = thisMonthStart+relativedelta(months=+1)
        endTime = thisMonthStart+relativedelta(months=+2)
        data_str=u'%s年%s月' % (startTime.year,startTime.month)
        #data_str=datetime.datetime.strftime(startTime,'%Y年%m月')

    elif date == 'new':
        data_str=u'最新'

    
    head_list={}
    if cat_id_li.has_key( cat ):
        catname=cat_id_li[cat]['catname']
        if cat_id_li[cat]['seo']:
            head_list = cat_id_li[cat]['seo']
    else:
        catname=''
        head_list=None
            

    if  head_list:
        if head_list.has_key('title'):
            head_list['title']=head_list['title'].replace('XX',city_name).replace(u'大活动',u'活动家') 
            head_list['title']=head_list['title'].replace('(city)',city_name)
            head_list['title']=head_list['title'].replace('(date)',data_str)
            head_list['title']=head_list['title'].replace('(cat)',catname)
        else:
            head_list['title']=u'会议网_活动网_公开课培训_%s展会_活动家'%city_name
        
        if head_list.has_key('keywords'):
            head_list['keywords']=head_list['keywords'].replace('XX',city_name).replace(u'大活动',u'活动家')
            head_list['keywords']=head_list['keywords'].replace('(city)',city_name)
            head_list['keywords']=head_list['keywords'].replace('(date)',data_str)
            head_list['keywords']=head_list['keywords'].replace('(cat)',catname)
        else:
            head_list['keywords']=u'会议网,活动网,商务活动,公开课培训,%s展览,%s展会,%s会展,%s会议'%(city_name,city_name,city_name,city_name)
        
        if head_list.has_key('description'):
        
            head_list['description']=head_list['description'].replace('XX',city_name).replace(u'大活动',u'活动家')
            head_list['description']=head_list['description'].replace('(city)',city_name)
            head_list['description']=head_list['description'].replace('(date)',data_str)
            head_list['description']=head_list['description'].replace('(cat)',catname)
        else:
            head_list['description']=u'活动家www.huodongjia.com为你提供会议报名，会展参展，公开课报名服务。服务热线:400-003-3879'
        head =head_list
    else:
        head = getListHead(city ,cat ,date)
        
    return head
def getListHead(city ,cat ,date):
    city_name=city[1]
    cat_id_li=NewCatUrl(False,city[2])
    
    try:
        catEname=cat_id_li[cat]['ename']
    except:
        catEname=''
    
    head = dict()
    if date == 'thisweek':
        if 'meeting' == catEname:
            head = {'title':u'%s近期会议_活动家'%(city_name),
                 'keywords':u'%s近期会议，%s近期论坛'%(city_name,city_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区高大上会议，峰会等商务活动查询、报名。学习提升，积累人脉，精准标签，个性定制。服务热线:400-003-3879'%city_name
                 }
        elif 'concert' == catEname:
            head = {'title':u'%s近期演唱会_活动家'%(city_name),
                 'keywords':u'%s近期演唱会'%(city_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区演唱会活动查询、门票购买服务。服务热线:400-003-3879'%city_name
                 }
        elif 'music' == catEname:
            head = {'title':u'%s近期音乐会_活动家'%(city_name),
                 'keywords':u'%s近期音乐会'%(city_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区音乐会活动查询、门票购买服务。服务热线:400-003-3879'%city_name
                 }
        elif 'drama' == catEname:
            head = {'title':u'%s近期话剧_活动家'%(city_name),
                 'keywords':u'%s近期话剧'%(city_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区话剧活动查询、门票购买服务。服务热线:400-003-3879'%city_name
                 }
        elif 'expo' == catEname:
            head = {'title':u'%s近期会展_%s近期展会_活动家'%(city_name,city_name),
                 'keywords':u'%s近期会展,%s近期展会'%(city_name,city_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区会展，展会查询、场地预订服务。服务热线:400-003-3879'%city_name
                 }
        elif 'training' == catEname:
            head = {'title':u'%s近期培训_%s近期公开课_活动家'%(city_name,city_name),
                 'keywords':u'%s近期培训,%s近期公开课'%(city_name,city_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区会展，展会查询、场地预订服务。服务热线:400-003-3879'%city_name
                 }
        else:
            head = {'title':u'%s近期活动_活动家'%(city_name),
                 'keywords':u'%s近期活动，%s近期会议，%s近期公开课，%s近期培训，%s近期会展，%s近期展会'%(city_name,city_name,city_name,city_name,city_name,city_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区高大上会议，峰会，公开课，培训，会展，展会等商务活动查询、报名。学习提升，积累人脉，精准标签，个性定制。服务热线:400-003-3879'%city_name
                 }
    elif date == 'nextweek':
        head = {'title':u'%s最近活动_活动家'%(city_name),
                 'keywords':u'%s最近活动，%s最近会议，%s最近公开课，%s最近培训，%s最近会展，%s最近展会'%(city_name,city_name,city_name,city_name,city_name,city_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区高大上会议，峰会，公开课，培训，会展，展会等商务活动查询、报名。学习提升，积累人脉，精准标签，个性定制。服务热线:400-003-3879'%city_name
                 }
    elif date == 'nextmonth':
        today = datetime.date.today()
        nextmonth = today + relativedelta(months=1)
        datlist = str(nextmonth).split('-')
        year = datlist[0]
        month = datlist[1]
        dt = u"%s年%s月"%(year,month)
        head = {'title':u'%s%s活动_活动家'%(city_name,dt),
                 'keywords':u'%s%s活动,%s%s会议，%s%s公开课，%s%s培训，%s%s会展，%s%s展会'%(dt,city_name,dt,city_name,dt,city_name,dt,city_name,dt,city_name,dt,city_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区高大上会议，峰会，公开课，培训，会展，展会等商务活动查询、报名。学习提升，积累人脉，精准标签，个性定制。服务热线:400-003-3879'%city_name
                 }
    elif date == 'new':
        head = {'title':u'%s最新活动_活动家'%(city_name),
                 'keywords':u'%s最新会议，%s最新公开课，%s最新培训，%s最新会展，%s最新展会'%(city_name,city_name,city_name,city_name,city_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区高大上会议，峰会，公开课，培训，会展，展会等商务活动查询、报名。学习提升，积累人脉，精准标签，个性定制。服务热线:400-003-3879'%city_name
                 }
    else:
        pass
    
    if 0 != len(head):
        return head
    
    if catEname == 'business':
        head = {'title':u'%s会议网,会展网,%s展览会,活动家商务会议频道'%(city_name,city_name),
                 'keywords':u'%s会议，%s峰会，%s公开课，%s培训，%s会展，%s展会'%(city_name,city_name,city_name,city_name,city_name,city_name),
                 'description':u'活动家（www.huodongjia.com）商务会议频道为您提供%s地区高大上会议，峰会，公开课，培训，会展，展会等商务活动查询、报名。学习提升，积累人脉，精准标签，个性定制。服务热线:400-003-3879'%city_name
                 }
        
    elif catEname == 'fun':
        head = {'title':u'%s演唱会,%s演出折扣票,%s同城活动,%s娱乐活动,活动家娱乐演出频道'%(city_name,city_name,city_name,city_name),
                 'keywords':u'%s演唱会、音乐会、话剧、儿童亲子、戏曲综艺、舞蹈 、小型现场、同城活动、周末活动'%city_name,
                 'description':u'活动家（www.huodongjia.com）娱乐演出频道为您提供%s地区文娱演出和其他娱乐活动查询、订票。海量活动，随时随地购票！服务热线:400-003-3879'%city_name
                 }
    else:
        head_list=None
        try:
            if cat.isdigit():
                cat=int(cat)
            if cat_id_li.has_key( cat ):
                if cat_id_li[cat]['seo']:
                    head_list = cat_id_li[cat]['seo']
                    
                    if not head_list:
                        return {'title':u'会议网_活动网_公开课培训_%s展会_活动家'%city_name,
                                 'keywords':u'会议网,活动网,商务活动,公开课培训,%s展览,%s展会,%s会展,%s会议'%(city_name,city_name,city_name,city_name),
                                 'description':u'活动家网www.huodongjia.com为你提供会议报名，会展参展，公开课报名服务。服务热线:400-003-3879'
                                 }
            
            #cat_seo = SysEventCat.objects.get(cat_ename = catEname).cat_seo
        except:
            return {'title':u'会议网_活动网_公开课培训_%s展会_活动家'%city_name,
                 'keywords':u'会议网,活动网,商务活动,公开课培训,%s展览,%s展会,%s会展,%s会议'%(city_name,city_name,city_name,city_name),
                 'description':u'活动家网www.huodongjia.com为你提供会议报名，会展参展，公开课报名服务。服务热线:400-003-3879'
                 }
        
        #head_list = cat_seo.split('[|]')
        if  head_list:
            if head_list.has_key('title'):
                head_list['title']=head_list['title'].replace('XX',city_name).replace(u'大活动',u'活动家') 
            else:
                head_list['title']=u'会议网_活动网_公开课培训_%s展会_活动家'%city_name
            
            if head_list.has_key('keywords'):
                head_list['keywords']=head_list['keywords'].replace('XX',city_name).replace(u'大活动',u'活动家')
            else:
                head_list['keywords']=u'会议网,活动网,商务活动,公开课培训,%s展览,%s展会,%s会展,%s会议'%(city_name,city_name,city_name,city_name)
            
            if head_list.has_key('description'):
            
                head_list['description']=head_list['description'].replace('XX',city_name).replace(u'大活动',u'活动家')
            else:
                head_list['description']=u'活动家www.huodongjia.com为你提供会议报名，会展参展，公开课报名服务。服务热线:400-003-3879'
            head =head_list
                   
        else:
            head = {'title':u'会议网_活动网_公开课培训_%s展会_活动家'%city_name,
                 'keywords':u'会议网,活动网,商务活动,公开课培训,%s展览,%s展会,%s会展,%s会议'%(city_name,city_name,city_name,city_name),
                 'description':u'活动家www.huodongjia.com为你提供会议报名，会展参展，公开课报名服务。服务热线:400-003-3879'
                 }
    return head

''' 
def getListHead(city ,cat ,date):
    head = {}
    city_name=city[1]
    cat_id_li=NewCatUrl(False,city[2])
    if cat.isdigit():
        cat=int(cat)
    if cat_id_li.has_key( cat ):
        if cat_id_li[cat]['seo']:
            head = cat_id_li[cat]['seo']
        
    if date == 'thisweek':
        dat_name=u'近期'
    elif date == 'nextweek':
        dat_name=u'最近'
    elif date == 'nextmonth':
        today = datetime.date.today()
        nextmonth = today + relativedelta(months=1)
        datlist = str(nextmonth).split('-')
        year = datlist[0]
        month = datlist[1]
        dat_name = u"%s年%s月"%(year,month)
    elif date == 'new':
        dat_name=u"最新"
    else:
        dat_name=''
    
 
        
    if head:
        head['title']="%s" % (head['title'].replace('XX',city_name).replace(u'大活动',u'活动家'))
        head['keywords']="%s" % (head['keywords'].replace('XX',city_name).replace(u'大活动',u'活动家'))
        head['description']="%s" % (head['description'].replace('XX',city_name).replace(u'大活动',u'活动家'))
        
    else:   
        
        try:
            catEname=cat_id_li[cat]['ename']
        except:
            catEname=''
            
            
        if catEname == 'business':
            head = {'title':u'%s会议网,会展网,%s展览会,活动家商务会议频道'%(city_name,city_name),
                     'keywords':u'%s会议，%s峰会，%s公开课，%s培训，%s会展，%s展会'%(city_name,city_name,city_name,city_name,city_name,city_name),
                     'description':u'活动家（www.huodongjia.com）商务会议频道为您提供%s地区高大上会议，峰会，公开课，培训，会展，展会等商务活动查询、报名。学习提升，积累人脉，精准标签，个性定制。服务热线:400-003-3879'%city_name
                     }
        
        elif catEname == 'fun':
            head = {'title':u'%s演唱会,%s演出折扣票,%s同城活动,%s娱乐活动,活动家娱乐演出频道'%(city_name,city_name,city_name,city_name),
                     'keywords':u'%s演唱会、音乐会、话剧、儿童亲子、戏曲综艺、舞蹈 、小型现场、同城活动、周末活动'%city_name,
                     'description':u'活动家（www.huodongjia.com）娱乐演出频道为您提供%s地区文娱演出和其他娱乐活动查询、订票。海量活动，随时随地购票！服务热线:400-003-3879'%city_name
                     }
 
    
        elif 'meeting' == catEname:
            head = {'title':u'%s%s会议_活动家'%(city_name,dat_name),
                 'keywords':u'%s%s会议，%s%s论坛'%(city_name,dat_name,city_name,dat_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区高大上会议，峰会等商务活动查询、报名。学习提升，积累人脉，精准标签，个性定制。服务热线:400-003-3879'%city_name
                 }
        elif 'concert' == catEname:
            head = {'title':u'%s%s演唱会_活动家'%(city_name,dat_name),
                 'keywords':u'%s%s演唱会'%(city_name,dat_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区演唱会活动查询、门票购买服务。服务热线:400-003-3879'%city_name
                 }
        elif 'music' == catEname:
            head = {'title':u'%s%s音乐会_活动家'%(city_name,dat_name),
                 'keywords':u'%s%s音乐会'%(city_name,dat_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区音乐会活动查询、门票购买服务。服务热线:400-003-3879'%city_name
                 }
        elif 'drama' == catEname:
            head = {'title':u'%s%s话剧_活动家'%(city_name,dat_name),
                 'keywords':u'%s%s话剧'%(city_name,dat_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区话剧活动查询、门票购买服务。服务热线:400-003-3879'%city_name
                 }
        elif 'expo' == catEname:
            head = {'title':u'%s%s会展_%s%s展会_活动家'%(city_name,dat_name,city_name,dat_name),
                 'keywords':u'%s%s会展,%s%s展会'%(city_name,dat_name,city_name,dat_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区会展，展会查询、场地预订服务。服务热线:400-003-3879'%city_name
                 }
        elif 'training' == catEname:
            head = {'title':u'%s%s培训_%s%s公开课_活动家'%(city_name,dat_name,city_name,dat_name),
                 'keywords':u'%s%s培训,%s%s公开课'%(city_name,dat_name,city_name,dat_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区会展，展会查询、场地预订服务。服务热线:400-003-3879'%city_name
                 }
        else:
            head = {'title':u'%s%s活动_活动家'%(city_name,dat_name),
                 'keywords':u'%s%s活动，%s%s会议，%s%s公开课，%s%s培训，%s%s会展，%s%s展会'%(city_name,dat_name,city_name,dat_name,city_name,dat_name,city_name,dat_name,city_name,dat_name,city_name,dat_name),
                 'description':u'活动家（www.huodongjia.com）为您提供%s地区高大上会议，峰会，公开课，培训，会展，展会等商务活动查询、报名。学习提升，积累人脉，精准标签，个性定制。服务热线:400-003-3879'%city_name
                 }
  
    
 
         
    return head
''' 

def showList(request,city, cat, date, offset):
    #translate city character to city digit
    #log.debug('get showlist')
    cityObj = NewCity(3)
    if cityObj.has_key(city):
        ci=cityObj[city]
    else:
        ci=(0,'','')#cityObj['beijing']

    cityId = ci[0]
 
    cityName = ci[1]
    cityPy = ci[2]
     
    
    #get sql query condition
    perpage=10
    offset = int(offset)
    cout = perpage*(offset-1)
    try:
        url=request.META['PATH_INFO']
        if url[-1]=="/":
            url=url[:-1] 
    except:
        url=''
    
    count =   get_event_list( cat,ci,date ,False,False,False)      
    
    count=count if count else 0
    pages = count/perpage
    if 0 != (count%perpage):
        pages = pages + 1
    
    orderStr = 'end_time'

    if 'new' == date:
        orderStr = '-rel_time'
        
    mlist =  get_event_list( cat,ci,date, cout,cout+perpage,orderStr)
    tmp = []
    if mlist:
        print mlist
        for item in mlist:
            tmp.append(NewformatEvent(False,item))
    
    #list page: dat url,cat url,navigation url,slice page url
    #datList = constructDatUrl(city,cat,date)
    #constructCatUrl(city,cat,date)
    #catUrlLv1 = constructCatUrl(city,cat,date)
    
    navigationList =constructNavigationUrl ( cityPy,cat)
    
 
            
    ''' 
    i=len(navigationList)
    nv=[]
    #import copy 
    catss= NewCatUrl(2)
    for k in range(i):
        
        if k==3:
            break
        nv.append(navigationList[i-1-k])
    cstr=[] 
    le=len(nv)
    for kh in range(le):        
        if nv[le-1-kh].has_key('id'):
            cat_k=[]      
            for ch in catss[nv[le-1-kh]['id']]['child']:
                for n in nv:
                    if n.has_key('id'):
                        if ch['id']==n['id']:
                            ch['flag'] = 'true'
                
                if ch['ename']:
                    cat_k.append(ch)
            cstr.append(cat_k)
        
            
 
    
    le= len(nv)   
    cat_k={}
    for ki in range(le):
        
        cstr='c%s' % ki
        cat_k[cstr]=[]
        if nv[le-1-ki]
        for ch in catss[nv[le-1-ki]['id']]['child']:
            cat_k[cstr].append(ch)
            
    '''
            
            
         
            
        
        
    
    
    firstPage,lastPage,prePage,nextPage,pageList = constructSliceUrl(city,cat,date,pages,offset)
    
    head = getListHeadNew(ci,cat,date)
    if offset>1:

        head['title']=u'%s[第%s页]' % (head['title'],str(offset))

    #head = getListHead(cityName,cat,date)
    datList = constructDatUrl(city,cat, date)
    listDict = {'city':cityName,
                'city_py':cityPy,
                 'list':tmp,
                 'datList':datList,
                 'catUrlLv1':NewCatUrl(1,cityPy,False,cat),
                 'allcat':'/'+cityPy+'/all/' if cityPy else '/',
                 'navigationList':navigationList,
                 'firstPage':firstPage,
                 'lastPage':lastPage,
                 'prePage':prePage,
                 'nextPage':nextPage,
                 'countpage':pages,
                 'pageList':pageList,
                 'head':head,
                 'cat':cat,
                 'cat_k':mlist
                               }
    return listDict


def constructSliceUrl(city,cat,date, amountPages,curpage):
    if curpage > amountPages:
        curpage =  amountPages
    if curpage <= 0 or False == curpage:
        curpage = 1
    pageList = []
    #url = '/'+city+'/'+cat+'/'+date 
    url = '/'+city+'/'+cat+'/?'+'dat='+date if city else '/'+cat+'/?'+'dat='+date
    #construct section page
    startPage = 1
    endPage = amountPages
    if 3 <= curpage:
        startPage = curpage-2
    if 2 <= amountPages - curpage:
        endPage =  curpage+2
        
        
        

    #first last page
    firstPage = 'false'
    lastPage = 'false'
    if curpage != 1:
        firstPage ='/'+city+'/'+cat+'/' if city else '/'+cat+'/' #url+'&page='+'1'
    if curpage != amountPages:
        lastPage = url+'&page='+str(amountPages)
    #prepage nextpage
    prePage = 'false'
    nextPage = 'false'
    if 1 < curpage:
        prePage = url+'&page='+str(curpage-1)
    if curpage < amountPages and 1 < amountPages:
        nextPage = url+'&page='+str(curpage+1)
        
    for i in range(startPage,endPage+1):
        curPageFlg = 'false'
        if curpage == i:
            curPageFlg = 'true'
        if i==1:
            pageDict = {'page':i, 'pageurl':'/'+city+'/'+cat+'/' if city else '/'+cat+'/','flag':curPageFlg}
        else:
            pageDict = {'page':i, 'pageurl':url+'&page='+str(i),'flag':curPageFlg}
        pageList.append(pageDict)
    return (firstPage,lastPage,prePage,nextPage,pageList)    
    
    '''
    for i in range(startPage,endPage+1):
        curPageFlg = 'false'
        if curpage == i:
            curPageFlg = 'true'
        pageDict = {'page':i, 'pageurl':url+'/'+str(i)+'/','flag':curPageFlg}
        pageList.append(pageDict)
    #first last page
    firstPage = 'false'
    lastPage = 'false'
    if curpage != 1:
        firstPage = url+'/'+'1'+'/'
    if curpage != amountPages:
        lastPage = url+'/'+str(amountPages)+'/'
    #prepage nextpage
    prePage = 'false'
    nextPage = 'false'
    if 1 < curpage:
        prePage = url+'/'+str(curpage-1)
    if curpage < amountPages and 1 < amountPages:
        nextPage = url+'/'+str(curpage+1)+'/'
    return (firstPage,lastPage,prePage,nextPage,pageList)
    '''
