#coding:utf-8
from django.http import HttpResponse
from django.utils import simplejson as json
from LifeApi.functions import getcat,getTheme,getCity,FindEvent,getevent,dic2text,getCatArticle
from LifeApi.common import getPageAndOffset,search,sendMail,ip_Filter,SendOrderMsg,SendRegisterMsg,NewAppEvent,get_time_line,replaceCharEntity, find_img
import datetime,time
from LifeApi.models import feelnum,NewEventTag,NewOrder,NewEventTable,VisitRecord
from django.db import connection
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from spot.models import SysSpotEvent
from user_activity.models import UserInfo 
from User.models import Customer
from django.shortcuts import render_to_response
from bs4 import BeautifulSoup
import re
import logging
log = logging.getLogger('XieYin.app')  

def tag_hot(request):
    cds = request.GET
    (page,offset) = getPageAndOffset(cds)

    tag=NewEventTag.objects.order_by('-hot','-id')[offset*(page-1):offset*page]
    key=''
    for ta in tag:
        if key:
            key+='/'
        key+=ta.name
        
    return HttpResponse(json.dumps({"code":1,"msg":"Request is successful","keyword":key}), content_type="application/json")
 

def SearchKey(request):
    cds = request.GET
    keyword = cds.get('keywords',None)
    cityid = cds.get('city',None)
    p={}
    p['code']=1

    p['cat']=getcat(4)
    p['city']=getCity()
    if not keyword:
        p['msg']='keyword Fail'
        return HttpResponse(json.dumps(p), content_type="application/json")
    if len(keyword) > 20:
        p['msg']='keyword Fail'
        return HttpResponse(json.dumps(p), content_type="application/json")
    else:
        #events_lis = mc.get(keyword+'_search_lis')
        keyword= keyword.replace('/',' ')
        keyword= keyword.replace(',',' ')
        events_lis = cache.get('_'.join(keyword.split())+'_search_lis')
            
        p['code']=1
        p['msg']='Request is successful'
        p['keys']=keyword
        p['list'] =[]

        if not events_lis:
            ids=[]
            for key in keyword.split():
                ids.extend(search(key))
            if ids:
                
                try:
                    tag=NewEventTag.objects.get(name=keyword)
                    tag.hot=tag.hot+1
                    tag.save()
                except:
                    try:
                        NewEventTag.objects.create(name=keyword,hot=1)
                    except:
                        pass
                
                
                cache.set('_'.join(keyword.split())+'_search_lis',events_lis,300)
                events_lis = feelnum.objects.filter(event__old_event__in = ids)#.order_by('district_id='+str(district_id),'event_begin_time')
                
                if cityid:
                    try:
                        events_lis = events_lis.filter(event__city__in=cityid.split(','))
                    except:
                        pass
                p['list'] = [getevent(item.event.old_event_id) for item in events_lis[0:10]]
 
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
            

    
def DateApi(request):
    p={}
    p['code']=1
    p['msg']='Request is successful'    
    p['list']=[]
    cds = request.GET
    date = cds.get('date',None)
    try:
        day = int(cds.get('day',10))
    except:
        p['code']=0
        p['msg']='url err'
        response = json.dumps(p)
        return HttpResponse(response, mimetype="application/json")
    orders = cds.get('order',None)
    cityid = cds.get('cityid',None)
    price_type = cds.get('price_type',None)
    #random = cds.get('random',None)
    new = cds.get('new',None)
    if not date:
        date=datetime.date.today()
    else:
        try:
            date=datetime.datetime.strptime( date, "%Y-%m-%d").date()
        except:            
            try:
                date = time.strptime(date,"%Y-%m-%d %H:%M:%S")
                date=datetime.datetime(* date[:6])
            except:
                date=datetime.date.today()
         
    oneday = datetime.timedelta(days=1)
    


    for da in range(day):        
        info={}
        info['daytitle']=''
        info['events']=[]
        
        if cityid:
            fe0 = feelnum.objects.filter(event__city=cityid)
        else:
            fe0 = feelnum.objects
        
        fe=fe0.filter(showtime=date).order_by('-feelnum').distinct()


        if not fe.count():
            if orders:
                fe1=fe0.filter(showtime__lt=date).order_by('-showtime')
            else:
                fe1=fe0.filter(showtime__gt=date).order_by('showtime')
            #fe1.query.group_by=['showtime']
            try:
                date=fe1[0].showtime
                
                fe=fe0.filter(showtime=date).order_by('-feelnum').distinct()
            except:
                break
        
        info['date']=datetime.datetime.strftime(date,'%Y-%m-%d')
        if orders:
            date=date-oneday
        else:
            date=date+oneday
 
           
        #info['count']=fe.count()
        
        for ev in fe:
            event=getevent(ev.event.old_event_id,new,cds.get('version',''))
            info['events'].append(event)
            if not info['daytitle']:
                info['daytitle']=event['feeltitle'] if event['feeltitle'] else ''
        #cou=len(info['events'])    


            
            

        
        if da==0 and '1.2' in cds.get('version',''):
            info['events'].append(getevent(245504,new,cds.get('version','')))
        p['list'].append(info)
        #p['category']=getcat()           

        p['newdate']=datetime.datetime.strftime(date,'%Y-%m-%d')

        
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

# DateApi新版 测试中
def DateApiT(request):
    p={}
    p['code']=1
    p['msg']='Request is successful'
    p['list']=[]
    cds = request.GET
    date = cds.get('date',None)
    try:
        day = int(cds.get('day',10))
    except:
        p['code']=0
        p['msg']='url err'
        response = json.dumps(p)
        return HttpResponse(response, mimetype="application/json")
    orders = cds.get('order',None)
    cityid = cds.get('cityid',None)
    price_type = cds.get('price_type',None)
    #random = cds.get('random',None)
    new = cds.get('new',None)
    if not date:
        date=datetime.date.today()
    else:
        try:
            date=datetime.datetime.strptime( date, "%Y-%m-%d").date()
        except:
            try:
                date = time.strptime(date,"%Y-%m-%d %H:%M:%S")
                date=datetime.datetime(* date[:6])
            except:
                date=datetime.date.today()

    oneday = datetime.timedelta(days=1)



    for da in range(day):
        info={}

        fe0 = get_time_line(0, city_id = cityid, new = False)

        fe = []
        date_str = datetime.datetime.strftime(date, '%Y-%m-%d')
        if fe0.has_key(date_str):
            fe = fe0[date_str]

        if not fe:
            date_str_list = []
            for cur_date_str in fe0.keys():
                cur_date = datetime.datetime.strptime(cur_date_str, "%Y-%m-%d").date()
                if orders:
                    if cur_date < date:
                        date_str_list.append(cur_date_str)
                else:
                    if cur_date > date:
                        date_str_list.append(cur_date_str)
            if orders:
                date_str_list.sort(reverse=True)
            else:
                date_str_list.sort()

            try:
                candidate_date_str = date_str_list[0]

                fe = fe0[candidate_date_str]
            except IndexError:
                break

        info = fe[0]
        info['events'] = []

        if orders:
            date=date-oneday
        else:
            date=date+oneday

        for ev in fe:
            event = getevent(ev['id'], new, cds.get('version',''))
            info['events'].append(event)

        if da==0 and '1.2' in cds.get('version',''):
            info['events'].append(getevent(245504,new,cds.get('version','')))
        p['list'].append(info)
        p['newdate']=datetime.datetime.strftime(date,'%Y-%m-%d')


    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def CatApi(request):
    cds = request.GET
    lastdate = request.GET.get('lastdate',None)
    if lastdate == '0':
        lastdate=None
    (page,offset) = getPageAndOffset(cds)
    city=request.GET.get('cityid',None)
    #city=None
    p={}
    p['code']=1
    p['msg']='Request is successful'      
    #if not lastdate: 
    p['list']=getcat(3,None,city,page,offset)
    #else:
    if lastdate:
        p['count']=getcat(3,lastdate,city)
    else:
        p['count']=0

    p['lastdate']=0
    if p.has_key('list'):
        if len(p['list'])>0 :
            if not page>1:
        
                p['lastdate']=p['list'][0]['begin_time']
        
            
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

@csrf_exempt
def CustomMessage(request):
    p={}
    p['code']=0
    
    if request.method != 'POST':
        p['msg']='Only POSTs are allowed'   
        return HttpResponse(json.dumps(p), content_type="application/json")
    if not ip_Filter(request,10):
        p['msg']='The request is limited'   
        return HttpResponse(json.dumps(p), content_type="application/json")
    
    phone = request.POST.get('phone','')
    email = request.POST.get('email','')   
    content=request.POST.get('content','') 
    con={
    'content':content,
    'work':request.POST.get('work','') ,
    'need':request.POST.get('need','') ,
    'price':request.POST.get('price','') ,
    'other':request.POST.get('other','') ,
    'username':request.POST.get('username','') ,
    'usersex':request.POST.get('usersex','') ,
    'userage':request.POST.get('userage','') ,
    'city':request.POST.get('city','') ,
    }
    con_str=''
    for k,v in con.items():
        con_str+='%s:%s' % (k,v)
    if not phone and not email :
        p['msg']='Incomplete information'
        return HttpResponse(json.dumps(p), content_type="application/json")
    p['msg']='Request is successful'
    p['code']=1
    subject=u'生活家私人定制，邮件提醒  %s %s' % (phone,email)
    cont=u'私人定制客户留言\r\n'
    cont+=u'手机:%s\r\n' % phone
    cont+=u'邮箱:%s\r\n' % email
    cont+=u'内容:%s\r\n' % con_str
    log.debug(cont)
    sendMail(subject.encode('utf-8'),cont.encode('utf-8'),['shaye7@qq.com','252925359@qq.com','516139718@qq.com'])
    
    return HttpResponse(json.dumps(p), content_type="application/json")
            
def HomeApi(request):
    p={}
    p['code']=1
    p['msg']='Request is successful'
    p['theme']=getTheme()
    p['city']=getCity()
    p['category']=getcat()
    callback = request.GET.get('callback',None)
    if callback:
        response = '%s(%s)' % (callback,json.dumps(p))
    else:    
        response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
#往期数据
def PreviousEventApi(request):
    p={}
    try:
        lastid = int(request.GET.get('last_id',0))
        num = int(request.GET.get('num',5))
        
    except:
        
        p['code']=0
        p['msg']='Get err'        
        
        response = json.dumps(p)
        return HttpResponse(response, mimetype="application/json")        
    
    p['code']=1
    p['msg']='Request is successful'
    p['list']=[]
    p['last_id']=0
    

    showtime_Week = get_time_line(dict_type=2,city_id=request.GET.get('city',None),new=request.GET.get('new',None))
    week_len=len(showtime_Week)
    if lastid+1<week_len:
        
        i=0
        for we in showtime_Week[lastid:week_len]:
            p['last_id']=showtime_Week.index(we)
            i+=1
            if i>num:
                break
            
            
            p['list'].append({'week_id':week_len-p['last_id'],'data':we})
        
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def EventApi(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({"code":0,"msg":"Only GETs are allowed","list":[]}), content_type="application/json")
    cds = request.GET
    catid = cds.get('catid',None)
    cityid = cds.get('cityid',None)
    price_type = cds.get('price_type',None)
    people=cds.get('people',None)
    money_min=cds.get('money_min',None)
    money_max=cds.get('money_max',None)
    random=cds.get('random',None)

    '''
    if  not catid and not cityid:
        return HttpResponse(json.dumps({"code":0,"msg":"Only GETs are allowed","list":[]}), content_type="application/json")
    '''
    (page,offset) = getPageAndOffset(cds)
    p={}
    p['code']=1
    p['msg']='Request is successful'
    p['list']=FindEvent(catid,cityid,people,price_type,money_min,money_max,random,page=page,offset=offset)
    if catid:
        p['text']=getCatArticle(catid)
    #p['sql']=connection.queries
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
def EventInfoApi(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({"code":0,"msg":"Only GETs are allowed","list":[]}), content_type="application/json")
    cds = request.GET 
    eventid = cds.get('eventid',None)
    p={}
    p['code']=1
    p['msg']='Request is successful'
    # always use the newest version:for now, it is v1.2
    p['data']=getevent(eventid,cds.get('new',False), '1.2')
    p['data']=test_xml(eventid)
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def test_xml(id):
    event = {}
    ca = NewAppEvent(None,id)
    cont = ca['event_content'][0][1]
    cont = cont.replace('\n', '').replace('\r', '').replace('\r\n', '')
    event['mobileU'] = cont
    
    soup = BeautifulSoup(cont)

    # remove tag and its contents
    soup = unwrap_tag(soup, ['br', 'span','pre'])

    # rename tag: div -> p
    for i in soup.find_all('div'):
        i.name = 'p'

    # deal with the 'style' attributes in <img>
    tag_img = soup.find_all('img')
    for i in tag_img:
        try:
            couple = get_style_couple(i['style'].replace('px', ''))
            for attr, val in couple:
                i[attr] = val
            del i['style']
        except KeyError:
            pass
    
    #soup_fmt = soup.prettify(formatter=None)
    #soup_fmt = replaceCharEntity(str(soup))
    #pattern = re.compile(r"<p>img\d+\</p>")
    #soup=replaceCharEntity(str(soup))
    #soup_fmt = re.sub(ur"<p>img\d+\</p>" , find_img, soup )
    
    #try:
    soup_fmt = re.sub(ur"<p>img\d+\</p>" , find_img,replaceCharEntity(str(soup)) )
    #except:
    #    soup_fmt =replaceCharEntity(str(soup))
    
    soup_fmt = '<body>' + soup_fmt + '</body>'

    # convert <img.../> tag into <img...></img> 
    soup_fmt = soup_fmt.replace('/>', '></img>')
    #soup_fmt = re.sub('<img[^>]+>', lambda x: x.group() + '</img>', soup_fmt)

    event['mobileURL'] = soup_fmt.replace('\r', '').replace('\n', '')

    return event

def unwrap_tag(html, tag_list=[]):
    if not isinstance(tag_list, (list, tuple)):
        tag_list = [tag_list]
    for tag in tag_list:
        for html_tag in html.find_all(tag):
            html_tag.unwrap()
    return html

def get_style_couple(str_in):
    return re.findall('([\w-]+) ?: ?([\w\.-]+);?', str_in)

def remove_tag(html, tag_list=[]):
    '''
    html is bs4.BeautifulSoup
    '''
    if not isinstance(tag_list, (list, tuple)):
        tag_list = [tag_list]
    for tag in tag_list:
        for html_tag in html.find_all(tag):
            html_tag.decompose()
    return html


def submitOrder(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({"code":0,"msg":"Only GETs are allowed","list":[]}), content_type="application/json")

    cds = request.GET
    price =cds['price']
    price = round( float(price),2)
    eventId = int(cds['eventid'])
    event=NewAppEvent(None,eventId)
    '''
    pr_ok=False
    for i in range(len(event['price_unit_info'])):
        pr1=round(float(event['price_unit_info'][i]['price'])*float(event['price_unit_info'][i]['discount']),1)
        if price  is pr1:
            pr_ok=True
            break
    if not pr_ok:
        return HttpResponse(json.dumps({"code":0,"msg":"price is wrong %s,%s" % (price,pr1),"list":[]}), content_type="application/json")

    '''

    import random 
    number = '%s%s'%(int(time.time()),random.randint(100,1000))
    if int(cds['amount']) < 1:
        return HttpResponse(json.dumps({"code":0,"msg":"amount must be bigger than 1","list":[]}), content_type="application/json")
    totalpay = float(price)*int(cds['amount']) 
    #print cds['payMode']
    
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    userid = cds.get('userid')
    if not userid:
        userid = 0
    else:
        userid = int(userid)
    try:
        NewOrder.objects.create(
                                order_number=number,
                                order_user_name=cds.get('name',''),
                                order_tel = cds.get('phone',''),
                                order_email = cds.get('email',''), 
                                order_totalpay = totalpay,
                                order_price = float(price),
                                order_amount = cds['amount'],
                                order_address = cds.get('address',''),
                                order_payment = 'alipay',
                                order_telphone = cds.get('phone',''),
                                order_pay_status = 0,
                                order_status = 0,
                                event_id = eventId,
                                event_name = event['title'],
                                city_title = event['district_name'],
                                order_reg_fields = 0,
                                order_addtime = time.time(),
                                order_addip = ip,
                                order_text = cds.get('message',''),
                                order_userid = userid,
                                event_to=4,
                                )
    except:
        return HttpResponse(json.dumps({"code":0,"msg":"err","list":[]}), content_type="application/json")
        
    subject = '来自闲时app的订单通知.客户:%s,电话:%s'%(cds.get('name','').encode('utf-8'),cds.get('mobilphone','').encode('utf-8'))
    content = '点单号:%s\n总价:%s\n活动链接:http://www.huodongjia.com/event-%s.html'%(number,totalpay,eventId)
    content += dic2text(cds)
    sendMail(subject,content)
    order = {
    'price':price,
    'order_id':number,
    'user_id':cds.get('userid',''),
    'addtime':int(time.time()),
    'name':cds.get('name',u'匿名'),
    'phone':cds['phone'],
    'address':cds.get('address',''),
    'message':cds.get('message',''),
    "total":totalpay,
    "amount":cds['amount'],
    "order_pay_status":u"未付款",
    "order_status":u"未处理",
    }
    
    eventdic = getevent(eventId)
    return HttpResponse(json.dumps({"code":1,"msg":u"下单成功","data":{'order':order,'event':eventdic}}), content_type="application/json")
        

def searchOrder(request):
    cds = request.GET
    key = cds.get('key')
    order_list = []
    data = cds['data'] 
    if key == 'user_id':
        order_list = NewOrder.objects.filter(order_userid = int(data))
    elif key == 'phone':
        order_list = NewOrder.objects.filter(order_tel = data)
    elif key == 'order_number':
        order_list = NewOrder.objects.filter(order_number = data)
    else:
        return HttpResponse(json.dumps({"code":0,"msg":'key error'}), content_type="application/json")
    
    list = []

    for item in order_list.order_by('-order_addtime'):
        order_pay_status="未付款"
        if item.order_pay_status == 20:
            order_pay_status = '已付款'
        elif item.order_pay_status == 30:
            order_pay_status = '退款'
        else:
            pass 
        
        order_status = '未处理'
        if item.order_status == 10:
            order_status = '正在处理'
        dicOrder = {
        'price':float(item.order_price),
        'order_id':item.order_number,
        'user_id':item.order_userid,
        'addtime':item.order_addtime,
        'name':item.order_user_name,
        'phone':item.order_tel,
        'address':item.order_address,
        'message':item.order_text,
        "total":float(item.order_totalpay),
        "amount":item.order_amount,
        "order_pay_status":order_pay_status,
        "order_status":order_status,
        }
        event =getevent(item.event_id)
        list.append({'order':dicOrder,'event':event})
    res = {'code':1,'message':'request success','list':list}
    return HttpResponse(json.dumps(res), content_type="application/json")

    
def collect(request,eventid):
    try:
        e=SysSpotEvent.objects.get(event_id=int(eventid))
            
        if VisitRecord.objects.filter(event_id = eventid).count():
            r = VisitRecord.objects.filter(event_id = eventid)[0]
            r.collection = r.collection+1
            r.save()
            collection = r.collection
        else:
            VisitRecord.objects.create(event_id=eventid,collection=1)
            collection = 1
           
        userid= request.GET.get('userid',False)
        if userid:
            try:
                u=UserInfo.objects.get(user_id=userid)
                
            except:
                
                u1=Customer.objects.get(id=userid)
                u=UserInfo.objects.create(user_id=userid,user_name=u1.name,user_cumulative=0)
                
                    
            
            u.event.add(e)
         
        res = {'code':1,'message':'request success','hot':collection}        
    except:
        res = {'code':2,'message':'err'}   
        
    #return HttpResponse(json.dumps(res), content_type="application/json")
    return HttpResponse(json.dumps(res), content_type="application/json")
    

def collect_del(request):
    userid= request.GET.get('userid',False)
    eventid= request.GET.get('eventid',False)
    try:        
        e=SysSpotEvent.objects.get(event_id=int(eventid))
            

        
        if userid:
            try:
                u=UserInfo.objects.get(user_id=userid)
            except:
                u1=Customer.objects.get(id=userid)
                u=UserInfo.objects.create(user_id=userid,user_name=u1.name,user_cumulative=0)
            #event.cat.remove(cat1)
            if e:
                u.event.remove(e)
         
        res = {'code':1,'message':'request success'}        
    except:
        
        
        res = {'code':2,'message':'err'}
        
    #return HttpResponse(json.dumps(res), content_type="application/json")
    return HttpResponse(json.dumps(res), content_type="application/json")
    
    
    '''
    
    eventid=int(eventid)
    event = NewEventTable.objects.get(old_event_id=eventid)
    if not event.hot:
        event.hot = 1
    else:
        event.hot = event.hot + 1
    event.save()
    return HttpResponse(json.dumps({'code':1,'message':'request success','hot':event.hot}), content_type="application/json")
    '''
def downloadapp(request, param):
    city_py = request.COOKIES.get('city_py',False)
    city = request.COOKIES.get('city',False)
    head = {'title':u'闲时客户端_闲时App下载',
              'keywords':u'闲时App下载',
             'description':u'闲时App下载'}
    
    if 0 != len(param):
        return render_to_response(param,{'head':head,'city':city,'city_py':city_py})
    else:
        return render_to_response('download.html',{'head':head,'city':city,'city_py':city_py})

def send_msg_text(request):
    #msg = u'您好,您的验证码%s,10分钟内有效,请及时校验【大活动网】'% (2111)
    #msg=u'您好测试,utf8短信[签名]'
    msg= u'您好，你在活动家(huodongjia.com)预订了极限运动活动，还未支付，请你尽快支付，我们好为你出票。你可以在huodongjia.com上查询订单号2121支付即可。谢谢！【闲时】'
    ph={'msg':msg,
        'flag':SendOrderMsg('18628175526',msg),
        }
    #SendOrderMsg('18628175526',msg)
    #getMsgU()
    #ph=[msg]
    response = json.dumps(ph)
    return HttpResponse(response, mimetype="application/json")    
# 针对优惠券接口重写的提交订单
def submitOrder_with_coupon(request, coupon_record):
    if request.method != 'GET':
        return HttpResponse(json.dumps({"code":0,"msg":"Only GETs are allowed","list":[]}), content_type="application/json")

    cds = request.GET
    price =cds['price']
    price = round( float(price),2)
    eventId = int(cds['eventid'])
    event=NewAppEvent(None,eventId)
    '''
    pr_ok=False
    for i in range(len(event['price_unit_info'])):
        pr1=round(float(event['price_unit_info'][i]['price'])*float(event['price_unit_info'][i]['discount']),1)
        if price  is pr1:
            pr_ok=True
            break
    if not pr_ok:
        return HttpResponse(json.dumps({"code":0,"msg":"price is wrong %s,%s" % (price,pr1),"list":[]}), content_type="application/json")

    '''

    import random
    number = '%s%s'%(int(time.time()),random.randint(100,1000))
    if int(cds['amount']) < 1:
        return HttpResponse(json.dumps({"code":0,"msg":"amount must be bigger than 1","list":[]}), content_type="application/json")
    totalpay = float(price)*int(cds['amount'])
    #print cds['payMode']

    # 使用了优惠券
    totalpay = coupon_record.cost

    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    userid = cds.get('userid')
    if not userid:
        userid = 0
    else:
        userid = int(userid)
    try:
        NewOrder.objects.create(
                                order_number=number,
                                order_user_name=cds.get('name',''),
                                order_tel = cds.get('phone',''),
                                order_email = cds.get('email',''),
                                order_totalpay = totalpay,
                                order_price = float(price),
                                order_amount = cds['amount'],
                                order_address = cds.get('address',''),
                                order_payment = 'alipay',
                                order_telphone = cds.get('phone',''),
                                order_pay_status = 0,
                                order_status = 0,
                                event_id = eventId,
                                event_name = event['title'],
                                city_title = event['district_name'],
                                order_reg_fields = 0,
                                order_addtime = time.time(),
                                order_addip = ip,
                                order_text = cds.get('message',''),
                                order_userid = userid,
                                event_to=4,
                                )
    except:
        return HttpResponse(json.dumps({"code":0,"msg":"err","list":[]}), content_type="application/json")

    subject = '来自闲时app的订单通知.客户:%s,电话:%s'%(cds.get('name','').encode('utf-8'),cds.get('mobilphone','').encode('utf-8'))
    content = '点单号:%s\n总价:%s\n活动链接:http://www.huodongjia.com/event-%s.html'%(number,totalpay,eventId)
    content += dic2text(cds)
    sendMail(subject,content)
    order = {
    'price':price,
    'order_id':number,
    'user_id':cds.get('userid',''),
    'addtime':int(time.time()),
    'name':cds.get('name',u'匿名'),
    'phone':cds['phone'],
    'address':cds.get('address',''),
    'message':cds.get('message',''),
    "total":totalpay,
    "amount":cds['amount'],
    "order_pay_status":u"未付款",
    "order_status":u"未处理",
    }

    # 记录order_number
    coupon_record.order_id = number
    coupon_record.save()

    eventdic = getevent(eventId)
    return HttpResponse(json.dumps({"code":1,"msg":u"下单成功","data":{'order':order,'event':eventdic}}), content_type="application/json")

