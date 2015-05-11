#coding:utf-8
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from dahuodong.models import SysCommonDistrict,SysVenue,Crowfunding,SysEventCat,SysOrderMessage
from django.shortcuts import render_to_response
from BeautifulSoup import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time  
import urllib2
import sphinxapi
from django.core.cache import cache
from dahuodong.models import SysEvent,PubEventCat
import HTMLParser
from dateutil.relativedelta import relativedelta
import datetime
from new_event.models import NewEventTable

def formatEvent(event,detail = False):
    res = {}
    res['event_id'] = event.event_id
    res['event_name'] = event.event_name
    if detail:
        res['event_content'] = resolveContent(event.event_content)
        res['district_id'] = event.district_id
        res['time_expire'] = event.event_time_expire
    res['event_venue'] = getVenueById(event.venue_id)
    res['event_address'] = event.event_address
    res['event_cat'] = event.event_cat
    res['event_islongtime'] = event.event_islongtime
    if getCatEnameById(event.event_cat):
        res['cat_name'] = getCatNameById(event.event_cat)
        res['cat_ename'] = getCatEnameById(event.event_cat)
    else:
        res['cat_name'] = getCatNameById(event.event_cat1)
        res['cat_ename'] = getCatEnameById(event.event_cat1)
    res['event_tag'] = event.event_cat_tag.split(',')
    event_cat1 = event.event_cat1
    res['event_cat1'] = event_cat1
    if event_cat1 in [2,3,6]:
        res['has_picture'] = True
    res['district_title'] = getTitleById(event.district_id)
    res['district_name'] = getCityNameById(event.district_id)
    res['event_begin_time'] = time.strftime('%Y-%m-%d',time.localtime(event.event_begin_time))
    res['event_end_time'] = time.strftime('%Y-%m-%d',time.localtime(event.event_end_time))
    res['event_img'] = getPicSource(event.event_img,str(event.event_cat))
    currency_dic = {"1":("RMB",u'人民币'),"2":("HKD",u'港币'),"3":("TWD",u'新台币'),"4":("USD",u'美元'),
                    "5":("EUR",u'欧元'),"6":("GBP",u'英镑'),"7":("JPY",u'日元'),"8":("THB",u'泰铢'),"9":("KER",u'韩元'),"10":("SGD",u'新加坡币'),
                    "11":("VND",u'越南盾'),"12":("MYR",u'马币')}
    res['event_price_unit'] = currency_dic.get(str(event.event_price_currency),("RMB",u'人民币'))[0]
    res['event_price_unit_name']=currency_dic.get(str(event.event_price_currency),("RMB",u'人民币'))[1]
    res['event_price'] = event.event_price
    res['event_isfree'] = event.event_isfree
    res['event_discount'] = event.event_discount
    res['event_discount_price'] = event.event_discount_price
    event_price_model = event.event_price_model
    res['event_price_model'] = event_price_model
    if event_price_model == 3:
        res['cf'] = Crowfunding.objects.get(event_id = event.event_id)
    return res

def getCatObjByEName(ename):
    catDict = cache.get('catEDict',None)
    if not catDict:
        try:
            catobj = SysEventCat.objects.get(cat_ename = ename)
            return (catobj.cat_name,catobj.cat_ename,catobj.cat_id,catobj.cat_fid)
        except:
            return None
    if catDict:
        if catDict.has_key(ename):
            return catDict[ename]
    return None

def getCatIdByName(name):
    try:
        catobj = SysEventCat.objects.get(cat_name = name)
        return catobj.cat_id
    except:
        return None
    
def getCatNameById(catId):
    catDict = cache.get('catDict',None)
    if not catDict:
            cat_name = SysEventCat.objects.get(cat_id = catId).cat_name
            return cat_name
    else:        
        try:
            return catDict[catId][0]
        except:
            return ''
        
def getCatEnameById(catId):
    catDict = cache.get('catDict')
    if not catDict:
            cat_ename = SysEventCat.objects.get(cat_id = catId).cat_ename
            return cat_ename
    else:        
        try:
            return catDict[catId][1]
        except:
            return ''
    
def getCityNameById(cityId):
    districtIdDict = cache.get('districtIdDict',None)
    try:
        return districtIdDict[cityId][1]
    except:
        try:
            city_name = SysCommonDistrict.objects.get(district_id = cityId).district_name
            return city_name
        except:
            return None
    

def getTitleById(cityId):
    districtIdDict = cache.get('districtIdDict',None)
    try:
        return districtIdDict[cityId][2]
    except:
        try:
            title = SysCommonDistrict.objects.get(district_id = cityId).title
            return title
        except:
            return None


def getCityPyBySession(request):
    cityPy = request.session.get('city_py',False)
    return cityPy
    
def getVenueById(venueId):
    venueDict = cache.get('venueDict')
    #print venueDict
    if not venueDict:
        return SysVenue.objects.get(venue_id = venueId).venue_title
    else:
        if venueDict.has_key(venueId):
            return venueDict[venueId]
    return None
    
def getPicSource(img,event_cat):
    if not img:
        return 'http://pic.huodongjia.com' + '/img/default'+event_cat+'.jpg'
    if img[0] != '/':
        img = '/'+img
    return 'http://pic.huodongjia.com'+img
    
def resolveContent(html_content):
    content_parts = []        
    soup = BeautifulSoup(html_content.replace('\n','</br>'))
    for tag in soup.findAll('img'):
        tag['class'] = 'img-responsive'
        if 'http' not in tag['src']:
            tag['src'] = 'http://pic.huodongjia.com'+tag['src']    
    for item in soup.findAll('h2'):
        parts = ''
        #content_parts[str(item.next).strip()] = ''
        cmd = item.nextSibling
        while cmd and '<h2>' not in str(cmd):
            #content_parts[str(item.next).strip()] += str(cmd).strip()
            parts += str(cmd).strip()
            cmd = cmd.nextSibling
        if parts:
            html_parser = HTMLParser.HTMLParser()
            txt = html_parser.unescape(item.text)
            content_parts.append((txt, parts))
    return content_parts

def cityId2Pinyin(cityId):
    try:
        pinyin = SysCommonDistrict.objects.get(district_id = cityId).title
        return pinyin
    except:
        return False
    
def sendMail(sub,content,to_list=['252925359@qq.com','241617467@qq.com','1010478998@qq.com','9682539@qq.com','276753659@qq.com']):
    #设置服务器，用户名、口令以及邮箱的后缀
    mail_host="smtp.exmail.qq.com"
    mail_user="order@veryevent.com"
    mail_pass="ve2013"
    msg =MIMEText(content)
    msg['Subject'] = sub
    msg['to'] = ';'.join(to_list)
    msg['From'] = mail_user
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        #s.esmtp_features["auth"]="LOGIN PLAIN"
        s.login(mail_user,mail_pass)
        for to in to_list:
            s.sendmail(mail_user, to, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
    
def dic2text(dic):
    res = ''
    for key,value in dic.items():
        if key == 'csrfmiddlewaretoken':
            continue
        res += key+':'+value+'\n'   
    return res.encode('utf-8')

def getCityNameByIp(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    #print 'ip=',ip
    locApiUrl = 'http://api.map.baidu.com/location/ip?ak=Te0lHkIjEpurR7H2Ykz5oVaA&ip=%s&coor=bd09ll'%ip
    rp = urllib2.urlopen(locApiUrl).read()
    try:
        jsondic = eval(rp)
        content = jsondic.get('content',False)
        if content:
            address_detail = content.get('address_detail',False)
            if address_detail:
                city = address_detail.get('city_code',False)
                if city:
                    return city
        return False
    except:
        return False
    
def getEventHead(event):
    
    catId = event['event_cat1']
    
    new_event = NewEventTable.objects.filter(old_event_id=event['event_id'])
    keyword = ''
    title = ''
    des = ''
    if new_event:
        new_event = new_event[0]
        seo = new_event.seo
        if seo:
            from dahuodong.models import singers
            names = [item.name for item in singers.objects.all()]
            s_name = ''
            for name in names:
                if name in event['event_name']:
                    s_name = name
                    break
                
            eventVenue = event['event_venue']
            if None == event['event_venue']:
                eventVenue = ''
                
            title = seo.title.replace('(city)', event['district_name']).replace('(name)', event['event_name']).replace('(year)',event['event_begin_time'].split('-')[0]).replace('(singer)',s_name)
            keyword = seo.keywords.replace('(city)', event['district_name']).replace('(name)', event['event_name']).replace('(year)',event['event_begin_time'].split('-')[0]).replace('(singer)',s_name)
            des = seo.description.replace('(city)', event['district_name']).replace('(name)', event['event_name']).replace('(year)',event['event_begin_time'].split('-')[0]).replace('(month)',event['event_begin_time'].split('-')[1]).replace('(day)',event['event_begin_time'].split('-')[2]).replace('(venue)',eventVenue).replace('(singer)',s_name)
    
    if not keyword:
        keyword = u'%s'%event['event_name']
        
    if not des:
        if event['event_content']:
            des = BeautifulSoup(event['event_content'][0][1]).text[0:100]
        else:
            des = u'精彩活动尽在活动家'
        h = HTMLParser.HTMLParser()
        des = h.unescape(des)
        
    if not title:
        if catId == 1:
            title = u'%s%s【门票-报名-参会-购票-买票】_活动家'%(event['event_name'],event['district_name'])
        elif catId == 2:
            title = u'%s【打折票-折扣票-买票】%s演出_活动家'%(event['event_name'],event['district_name'])
        elif catId == 3:
            title = u'%s【门票-订票-价格-买票】%s特色旅游_活动家'%(event['event_name'],event['district_name'])
        elif catId == 4:
            title = u'%s【报名】公开课培训_活动家'%event['event_name']
        elif  catId == 5:
            title = u'%s【参展-展位预定-费用】_活动家'%event['event_name']
        elif catId == 6:
            title = u'%s【门票-报名】%s同城活动_活动家'%(event['event_name'],event['district_name'])
        else:
            pass
        
        
    head = {'title':title,
          'keywords':keyword,
          'description':des
          }

    
    return head


def getListHead(city_name,catEname,date):
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
        try:
            cat_seo = SysEventCat.objects.get(cat_ename = catEname).cat_seo
        except:
            return {'title':u'会议网_活动网_公开课培训_%s展会_活动家'%city_name,
                 'keywords':u'会议网,活动网,商务活动,公开课培训,%s展览,%s展会,%s会展,%s会议'%(city_name,city_name,city_name,city_name),
                 'description':u'活动家网www.huodongjia.com为你提供会议报名，会展参展，公开课报名服务。服务热线:400-003-3879'
                 }
        
        head_list = cat_seo.split('[|]')
        if len(head_list) == 3:
            head = {'title':head_list[0].replace('XX',city_name).replace(u'大活动',u'活动家'),
                    'keywords':head_list[1].replace('XX',city_name).replace(u'大活动',u'活动家'),
                    'description':head_list[2].replace('XX',city_name).replace(u'大活动',u'活动家')
                    }
        else:
            head = {'title':u'会议网_活动网_公开课培训_%s展会_活动家'%city_name,
                 'keywords':u'会议网,活动网,商务活动,公开课培训,%s展览,%s展会,%s会展,%s会议'%(city_name,city_name,city_name,city_name),
                 'description':u'活动家www.huodongjia.com为你提供会议报名，会展参展，公开课报名服务。服务热线:400-003-3879'
                 }
    return head

def search(keyword):
    #import logging
    #log = logging.getLogger('XieYin.app')  
    #log.debug('enter corseek')
    cl = sphinxapi.SphinxClient()
    cl.SetServer('10.10.64.15',9312)
    #cl.SetConnectTimeout(3)
    cl.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED)
    cl.SetLimits(0,100)
    res = cl.Query(keyword,'*')
    
    if not res:
        return []
    
    if res.has_key('matches'):
        return [match["id"] for match in res['matches']]
    return []



#begin cache for table sys_common_district
def constructDistrict():
    cityList = SysCommonDistrict.objects.filter(level=2)
    baiDuCodeDict = dict()
    districtIdDict = dict()
    titleDict = dict()
    venueDict = dict()
    dvenueDict = dict()
    for cityObj in cityList:
        baiDuCodeDict[cityObj.baidu_code] = (cityObj.district_id,cityObj.district_name,cityObj.title)
        districtIdDict[cityObj.district_id] = (cityObj.district_id,cityObj.district_name,cityObj.title)
        titleDict[cityObj.title] = (cityObj.district_id,cityObj.district_name,cityObj.title)
    venueList = SysVenue.objects.all()
    for venue in venueList:
        venueDict[venue.venue_id] = venue.venue_title
    catDict = dict()
    catEDict = dict()
    catList = SysEventCat.objects.all()
    for cat in catList:
        catDict[cat.cat_id]= (cat.cat_name,cat.cat_ename,cat.cat_id)
        catEDict[cat.cat_ename] = (cat.cat_name,cat.cat_ename,cat.cat_id,cat.cat_fid)
    return baiDuCodeDict,districtIdDict,titleDict,venueDict,catDict,catEDict

def getDictVal(varDict, key):
    if varDict.has_key(key):
        return varDict[key]
    return None

def doGetCityObj(cacheKey, searchVal):
    varDict = cache.get(cacheKey)
    if varDict:
        return getDictVal(varDict,searchVal)
    else:
        baiDuCodeDict,districtIdDict,titleDict,venueDict,catDict,catEDict = constructDistrict()
        cache.set('baiDuCodeDict',baiDuCodeDict,86400)
        cache.set('districtIdDict',districtIdDict,86400)
        cache.set('titleDict',titleDict,86400)
        cache.set('venueDict',venueDict,86400)
        cache.set('catDict',catDict,86400)
        cache.set('catEDict',catEDict,86400)
        if 'baiDuCodeDict' == cacheKey:
            varDict = baiDuCodeDict
        elif 'districtIdDict' == cacheKey:
            varDict = districtIdDict
        else:
            varDict = titleDict
        return getDictVal(varDict,searchVal)

def getCityObjFromBaiDuCode(baiducode):
    return doGetCityObj('baiDuCodeDict', baiducode)

def getCityObjFromTitle(title):
    return doGetCityObj('titleDict', title)

def getCityObjFromId(id):
    return doGetCityObj('districtIdDict', id)
#end cache for table sys_common_district

#begin cache for table sys_event_cat
def doConstructCat(catObj, catDict, catIdMap, catNameMap, pid):
    catDict['catname'] = catObj.cat_name
    catDict['catename'] = catObj.cat_ename
    catIdMap[catObj.cat_id_map] = (catObj.cat_name,catObj.cat_id_map,pid,catObj.cat_ename)
    catNameMap[catObj.cat_ename] = (catObj.cat_name,catObj.cat_id_map,pid,catObj.cat_ename)
    
def updateChildRec(childRec, catDict):
    catDict['child'] = childRec

def constructCat():
    catNameMap = dict()
    catIdMap = dict()
    catParent_list = PubEventCat.objects.filter(cat_fid = 0).order_by('cat_order')
    catLv1List = []
    catLv2List = []
    catLv3List = []
    i= 0
    for catParent in catParent_list:
        fircatDict = dict()
        doConstructCat(catParent, fircatDict, catIdMap, catNameMap,0)
        catChild_list = PubEventCat.objects.filter(cat_fid = catParent.cat_id).order_by('cat_order')
        secChildRec = []
        for catChild in catChild_list:
            secatDict = dict()
            doConstructCat(catChild,secatDict,catIdMap,catNameMap,catParent.cat_id_map)
            thirdcatChild_list = PubEventCat.objects.filter(cat_fid = catChild.cat_id).order_by('cat_order')
            thirdChildRec = []
            for thirdcatChild in thirdcatChild_list:
                thcatDict = dict()
                doConstructCat(thirdcatChild,thcatDict,catIdMap,catNameMap,catChild.cat_id_map)
                thirdChildRec.append(thcatDict)
                catLv3List.append(thcatDict)
            updateChildRec(thirdChildRec,secatDict)
            secChildRec.append(secatDict)
            catLv2List.append(secatDict)
        updateChildRec(secChildRec,fircatDict)
        catLv1List.append(fircatDict)
    return catLv1List,catLv2List,catLv3List,catIdMap,catNameMap

def doConstructCatUrl(city,cat,date,lv):
    tmp = dict()
    tmp ['catename'] = lv['catename']
    tmp ['catname'] = lv['catname'] 
    tmp ['caturl'] = '/'+city+'/'+lv['catename']+'/'
    tmp['flag'] = 'false'
    if cat == lv['catename'] :
        tmp['flag'] = 'true'
    return tmp

def constructCatUrl(city,cat,date):
    catLv1List = cache.get('cat_level1')
    catLv2List = cache.get('cat_level2')
    catLv3List = cache.get('cat_level3')
    if catLv1List and catLv2List and catLv3List:
        pass
    else:
        catLv1List,catLv2List,catLv3List,catIdMap,catNameMap = constructCat()
        cache.set('cat_level1',catLv1List,86400)
        cache.set('cat_level2',catLv2List,86400)
        cache.set('cat_level3',catLv3List,86400)
        cache.set('cat_idmap',catIdMap,86400)
        cache.set('cat_namemap',catNameMap,86400)
    tCat = []
    for lv1 in catLv1List:
        fircatDict = doConstructCatUrl(city,cat,date,lv1)
        lv2List = []
        for lv2 in lv1['child']:
            seccatDict = dict()
            seccatDict = doConstructCatUrl(city,cat,date,lv2)
            lv3List = []
            for lv3 in lv2['child']:
                thircatDict = doConstructCatUrl(city,cat,date,lv3)
                lv3List.append(thircatDict)
            updateChildRec(lv3List,seccatDict)
            lv2List.append(seccatDict)
        updateChildRec(lv2List,fircatDict)
        tCat.append(fircatDict)
    return tCat

def getCatENamefromID(catt):
    catIdMap = cache.get('cat_idmap')

    if catIdMap and catIdMap.has_key(catt):
        return catIdMap[catt][3]
    return None

def constructNavigationUrl(city,catt):
    catNameMap = cache.get('cat_namemap')
    catIdMap = cache.get('cat_idmap')
    navigationList = []
    if catNameMap and catIdMap:
        while True:
            try:
                catObj = catNameMap[catt]
                navigationDict = dict()
                navigationDict['catname'] = catObj[0]
                navigationDict['caturl'] = '/'+city+'/' + catObj[3]+'/'
                navigationList.append(navigationDict)
                catt = catIdMap[catObj[2]][3]
            except:
                break
    navigationDict = dict()
    navigationDict['catname'] = '首页'
    navigationDict['caturl'] = '/'
    navigationList.append(navigationDict)
    navigationList.reverse()
    return navigationList

def captcha(func): 
    def _is_captcha_right(request,*arg):
        if not request.session.get('captcha',False):
            return render_to_response('base_error.html',{'error_msg':u'验证码错误'})
        if not request.POST.get('captcha',False):
            return render_to_response('base_error.html',{'error_msg':u'请输入验证码'})
        if request.session['captcha'].lower() == request.POST['captcha'].lower():
            return func(request,*arg)
        else:
            return render_to_response('base_error.html',{'error_msg':u'验证码错误'})
    return _is_captcha_right

    
@captcha
def saveSuggestion(request,eventId,eventName):
    try:
        if request.method == 'POST':
            cds = request.POST
            if cds.get('msg_type') != 'suggestion':
                return False
            
            if cds.get('suggestion',False) and cds.get('where',False) and cds.get('phone',False):
                timeNow = time.time()
                msg_content = cds.get('where','')+'\n'+cds.get('suggestion','')
                SysOrderMessage.objects.create(event_id = eventId,
                                               event_name = eventName,
                                               msg_tel = cds.get('phone',''),
                                               msg_content = msg_content,
                                               msg_addtime = timeNow,
                                               type=1,
                                               ) 
                subject ='活动家-新的纠错,活动名:%s'%eventName.encode('utf-8')
                content = '客户姓名:%s\n联系邮箱:%s\n联系电话:%s\n活动id:%s\n活动名:%s\n活动链接:%s\n纠错内容:%s\n纠错时间:%s'%(cds.get('name','').encode('utf-8'),
                                                                                                   cds.get('email','').encode('utf-8'),
                                                                                                   cds.get('phone','').encode('utf-8'),
                                                                                                   eventId,
                                                                                                   eventName.encode('utf-8'),
                                                                                                   'http://www.huodongjia.com/event-%s.html'%eventId,
                                                                                                   msg_content.encode('utf-8'),
                                                                                                   time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timeNow))
                                                                                                   ) 
                sendMail(subject,content)
                return True
            else:
                return False
        else:
            return False
    except Exception,e:
        print e
        return False
    
    

@captcha
def saveConsult(request,eventId,eventName):
    try:
        if request.method == 'POST':
            cds = request.POST
            if cds.get('msg_type') != 'consult':
                return False
            if cds.get('name',False) and (cds.get('email',False) or cds.get('phone',False)):
                timeNow = time.time()
                SysOrderMessage.objects.create(event_id = eventId,
                                               event_name = eventName,
                                               msg_name = cds.get('name',''),
                                               msg_tel = cds.get('phone',''),
                                               msg_email = cds.get('email',''),
                                               msg_content = cds.get('content',''),
                                               msg_addtime = timeNow
                                               ) 
                subject ='活动家-留言咨询,活动名:%s,客户:%s'%(eventName.encode('utf-8'),cds.get('name','').encode('utf-8'))
                content = '活动id:%s\n活动链接:http://www.huodongjia.com/event-%s.html\n活动名:%s\n'%(eventId,eventId,eventName.encode('utf-8'))+dic2text(cds)+'留言时间:%s'%time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timeNow)) 
                sendMail(subject,content)
                return True
            else:
                return False
        else:
            return False
    except Exception,e:
        print e
        return False
