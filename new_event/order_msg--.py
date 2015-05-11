#coding:utf-8
from django.views.decorators.csrf import csrf_exempt
import  hashlib,cStringIO,datetime,random,json
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from admin_self.common import NewCatUrl, NewCity,NewformatEvent,event_city_cat
from new_event.models import   NewEventTable,NewOrder
from new_event.common import sendMail,SendOrderMsg,Telcaptcha,captcha,captcha_s
from django.template import RequestContext
from django.db.models import Q
from django.core.cache import cache
import time,re
from django.conf import settings
import logging

log = logging.getLogger('XieYin.app')  
_letter_cases = "abcdefghjkmnpqrstuvwxy" # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper() # 大写字母
_numbers = ''.join(map(str, range(3, 10))) # 数字
init_chars = ''.join([_letter_cases, _upper_cases, _numbers])

def get_check_code(request):

    rand_str='%s%s%s%s' % (random.randint(1, 9),random.randint(1, 9),random.randint(1, 9),random.randint(1, 9))
    #request.session['tel_code'] = rand_str
    return rand_str

def send_check_mesage(request):
    p={}
    p['flag']=False
    tel=request.GET.get('tel',None)
    
    if tel :
        rand_str=get_check_code(request)
        
        
        msgs= u'感谢使用活动家手机验证系统，您的手机验证码为%s，10分钟内有效。更多精彩关注http://www.huodongjia.com【活动家】'\
         % (rand_str)
        #print type(msgs)
        if SendOrderMsg(tel,msgs):
            cache.set(tel,rand_str,60*10)
            p['flag']=True
        else:
            cache.set(tel,rand_str,60*10)
            
    return HttpResponse(json.dumps(p))    

@csrf_exempt
def verify_tel_captcha(request):
    #erify_captcha(request)
    verify_captcha(request)
    
    p={}
    p['flag']=False
    return HttpResponse(json.dumps({'flag':True}))
    captcha = request.POST.get('captcha',False)
    tel = request.POST.get('mobilphone',False)
    if not captcha:
        return HttpResponse(json.dumps(p))
        #return False #render_to_response('base_error.html',{'error_msg':u'请输入验证码'})
    if not tel:
        return HttpResponse(json.dumps(p))
        #return False #render_to_response('base_error.html',{'error_msg':u'验证码错误'})
    
    if captcha == cache.get(tel):
        p['flag']=True
        #return HttpResponse(json.dumps(p))
        #return func(request,*arg)
    return HttpResponse(json.dumps(p))

@csrf_exempt
def get_check_code_image(request):
    from PIL import Image,ImageDraw,ImageFont      
    width = 200
    height = 70
 
    g1=random.randint(240, 255)
    b1=random.randint(240, 255)
    k1=random.randint(240, 255)
    
    bgcolor = (g1,b1,k1)
    
    #bgcolor = (255,255,255)
    image = Image.new('RGB',(width,height),bgcolor)
    
    font = ImageFont.truetype(settings.STATIC_ROOT+'/fonts/iNked God.ttf',40)    
    g=random.randint(10, 200)
    b=random.randint(10, 200)
    k=random.randint(10, 200)
    fontcolor = (g,b,k)    
    #fontcolor = (45,157,169)
    draw = ImageDraw.Draw(image)
    str=random.sample(init_chars, 4)
    rand_str = ' %s ' % ' '.join(str)
    request.session['captcha'] = ''.join(str)
    
    #font_width, font_height = font.getsize(rand_str)
    font_width, font_height = font.getsize(rand_str)

    draw.text(((width - font_width) / 3, (height - font_height) / 3),rand_str, font=font, fill=fontcolor)
    
    
    #draw.text((0,0),rand_str,font=font,fill=fontcolor)
    del draw
    
    buf = cStringIO.StringIO()  
    image.save(buf,'GIF')    
    
    '''    
    #image.save('1234_1.jpeg')
    newImage = Image.new('RGB',(width,height),bgcolor)
    
    newPix = newImage.load()
    pix = image.load()

    
    offset = 0
    
    for y in range( height) :
        #offset += 1 
        for x in range( width ):
            #newx = x + offset
            #if newx < width:                        
            newPix[x,y] = pix[x,y]         
    #newImage.save('1234_2.jpeg')
    
    draw = ImageDraw.Draw(newImage)

    linecolor= (134,126,177)
    for i in range(1,13):
        x1 = random.randint(0,width)
        x2 = random.randint(0,width)
        y1 = random.randint(0,height)
        y2 = random.randint(0,height)
        draw.line([(x1, y1), (x2, y2)], linecolor)
    '''
    
    '''
    line_num = random.randint(1,4) # 干扰线条数

    for i in range(line_num):
        # 起始点
        begin = (random.randint(0, width), random.randint(0, height))
        #结束点
        end = (random.randint(0,width), random.randint(0, height))
        draw.line([begin, end], fill=(g+i, b+i,k+i))
    
    chance = min(100, max(0, 2))
    for w in xrange(width):
        for h in xrange(height):
            tmp = random.randint(0, 100)
            if tmp > 100 - chance:
                draw.point((w, h), fill=(g, b, k))
    del draw
    
    buf = cStringIO.StringIO()  
    newImage.save(buf,'GIF')
    '''
    return HttpResponse(buf.getvalue(),'image/gif') 

@csrf_exempt
def verify_captcha(request):
    if request.method == 'POST':
        p = request.POST
        if request.session.get('captcha').upper() == p.get('captcha','false').upper():
            return HttpResponse(json.dumps({'flag':'true'}))
    return HttpResponse(json.dumps({'flag':'false'}))


@csrf_exempt
def writeZhuantiOrder(request,event_id):
    #title = request.COOKIES.get('city_py',False)
    #city_name = request.COOKIES.get('city',False)
    eventId= int(event_id)
    ne=NewEventTable.objects.get(old_event_id=eventId)
    event = NewformatEvent(ne)
    print '1'
    pricecontent = ''
    for item in event['event_content']:
        if item[0] == u'会议门票':
            pricecontent = item
            break
    return render_to_response('zhuanti_order.html',{'city':event['district_name'],
                                           'city_py':event['district_title'],
                                           'event':event,
                                           'price_txt':pricecontent,},context_instance=RequestContext(request))


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
            return render_to_response('form.html',{'city':event['district_name'],
                                                   'city_py':event['district_title'],
                                                   'price':price,'cheapMoney':cheapMoney,
                                                   'ticketNum':ticketNum,
                                                   'event':event,
                                                   'raw_price':raw_price,
                                                   'price_unit':event['event_price_unit'],
                                                   'price_unit_name':event['event_price_unit_name'],},context_instance=RequestContext(request))

    return HttpResponseRedirect('http://www.huodongjia.com/event-%s.html'%event_id)
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@csrf_exempt
#@Telcaptcha
@captcha_s
def submitOrder(request):
    title = request.COOKIES.get('city_py',False)
    city_name = request.COOKIES.get('city',False)
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
                                    event_to=0,
                                    )
            
            subject = '活动家 -新的订单通知.客户:%s,电话:%s'%(cds.get('name','').encode('utf-8'),cds.get('mobilphone','').encode('utf-8'))
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
            return render_to_response('orderDetails.html',{'city':city_name,'city_py':title,'order_info':cds,'order_number':number,'total_price':totalpay},context_instance=RequestContext(request))
        else:
            return render_to_response('base_error.html',{'city':city_name,'city_py':title,'error_msg':u'下订单时遇到错误,请重新下单2'},context_instance=RequestContext(request))
            
            
    return render_to_response('base_error.html',{'city':city_name,'city_py':title,'error_msg':u'下订单时遇到错误,请重新下单1'},context_instance=RequestContext(request))
 

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
    error = u'请输入手机号或者订单号查询订单'
    if request.GET.get('order_search',''):
        order_search = request.GET['order_search']
        if order_search.isdigit():
            order_list = NewOrder.objects.filter(Q(order_number = order_search.strip())|Q(order_tel = order_search.strip()))
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

