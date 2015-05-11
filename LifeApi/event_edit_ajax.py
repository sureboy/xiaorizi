#coding:utf-8
#from mptt.models import MPTTModel
from LifeApi.models import NewDistrict,NewEventCat,NewEventTag,NewVenue,NewEventParagraph,NewEventImg,\
                            NewEventFrom,NewEventFromClass,NewEventFromType,NewEventImg,NewEventSeo,NewEventPriceType,\
                            NewEventPriceCurrency,NewEventTable
from django.http import HttpResponse
from django.utils import simplejson as json
from django.db import models
from django.db import connection
import operator
import re
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt 
from django import forms
from django.core.files.base import ContentFile 
from LifeApi.common import sendMail 
from dahuodong.models import SysCommonDistrict
from admin_self.common import city_ss

@csrf_exempt
def send_email(request,email=None,content=None,subject=None):
    if not email:
        email=request.POST.get('email',None)        
    if not content:
        content=request.POST.get('content',None)
    if not subject:        
        subject=request.POST.get('subject',None)

    p={}
    p['flag']=False    
    if   email and content and  subject:
        p['email']=email
        p['content']=content
        p['subject']=subject
        
        mailre=re.compile(r"([0-9a-zA-Z_.]+@[0-9a-zA-Z_.]+)")
        mail=mailre.findall(email)
        
        for i in range(len(mail)):
            mail[i]=mail[i].lower()
            
        
    
        if len(mail)>0:
            p['mail']=mail
            if sendMail(subject.encode('utf-8'),content.encode('utf-8'),mail,host=2):
                p['flag']=True
     
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")       


@csrf_exempt
def save_seo(request):
    name=request.POST.get('name',None)
    title=request.POST.get('title',None)    
    keywords=request.POST.get('keywords',None)
    description=request.POST.get('description',None)

    
    p={}    
    p['flag']=False
    if  keywords :
        
        
        try:
            ci=NewEventSeo.objects.get(keywords=keywords)
        except:
            try:
                ci=NewEventSeo.objects.create(name=name,
                                              title=title,
                                              keywords=keywords,
                                              description=description,
                                                       
                                              )
            except:
                ci=None
        
        if ci:
            p['id']=ci.id
            p['name']=ci.name
            
            p['title']=title
            p['keywords']=keywords
            p['description']=description
            p['flag']=True
             
        
         
     
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")       

@csrf_exempt
def save_img(request):
    
    p={}    
    p['flag']=False 
    
    if request.method == 'POST':#提交表单
        name=request.POST.get('name',False)
        file_content = ContentFile(request.FILES['img'].read()) 
       
        #try:
        m = NewEventImg.objects.create(name=name)
        m.imgs.save(request.FILES['img'].name, file_content)
        p['id']=m.id
        p['url']='%s%s' % (m.server.name if m.server else "http://pic.huodongjia.com/", m.urls)
        p['flag']=True
        p['name']=name
        #except:
        #    pass
    elif request.method == 'GET':
        img_id=request.GET.get('img_id',False)
        order=request.GET.get('order',False)
        url=request.GET.get('url',False)
        if img_id and order:
            try:
                m=NewEventImg.objects.get(id=img_id)
                m.order=order
                m.urls=url
                m.save()
                p['id']=m.id
                p['url']='%s%s' % (m.server.name, m.urls)
                p['flag']=True
                p['name']=m.name
                p['order']=m.order
            except:
                
                pass
                      
            
        

            

 
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")      

def del_tag(request):
    tag_id=request.GET.get('tag_id',False)
    p={}
    p['flag']=False
    if tag_id:
        try:
            Tag=NewEventTag.objects.get(id=int(tag_id))
            for ca in Tag.neweventcat_set.all():
                ca.tag.remove(Tag)
            '''
            for ev in Tag.neweventtable_set.all():
                ev.tag.remove(Tag)
            Tag.delete()
            '''
            p['flag']=True
        except:
            pass
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")  
    
@csrf_exempt
def save_tag(request):
    
    tag=request.POST.get('tag',False)
    cat=request.POST.get('cat',False)
    p={}
    p['flag']=False
    if tag:
        p['tag']=[]
        tag=re.sub(ur"[^\u4e00-\u9fa5\w\.]", ",", tag)
        
        for ta in tag.split(','): 
            
            try:
                ci=NewEventTag.objects.get(name=ta)
            except:
                try:
                    ci=NewEventTag.objects.create(name=ta)
                except:
                    ci=None
            
            if ci:
                pe={}
                pe['id']=ci.id
                pe['name']=ci.name
                pe['flag']=True
                p['tag'].append(pe)
                p['flag']=True
                '''
                try:
                    cats=NewEventCat.objects.get(id=cat)
                    cats.tag.add(ci)
                    
                except:
                    pass
                '''
        
         
     
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")  


@csrf_exempt
def save_city(request):
    
    city_name=request.POST.get('city_name',False)
    city_py=request.POST.get('city_py',False)    
    city_f=request.POST.get('city_f',False)
    p={}    
    p['flag']=False
    if city_name and city_py and city_f:
        try:
            ci=NewDistrict.objects.get(district_name=city_name)
        except:
            try:
                ci=NewDistrict.objects.create(district_name=city_name,
                                              title=city_py,
                                              capital_letter=city_f            
                                              )
            except:
                ci=None
        
        if ci:
            p['id']=ci.id
            p['flag']=True
        
         
     
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json") 
  

def show_city_json(request):
    id_city={}
    map_city=[]
    map_city_list=city_ss()
    '''
    sf=SysCommonDistrict.objects.filter(upid=0).order_by('-displayorder','district_id')
    for s in sf:
        city_m={}
        city_m['id']=0
        city_m['district_name']=s.district_name
        city_m['title']=s.title
        city_m['child']=[]
        city=SysCommonDistrict.objects.filter(upid=s.district_id).order_by('-displayorder','district_id')
        for cit in city:
            try:
                ci=NewDistrict.objects.get(district_name=cit.district_name)
                c_m={}
                c_m['id']=ci.id
                c_m['district_name']=ci.district_name
                c_m['title']=ci.title
                city_m['child'].append(c_m)
            except:
                pass
        map_city_list.append(city_m)
    
    for cityObj in NewDistrict.objects.all():
        city_m={}
        city_m['id']=cityObj.id
        city_m['fid']=cityObj.parent_id
        city_m['district_id']=cityObj.district_id
        city_m['district_name']=cityObj.district_name
        city_m['event_count']=cityObj.event_count
        city_m['title']=cityObj.title
        city_m['child']=[]
        id_city[cityObj.id]=city_m
        map_city_list.append(city_m)
    for ci in map_city_list:
        if id_city.has_key(ci['fid']):
            id_city[ci['fid']]['child'].append(ci)
        else:
            if ci['event_count']>1000:
                map_city.append(id_city[ci['id']])
    
    try: 
        if offset:
            #count = NewDistrict.objects.count()
            offset=int(offset)
            
            if not page:
                page=1
            else:
                page=int(page) 
            diss=NewDistrict.objects.all()[offset*(page-1):offset*page]
        else:
            diss=NewDistrict.objects.all()
        p=[ {"name":dis.district_name, "id":dis.id  } for dis in diss ]
    except:
        p=[]    
    '''
    response = json.dumps(map_city_list)
    return HttpResponse(response, mimetype="application/json")    


def show_FromClass_json(request):
    try:
        diss=NewEventFromClass.objects.all()
        p=[ {"name":dis.name, "id":dis.id  } for dis in diss ]
    except:
        p=[]
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json") 

def show_FromType_json(request):
    try:
        diss=NewEventFromType.objects.all()
        p=[ {"name":dis.name, "id":dis.id  } for dis in diss ]
    except:
        p=[]
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json") 


def show_PriceCurrency_json(request):
    try:
        diss=NewEventPriceCurrency.objects.all()
        p=[ {"name":dis.name, "id":dis.id, "ename":dis.ename  , "rate":dis.rate,"sign":dis.sign } for dis in diss ]
    except:
        p=[]
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json") 

def show_PriceType_json(request):
    try:
        diss=NewEventPriceType.objects.all()
        p=[ {"name":dis.name, "id":dis.id  } for dis in diss ]
    except:
        p=[]
        
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json") 
                
    
@csrf_exempt
def save_from(request):        
    f_class=request.POST.get('f_class',None)
    url=request.POST.get('Website',None)   
    email=request.POST.get('email',None)
    tel=request.POST.get('tel',None)
    content=request.POST.get('f_content',None)
    types=request.POST.get('type',1)
    from_id=request.POST.get('from_id',None)
    
    p={}    
    p['flag']=False
    p['old']=False
    #p['user']=request.user
    ci=None
    if f_class  :
        if from_id:
            try:
                ci=NewEventFrom.objects.get(id=from_id)
                ci.f_Class_id=f_class
                if url:
                    ci.Website=url 
                if email:
                    ci.email=email 
                if tel:
                    ci.tel=tel 
                if content:
                    ci.content=content 
                if types:
                    ci.type_id=types 
    
                ci.last_edit=request.user 
                ci.save()
                p['old']=True
                #obj.from_info.add(ci)
            except Exception,e:
                print e
                ci=None
        if not ci:
            if url:
                try:
                    ci=NewEventFrom.objects.get(Website=url)
                    ci.f_Class_id=f_class
                    if url:
                        ci.Website=url 
                    if email:
                        ci.email=email 
                    if tel:
                        ci.tel=tel 
                    if content:
                        ci.content=content 
                    if types:
                        ci.type_id=types 
        
                    ci.last_edit=request.user 
                    ci.save()
                    p['old']=True
                except:
                    try:
                        ci=NewEventFrom.objects.create(f_Class_id=f_class,
                                                      Website=url,
                                                      email=email,
                                                      tel=tel,
                                                      content=content,
                                                      type_id=types,
                                                      edit=request.user,
                                                      last_edit=request.user,            
                                                      )
                        #obj.from_info.add(ci)
                        
                    except Exception,e:
                        print e        
            else:      
                try:
                    ci=NewEventFrom.objects.create(f_Class_id=f_class,
                                                  #Website=url,
                                                  email=email,
                                                  tel=tel,
                                                  content=content,
                                                  type_id=types,
                                                  edit=request.user,
                                                  last_edit=request.user,            
                                                  )
                    #obj.from_info.add(ci)
                    
                except Exception,e:
                    print e
                     

    if ci:
        p['id']=ci.id
        try:
            p['f_class']=ci.f_Class.name
            p['f_class_id']=ci.f_Class.id
        except:
            pass
            
        p['Website']=ci.Website
        p['content']=ci.content
        try:
            p['type']=ci.type.name
            p['type_id']=ci.type.id
        except:
            pass
        p['flag']=True
    

   
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")   

def show_from_json(request,offset = 15,page = 1):
   
    try: 
        if offset:
             
            offset=int(offset)
            
            if not page:
                page=1
            else:
                page=int(page) 
            diss=NewEventFrom.objects.all()[offset*(page-1):offset*page]
        else:
            diss=NewEventFrom.objects.all()[:20]
        p=[ {"id":dis.id,"f_Class":dis.f_Class.name,"Website":dis.Website,"email":dis.email,"tel":dis.tel,"content":dis.content,"type":dis.type,"edit":dis.edit } for dis in diss ]
    except:
        p=[]    
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")   

 
def show_img_json(request,offset = 15,page = 1):
   
    try: 
        if offset:             
            offset=int(offset)            
            if not page:
                page=1
            else:
                page=int(page) 
            diss=NewEventImg.objects.all().order_by('-order')[offset*(page-1):offset*page]
        else:
            diss=NewEventImg.objects.all().order_by('-order')[:20]
            
        p=[ {"id":dis.id,"name":dis.name,"url":'%s%s' % (dis.server.name, dis.urls),"order":dis.order } for dis in diss ]
    except:
        p=[]    
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")  
def show_seo_json(request,offset = 15,page = 1):
   
    try: 
        if offset:
             
            offset=int(offset)
            
            if not page:
                page=1
            else:
                page=int(page) 
            diss=NewEventSeo.objects.all()[offset*(page-1):offset*page]
        else:
            diss=NewEventSeo.objects.all()[:20]
        p=[ {"id":dis.id,"name":dis.name,"title":dis.title,"keywords":dis.keywords,"description":dis.description} for dis in diss ]
    except:
        p=[]    
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")  

def find_seo_json(request,offset = 15,query=''):
    
    diss=NewEventSeo.objects.order_by('-id')
    
    
    if query.isdigit():
        diss = diss.filter(id=query)
    else:
        
        import jieba
        
        
        for bit in  query.split():
            seg_list = jieba.cut(bit)
            or_queries=[]
            for se in seg_list:
                #print se
                or_queries += [models.Q(**{orm_lookup: se})
                  for orm_lookup in ['name__icontains','title__icontains','keywords__icontains','description__icontains']]
            #arg+=[Q(address__icontains=qu)|Q(title__icontains=qu)|Q(city__district_name__icontains=qu)] 
 
            diss = diss.filter(reduce(operator.or_, or_queries))   
            #print diss.count()
         
    p=[ {"id":dis.id,"name":dis.name,"title":dis.title,"keywords":dis.keywords,"description":dis.description} for dis in diss[:offset] ]

    #p = [ {"name":"%s" % (Add.title if Add.title else Add.address), "id":Add.venue_id ,"city":Add.city.district_name if Add.city  else ''} for Add in Addr[:20] ]
    #p.append([{'sql':connection.queries}])
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")


def find_from_json(request,offset = 15,query=''):
    diss=NewEventFrom.objects
    
    if query.isdigit():
        diss = diss.filter(id=query)
    else:
        
        import jieba
        
        
        for bit in  query.split():
            seg_list = jieba.cut(bit)
            or_queries=[]
            for se in seg_list:
                or_queries += [models.Q(**{orm_lookup: se})
                  for orm_lookup in ['f_Class__icontains','Website__icontains','email__icontains','tel__icontains','content__icontains']]
            #arg+=[Q(address__icontains=qu)|Q(title__icontains=qu)|Q(city__district_name__icontains=qu)] 
            
            diss = diss.filter(reduce(operator.or_, or_queries))   
         
    p=[ {"id":dis.id,"f_Class":dis.f_Class.name,"Website":dis.Website,"email":dis.email,"tel":dis.tel,"content":dis.content,"type":dis.type,"edit":dis.edit } for dis in diss ]
    

    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")   
  
        
