#coding:utf-8
from User.models import Customer,Address,AppGetui,UserPushInfo
from User.forms import RegisterForm,PictureForm
import json
from django.http import HttpResponse
from django.core.cache import cache
from User.functions import queryset2list, make_password, check_password
import time
from django.views.decorators.csrf import csrf_exempt
#from api.functions import eventDic
from User.functions import isAPP
from LifeApi.common import SendOrderMsg
from LifeApi.models import NewEventTable

@isAPP
def Register(request):
    error = ''
    if request.method == 'GET':
        f = RegisterForm(request.GET)
        
        if f.is_valid():
            cds = f.cleaned_data
            if len(cds['password']) < 6:
                error = u'密码至少6位'
            #print Customer.objects.filter(name=cds['name'])
            if Customer.objects.filter(name=cds['name']):
                error = u'存在相同昵称'
            if Customer.objects.filter(phone=cds['phone'],is_temporary=0):
                error = u'该手机号已注册'
            if not error:
                address_list = []
                if Customer.objects.filter(phone=cds['phone'],is_temporary=1):
                    temp_customer = Customer.objects.get(phone=cds['phone'],is_temporary=1)
                    temp_customer.name = cds['name']
                    temp_customer.email = cds['email']
                    temp_customer.password = make_password(cds['password'])
                    temp_customer.register_time = int(time.time())
                    temp_customer.last_login_time = int(time.time())
                    temp_customer.is_temporary=1
                    temp_customer.save()
                    if temp_customer.address_set.all():
                        address_list = queryset2list(temp_customer.address_set.values())
                else:
                    new_customer = Customer(name = cds['name'],
                                            phone = cds['phone'],
                                            email = cds['email'],
                                            password = make_password(cds['password']),
                                            register_time = int(time.time()),
                                            last_login_time = int(time.time()),
                                            is_temporary=0,
                                            )
                    new_customer.save()
             
                        
                        
                json_data = {'id':new_customer.id,
                             'phone':new_customer.phone,
                             'name':new_customer.name,
                             'email':new_customer.email,
                             'address':address_list,
                             'headpoto':'',
                             }
                        
                return HttpResponse(json.dumps({"code":1,"msg":'',"data":json_data}))
        else:
            error = u'数据传输错误'
        return HttpResponse(json.dumps({"code":0,"msg":error}), content_type="application/json")
@isAPP    
def Login(request):
    error = ''
    if request.method == 'GET':
        cds = request.GET
        if not cds.get('phone'):
            error = u'未输入手机号'
        if not cds.get('password'):
            error = u'未输入密码'
        if not error:
            try:
                user = Customer.objects.get(phone = cds['phone'],is_temporary = 0)  
            except:
                return HttpResponse(json.dumps({"code":0,"msg":u'该手机尚未注册'}), content_type="application/json")   
            password = cds['password']
            '''
            f = open('private.pem','r')
            p = f.read()
            privkey = rsa.PrivateKey.load_pkcs1(p)
            try:
                password = binascii.a2b_hex(password)
                raw_password = rsa.decrypt(password,privkey) #解密得到原始密码
            except:
                return HttpResponse(json.dumps({"code":0,"msg":u'decrypt failed'}), content_type="application/json")
            passowrd_in_db = user.password
            if check_password(raw_password,passowrd_in_db):
            '''
            if password.lower() == user.password.lower():
                request.session['islogin'] = True
                request.session['user_id'] = user.id
                address_list = queryset2list(user.address_set.values())
                user.last_login_time = int(time.time())
                user.save()
                
                #if not address_list:
                if user.email:
                    email = user.email
                else:
                    email = ''
                json_data = {'id':user.id,
                             'phone':user.phone,
                             'name':user.name,
                             'email':email,
                             'address':address_list,
                             'headphoto':user.headphoto_path,
                             }
                return HttpResponse(json.dumps({"code":1,"msg":'',"data":json_data}), content_type="application/json")
            else:
                error = u'密码错误'
    else:
        error = u'数据传输错误'
    return HttpResponse(json.dumps({"code":0,"msg":error}), content_type="application/json")

@isAPP
def quickLogin(request):
    phone = request.GET['phone']
    checkcode = request.GET['checkcode']
    error = ''
    ch=cache.get(phone)
    if str(checkcode) != str(ch):
        error =  u'验证码不正确'   
        return HttpResponse(json.dumps({"code":0,"msg":error,"phone":phone,"ch":ch,"checkcode":checkcode}), content_type="application/json")
    
    address_list=[]
    if not Customer.objects.filter(phone = phone):
        new_customer = Customer(name = phone,
                                phone = phone,
                                email = '',
                                password = make_password(phone),
                                register_time = int(time.time()),
                                last_login_time = int(time.time()),
                                is_temporary=1,
                                )
        new_customer.save()
        ids = new_customer.id
        name = new_customer.name
    else:
        customer = Customer.objects.filter(phone = phone).order_by('-is_temporary')[0]    
        ids = customer.id
        name = customer.name
        address_list = queryset2list(customer.address_set.values()) 
    json_data = {'id':ids,
                 'phone':phone,
                 'name':name,
                 'email':'',
                 'headphoto':customer.headphoto_path,
                 'address':address_list,
                 }
    request.session['islogin'] = True
    request.session['user_id'] = ids
    return HttpResponse(json.dumps({"code":1,"msg":'',"data":json_data}), content_type="application/json")

@isAPP
def Logout(request):
    if request.session.get('islogin'):
        del request.session['islogin']
        del request.session['user_id']
        return HttpResponse(json.dumps({"code":1,"msg":u'成功退出'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"code":0,"msg":u'未登录,无法进行注销操作'}), content_type="application/json")
    
@isAPP    
def SendCheckCode(request):
    if request.GET.get('phone'):
        
        phone = request.GET['phone']
        import random
        #url = 'http://sdk.entinfo.cn:8060/z_mdsmssend.aspx'
        checkcode = random.randint(100000,999999)
        msg = u'您好,您的验证码%s,10分钟内有效,请及时校验【小日子】'%checkcode
        '''
        SendOrderMsg(phone,msg)
        SN = 'SDK-SRF-010-00554'
        m = hashlib.md5()
        m.update(SN+'240256')
        pwd = m.hexdigest().upper()
        data = {'sn':SN,
                    'pwd':pwd,
                    'mobile':phone,
                    'content':msg.encode('gb2312'),
                    }
        res = urllib2.urlopen(url,urllib.urlencode(data)).read()
        '''
        if SendOrderMsg(phone,msg):
            cache.set(str(phone),str(checkcode),60*10)
            return HttpResponse(json.dumps({"code":1,"msg":u'验证码发送成功',"phone":phone}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"code":0,"msg":u'验证码发送失败',"phone":phone}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"code":0,"msg":u'there is no phone number'}), content_type="application/json") 
@isAPP    
def VerifyCheckCode(request):
    phone = request.GET['phone']
    checkcode = request.GET['checkcode']  
    if checkcode == cache.get(phone):
        return HttpResponse(json.dumps({"code":1,"msg":u'验证成功',"phone":phone}), content_type="application/json")  
    else:
        return HttpResponse(json.dumps({"code":0,"msg":u'验证失败',"phone":phone}), content_type="application/json")

@isAPP    
def ChangePassword(request):
    try:
        password = request.GET['password']
        #user_id = request.session['user_id']
        user_id = request.GET['userid']
        if user_id:
            user = Customer.objects.get(id = user_id)
            #user.password = make_password(password)
            user.password = password
            user.save()        
            return HttpResponse(json.dumps({"code":1,"msg":u'修改成功'}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"code":0,"msg":u'修改失败,没有用户id'}), content_type="application/json")

    except Exception,e:
        return HttpResponse(json.dumps({"code":0,"msg":u'修改失败%s' % e}), content_type="application/json")

@isAPP
def GetBackPassword(request):
    phone = request.GET.get('phone',None)
    password = request.GET.get('password',None)
    checkcode = request.GET.get('checkcode',False)  
    if not phone:
        return HttpResponse(json.dumps({"code":0,"msg":u'手机号为空',"phone":phone}), content_type="application/json")
    if checkcode != cache.get(phone):
        return HttpResponse(json.dumps({"code":0,"msg":u'验证失败',"phone":phone}), content_type="application/json") 
    if  not Customer.objects.filter(phone = phone).filter(is_temporary=0):
        return HttpResponse(json.dumps({"code":0,"msg":u'该手机号未注册',"phone":phone}), content_type="application/json")
    user = Customer.objects.filter(phone = phone).filter(is_temporary=0)[0]
    #user.password =  make_password(password)
    user.password =   password
    user.save()
    return HttpResponse(json.dumps({"code":1,"msg":u'取回密码成功'}), content_type="application/json")
    
@isAPP 
def ChangeUserInfo(request):
    if request.method == 'GET':
        cds = request.GET
        #user_id = request.session['user_id']
        user_id = request.GET['userid']
        user = Customer.objects.get(id = user_id)
        if cds.get('name'):
            user.name = cds['name']
        if cds.get('email'):
            user.email = cds['email']
        user.save()
        address_list = queryset2list(user.address_set.values())
        json_data = {'id':user.id,
                             'phone':user.phone,
                             'name':user.name,
                             'email':user.email,
                             'address':address_list,
                             'headphoto':user.headphoto_path,
                             }
        return HttpResponse(json.dumps({"code":1,"msg":'',"data":json_data}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"code":0,"msg":u'数据传输错误'}), content_type="application/json")
    
#@islogin 
@isAPP
def AddAddress(request):
    if request.method == 'GET':
        cds = request.GET
        #user_id = request.session['user_id']
        user_id = cds.get('userid')
        user = Customer.objects.get(id=user_id)
        name = cds.get('name')
        phone = cds.get('phone')
        address_name = cds.get('address_name')
        if name and phone and address_name:
            if user.address_set.all():
                default = 0
            else:
                default = 1
            newAddress = Address(address_name = address_name,
                                   phone = phone,
                                   name = name,
                                   default = default,
                                   user = user,
                                   )
            newAddress.save()
            json_data = {
                        'id':newAddress.id,
                        'name':name,
                        'phone':phone,
                        'address_name':address_name,
                        'default':default, 
                        }
           
            return HttpResponse(json.dumps({"code":1,"msg":'',"data":json_data}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"code":0,"msg":u'数据有缺漏'}), content_type="application/json")  
                
    else:
        return HttpResponse(json.dumps({"code":0,"msg":u'数据传输错误'}), content_type="application/json")   

@isAPP
def ShowAddress(request):
    if request.method == 'GET':
        cds = request.GET
        user_id=cds.get('userid')
        try:
            user = Customer.objects.get(id = user_id)
            json_data=[{
                'id':address.id,
                'name':address.name,
                'phone':address.phone,
                'address_name':address.address_name,
                'default':address.default, 
                } for address in user.address_set.all() ]
          
            return HttpResponse(json.dumps({"code":1,"msg":'',"data":json_data}), content_type="application/json")

        except Exception,e:
            return HttpResponse(json.dumps({"code":0,"msg":u'数据传输错误 %s' % e}), content_type="application/json")   

            
            
                    
@isAPP
def ChangeAddress(request):
    if request.method == 'GET':
        cds = request.GET
        #user_id = request.session['user_id']
        user_id=cds.get('userid')
        user = Customer.objects.get(id = user_id)
        name = cds.get('name')
        phone = cds.get('phone')
        address_name = cds.get('address_name')
        address_id = int(cds.get('address_id'))
        default = int(cds.get('default',0))
        if name and phone and address_name and address_id:
                if default == 1:
                    if user.address_set.filter(default=1):
                        old_default_address = user.address_set.get(default=1)                      
                        old_default_address.default = 0
                        old_default_address.save()
                try:
                    address = user.address_set.get(id = address_id)
                except:
                    return HttpResponse(json.dumps({"code":0,"msg":u'地址id不存在'}), content_type="application/json")
                address.name = name
                address.phone = phone
                address.address_name = address_name
                address.default = default
                address.save()
                json_data = {
                            'id':address_id,
                            'name':name,
                            'phone':phone,
                            'address_name':address_name,
                            'default':default, 
                            }
                return HttpResponse(json.dumps({"code":1,"msg":'',"data":json_data}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"code":0,"msg":u'数据有缺漏'}), content_type="application/json")  
                
    else:
        return HttpResponse(json.dumps({"code":0,"msg":u'数据传输错误'}), content_type="application/json") 
    
#@islogin
@isAPP
def DeleteAddress(request):
    if request.method == 'GET':
        #user_id = request.session['user_id']
        user_id = request.GET['userid']
        address_id = int(request.GET['address_id'])
        user = Customer.objects.get(id = user_id)
        try:
            address = user.address_set.get(id = address_id)
        except:
            return HttpResponse(json.dumps({"code":0,"msg":u'该地址不存在'}), content_type="application/json")
        default = address.default
        address.delete()
        address_list = user.address_set.all()
        if address_list and default:
            address_list[0].default = 1
            address_list[0].save()
        return HttpResponse(json.dumps({"code":1,"msg":''}), content_type="application/json")    
    else:
        return HttpResponse(json.dumps({"code":0,"msg":u'数据传输错误'}), content_type="application/json") 
@isAPP
def getCid(request):
    if request.method == 'GET':
        cds = request.GET
        client_id = cds.get('client_id','')
        token = cds.get('token','')
        udid = cds.get('udid',0)
        user_id = cds.get('userid',0)
        update_time = time.time()
        if not client_id or not token:
            return HttpResponse(json.dumps({"code":0,"msg":u'未获取到client_id或token'}), content_type="application/json")
        if not AppGetui.objects.filter(client_id = client_id,token=token,udid=udid,user_id=user_id).exists():
            AppGetui.objects.create(client_id = client_id,token=token,user_id = cds.get('user_id',0),udid=udid,update_time=update_time)
            return HttpResponse(json.dumps({"code":1,"msg":''}), content_type="application/json")  
        else:
            getui_info =  AppGetui.objects.get(client_id = client_id,token=token,user_id = cds.get('user_id',0),udid=udid)
            getui_info.update_time = update_time
            getui_info.save()
            return HttpResponse(json.dumps({"code":0,"msg":u'已记录该客户端用户'}), content_type="application/json")

@csrf_exempt
#@islogin    
def addPicture(request):
    from os.path import join
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES["headphoto"]
            #user_id = form.user_id
            user_id = request.POST.get('userid')
            user = Customer.objects.get(id=user_id)
            path = join('/data/web/LifeExpert/static/headphoto','headphoto-%s.jpg'%user_id)
            #path = join(dirname(__file__),'headphoto','headphoto-%s.jpg'%user_id)
            des_origin_f = open(path,"wb")
            for chunk in f.chunks():
                des_origin_f.write(chunk)
            des_origin_f.close()
            photo_path = 'http://api.huodongjia.com/headphoto/'+'headphoto-%s.jpg'%user_id
            user.headphoto_path=photo_path
            user.save()
            return HttpResponse(json.dumps({"code":1,"msg":u'上传成功',"photopath":photo_path}), content_type="application/json")  
        else:
            return HttpResponse(json.dumps({"code":0,"msg":u"上传失败","errorlist":form.errors}), content_type="application/json") 
    else:
        return HttpResponse(json.dumps({"code":0,"msg":u"post only"}), content_type="application/json")
@isAPP
def delPushInfo(request):
    cds = request.GET
    push_id = cds.get('push_id',None)    
    event_id = cds.get('event_id',None)
    if not push_id or   not event_id:
        return HttpResponse(json.dumps({"code":0,"msg":u"err 1"}), content_type="application/json")
    try:
        #u=Customer.objects.get(id=user_id)
        e=NewEventTable.objects.get(old_event_id=event_id)      
        p=UserPushInfo.objects.get(push_user=push_id)
        p.event.remove(e)
        
        return HttpResponse(json.dumps({"code":1,"msg":u"Request is successful"}), content_type="application/json")
    except:
        return HttpResponse(json.dumps({"code":0,"msg":u"err 2"}), content_type="application/json")
#@isAPP    
def addPushInfo(request):
    cds = request.GET
    user_id = cds.get('user_id',None)
    push_id = cds.get('push_id',None)
    channel_id = cds.get('channel_id',None)
    event_id = cds.get('event_id',None)    
    app_type = cds.get('app_type',None)
    
    if not push_id or not event_id:
        return HttpResponse(json.dumps({"code":0,"msg":u"err 1"}), content_type="application/json")
    
    try:
        
        e=NewEventTable.objects.get(old_event_id=event_id)
        try:
            p=UserPushInfo.objects.get(push_user=push_id)
        except:
            p=UserPushInfo()
            p.push_user=push_id
        if user_id:
            u=Customer.objects.get(id=user_id)
            p.user=u
        
        
        if channel_id:
            p.push_channel=channel_id
        if app_type:
            p.app_type=app_type
        p.save()
        p.event.add(e)

        
        return HttpResponse(json.dumps({"code":1,"msg":u"Request is successful"}), content_type="application/json")
        
    except:
        return HttpResponse(json.dumps({"code":0,"msg":u"err 2"}), content_type="application/json")
        
    
