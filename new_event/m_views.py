#coding:utf-8

from admin_self.common import NewCatUrl,NewCity,NewformatEvent,event_city_cat,\
                                oldEventToNewEvent,find_cat_fid ,ip_Filter                           

from new_event.common import find_from_city
from new_event.showlist import showList

from django.http import Http404

from django.views.decorators.csrf import csrf_exempt
import  random,json
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response

from new_event.models import   NewEventTable,NewOrder,NewOrderMessage
from new_event.common import sendMail,SendOrderMsg,captcha
from django.template import RequestContext
from django.db.models import Q
from django.core.cache import cache
import time,re
from django.shortcuts import redirect


import logging
log = logging.getLogger('XieYin.app')  
def captcha_s(func):     
    def _is_captcha_right(request,*arg):
        if not request.POST.get('captcha',False):
            return  render_to_response('m_base_error.html',{'error_msg':u'请输入验证码'})
 
        if not request.session.get('captcha',False):
            return  render_to_response('m_base_error.html',{'error_msg':u'验证码错误'})
 
        if request.session['captcha'].lower() == request.POST['captcha'].lower():
            return func(request,*arg)
        else:
            return render_to_response('m_base_error.html',{'error_msg':u'验证码错误'})
    return _is_captcha_right
def Telcaptcha(func):    
    
    def _is_captcha(request,*arg):
        captcha = request.POST.get('captcha',False)
        tel = request.POST.get('mobilphone',False)
        
        p={}
        eventId = request.POST.get('event_id',False)
        if eventId:
            p['url']='http://m.huodongjia.com/event-%s' % (eventId)
        else:
            p['url']='http://m.huodongjia.com'
        
        if not captcha:
            p['error_msg']='请输入验证码'
            return render_to_response('m_base_error.html',p)
        if not tel:
            p['error_msg']='没有手机号'
            return render_to_response('m_base_error.html',p)
        
        try:
            if str(captcha) == str(cache.get(tel)):
                return func(request,*arg)
            else:
                p['error_msg']='验证码错误'
                return render_to_response('m_base_error.html',p)
        except:
            p['error_msg']='验证错误'
            return render_to_response('m_base_error.html',p)

    return _is_captcha
def indexPage(request,city=None):
    cityObj = find_from_city(request,city)
    tim=2015
    www={'id':2,'name':'互联网会','img':'http://pic.huodongjia.com/html5/pic/www.png?time=%s'%tim,'url':'/%s/it/' % cityObj[2] }
    jinrong={'id':6,'name':'金融会议','img':'http://pic.huodongjia.com/html5/pic/jinrong.png?time=%s'%tim,'url':'/%s/finance/'  % cityObj[2]}
    hospity={'id':23,'name':'医疗会议','img':'http://pic.huodongjia.com/html5/pic/hospity.png?time=%s'%tim,'url':'/%s/medical/'  % cityObj[2]}
    maer={'id':93,'name':'骑马运动','img':'http://pic.huodongjia.com/html5/pic/maer.png?time=%s'%tim,'url':'/tag/?keyword=骑马运动' }
    fly={'id':94,'name':'飞行体验','img':'http://pic.huodongjia.com/html5/pic/fly.png?time=%s'%tim,'url':'/tag/?keyword=飞行体验' }
    foot={'id':76,'name':'美食烹饪','img':'http://pic.huodongjia.com/html5/pic/foot.png?time=%s'%tim,'url':'/chengdu/food/'}
    child={'id':24,'name':'亲子活动','img':'http://pic.huodongjia.com/html5/pic/child.png?time=%s'%tim,'url':'/tag/?keyword=亲子活动'}
    snow={'id':24,'name':'滑雪活动','img':'http://pic.huodongjia.com/html5/pic/snow.png?time=%s'%tim,'url':'/tag/?keyword=滑雪活动'}
    
    hot_cat=[www,jinrong,hospity,maer,fly,foot,child,snow]
    
    m_list=event_city_cat(cityObj[0])
    response = render_to_response('m_home.html',{'city':cityObj[1],
                                           'city_id':cityObj[0],
                                           'city_py':cityObj[2],
                                           'hot_cat':hot_cat,
                                           'list':m_list[:5],
                                           },
                                           context_instance=RequestContext(request))
    response.set_cookie('city_id',cityObj[0])
    response.set_cookie('city_py',cityObj[2])
    response.set_cookie('city',cityObj[1].encode('utf-8'))
    response['Cache-Control'] = 'max-age=300'
    return response    

def showQ(request,query=False,template_name='q_showEvent.html'):
    event={}
    if query.isdigit():
        event= NewformatEvent(False,int(query),request.GET.get('new',False))        

    if not event.has_key('isshow'):
        return render_to_response('not.html',{'error_msg':u'没有该活动  '  })
  
    else:
        if not event['isshow'] in [1,8]:
            return render_to_response('not.html',{'error_msg':u'活动没有发布' })       


        note=None
        for con in event['event_content']:
            if con[0] in [u'购买须知']:
                note=con
                break

                
 
        body={'note':note,
              'event_id':event['event_id']
             }
        return render_to_response(template_name,body,context_instance=RequestContext(request))
def showCont(request,query=False,template_name='s_showEvent.html'):
    event={}
    if query.isdigit():
        event= NewformatEvent(False,int(query),request.GET.get('new',False))        

    if not event.has_key('isshow'):
        return render_to_response('not.html',{'error_msg':u'没有该活动  '  })
  
    else:
        if not event['isshow'] in [1,8]:
            return render_to_response('not.html',{'error_msg':u'活动没有发布' })       


        note=[]
        for i in range(len(event['event_content'])):
            event['event_content'][i]=(event['event_content'][i][0],event['event_content'][i][1].replace('<br>',''))
            if i is 0:                
                
                note.append(event['event_content'][i])
            elif event['event_content'][i][0] in  [u'行程安排']:
                note.append(event['event_content'][i])
        
                

        body={'note':note,
              'event_id':event['event_id'],
              'event_name':event['event_name']
              
             }
        return render_to_response(template_name,body,context_instance=RequestContext(request))
def showPage(request,query=False,template_name='m_event.html'): 
    event={}
    if query.isdigit():
        event= NewformatEvent(False,int(query),request.GET.get('new',False))        
 
    if not event.has_key('isshow'):
        return render_to_response('not.html',{'error_msg':u'没有该活动  '  })
  
    else:
        if not event['isshow'] in [1,8]:
            return render_to_response('not.html',{'error_msg':u'活动没有发布' })       

        city_t=event['district_title']
        city_n=event['district_name']
   

        qu=False
           
        for con in event['event_content']:
            if con[0]==u'常见问题':
                qu=True
                break
        if not qu:
            fid=find_cat_fid(NewCatUrl(2),event['catid'],city_t) 
            ark=False
            for f in fid:
                if f['article']:
                    for ar in f['article']:
                        if ar['name']==u'常见问题':
                            event['event_content'].append((ar['name'],ar['content'].replace('pic1.qkan.com','pic.huodongjia.com'),))
                            ark=True
                            qu=True
                            break
                if ark:
                    break


        new=False
        tran_rec_list =event_city_cat(None,event['catid'],new) 

        number=3
        
        
        l= len(tran_rec_list)-number
        if l<0:  
            b = event_city_cat(None,None,new )  
            #print b
            tran_rec_list.extend(b [:abs(l)] )
        #tran_rec_list =[]#  [formatEvent(item) for item in recommend_list[randloc:randloc+number]]

                        
                    
                
 
        body={'head':event['head'],
             'event':event,
             'list':tran_rec_list[:number],
             'city':city_n,
             'city_py':city_t,
             'navigationList':event['navigationList']}

        if event.has_key('cf'):
            body['cf']=event['cf']
        return render_to_response(template_name,body,context_instance=RequestContext(request))
         

def SearchKey_ajax(request):
    cds = request.GET
    keyword = cds.get('keyword',None)
    city = cds.get('city',None)
    cityObj = find_from_city(request,city)
    
    (page,offset) = getPageAndOffset(cds)
    p={}
    if not keyword:
        return HttpResponse(json.dumps({"code":0,"msg":"Only GETs are allowed","list":[]}), content_type="application/json")
    if len(keyword) > 20:
        return HttpResponse(json.dumps({"code":0,"msg":"keyword Fail","list":[]}), content_type="application/json")
    else:
        #events_lis = mc.get(keyword+'_search_lis')
        keyword= keyword.replace('/',' ')
        ids = cache.get('_'.join(keyword.split())+'_search_lis')
        
        p['code']=1
        p['msg']='Request is successful'
        p['keys']=keyword
        p['list'] =[]
        if not ids:
            ids = search(keyword)
        if ids:

            cache.set('_'.join(keyword.split())+'_search_lis',ids,300)
            events_lis = NewEventTable.objects.filter(old_event__in = ids)#.order_by('district_id='+str(district_id),'event_begin_time')
            
            if cityObj:
                events_lis = events_lis.filter(city=cityObj[0])
                
            start = (page-1)*offset
            end = page*offset
            p['list'] = [NewformatEvent(None,item.old_event_id) for item in events_lis[start:end]]
            p['page']=page+1

    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def SearchKey(request):
    cds = request.GET
    keyword = cds.get('keyword',None)
    city = cds.get('city',None)
 
    cityObj = find_from_city(request,city)
    (page,offset) = getPageAndOffset(cds)
    
    list_s=[]
    ids=None
    if not keyword:
        return render_to_response('not.html',{'list':list_s},context_instance=RequestContext(request))
        #return HttpResponse(json.dumps({"code":0,"msg":"Only GETs are allowed","list":[]}), content_type="application/json")
    if len(keyword) > 20:
        return render_to_response('not.html',{'list':list_s},context_instance=RequestContext(request))
        #return HttpResponse(json.dumps({"code":0,"msg":"keyword Fail","list":[]}), content_type="application/json")
    else:
        #events_lis = mc.get(keyword+'_search_lis')
        keyword= keyword.replace('/',' ')
        ids = cache.get('_'.join(keyword.split())+'_search_lis')
        

        if not ids:
            ids = search(keyword)
            
        if ids:

            cache.set('_'.join(keyword.split())+'_search_lis',ids,300)
            events_lis = NewEventTable.objects.filter(old_event__in = ids)#.order_by('district_id='+str(district_id),'event_begin_time')
            
            if cityObj:
                events_lis = events_lis.filter(city=cityObj[0])
            
            start = (page-1)*offset
            end = page*offset
            list_s = [NewformatEvent(None,item.old_event_id) for item in events_lis[start:end]]

    #response = json.dumps(p)
    #return HttpResponse(response, mimetype="application/json")
    head = {'title':u'%s_门票预订_报名参加_活动网_活动家'%(keyword),
              'keywords':u'%s,门票,报名,活动网,活动家'%(keyword),
             'description':u'找%s相关近期活动，就上【活动家www.huodongjia.com】。活动家为您提供%s相关活动信息，包含门票预订、报名参加、价格咨询等全方位服务，实时更新%s最新活动，随时随地轻松购票！服务热线:400-003-3879'%(keyword,keyword,keyword)}

    if len(list_s)>0:
        return render_to_response('m_tag.html',{'head':head,'city':request.COOKIES.get('city',u'北京'),'city_py':request.COOKIES.get('city_py','beijing'),'list':list_s,'len_list':len(list_s),'keyword':keyword,'page':page,'offset':offset},context_instance=RequestContext(request))
    else:
        return render_to_response('not.html',{'list':list_s},context_instance=RequestContext(request))
        
def list_ajax(request,city=None,cat=None,date=None,offset=1):
    date = request.GET.get('dat')
    offset = request.GET.get('page')
    p={}
    if not city: city='beijing'
    if not cat: cat = 'all'
    if not date: date = 'latest'
    if not offset: 
        offset = 1 
    else: 
        offset = int(offset)    
    listDict = showList(request,city,cat,date,offset)
    p['code']=1
    p['msg']='Request is successful'
    p['navigationList']=listDict['navigationList']
    p['list'] =listDict['list']
    p['page']=offset+1
    p['city']=city
    p['cat']=cat
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
     
def list(request,city=None,cat=None,date=None,offset=1):
    
    date = request.GET.get('dat')
    offset = request.GET.get('page')
        
    if not date and not cat:    
        return indexPage(request,city)
        #return False


    

    if not city: city='beijing'
    if not cat: cat = 'all'
    if not date: date = 'latest'
    if not offset: 
        offset = 1 
    else: 
        offset = int(offset)
 
    
    
    listDict = showList(request,city,cat,date,offset)
    

    i=len(listDict['navigationList'])
    
    
    nv=[]
    #import copy 
    catss= NewCatUrl(2,city)
    catt=listDict['navigationList'][i-1]
    try:
        cstr=catss[catt['id']]['child']
        if not cstr :
            cstr=catss[catss[catt['id']]['fid']]['child']
    except:
        return render_to_response('not.html',{'list':[]},context_instance=RequestContext(request))
        
    if not cstr :
        for k in range(i):
            
            if k==3:
                break
            nv.append(listDict['navigationList'][i-1-k])
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
        
    listDict['cat_k']=cstr
    if len(listDict['list'])>0:
        listDict['city_py']=city
        listDict['len_list']=len(listDict['list'])
        try:
            listDict['cat']=int(cat)
        except:
            listDict['cat']=cat
        listDict['page']=offset
        listDict['offset']=10
        

        for nv in listDict['navigationList']:
            try:
                if nv['ename']=='travel':
                    return render_to_response('m_travel_list.html',listDict,context_instance=RequestContext(request))
                    break
            except:
                pass
        #travel
        #return render_to_response('m_travel_list.html',listDict,context_instance=RequestContext(request))
        return render_to_response('m_list.html',listDict,context_instance=RequestContext(request))
    else:
        return render_to_response('not.html',{'list':[]},context_instance=RequestContext(request))    
    
          
def search(keyword):
    import sphinxapi
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
 

def getPageAndOffset(cds):
    if cds.get('page',False):
        try:
            page = int(cds['page'])
            if page <= 0:
                raise Http404('page cannot be %s'%page)
        except:
            raise Http404('GET Type Error')
    else:
        page = 1
        
    if cds.get('offset',False):
        try:
            offset = int(cds['offset'])
        except:
            raise Http404('GET Type Error')
    else:
        offset = 20
        
    return (page,offset)


@csrf_exempt
def writeOrder(request,event_id):
    #print 1
    #title = request.COOKIES.get('city_py',False)
    #city_name = request.COOKIES.get('city',False)
    if request.method == 'POST':
        eventId = int(event_id)
        ne=NewEventTable.objects.get(old_event_id=eventId)
        event = NewformatEvent(ne)
        info = request.POST
        if info.get('price',False) and info.get('cheapMoney',False) and info.get('ticketNum',False):
            #currencyDic = {"RMB":1,"HKD":1.24,"TWD":4.84,"USD":0.16,"EUR":0.12,"GBP":0.095,"JPY":16.33,"THB":5.23,"KER":164.46,"SGD":0.2,"VND":3388.90,"MYR":0.52}
            ra=ne.Price.Currency.rate if ne.Price.Currency else 1
            price = '%.2f'%(float(info['price'])/float(ra))
            raw_price = info['price']
            cheapMoney = info['cheapMoney']
            ticketNum = info['ticketNum']
            return render_to_response('m_form.html',{'city':event['district_name'],
                                                   'city_py':event['district_title'],
                                                   'price':price,'cheapMoney':cheapMoney,
                                                   'ticketNum':ticketNum,
                                                   'event':event,
                                                   'raw_price':raw_price,
                                                   'price_unit':event['event_price_unit'],
                                                   'price_unit_name':event['event_price_unit_name'],},context_instance=RequestContext(request))

    return HttpResponseRedirect('http://m.huodongjia.com/event-%s.html'%event_id)
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@csrf_exempt
def writeOrder_weixin(request,event_id):
    #print 1
    #title = request.COOKIES.get('city_py',False)
    #city_name = request.COOKIES.get('city',False)
    if request.method == 'POST':
        eventId = int(event_id)
        ne=NewEventTable.objects.get(old_event_id=eventId)
        event = NewformatEvent(ne)
        info = request.POST
        if info.get('price',False) and info.get('cheapMoney',False) and info.get('ticketNum',False):
            #currencyDic = {"RMB":1,"HKD":1.24,"TWD":4.84,"USD":0.16,"EUR":0.12,"GBP":0.095,"JPY":16.33,"THB":5.23,"KER":164.46,"SGD":0.2,"VND":3388.90,"MYR":0.52}
            ra=ne.Price.Currency.rate if ne.Price.Currency else 1
            price = '%.2f'%(float(info['price'])/float(ra))
            raw_price = info['price']
            cheapMoney = info['cheapMoney']
            ticketNum = info['ticketNum']
            return render_to_response('m_form.html',{'city':event['district_name'],
                                                   'city_py':event['district_title'],
                                                   'price':price,'cheapMoney':cheapMoney,
                                                   'ticketNum':ticketNum,
                                                   'event':event,
                                                   'raw_price':raw_price,
                                                   'price_unit':event['event_price_unit'],
                                                   'price_unit_name':event['event_price_unit_name'],},context_instance=RequestContext(request))

    return HttpResponseRedirect('http://m.huodongjia.com/event-%s.html'%event_id)
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def submitOrder_p(request):
    title = request.COOKIES.get('city_py',False)
    city_name = request.COOKIES.get('city',False)
    order_id = request.GET.get('order_id',False)
    try:
        order=NewOrder.objects.get(order_number=order_id)
        ord={}
        ord['mobilphone']=order.order_tel
        ord['email']=order.order_email
        ord['name']=order.order_user_name
        ord['price']=order.order_price
        ord['number']=order.order_amount
        ord['address']=order.order_address
        ord['payMode']=order.order_payment
        ord['phone']=order.order_telphone
        ord['event_name']=order.event_name
        return render_to_response('m_orderDetails.html',{'city':city_name,'city_py':title,'order_info':ord,'order_number':order_id,'total_price':order.order_totalpay},context_instance=RequestContext(request))
 
    except:
        return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'订单错误'},context_instance=RequestContext(request))

@csrf_exempt
@Telcaptcha
#@captcha_s
def submitOrder(request):
    title = request.COOKIES.get('city_py',False)
    city_name = request.COOKIES.get('city',False)
    if request.method == 'POST':
        cds = request.POST
        error = False
        if not cds.get('name',''):
            return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'姓名提交错误'},context_instance=RequestContext(request))
            error = True
        if not cds.get('mobilphone',''):
            return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'电话提交错误'},context_instance=RequestContext(request))
            error = True
        if not cds.get('address',''):
            return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'地址提交错误'},context_instance=RequestContext(request))
            error = True
        eventId = int(cds.get('event_id','0')) 
        if not eventId:   
            return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'event id 提交错误'},context_instance=RequestContext(request))          
            error = True
        else:
            try:
                pn=NewEventTable.objects.get(old_event_id=eventId,isshow_id__in=(1,8))
                
                event = NewformatEvent(pn)
                #return HttpResponse(json.dumps({'flag':event}))
                #event = NewEventTable.objects.get(Q(event_isshow=1)|Q(event_isshow=8),id=eventId)
                if event['event_price_model'] != 2:
                    if event['event_price_model'] == 1:
                        priceString = event['event_discount_price']
                    else:        
                        priceString = event['event_price']
                    priceList = priceString.split('/')
                    #return HttpResponse(json.dumps({'flag':priceList})) 
                    #currencyDic = [1,1,1.24,4.84,0.16,0.12,0.095,16.33,5.23,164.46,0.2,3388.90,0.52]
                    for i in range(len(priceList)):
                        if priceList[i].replace('.','').isdigit():
                            ra=pn.Price.Currency.rate if pn.Price.Currency else 1
                            priceList[i] = '%.2f'% (float(priceList[i])/float(ra) )
                    if '%.2f'%float(cds.get('price')) not in priceList:
                        return HttpResponse(json.dumps({'flag':priceString}))
                        error = True
            except:
                return HttpResponse(json.dumps({'flag':1})) 
                error = True
        if not error:
            city_name =event['district_name']
            number = '%s%s'%(int(time.time()),random.randint(100,1000))
            totalpay = float(cds['price'])*int(cds['number']) 
            #print cds['payMode']
 
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip =  request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            
            NewOrder.objects.create(
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
                                    event_id = event['event_id'],
                                    event_name = cds.get('event_name',''),
                                    city_title = city_name,
                                    order_reg_fields = 0,
                                    order_userid = 0,
                                    order_addtime = time.time(),
                                    order_addip = ip,
                                    order_text = cds.get('remark',''),
                                    event_to=2,
                                    )
            
            subject = '活动家 -来自手机网站的订单通知.客户:%s,电话:%s'%(cds.get('name','').encode('utf-8'),cds.get('mobilphone','').encode('utf-8'))
            content = '点单号:%s\n总价:%s\n'%(number,totalpay)
            content += dic2text(cds)
            sendMail(subject,content)
            msgs= u'您好，您预定的《%s》项目还未付款，请继续安排支付，支付成功后将有短信或电邮通知，请注意查收。【活动家】' % (re.sub(ur"[^\u4e00-\u9fa5\w]", " ", cds.get('event_name','')))
            #msgs= u'您好，你在活动家(huodongjia.com)预订了%s活动，还未支付，请你尽快支付，我们好为你出票。你可以在huodongjia.com上查询订单号%s支付即可。谢谢！【活动家】'\
            # % (re.sub(ur"[^\u4e00-\u9fa5\w]", " ", cds.get('event_name','')),number)
            #print type(msgs)
            
            
            SendOrderMsg(cds.get('mobilphone',''),msgs)
            '''
            msg = u'活动家新的订单通知，活动名称:%s,客户:%s,电话:%s,单号:%s,总价:%s,'%( cds.get('event_name',''),cds.get('name',''),cds.get('mobilphone',''),number,totalpay)
            msg = re.sub(ur"[^\u4e00-\u9fa5\w]", ",", msg)
            try:
                SendOrderMsg('18628175526','%s【活动家】' % msg)
            except Exception,e:
                log.debug('order_c')
                log.debug(e)
            '''
            return render_to_response('m_orderDetails.html',{'city':city_name,'city_py':title,'order_info':cds,'order_number':number,'total_price':totalpay},context_instance=RequestContext(request))
        else:
            return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'下订单时遇到错误,请重新下单4'},context_instance=RequestContext(request))
            
            
    return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'下订单时遇到错误,请重新下单1'},context_instance=RequestContext(request))
@csrf_exempt
#@Telcaptcha
#@captcha_s
def submitOrder_weixin(request):
    title = request.COOKIES.get('city_py',False)
    city_name = request.COOKIES.get('city',False)
    if request.method == 'GET':
        cds = request.GET
        error = False
        if not cds.get('name',''):
            return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'用户名未填写'},context_instance=RequestContext(request))
            error = True
        if not cds.get('mobilphone',''):
            return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'电话提交错误'},context_instance=RequestContext(request))
            error = True
        if not cds.get('address',''):
            return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'地址提交错误'},context_instance=RequestContext(request))
            error = True
        eventId = int(cds.get('event_id','0')) 
        if not eventId:   
            return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'event id 提交错误'},context_instance=RequestContext(request))          
            error = True
        else:
            try:
                pn=NewEventTable.objects.get(old_event_id=eventId,isshow_id__in=(1,8))
                
                event = NewformatEvent(pn)
                #return HttpResponse(json.dumps({'flag':event}))
                #event = NewEventTable.objects.get(Q(event_isshow=1)|Q(event_isshow=8),id=eventId)
                if event['event_price_model'] != 2:
                    if event['event_price_model'] == 1:
                        priceString = event['event_discount_price']
                    else:        
                        priceString = event['event_price']
                    priceList = priceString.split('/')
                    #return HttpResponse(json.dumps({'flag':priceList})) 
                    #currencyDic = [1,1,1.24,4.84,0.16,0.12,0.095,16.33,5.23,164.46,0.2,3388.90,0.52]
                    for i in range(len(priceList)):
                        if priceList[i].replace('.','').isdigit():
                            ra=pn.Price.Currency.rate if pn.Price.Currency else 1
                            priceList[i] = '%.2f'% (float(priceList[i])/float(ra) )
                    if '%.2f'%float(cds.get('price')) not in priceList:
                        return HttpResponse(json.dumps({'flag':priceString}))
                        error = True
            except:
                return HttpResponse(json.dumps({'flag':1})) 
                error = True
        if not error:
            city_name =event['district_name']
            number = '%s%s'%(int(time.time()),random.randint(100,1000))
            totalpay = float(cds['price'])*int(cds['number']) 
            #print cds['payMode']
 
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip =  request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            
            NewOrder.objects.create(
                                    order_number=number,
                                    order_user_name=cds.get('name',''),
                                    order_tel = cds.get('mobilphone',''),
                                    order_email = cds.get('email',''), 
                                    order_totalpay = totalpay,
                                    order_price = cds.get('price',''),
                                    order_amount = cds.get('number',''),
                                    order_address = cds.get('address',''),
                                    order_payment = 'weixin',
                                    order_telphone = cds.get('phone',''),
                                    order_pay_status = 0,
                                    order_status = 0,
                                    event_id = event['event_id'],
                                    event_name = cds.get('event_name',''),
                                    city_title = city_name,
                                    order_reg_fields = 0,
                                    order_userid = 0,
                                    order_addtime = time.time(),
                                    order_addip = ip,
                                    order_text = cds.get('remark',''),
                                    event_to=3,
                                    )
            
            subject = '活动家 -来自微信的订单通知.客户:%s,电话:%s'%(cds.get('name','').encode('utf-8'),cds.get('mobilphone','').encode('utf-8'))
            content = '点单号:%s\n总价:%s\n'%(number,totalpay)
            content += dic2text(cds)
            sendMail(subject,content)
            #msgs= u'您好，您预定的《%s》项目还未付款，请继续安排支付，支付成功后将有短信或电邮通知，请注意查收。【活动家】' % (re.sub(ur"[^\u4e00-\u9fa5\w]", " ", cds.get('event_name','')))
            #msgs= u'您好，你在活动家(huodongjia.com)预订了%s活动，还未支付，请你尽快支付，我们好为你出票。你可以在huodongjia.com上查询订单号%s支付即可。谢谢！【活动家】'\
            # % (re.sub(ur"[^\u4e00-\u9fa5\w]", " ", cds.get('event_name','')),number)
            #print type(msgs)
            
            
            SendOrderMsg(cds.get('mobilphone',''),msgs)
            url_log=request.COOKIES.get('urllogorder',None)
            if url_log:
                cache.set('order_%s' % number,[json.loads(url_log),ip],86400*30)
            '''
            msg = u'活动家新的订单通知，活动名称:%s,客户:%s,电话:%s,单号:%s,总价:%s,'%( cds.get('event_name',''),cds.get('name',''),cds.get('mobilphone',''),number,totalpay)
            msg = re.sub(ur"[^\u4e00-\u9fa5\w]", ",", msg)
            try:
                SendOrderMsg('18628175526','%s【活动家】' % msg)
            except Exception,e:
                log.debug('order_c')
                log.debug(e)
            '''
            return HttpResponseRedirect('/weixin/js_api_call.php?order_number=%s' % number)
            #return render_to_response('m_orderDetails.html',{'city':city_name,'city_py':title,'order_info':cds,'order_number':number,'total_price':totalpay},context_instance=RequestContext(request))
        else:
            return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'下订单时遇到错误,请重新下单2'},context_instance=RequestContext(request))
            
            
    return render_to_response('m_base_error.html',{'city':city_name,'city_py':title,'error_msg':u'下订单时遇到错误,请重新下单1'},context_instance=RequestContext(request))


def dic2text(dic):
    res = ''
    for key,value in dic.items():
        if key == 'csrfmiddlewaretoken':
            continue
        res += key+':'+value+'\n'
    return res.encode('utf-8')    

def searchOrder(request):
    title = request.COOKIES.get('city_py',False)
    city_name = request.COOKIES.get('city',False)
    order_search=request.GET.get('order_search',None)
    
    if order_search:
        #order_search = request.GET['order_search']
        if order_search.isdigit():
            order_list = NewOrder.objects.filter(Q(order_number = order_search.strip())|Q(order_tel = order_search.strip())).order_by('-order_id')
            if order_list:
                for item in order_list:
                    item.order_addtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item.order_addtime))
                    if item.order_paytime:
                        item.order_paytime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item.order_paytime))
                    else:
                        item.order_paytime = ''
                return render_to_response('m_search_order.html',{'order_list':order_list,'city':city_name,'city_py':title},context_instance=RequestContext(request))
            else:
                error = u'没有找到订单,请确认电话号码和订单号是否正确'
        else:
            error = u'订单号由纯数字组成！'
    else:
        error = u'请输入手机号或者订单号查询订单'
    head = {'title':u'订单查询_活动网_活动家',
              'keywords':u'订单查询',
             'description':u'订单查询页面,活动家（huodongjia.com）'}
    return render_to_response('m_search_order.html',{'head':head,'city':city_name,'city_py':title,'error_msg':error },context_instance=RequestContext(request))

def city_map(request):
    title = request.COOKIES.get('city_py',False)
    city_name = request.COOKIES.get('city',False)
    return render_to_response('city.html',{'city':city_name,'city_py':title,},context_instance=RequestContext(request))

def msg(request):
    title = request.COOKIES.get('city_py',False)
    city_name = request.COOKIES.get('city',False)
    if request.method == 'POST':
        cds = request.POST
        eventId=cds.get('eventId')
        eventName=cds.get('eventName',None)
        if not eventId:
            
            return redirect('/msg/')
        if not eventName:
            try:
                eventName=NewEventTable.objects.get(old_event_id=eventId).name
            except:
                return redirect('/msg/')
        if cds.get('eventId',False) and cds.get('name',False) and (cds.get('email',False) or cds.get('phone',False)) and cds.get('content',False):
            timeNow = time.time()

            try:
                NewOrderMessage.objects.create(event_id = eventId,
                                               event_name = eventName,
                                               msg_name = cds.get('name',''),
                                               msg_tel = cds.get('phone',''),
                                               msg_email = cds.get('email',''),
                                               msg_content = cds.get('content',''),
                                               msg_addtime = timeNow
                                               ) 
            
                
                subject ='活动家-留言咨询,活动名:%s,客户:%s'%(eventName.encode('utf-8'),cds.get('name','').encode('utf-8'))
                content = '活动id:%s\n活动名:%s\n'%(eventId,eventName.encode('utf-8'))+dic2text(cds)+'留言时间:%s'%time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timeNow)) 
                sendMail(subject,content)
            except Exception,e:
                log.debug(e)
            return redirect('/event-%s.html' % eventId)
        else:
            return redirect('/msg/')
    else:
        return render_to_response('m_form.html',{'city':city_name,'city_py':title,},context_instance=RequestContext(request))


    
