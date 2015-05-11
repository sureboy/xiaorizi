#coding:utf-8
import smtplib 
from email.mime.text import MIMEText
from admin_self.common import NewCatUrl,NewCity
import  datetime
import urllib2,re
from new_event.models import  Crowfunding
from django.shortcuts import render_to_response
from django.core.cache import cache
from django.http import HttpResponse
import json

#code 2表示电话验证错误
def Telcaptcha_ajax(func):    
    def _is_captcha(request,*arg):
        if request.method == 'POST':
            captcha = request.POST.get('captcha',False)
            tel = request.POST.get('telephone',False)
            
            p={}
            eventId = request.POST.get('event_id',False)
            if eventId:
                p['url']='http://www.huodongjia.com/event-%s' % (eventId)
            else:
                p['url']='http://www.huodongjia.com'
        
            if not captcha or not tel:
                return HttpResponse(json.dumps({'code':2,'city_py':'beijing','head':{}}), content_type="text/html")
            try:
                if str(captcha) == str(cache.get(tel)):
                    return func(request,*arg)
                else:
                    return HttpResponse(json.dumps({'code':2,'city_py':'beijing','head':{}}), content_type="text/html")
            except:
                return HttpResponse(json.dumps({'code':2,'city_py':'beijing','head':{}}), content_type="text/html")
        else:
            return func(request,*arg)

    return _is_captcha

def Telcaptcha(func):    
    
    def _is_captcha(request,*arg):
        captcha = request.POST.get('captcha',False)
        tel = request.POST.get('mobilphone',False)
        
        p={}
        eventId = request.POST.get('event_id',False)
        if eventId:
            p['url']='http://www.huodongjia.com/event-%s' % (eventId)
        else:
            p['url']='http://www.huodongjia.com'
        
        if not captcha:
            p['error_msg']='请输入验证码 请返回重新输入'
            return render_to_response('base_error.html',p)
        if not tel:
            p['error_msg']='没有手机号 请返回重新输入'
            return render_to_response('base_error.html',p)
        
        try:
            if str(captcha) == str(cache.get(tel)):
                return func(request,*arg)
            else:
                p['error_msg']='验证码错误 请返回重新输入'
                return render_to_response('base_error.html',p)
        except:
            p['error_msg']='验证错误 请返回重新输入'
            return render_to_response('base_error.html',p)

    return _is_captcha

def Telcaptcha_m(func):    
    
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
            p['error_msg']='请输入验证码 请返回重新输入'
            return render_to_response('m_base_error.html',p)
        if not tel:
            p['error_msg']='没有手机号 请返回重新输入'
            return render_to_response('m_base_error.html',p)
        
        try:
            if str(captcha) == str(cache.get(tel)):
                return func(request,*arg)
            else:
                p['error_msg']='验证码错误 请返回重新输入'
                return render_to_response('m_base_error.html',p)
        except Exception,e:
            import logging
            log = logging.getLogger('XieYin.app')
            log.debug('mobile:',e)
            p['error_msg']='验证错误 请返回重新输入'
            return render_to_response('m_base_error.html',p)

    return _is_captcha

def captcha_s(func):     
    def _is_captcha_right(request,*arg):
        if not request.POST.get('captcha',False):
            return  render_to_response('base_error.html',{'error_msg':u'请输入验证码'})
 
        if not request.session.get('captcha',False):
            return  render_to_response('base_error.html',{'error_msg':u'验证码错误 请返回重新输入'})
 
        if request.session['captcha'].lower() == request.POST['captcha'].lower():
            return func(request,*arg)
        else:
            return render_to_response('base_error.html',{'error_msg':u'验证码错误 请返回重新输入'})
    return _is_captcha_right

def captcha(func):     
    def _is_captcha_right(request,*arg):
        if not request.POST.get('captcha',False):
            return False #render_to_response('base_error.html',{'error_msg':u'请输入验证码'})
        if not request.session.get('captcha',False):
            return False #render_to_response('base_error.html',{'error_msg':u'验证码错误'})
        if request.session['captcha'].lower() == request.POST['captcha'].lower():
            return func(request,*arg)
        else:
            return False #render_to_response('base_error.html',{'error_msg':u'验证码错误'})
    return _is_captcha_right

def find_from_city(request,city_title=False):
     
    cityObj=()
    if not city_title:
        try:
            title = request.COOKIES.get('city_py',False)
            city_name = request.COOKIES.get('city',False)
            cityId = request.COOKIES.get('city_id',False)
            
            city_name = city_name.decode('utf-8')
            cityObj=(cityId,city_name,title)
             
        except:
            pass
        
           
        if not title or not city_name or not cityId: 
            city_code = getCityNameByIp(request)
            if city_code:
                ci=NewCity(4)
                if  ci.has_key(city_code):            
                    cityObj =ci[city_code]
                    
        if cityObj:
            return cityObj

    else:
        ci=NewCity(3)
        if  ci.has_key(city_title):    
            cityObj =ci[city_title]
            return cityObj
                    
        
 
 
    cityId = 101
    city_name = u'北京'
    title = 'beijing'
    cityObj=(cityId,city_name,title,False)
        
        
    return cityObj
     
def find_cat_fid(cat_arr={},cat_str='',city=''):
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
        navigationDict['id'] = cat_k['id']
        navigationDict['catname'] = cat_k['catname']
        navigationDict['article'] = cat_k['article']
        navigationDict['ename'] = cat_str
        navigationDict['caturl'] = '/%s/%s/'%(city,cat_str) if city else '/%s/'%(cat_str)
        navigationList.append(navigationDict)    
           
        for key,cat_a in cat_arr.items():        
            if cat_k['fid']==cat_a['id']:
                navigationList.extend(find_cat_fid(cat_arr ,key ,city ) ) 
                break
                 

    
    return navigationList            

def constructNavigationUrl( city,catt):
 
    navigationList = []
    
    navigationList.extend(find_cat_fid(NewCatUrl(0),catt,city))
    new_navigationList=[]
    for i in range(len(navigationList)):
   
        if type(navigationList[i]['ename'])!=long:
 
            new_navigationList.append(navigationList[i])
 
            
    
    navigationDict = dict()
    navigationDict['catname'] = u'活动网'
    navigationDict['caturl'] = '/%s/' % (city) if city else '/'
    new_navigationList.append(navigationDict)
    new_navigationList.reverse()
    return new_navigationList


def sendMail(sub,content,to_list=['252925359@qq.com', '241617467@qq.com','1010478998@qq.com','9682539@qq.com','276753659@qq.com']):
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

def sendMailForPostEvent(sub,content,to_list=['584243616@qq.com','276753659@qq.com', '241617467@qq.com','767142185@qq.com','313020458@qq.com','454077210@qq.com']):
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
    
def getMsgU():

    import urllib2,urllib,hashlib
    url = 'http://sdk.entinfo.cn:8060/webservice.aspx/balance'
    
    SN = 'SDK-SRF-010-00365'
    m = hashlib.md5()
    m.update(SN+'154282')
    pwd = m.hexdigest().upper()


    data = {'sn':SN,
                'pwd':pwd,

                }
    res = urllib2.urlopen(url,urllib.urlencode(data)).read()
    print res
    return
 
 
    
def SendOrderMsg(phone=None,msg=''):
    if phone and msg:         
        import urllib2,urllib,hashlib
        url = 'http://sdk.entinfo.cn:8060/z_mdsmssend.aspx'
        
        SN = 'SDK-SRF-010-00365'
        m = hashlib.md5()
        m.update(SN+'154282')
        pwd = m.hexdigest().upper()
        #print type(msg)
        #print msg.encode('gbk')
        #msg=re.sub(ur"[^\u4e00-\u9fa5\w]", " ", msg)
        #msg=msg[0:10]
        print phone
        data = {'sn':SN,
                    'pwd':pwd,
                    'mobile':phone,
                    'content':msg.encode('gb2312'),
                    }
        res = urllib2.urlopen(url,urllib.urlencode(data)).read()
        if int(res) > 0:
            
            return True
        else:
            print res
            return False
        
    else:
        return  False

def getCityNameByIp(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    #print 'ip=',ip
    locApiUrl = 'http://api.map.baidu.com/location/ip?ak=Te0lHkIjEpurR7H2Ykz5oVaA&ip=%s&coor=bd09ll'%ip
    try:
        rp = urllib2.urlopen(locApiUrl,timeout = 2).read()
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
