#coding:utf-8
#from mptt.models import MPTTModel
from LifeApi.models import NewDistrict,NewEventCat,NewEventTag,NewVenue,NewEventParagraph,NewEventImg,\
                            NewEventFrom,NewEventTable,NewEventParagraphTag,NewOrderMessage, \
                            NewEventPriceUnit
from django.http import HttpResponse
from django.utils import simplejson as json
from django.db import models
from django.db import connection
import operator
import re,time
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from LifeApi.common import sendMail,find_cat_fid
from admin_self.common import oldEventToNewEvent,NewCatUrl,event_city_cat,NewformatEvent,ip_Filter, cat_iter
from admin_self.froms import fill_topic_tree
from sponsor.models import NewSponsor

def update_cache():
    
    
    p=[]    
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
    
def get_from_info(request,query):
    
    '''
    # [^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$ 
    # ^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$
    mailre = re.compile(r"(\w+@\w+\.\w+)")
    f = open("a.txt",'r')
        >>> res = r'http:\/\/.*?\/'
     >>> m = re.findall(res,s)
    
    content = f.read()
    print "\n".join(mailre.findall(content))
    '''
    http=r'http:\/\/.*?\/'
    mailre = re.compile(http)
    mailre.findall(query)
    email=r'[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$'
    tel=r'^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$'
    
    p=[]    
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
    
def Txt_data_list(request,query):
    
    query= query.split(',')
    diss=NewEventParagraph.objects.filter(id__in=query).order_by('txt_order','-id')
    p=[ {"name":"%s" % (dis) , "id":dis.id ,"order":dis.txt_order ,"txt":dis.txt,"tag":dis.tag,'tab_id':dis.cat_name_id,'tab_name':dis.cat_name.name,'img':[{'urls':imgs.urls,'name':imgs.name} for imgs in dis.img.all()] } for dis in diss ]
    

    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def Addr_data_str(request,query=None):
 
    p=[]
    Addr=None
    if query:
        if query.isdigit():
            Addr=NewVenue.objects.order_by('-event_count')
            Addr = Addr.filter(id=query)
        else:
            
            #import jieba
            
            
            #for bit in  query.split():
                #seg_list = jieba.cut(bit)
            or_queries=[]
            for se in query.split():
                or_queries += [models.Q(**{orm_lookup: se})
                  for orm_lookup in ['address__icontains','title__icontains','city__district_name']]
            #arg+=[Q(address__icontains=qu)|Q(title__icontains=qu)|Q(city__district_name__icontains=qu)] 
            if or_queries:
                Addr=NewVenue.objects.order_by('-event_count')
                Addr = Addr.filter(reduce(operator.or_, or_queries))   
     
    if Addr:
        p = [ { "address":Add.address,"title":Add.title,"longlat":"%s-%s" % (Add.latitude_baidu,Add.longitude_baidu) if Add.latitude_baidu else '', "id":Add.id ,"city":Add.city.district_name if Add.city  else ''} for Add in Addr[:20] ]
    #p.append([{'sql':connection.queries}])
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

# 对主办方进行查询，返回格式化后的json
# 以Addr_data_str为模板书写
def sponsor_data_str(request, query=None):

    p = []
    ms = None
    if query:
        if query.isdigit():
            ms = NewSponsor.objects.filter(id=query)
        else:
            or_queries = []
            for se in query.split():
                or_queries += [models.Q(**{orm_lookup: se}) for orm_lookup in ['name__icontains']]
            if or_queries:
                ms = NewSponsor.objects.filter(reduce(operator.or_, or_queries))
    if ms:
        p = [ { "name": s.name,"pic_id":s.pic.id if s.pic else None,"intro":s.intro,"pic":"http://pic.huodongjia.com/"+s.pic.urls if s.pic else None, "id": s.id, "is_verify": s.is_verify, 'event_count': s.event_count if s.event_count else 0} for s in ms[:20] ]
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

# 返回某活动的所有主办方
def get_event_sponsor(request):
    eid = request.GET.get('id')
    response = None
    result = []
    if eid:
        ms = NewSponsor.objects.filter(events__in=[eid])
        result = [{ "name": s.name,"pic_id":s.pic.id if s.pic else None,"intro":s.intro,"pic":"http://pic.huodongjia.com/"+s.pic.urls if s.pic else None, "id": s.id, "is_verify": s.is_verify, 'event_count': s.event_count if s.event_count else 0} for s in ms]
    else:
        pass
    response = json.dumps(result)
    return HttpResponse(response, mimetype="application/json")

def Addr_data(request,query):

    query= query.split()
    diss=NewVenue.objects.filter(id__in=query) 
    p=[ {"address":dis.address, "longlat":"%s-%s" % (dis.latitude_baidu,dis.longitude_google) , "id":dis.id ,"title":dis.title,"city":dis.city.id if dis.city  else '',"city_name":dis.city.district_name if dis.city  else '' } for dis in diss ]
 
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")



def District_data(request,query):
    try: 
        query= query.split(',')
        diss=NewDistrict.objects.filter(id__in=query) 
        p=[ {"name":dis.district_name, "id":dis.id , "py":dis.title  } for dis in diss ]
    except:
        p=[]    
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")


def Cat_data(request,query=False):
    
    if query:
        try: 
            query= query.split(',')
            diss=NewEventCat.objects.filter(id__in=query) 
            p=[ {"name":dis.name, "id":dis.id ,'tag':[{'name':tags.name,'id':tags.id} for tags in dis.tag.all().order_by('-hot')[:100]],\
                 'ftag':[{'name':tags.name,'id':tags.id} for tags in dis.parent.tag.all().order_by('-hot')] if dis.parent else [] } for dis in diss ]
        except:
            p=[]
    else:
        try:
            ch = [()]
            fill_topic_tree(choices = ch, only_py=True)
            choices = ch[0]
            p=[{"name":option_label, "id":option_value} for option_value, option_label in  choices]
        except:
            p=[]
      

    
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")


# 返回某活动的所有分类
def get_event_cat(request):
    eid = request.GET.get('id')
    response = None
    result = []
    exclude_id=[]
    top_level_cat_id = [91, 92]
    if eid:
        e = NewEventTable.objects.get(pk=eid)
        e_all_cat = e.cat.all()
        # 获得所有的分类，并筛选出需要的分类
        all_cat = cat_iter(exclude_id=exclude_id, new=True)
        need_cat = []
        need_cat_id_list = top_level_cat_id
        for cat in all_cat:
            if cat['id'] in need_cat_id_list:
                need_cat.append(cat)
        # 寻找选中的分类，增加新的信息
        for e_cat in e_all_cat:
            cat_id = e_cat.id
            for first in need_cat:
                children = first['children']
                if first['id'] == cat_id:
                    first['selected'] = True
                for second in children:
                    if second['id'] == cat_id:
                        second['selected'] = True
        result = need_cat
    else:
        # 新建活动的时候，没有id传入，则返回所有可选分类
        # 获得所有的分类，并筛选出需要的分类
        all_cat = cat_iter(exclude_id=exclude_id, new=True)
        need_cat = []
        need_cat_id_list = top_level_cat_id
        for cat in all_cat:
            if cat['id'] in need_cat_id_list:
                need_cat.append(cat)
        result = need_cat
    response = json.dumps(result)
    return HttpResponse(response, mimetype="application/json")


def Tag_data(request,query):
    try: 
        query= query.split(',')
        diss=NewEventTag.objects.filter(id__in=query).order_by('-id')[:50] 
        p=[ {"name":dis.name, "id":dis.id ,'hot':dis.hot  } for dis in diss ]
        
    except:
        p=[]   
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def img_data(request,query):
    try: 
        query= query.split(',')
        diss=NewEventImg.objects.filter(id__in=query).order_by('-order')  
        p=[ {"name":dis.name, "id":dis.id,"url":dis.server.name+dis.urls  if dis.server else 'http://pic1.qkan.com/'+dis.urls   } for dis in diss ]
    except:
        p=[]   
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def float_or_none(data):
    if data:
        return float(data)
    else:
        return ''

def price_data(request):
    ids = request.GET.get('id')
    if ids:
        ids = ids.split(',')
        price_list = NewEventPriceUnit.objects.filter(event_id__in=ids).order_by('-id')
        p = [{'price_id': p.id, 'price': float_or_none(p.price), 
              'sale': float_or_none(p.sale), 'discount': float_or_none(p.discount), 
              'original_price': float_or_none(p.original_price), 'currency_id': p.Currency_id, 
              'begin_time': p.begin_time.strftime('%Y-%m-%d %H:%M'),
              'end_time': p.end_time.strftime('%Y-%m-%d %H:%M'),
              'status': p.status, 'content': p.content if p.content else ''} for p in price_list]
    else:
        p = []

    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

@csrf_exempt
def save_txt(request):
    txt_list=  request.POST.getlist("txtlist[]" )
    event_id=request.POST.get('event_id',False)
    
    if txt_list:
        p=[]
        
        
        for t in txt_list:
            t=json.loads(t)
            p1={}
             
            if t.has_key('txt'):
                txts=t['txt']
            else:
                txts=''
            
            if txts:
                
                if t.has_key('order'):
                    txt_orders=t['order']
                else:
                    txt_orders=''
                na=None
                if t.has_key('tabname'):
                    try:
                        na=NewEventParagraphTag.objects.get(name=t['tabname'])
                    except:
                        try:
                            na=NewEventParagraphTag.objects.create(
                                                                name= t['tabname'] 
                                                                   )
                        except:
                            na=NewEventParagraphTag.objects.get(id=2317)
                        
                if na:
                    pa=None
                    
                    if t.has_key('id'):
                        if na:
                            try:
                                pa=NewEventParagraph.objects.get(id=t['id'])
                                pa.txt=txts
                                pa.txt_order=txt_orders
                                pa.cat_name=na
                                pa.save()
                    
    
                            except Exception,e:
                                print e
                                 
                        else:
                            print 'not na'
                       
                    else:
                        pa=NewEventParagraph.objects.create(
                                                            txt_order=txt_orders,
                                                            txt=txts,
                                                            cat_name=na
                                                         
                                                         ) 
                    if event_id:
                        try:
                            ev=NewEventTable.objects.get(id=event_id)
                            ev.paragraph.add(pa)
                        except:
                            pass 
                        
                    
                         
                    if pa:
                        p1['flag']=True
                        p1['id']=pa.id
                    else:
                        p1['flag']=False
                        
                    p.append(p1)
                else:
                    p1['flag']=False
                    p.append(p1)
                    
                    
                         
        
    else:
        
        ids= request.POST.get('id',False)
        event_id=request.POST.get('event_id',False)
        txts=request.POST.get('txts','')    
        tab_txt=request.POST.get('tab_txt','')
        
        tab_order=request.POST.get('tab_order',False)
        
        tab_txt=re.sub(ur"[^\u4e00-\u9fa5\w]", "", tab_txt)
        p={}
        if ids and txts:
            p['msg']='update'
            
            try:
                pa=NewEventParagraph.objects.get(id=ids)
                pa.txt=txts
                pa.txt_order=tab_order
                if tab_txt:
                    try:
                        tab=NewEventParagraphTag.objects.get(name=tab_txt)
                        if pa.cat_name_id!=tab.id:
                            pa.cat_name_id=tab.id
                    except:
                        tab=NewEventParagraphTag.objects.create(name=tab_txt)
                        pa.cat_name_id=tab.id
                        
                    
                #if pa.cat_name.nam!=tab_txt:
                    
                
                pa.save()
                p['info']='已经保存'
            except:
                p['info']='信息保存失败'
        elif txts:
            p['msg']='save'
     
            
            try:
                tab=NewEventParagraphTag.objects.get(name=tab_txt)
            except:
                tab=NewEventParagraphTag.objects.create(name=tab_txt)
            try:
                pa=NewEventParagraph.objects.create(txt=txts,cat_name=tab,txt_order=tab_order)
                if event_id:
                    try:
                        ev=NewEventTable.objects.get(id=event_id)
                        ev.paragraph.add(pa)
                    except:
                        pass
                p['info']='已经添加'
                p['txt_id']=pa.id
                
            except:
                p['info']='信息保存失败'
     
            
             
         
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")    
    
def frominfo_data(request,query):
    #p=[query]
     
    query= query.split(',')
    #for k in  range(len(query)):
        #query[k]=int(query[k])
    p=[]
    diss=NewEventFrom.objects.filter(id__in=query) 
 
    p=[{"id":dis.id,"f_Class":dis.f_class.name if dis.f_class else None, "Website":dis.website,"email":dis.email ,"tel":dis.tel,"content":dis.content,"type":dis.type.name if dis.type else None ,"l_edit":dis.last_edit.username if dis.last_edit else None     } for dis in diss ]
     
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def find_fid(cats,pn=[]):
    
    for ta in NewEventParagraphTag.objects.filter(cat  = cats ):
        pn.append({'id':ta.id,'name':ta.name})    
        
    if cats.parent:
        find_fid(cats.parent,pn )
        
    

def get_paragraph_tag(request,query=0):
    p=[]
    if query:
        query= query.split(',')
        for ta in NewEventParagraphTag.objects.filter(cat_id__in=query):
            p.append({'id':ta.id,'name':ta.name})
        
        for cats in NewEventCat.objects.filter(id__in=query):
            find_fid(cats,pn=p)
        
         
    if not p:
        for ta in NewEventParagraphTag.objects.all():
            p.append({'id':ta.id,'name':ta.name})
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

def send_mail_from(request,event_id,event_name,mail=''):
    try:
        content='询问如何参加%s,请问该活动的费用是多少，如何报名，有官方网站或相关资料吗？谢谢' % event_name
        subject = u'信息求助'  
        sendMail(subject,content,to_list=[mail])
        
    except:
        p=[]
    response = json.dumps(p)
    
def update_save(request,query):
    
    p1=oldEventToNewEvent(query,False)
    p=[]
    if p1:
        for ci in p1.city.all():
            cat_l=NewCatUrl(0,ci.title)
            for ca in p1.cat.all():
                if not cat_l.has_key(ca.id):
                    NewCatUrl(0,ci.title,True)
                     
                fid=find_cat_fid(NewCatUrl(2,ci.title),ci.id,ci.title) 
                for f in fid:
                    
                    event_city_cat(ci.id,f['id'],True)
                
        #p=[p1.id,p1.old_event.event_id,p1.old_event.event_name]
        
        NewformatEvent(p1,p1.id,True)
        msg=u'保存成功'
        p={'success':True,'msg':msg,'eid':msg}
                
    else:
        p={'msg':'err'} 
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
     
def save_event(request,query):
    name= request.POST.get('name','')
    ename= request.POST.get('name','')
    fname= request.POST.get('name','')
    name= request.POST.get('name','')
    citys=request.POST.get('city','')
    if citys:
        citys=citys.split(',')
 
    from_info=request.POST.get('from_info','')
    cat=request.POST.get('cat','')
    if cat:
        cat=cat.split(',')    
    tag=request.POST.get('tag','')
    if tag:
        tag=tag.split(',')        
                
        
    pass

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
    eventId = request.POST.get('event_id',None)
    eventName = request.POST.get('event_name',None)
    name = request.POST.get('name',None)
    phone = request.POST.get('phone',None)
    email = request.POST.get('email',None)   
    content=request.POST.get('content',None) 
    if not phone and not email and not content:
        p['msg']='Incomplete information'
        return HttpResponse(json.dumps(p), content_type="application/json")
    try:
        timeNow = time.time()
        NewOrderMessage.objects.create(event_id = eventId,
                                       event_name = eventName,
                                       msg_name = name,
                                       msg_tel = phone,
                                       msg_email = email,
                                       msg_content = content,
                                       msg_addtime = timeNow,
                                       type=1,
                                       )
    except:
        p['msg']='Incomplete information'
        return HttpResponse(json.dumps(p), content_type="application/json")        
    p['msg']='Request is successful'
    p['code']=1
    subject=u'活动家留言，邮件提醒  %s %s' % (phone,email)
    cont=u'活动家留言\r\n'
    cont+=u'活动:<a href="http://www.huodongjia.com/event-%s.html">%s</a>\r\n' % (eventId,eventName)
    cont+=u'姓名:%s\r\n' % name
    cont+=u'手机:%s\r\n' % phone
    cont+=u'邮箱:%s\r\n' % email
    cont+=u'内容:%s\r\n' % content
    #log.debug(cont)
    sendMail(subject.encode('utf-8'),cont.encode('utf-8'),['shaye7@qq.com','252925359@qq.com'])
    
    return HttpResponse(json.dumps(p))

