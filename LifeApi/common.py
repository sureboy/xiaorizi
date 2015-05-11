#coding:utf-8
from LifeApi.models import NewEventTable, NewEventCat,NewDistrict,NewVenue, NewEventPrice,\
                            NewEventParagraph,NewEventImg,OldEvent,NewEventParagraphTag,\
                            NewEventPriceType,NewEventPriceCurrency,Crowfunding,\
                            NewEventTag, NewEventImgServer,NewCatInfo, NewArticle,NewEventSeo,feelnum
from sponsor.models import NewSponsor
                                                      
from LifeApi.old_models import SysVenue,SysCommonDistrict,SysEvent
from django.db.models import Q 
from django.http import HttpResponse
from django.utils import simplejson as json
import smtplib 
from email.mime.text import MIMEText
from django.shortcuts import render_to_response
import datetime ,time,random
from admin_self.froms import  resolveContent
from django.core.cache import cache
import re 
import hashlib
from dateutil.relativedelta import relativedelta,MO
from email.mime.multipart import MIMEMultipart
from django.http import Http404

 
from email.header import Header
from email.utils import formataddr



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

 
def oldEventToNewEvent(ids=0,edit=True):
    if not ids:
        return None
    oldevent=None
    try:
        oldevent= OldEvent.objects.get(event_id=ids)
    except:
        return None
    
    if not oldevent:
        return None
    
    
    '''
    try:
        oldevent= NowEvent.objects.get(event_id=ids)
    except:
        event=OldEvent.objects.get(event_id=ids)
        
     
        data={}
        for f in event._meta.fields:
            try:
                data[f.name] = getattr(event, f.name)
            except:
                break
        try:
            oldevent = NowEvent.objects.create(**data)
            oldevent.save()
        except:
            return None
    
    '''
    
    #oldevent=NowEvent.objects.create(oldevent)ids
    #p=oldevent.neweventtable_set[0]  self.formfield_overrides
    p=None
    try: 
        p=NewEventTable.objects.get(old_event_id=ids)
        if edit:  
            #p.save() 
            return p  
        
         
        
    except:
        pass
    
    try:
        begin_dates = time.localtime(oldevent.event_begin_time)
        begin_dates = datetime.datetime(*begin_dates[:6])
    except:
        begin_dates=''
    
    try:
        if oldevent.event_islongtime==0:
            end_dates = time.localtime(oldevent.event_end_time)
            end_dates = datetime.datetime(*end_dates[:6])
        else:
            
            jo= '2015-12-30' 
            date_time=jo.split('-') 
            end_dates = datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
            #end_dates = None
    except:
        #state=oldevent.event_islongtime
        jo= '2015-12-30' 
        date_time=jo.split('-') 
        end_dates = datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
        #end_dates=None
    
    
 
    if not p:
        
    #con_list=

            
        try:
            p=NewEventTable.objects.create(
                                           #id=ids,
                                       name=oldevent.event_name,
                                       fname =oldevent.event_app_name if oldevent.event_app_name else '' ,
                                        
                                       old_event=oldevent,
                                       #content=oldevent.event_content if oldevent.event_content else '',
                                       begin_time=begin_dates,
                                       end_time=end_dates,   
                                       order=oldevent.event_recomend if oldevent.event_recomend else 0,
                                       hot=oldevent.event_rank if oldevent.event_rank else 0,
                                       search=re.sub(ur"[^\u4e00-\u9fa5\w]", " ", oldevent.event_search),
                                                                           
                                  )
        except:
 
            try:
                p=NewEventTable.objects.create(
                                   #id=ids,
                               name=re.sub(ur"[^\u4e00-\u9fa5\w]", " ", oldevent.event_name), 
                               fname =oldevent.event_app_name if oldevent.event_app_name else '' ,
                                
                               old_event=oldevent,
                               #content=oldevent.event_content if oldevent.event_content else '',
                               begin_time=begin_dates,
                               end_time=end_dates,   
                               order=oldevent.event_recomend if oldevent.event_recomend else 0,
                               hot=oldevent.event_rank if oldevent.event_rank else 0,
                               search=re.sub(ur"[^\u4e00-\u9fa5\w]", " ", oldevent.event_search),
                                                                   
                          )
 
                
            except:
                return None
            
    p.begin_time=begin_dates
    p.end_time=end_dates                
    
    if oldevent.event_time_expire is 2:
        p.state=int(oldevent.event_time_expire)
    
    else:             
        p.state=int(oldevent.event_islongtime) if oldevent.event_islongtime else 0
    p.hot=int(oldevent.event_rank) if oldevent.event_rank else 0
    
    if oldevent.event_editor:
        p.img.clear()
    if oldevent.event_img:
        try:
            imgss=NewEventImg.objects.get(name=oldevent.event_img)
             
            
            p.img.add(imgss)
        except:         
            try: 
                imgss=NewEventImg.objects.create(
                                           name=oldevent.event_img,
                                           urls=oldevent.event_img,
                                           server= NewEventImgServer.objects.get(id=1),
                                           #imgs=None,
                                           )
               
                p.img.add(imgss)
            except:
                pass
             

        
    p.cat.clear()    
    try:
        cat_now=NewEventCat.objects.get(cat_id=oldevent.event_cat  )
        if cat_now:            
            p.cat.add(cat_now)
            try:
                p.seo=NewEventSeo.objects.get(name=cat_now.name)
                #p.seo.save()               
            except:
                try:
                    if cat_now.parent:
                        p.seo=NewEventSeo.objects.get(name=cat_now.parent.name)
                        #p.seo.save()
                except:
                    pass
        
            
            
            
            
    except:
        print 'update cat %s' % p.id
        pass
    
    
    if oldevent.event_cool:
        try:
            cat_cool=NewEventCat.objects.get(cat_id=oldevent.event_cool+1000  )
            if cat_cool:
                #p.cat.clear()
                p.cat.add(cat_cool)
        except:
            pass
 

    
    
    try:
        tag_str= oldevent.event_cat_tag.replace(' ','')
        if tag_str:
            for tag in tag_str.split(','):
                try:
                    t=NewEventTag.objects.get(name=tag)
                    if not t:
                        t=NewEventTag.objects.create(name=tag)
                except:
                    t=NewEventTag.objects.create(name=tag)
                    
                p.tag.add(t)
    except:
        pass
     
    
    Ty=NewEventPriceType.objects.get(id=oldevent.event_price_model ) if oldevent.event_price_model  else NewEventPriceType.objects.get(id=4 ) if  oldevent.event_isfree else  NewEventPriceType.objects.get(id=6 ) 
    cu=NewEventPriceCurrency.objects.get(id=oldevent.event_price_currency ) if oldevent.event_price_currency  else NewEventPriceCurrency.objects.get(id=1 )

    mi=0
    mx=0   
    price=''
    
    if Ty.id == 3:
        try:
            k=Crowfunding.objects.get(event_id=oldevent.event_id)
            if k:
                price=k.cf_price#oldevent.cf_price if oldevent.cf_price else ''
                mx=k.cf_total#oldevent.cf_total if oldevent.cf_total else 0
                mi=k.cf_already
        except: 
            try:
                if p.Price:
                    price=p.Price.str# ''
                    mi=p.Price.min
                    mx=p.Price.max
            
            except: 
                mi=0
                mx=0
                #pass
                #p.Price=None
                

                              
    else:
        price=oldevent.event_price if oldevent.event_price else Ty.name if Ty else ''  
        if  price:
            if price==u'收费':
                Ty=NewEventPriceType.objects.get(id=5)
        else:
            Ty=NewEventPriceType.objects.get(id=7)
            price=''
                   
        mx=oldevent.event_highprice if oldevent.event_highprice else 0                 
        mi=oldevent.event_lowprice if oldevent.event_lowprice else 0 
        
    sa=oldevent.event_discount_price if oldevent.event_discount_price else ''
    po=oldevent.event_discount if oldevent.event_discount else ''     
    
        
            
 
    if not p.Price:  
        try:          
            p.Price=NewEventPrice.objects.create(                                         
                 Currency=cu,         
                 Type=Ty,         
                 str=price,# if price else '',
                 sale=sa,
                 points=po,
                 min=mi if mi else 0,
                 max=mx if mx else 0,      
                 ) 
        except Exception,e:
            print 'price_err'
            print e        
        
    else:
        p.Price.Currency=cu
        p.Price.Type=Ty
        p.Price.str=price
        p.Price.sale=sa
        p.Price.points=po
        p.Price.min=mi if mi else 0
        p.Price.max=mx if mx else 0
        try:
            p.Price.save()
        except Exception,e:
            print 'price_err1'
            print e
 
    #print 'price_model %s' % p.Price.Type.id     
    p.city.clear()   
    p.addr.clear()  
    try:
        
        citys=NewDistrict.objects.get(district_id=oldevent.district_id  )
        if citys:
            #p.city.clear()
            p.city.add(citys)
        
    except:
        try:
            ol_event=SysEvent.objects.get(event_id=oldevent.event_id)
            try:
                cityss=SysCommonDistrict.objects.get(district_id=ol_event.district_id)
                try:
                    citys=NewDistrict.objects.create(
                                                   district_id=cityss.district_id,
                                                   district_name=cityss.district_name,
                                                   title=cityss.title,                                                
                                                   usetype=cityss.usetype,
                                                   capital_letter=cityss.capital_letter,
                                                   baidu_code=cityss.baidu_code,
                                                   displayorder=cityss.displayorder,
                                                   recomendindex=cityss.recomendindex                                                  
                                                  )
                    #p.city.clear()
                    p.city.add(citys)
                except:
                    #print u'城市创建错误'
                    pass
            except:
                #print u'旧数据库查询错误'
                pass
        except:
            #print u'没有旧数据'
            pass
    if oldevent.venue_id:
        try:
            venu=NewVenue.objects.get(venue_id=oldevent.venue_id )
            if venu:
                venu.address
                #p.addr.clear()
                p.addr.add(venu)
                #p.city.add(venu.city)
            
            
        except:
    
            try:
                addrs=SysVenue.objects.get(venue_id=oldevent.venue_id)
                
                new_addr=NewVenue.objects.create(
                                   venue_id=addrs.venue_id,
                                   longitude_baidu=addrs.venue_longitude_baidu, 
                                   latitude_baidu=addrs.venue_latitude_baidu, 
                                   longitude_google=addrs.venue_longitude_google,
                                   latitude_google=addrs.venue_latitude_google,
                                   city=citys,                                           
                                   address=addrs.venue_address,
                                   title=addrs.venue_title,
                                   alias=addrs.venue_alias,
                                   )  
                #p.addr.clear()
                p.addr.add(new_addr)
            except:
    
                try:
                    v_i=[]
                    v_i=oldevent.venue_info.split()
                    if citys and oldevent.event_address and 0<len(v_i) :
                        
                         
                        v=NewVenue.objects.create(
                                                title=v_i[0],
                                                address=oldevent.event_address,
                                                city=citys
                                                )
                        #p.addr.clear()
                        p.addr.add(v)
                except Exception,e:
                    print 'NewVenue_err'
                    print e
 
            
        
        
         
    
    try:
        con_txt=resolveContent(oldevent.event_content)
    except:
        con_txt=[]
        
    if con_txt:
       
        p.paragraph.all().delete()        
        
        for t in con_txt:
            try:
                na=NewEventParagraphTag.objects.get(name=t[0])
            except:
                try:
                    na=NewEventParagraphTag.objects.create(
                                                        name= t[0] 
                                                           )
                except:
                    na=NewEventParagraphTag.objects.get(id=2317)
                     
            if na:
                try:
                    if t[1]:                        
                        txt=NewEventParagraph.objects.create(
                                                         txt=t[1],
                                                         cat_name=na,
                                                         )
                        p.paragraph.add(txt)
                except:
                    print 'not txt %s' % t[0]
                    continue
            else:
                print 'not%s' % t[0]
    if not p.paragraph.all().count():
        try:
            if oldevent.event_content:
                txt1=NewEventParagraph.objects.create(
                                     txt=oldevent.event_content,
                                     cat_name_id=2317
                                     )
                p.paragraph.add(txt1)
            else:
                print 'not txt'
        except:
            print 'not txt__'
            
           

 
    
    if oldevent.event_isshow:           
        #iss=NewEventTableType.objects.get(id=5)
        
        p.isshow_id=oldevent.event_isshow
        
    #if oldevent.event_islongtime==1:
        #p.end_time=None
            #p.save()
            
    p.order = int(oldevent.event_recomend) if oldevent.event_recomend else 0 
    p.name=oldevent.event_name
    p.fname =oldevent.event_app_name if oldevent.event_app_name else ''  
    p.search=re.sub(ur"[^\u4e00-\u9fa5\w]", " ", oldevent.event_search)    
    try:
        p.save()
    except Exception,e:
        print 'err save'
        print e
    return p



def NewCity(type=0,new=False):
    
    '''
    baiDuCodeDict = cache.get('NewbaiDuCodeDict') #通过百度代码获取城市信息 元组
    titleDict=cache.get('NewtitleDict')#通过城市名称获取 元组
    districtIdDict=cache.get('NewdistrictIdDict')#通过城市旧id获取 元组
    id_city =cache.get('id_city')#通过城市id获取字典
    map_city= cache.get('map_city')#城市地图 字典
    map_city_list= cache.get('map_city_list')#城市关系 字典
    '''
    
    
    
    if type==0:
        map_city= cache.get('map_city')#城市地图 字典
        if not map_city :
            new=True
    elif type==1:   
        id_city =cache.get('id_city')#通过城市id获取字典
        if not id_city :
            new=True 
    elif type==2:  
        districtIdDict=cache.get('NewdistrictIdDict')#通过城市旧id获取 元组         
        if not districtIdDict :
            new=True 
    elif type==3:            
        #return titleDict
        titleDict=cache.get('NewtitleDict')#通过城市名称获取 元组
        if not titleDict :
            new=True        
    elif type==4:   
        baiDuCodeDict = cache.get('NewbaiDuCodeDict')   #通过百度代码获取城市信息 元组      
        if not baiDuCodeDict :
            new=True
    else:
        map_city_list= cache.get('map_city_list')#城市关系 字典
        if not map_city_list:
            new=True
         
    
    
    
    
    
    
    if new : 
        baiDuCodeDict={}
        titleDict={}
        districtIdDict={}
        id_city={}
        map_city=[]
        map_city_list=[]
        #.filter(event_count__gte=4)
        for cityObj in NewDistrict.objects.order_by('-event_count'):
            baiDuCodeDict[cityObj.baidu_code] = (cityObj.id,cityObj.district_name,cityObj.title )
            districtIdDict[cityObj.district_id] = (cityObj.id,cityObj.district_name,cityObj.title )
            titleDict[cityObj.title] = (cityObj.id,cityObj.district_name,cityObj.title )
            city_m={}
            city_m['id']=cityObj.id
            city_m['fid']=cityObj.parent_id
            city_m['district_id']=cityObj.district_id
            city_m['district_name']=cityObj.district_name
            city_m['title']=cityObj.title
            city_m['event_count']=cityObj.event_count
            city_m['child']=[]
            id_city[cityObj.id]=city_m
            map_city_list.append(city_m)
        for ci in map_city_list:
            if id_city.has_key(ci['fid']):
                if ci['event_count']>4:
                    id_city[ci['fid']]['child'].append(ci)
            else:
                if ci['event_count']>1000:
                    map_city.append(id_city[ci['id']])
                
        '''
        map_city_s=[]
        for k in range(len(map_city)):
            #if len(map_city[k]['child'])>4:
            map_city_s.append(map_city[k])
        map_city=map_city_s
        '''
        if id_city:        
            cache.set('NewbaiDuCodeDict',baiDuCodeDict,86400)
            cache.set('NewtitleDict',titleDict,86400)
            cache.set('NewdistrictIdDict',districtIdDict,86400)
            cache.set('id_city',id_city,86400)#通过城市id获取 字典
            cache.set('map_city',map_city,86400)#城市地图 字典
            cache.set('map_city_list',map_city_list,86400)#城市关系 字典
        
    
    #titleDict[cityObj.title] = (cityObj.district_id,cityObj.district_name,cityObj.title)
    if type==0:
        return map_city
    elif type==1:            
        return id_city
    elif type==2:            
        return districtIdDict
    elif type==3:            
        return titleDict
    elif type==4:            
        return baiDuCodeDict 
    else:
        return map_city_list

def make_cat(cat=object,city_id=None):
    cat_x={}
    cat_x['catname']= cat.name
    ev=NewEventTable.objects.filter(isshow__in=(1,8)).filter(end_time__gte=datetime.date.today())
    
    if city_id:
  
        ev=ev.filter(city=city_id)
       
     
    ev=ev.filter(cat= cat.id )
  
    cat_x['count']=ev.count()
    #if cat_x['count']: 
        #cat_x['catname']+='(%s)' % (cat_x['count'])
        
    cat_x['fid']=cat.parent.id if cat.parent else None
    cat_x['id']=cat.id
    cat_x['cat_id']=cat.cat_id
    cat_x['ename']=cat.ename
    cat_x['order']=cat.order
    
    cat_x['seo']={}
    cat_x['flag'] = 'false'
    if cat.seo:
        cat_x['seo']['title']= cat.seo.title
        cat_x['seo']['keywords']= cat.seo.keywords
        cat_x['seo']['description']= cat.seo.description
    cat_x['child']= []  
    cat_x['article']=[]  
    for ar in NewArticle.objects.filter(cat=cat.id):
        cat_x['article'].append({'name':ar.name,'content':ar.content,'img':[im.urls for im in ar.img.all() ]})
    
    return  cat_x   

def find_cat(city_id=None,cat=object ,cat_arr=[], cat_k={}):
    if cat and not cat_k.has_key(cat.id): 
        #cat_x=make_cat(cat)  
        
        cat_k[cat.id]=make_cat(cat,city_id)
        cat_arr.append(cat_k[cat.id])
        if cat.parent :
            #cat_k[cat.parent.id]=make_cat(cat.parent)
            try:
                if not cat_k.has_key(cat.parent.id):
                #return cat_arr               
                    find_cat(city_id,cat.parent ,cat_arr,cat_k)
            except:
                return
            
            
   

def NewCatUrl(type=0,city='',new=False,catename=''):
    
    '''
    f_cat = cache.get('cat_event_map'+city) 
    x_cat = cache.get('cat_event_list'+city) 
    id_cat= cache.get('cat_event_id'+city) 
    '''
    if city=='0':
        city=''
 
            
    if type==0 or not type:
        x_cat = cache.get('cat_event_list%s' % city) 
        if not x_cat:
            new=True
    elif type==1: 
        f_cat = cache.get('cat_event_map%s' % city)            
        if not f_cat:
            new=True
    else:
        id_cat= cache.get('cat_event_id%s' % city) 
        if not id_cat:
            new=True
    
    
    if new:
        f_cat=[]
        x_cat={}
        id_cat={}     
        #title        
        #citys.query.group_by = ['neweventtable_id']         
        
        try:
            ci=NewCity(3)
            #print ci[city][0]
            
            ev=NewEventTable.objects.filter(city=ci[city][0]).filter(Q(end_time__gt=datetime.date.today())|Q(end_time=None)).filter(isshow__in=(1,8))
            catinfo=NewCatInfo.objects.filter(neweventtable_id__in=[e.id for e in ev]) 
             
            #cat.query.group_by = ['neweventcat_id'] 
            
            
            #catinfo = NewCatInfo.objects.filter(neweventtable_id__in=[cit.neweventtable_id  for cit in NewCityInfo.objects.filter(newdistrict_id=ci[city][3]).filter(neweventtable__end_time__lt=int(time.time()))]) 
        except:
            catinfo = NewCatInfo.objects.all()       
        
        
        catinfo.query.group_by = ['neweventcat_id'] 
 
        cat_list=[]
        
        id_cat={}
 
        for ca in catinfo:  
            try:
                if not ca.neweventcat.type:                
                    try:                         
                        find_cat(ci[city][0],ca.neweventcat , cat_arr=cat_list, cat_k=id_cat)  
                    except:
                        try:
                            find_cat(None,ca.neweventcat , cat_arr=cat_list, cat_k=id_cat)  
                             
                        except:
                            continue  
            except:
                continue  
             
         
             
        
        #cat_lists=sorted(cat_list,key = lambda x:x['order'],reverse=True)    
        cat_lists=sorted(cat_list,key = lambda x:x['order'])          
        for cat in cat_lists:            
            id_cat[cat['id']]
            
            

                 
            
            if cat['ename']:
                if city:
                    id_cat[cat['id']]['caturl']= '/%s/%s/' % (city,cat['ename'])
                else:
                    id_cat[cat['id']]['caturl']= '/%s/' % (cat['ename'])
                                    
 
                x_cat[cat['ename']]=id_cat[cat['id']]
                

                
            else:  
                #del id_cat[cat['id']]   
                #continue          
                  
                if city:
                    id_cat[cat['id']]['caturl']= '/%s/%s/' % (city,cat['id'])
                else:
                    id_cat[cat['id']]['caturl']= '/%s/' % (cat['id'])
       
                x_cat[cat['id']]=id_cat[cat['id']]
                
                 
                 
            if id_cat.has_key(cat['fid']):
                id_cat[cat['fid']]['child'].append(id_cat[cat['id']])
            else:
                #if cat['ename']:
                f_cat.append(id_cat[cat['id']])
                
                
                
        
        
        
        cache.set('cat_event_id%s' % city,id_cat,86400)
        cache.set('cat_event_map%s' % city,f_cat,86400)
        cache.set('cat_event_list%s' % city,x_cat,86400)
        
    
    if catename and x_cat.has_key(catename):
        x_cat[catename]['flag'] = 'true'
        id_cat[x_cat[catename]['id']]['flag'] = 'true'
        map_id(f_cat,x_cat[catename])
        
         
 
            

    if type==0 or not type: 
        return x_cat
    elif type==1:     
        import copy 
        f_cat= map_show(copy.deepcopy(f_cat))       
        return f_cat
    else:
        return id_cat

def map_show(maps=[]): 
    new_maps=[]
    for ma in maps:
        if not ma['ename']:
            del ma
            continue
        
        if ma['child']:            
            ma['child']=map_show(ma['child'])
            
        new_maps.append(ma)
    return new_maps
            
            
 
            
    
    
def map_id(maps=[],cat={} ):
    for index in range(len(maps)):
        
        if maps[index]['id']==cat['id']:
            maps[index]=cat
            return True
             
        else:
            if map_id(maps[index]['child'],cat):
                return True
            
def find_ch(id=0,cat_arr={}):
    cat_ll=[]
    if cat_arr.has_key(id):
        cat_ll.append(id)
        if cat_arr[id]['child']:
            for ch in cat_arr[id]['child']:
                cat_ll.extend(find_ch(ch['id'], cat_arr))
                
    return cat_ll
 
#通过城市id和分类id获取活动    
def event_city_cat(city_id=None,cat_id=None, new=False,cou=False):
 
    city=city_id
    if  type(city_id) == tuple :
        city=str(city_id).replace('(','').replace( ',' ,'').replace(')' ,'').replace(' ' ,'')  
    cats=cat_id
    if  type(cat_id) == tuple :
        cats= str(cat_id).replace('(','').replace( ',' ,'').replace(')' ,'').replace(' ' ,'')  
        
    event  = cache.get('event_%s_%s' % (city,cats)) 
    count  = cache.get('event_%s_%s_con' % (city,cats)) 

    if new or not event or not count :  
        
        event =[]
        ev=NewEventTable.objects.filter(isshow__in=(1,)).exclude(cat=111).filter(Q(end_time__gt=datetime.date.today())|Q(end_time=None))
  
        if city_id :
            if type(city_id) == tuple:
                ev=ev.filter(city__in=city_id)
            elif int(city_id)>0:
          
                ev=ev.filter(city=city_id)
        #ev=ev.filter(cat__in=[84,87,83,80,86,82])
        
        if cat_id:    
            if type(cat_id) == tuple:
                
                cat_s=[]
                for id in cat_id:
                    cat_s.extend(find_ch(int(id),NewCatUrl(2)))
                ev=ev.filter(cat__in=cat_id)
            elif int(cat_id)>0:                
                ev=ev.filter(cat__in=find_ch(int(cat_id),NewCatUrl(2)))
        
        #ev=ev.order_by("-order").order_by("begin_time").distinct()        
        ev=ev.order_by("-release_time").distinct() 
        #ev.query.group_by = ['id']
        
        #event = [NewformatEvent(item) for item in ev[:10] ]
        event = [int(item.old_event_id) for item in ev[:10] ]
        #print connection.queries
        if event :
            count=ev.count()
            cache.set('event_%s_%s' % (city,cats),event ,86400)
            cache.set('event_%s_%s_con' % (city,cats),count ,86400)
        

    if cou:
        print type(cou)
        return count
    else:
        return event
 
 
     

def get_str_event(new=False):
    event_str = cache.get('event_str')
    if new or not event_str:
        event_str={}
        for ev in NewEventTable.objects.exclude(ename=''):
            event_str[ev.ename]=ev.id
        cache.set('event_str',event_str,86400)
        

    return event_str
'''    
def get_site_links(new=False):
    site_links = cache.get('site_links')
    if new or not site_links:
        site_links=[]
        for ev in FriendlyLink.objects.all().order_by('-order'):
            site_links.append((ev.name,ev.url,ev.page,ev.img))
            
        cache.set('site_links',site_links,86400)
 
    return site_links
'''    
def get_str_singers(new=False):   
    singers_str = cache.get('singers_str')
    if new or not singers_str:
        from LifeApi.models import singers
        singers_str = [item.name for item in singers.objects.all()]
        cache.set('singers_str',singers_str,86400)
        
 
    return singers_str
 
    

 
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

   
def get_event_list( cat=False,city=False,date=False,page=False,offset=False,order=False,new=False):
 
    key_name=''
    if not offset:
        
        key_name='listcou_%s_%s_%s' % (cat,city,date)
        
        key_name = hashlib.md5(key_name).hexdigest()

    else:
        
        key_name='list_%s_%s_%s_%s_%s_%s' % (cat,city,date,page,offset,order)

        key_name = hashlib.md5(key_name).hexdigest()
        
        
    list  = cache.get(key_name)     
    
    if not list or new:
    
    
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
            
            list = args.distinct().count()
            
            
            
        else:
            #return SysSpotInfo.objects.filter(args).order_by(order)[page:offset]
            list = [ev.old_event_id for ev in args.order_by("-order").order_by(order).distinct()[page:offset]]
            
        cache.set(key_name,list,60*60)
        
            
    return list

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
        navigationDict['caturl'] = '/%s/%s/'%(city,cat_str)
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
    navigationDict['catname'] = u'首页'
    navigationDict['caturl'] = '/%s/' % (city)
    new_navigationList.append(navigationDict)
    new_navigationList.reverse()
    return new_navigationList   
  
def getEventHead(event_li,event,navigationList):
    head={}
     
    tags=','.join([ev.name for ev in event.tag.all()])
    
    '''
    if not event.seo:
        for ca in  event.cat.all():
            try:
                event.seo=NewEventSeo.objects.get(name=ca.name)
                event.seo.save()
                break
            except:
                try:
                    if ca.parent:
                        event.seo=NewEventSeo.objects.get(name=ca.parent.name)
                        event.seo.save()
                        break
                    
                except:
                    pass
    '''
    
    if not event.seo:
        tags=','.join([ev.name for ev in event.tag.all()])
        head['description'] =u"%s%s%s" % (event.search if event.search else '',tags, event.begin_time)
        cat_str=[]
        for nav in navigationList:            
            cat_str.append( nav['catname'].replace(u'首页',u'活动家'))
                        
        #head['title']=u"%s" % ( event.name)
        catId=event_li['event_cat1']
        if catId == 1:         
            title = u'%s%s【门票-报名-参会-购票-买票】_活动家'%(event_li['event_name'],event_li['district_name'])
        elif catId == 2:
            title = u'%s【打折票-折扣票-买票】%s演出_活动家'%(event_li['event_name'],event_li['district_name'])
        elif catId == 3:
            title = u'%s【门票-订票-价格-买票】%s特色旅游_活动家'%(event_li['event_name'],event_li['district_name'])
        elif catId == 4:
            title = u'%s【报名】公开课培训_活动家'%event_li['event_name']
        elif  catId == 5:
            title = u'%s【参展-展位预定-费用】_活动家'%event_li['event_name']
        elif catId == 6:
            title = u'%s【门票-报名】%s同城活动_活动家'%(event_li['event_name'],event_li['district_name'])
        else: 
            title=u"%s" % ( event.name)
        
        head['title']=title
        
        
        
        
        head['keywords']='%s,%s' % (','.join(cat_str),tags)
        for tag in event.tag.all():            
            head['keywords']+=tag.name+','
            
    else:     
        event_begin_time = datetime.datetime.strftime(event.begin_time,'%Y-%m-%d') if event.begin_time else ''
        
        #title = seo.title.replace('(city)', event['district_name']).replace('(name)', event['event_name']).replace('(year)',event['event_begin_time'].split('-')[0]).replace('(singer)',s_name)
        #keyword = seo.keywords.replace('(city)', event['district_name']).replace('(name)', event['event_name']).replace('(year)',event['event_begin_time'].split('-')[0]).replace('(singer)',s_name)
        '''
        des = seo.description.replace('(city)', event['district_name'])/
        .replace('(name)', event['event_name']).replace('(year)',event['event_begin_time']/
        .split('-')[0]).replace('(month)',event['event_begin_time'].split('-')[1])./
        replace('(day)',event['event_begin_time'].split('-')[2])./
        replace('(venue)',event['event_venue']).replace('(singer)',s_name)
        '''
        name_s=''
        if event.seo_id==113:            
            name_s=get_str_singers(event.name)
            if not name_s:
                try:
                    event.seo=NewEventSeo.objects.get(id=115)
                    event.seo.save()
                except:                    
                    return None
                
                    
                
                
                
        
        
        if event.seo.title:
            
            head['title']=event.seo.title.replace('(city)', event_li['district_name']).replace('(name)', event_li['event_name']).replace('(year)',event_li['event_begin_time'].split('-')[0]).replace('(month)',event_li['event_begin_time'].split('-')[1]).replace('(day)',event_li['event_begin_time'].split('-')[2]).replace('(singer)',name_s) 
        else:
            catId=event_li['event_cat1']
            if catId == 1:         
                title = u'%s%s【门票-报名-参会-购票-买票】_活动家'%(event_li['event_name'],event_li['district_name'])
            elif catId == 2:
                title = u'%s【打折票-折扣票-买票】%s演出_活动家'%(event_li['event_name'],event_li['district_name'])
            elif catId == 3:
                title = u'%s【门票-订票-价格-买票】%s特色旅游_活动家'%(event_li['event_name'],event_li['district_name'])
            elif catId == 4:
                title = u'%s【报名】公开课培训_活动家'%event_li['event_name']
            elif  catId == 5:
                title = u'%s【参展-展位预定-费用】_活动家'%event_li['event_name']
            elif catId == 6:
                title = u'%s【门票-报名】%s同城活动_活动家'%(event_li['event_name'],event_li['district_name'])
            else: 
                title=u"%s" % ( event.name)
            
            head['title']=title
            
            
            
            
            
            
        if event.seo.keywords:
            head['keywords']=event.seo.keywords.replace('(city)', event_li['district_name']).replace('(name)', event_li['event_name']).replace('(year)',event_li['event_begin_time'].split('-')[0]).replace('(month)',event_li['event_begin_time'].split('-')[1]).replace('(day)',event_li['event_begin_time'].split('-')[2]).replace('(singer)',name_s)
        else:
            cat_str=[]
            for nav in navigationList:           
                cat_str.append( nav['catname'].replace(u'首页',u'活动家'))
            head['keywords']='%s,%s' % (','.join(cat_str),tags)
            for tag in event.tag.all():            
                head['keywords']+=tag.name+','     
        if event.seo.description:   
            if not event_li['event_end_time']:
                event_li['event_end_time']='2014-12-30'
            head['description']=event.seo.description.replace('(city)', event_li['district_name']).\
            replace('(name)', event_li['event_name']).replace('(year)',event_li['event_begin_time']\
            .split('-')[0]).replace('(month)',event_li['event_begin_time'].split('-')[1]).\
            replace('(day)',event_li['event_begin_time'].split('-')[2]).\
            replace('(venue)',event_li['event_venue']).replace('(singer)',name_s).\
            replace('(end_year)',event_li['event_end_time'].split('-')[0]).\
            replace('(end_month)',event_li['event_end_time'].split('-')[1]).\
            replace('(end_day)',event_li['event_end_time'].split('-')[2])
            

        else:
            head['description']=u"%s%s%s" % (event.search if event.search else '',tags, event.begin_time)
        #return head
 
    
        
 
 
    return head   


   
def NewformatEvent(new_event,evnet_id=False,new=False,detail = False):
     
 
    res={}
    if evnet_id:
        res  = cache.get('event_%s' % evnet_id) 
    else:
        if new_event:
            res  = cache.get('event_%s' % (new_event.old_event_id,)) 
    if not res or new:
        
        res={}
        if not new_event:
            if evnet_id:                
                try:                    
                    new_event=NewEventTable.objects.get(old_event_id=evnet_id)
                except:
                    new_event = oldEventToNewEvent(evnet_id)
                    #return res
            else:
                return res

        if not new_event:
            return res
        
        #getEventHead(event_li,event,navigationList)
        updata_cache(new_event)
        res['isshow']=new_event.isshow_id    
        res['id']=new_event.id
        res['event_id'] =  new_event.old_event_id if new_event.old_event_id else new_event.id
        res['event_name'] = new_event.name
        try:  
            cats=new_event.cat.filter(type=None).order_by('-id')[0] 
            res['cat_id'] = cats.cat_id
            res['catid'] = cats.id
            res['event_cat1'] = cats.parent.cat_id
            res['cat_name'] = cats.name
            res['cat_ename'] = cats.ename
        except:
            res['cat_name']=None
            res['cat_ename']=None
            res['catid']=None
            res['cat_id'] = None
            res['event_cat1']=None

       
        try: 
            ci=new_event.city.all()[0]         
            res['district_id'] = ci.id
            res['district_title'] =ci.title   
            res['district_name'] = ci.district_name  
        except:
            res['district_id'] =''
            res['district_title'] =''
            res['district_name'] = ''
            
        try:
            addrs=new_event.addr.all()[0]
        #if addrs:
            '''
            res['district_id'] = addrs.city.id
            res['district_title'] =addrs.city.title   
            res['district_name'] = addrs.city.district_name    
            '''
            res['event_venue'] = addrs.title if addrs else '' 
            res['event_address'] = addrs.address if addrs else ''
        except:   
            res['event_venue'] = '' 
            res['event_address'] =new_event.old_event.event_address if new_event.old_event else '' 
        res['event_content']=[]
        
        try:
         
            for con in new_event.paragraph.all().order_by('-txt_order','id'):

                res['event_content'].append((con.cat_name.name,con.txt.replace('pic1.qkan.com','pic.huodongjia.com').replace('\n','').replace('\r','')))

            #res['event_content'] = [(con.cat_name.name,con.txt.replace('pic1.qkan.com','pic.huodongjia.com')) for con in new_event.paragraph.all().order_by('-txt_order','id')]   
        except:
            pass
            
     
    
      
        if new_event.end_time and new_event.end_time<datetime.datetime.today():
            #state
            res['time_expire'] = 2
        
        res['event_tag'] = [tag.name for tag in  new_event.tag.all()] 
        try:
            imgs=new_event.img.order_by('-order')[0]
        
            res['has_picture'] = True
            #pic.huodongjia.com
            res['event_img'] =imgs.server.name+imgs.urls
            if re.match('/',imgs.urls):
                res['event_img'] ='http://pic.huodongjia.com'+imgs.urls
            else:
                res['event_img'] ='http://pic.huodongjia.com/'+imgs.urls
        except:
            res['has_picture'] = False
            try:
                #cat=new_event.cat.order_by('-cat_id')[0]
             
                res['event_img'] = 'http://pic.huodongjia.com/img/default%s.jpg' % (res['cat_id'])
            except:
                pass
            
        res['event_begin_time'] = datetime.datetime.strftime(new_event.begin_time,'%Y-%m-%d') if new_event.begin_time else ''
         
        res['event_url']='/%s_%s.html' % (datetime.datetime.strftime(new_event.begin_time,'%Y%m%d') if new_event.begin_time else '',new_event.id) 
        res['event_end_time'] = datetime.datetime.strftime(new_event.end_time,'%Y-%m-%d') if new_event.end_time else ''
        res['event_islongtime'] = new_event.state
        if new_event.Price:
            
            res['event_price_unit'] = new_event.Price.Currency.ename if new_event.Price.Currency else "RMB"
            res['event_price_unit_name']=new_event.Price.Currency.name if new_event.Price.Currency else "人民币"
             
            if new_event.Price_event_table.all().count():
                pri=[]
                sal=[]
                
                prs=new_event.Price_event_table#.filter(Currency=new_event.Price.Currency)
                prs=prs.filter(begin_time__lte=datetime.datetime.now())
                prs=prs.filter(end_time__gte=datetime.datetime.now())
                prs=prs.filter(stock__gt=0)
                prs=prs.filter(status=1)
                for pr in prs:
                    if pr.price:
                        pri.append(str(pr.price))
                    if pr.sale:
                        sal.append(str(pr.sale))
                res['event_price'] = '/'.join(pri)  #if pri else new_event.Price.str
                res['event_discount_price'] = '/'.join(sal)  #if sal else   new_event.Price.sale if new_event.Price.sale else ''
            else:
            
                res['event_price'] =new_event.Price.str
                res['event_discount_price']=new_event.Price.sale if new_event.Price.sale else ''
                
            event_price_model = new_event.Price.Type_id
            if event_price_model!=1:
                res['event_discount_price'] =''
            if event_price_model==4:        
                res['event_isfree'] = 1
                res['event_price']='免费'
            elif event_price_model==5:
                res['event_price']='收费'
                
            res['event_price_model'] = event_price_model
            if event_price_model == 3:
                try:
                    res['cf'] = Crowfunding.objects.get(event_id = new_event.old_event_id)
                except:
                    pass
            elif event_price_model==7:
                res['event_price'] =''
        cat_s=res['cat_ename'] if res['cat_ename'] else res['catid']        
        navigationList = constructNavigationUrl(res['district_title'],cat_s)
        navigationList.append({'catname':new_event.name,
                               'caturl':'%s.html' % res['event_id'] })
        res['navigationList']=navigationList
        res['head']=getEventHead(res,new_event,navigationList) 
    
    if res.has_key('event_id'):
        cache.set('event_%s' % res['event_id'],res,86400)
    #print sys.getsizeof(res)    
            
    return res 

   
def NewAppEvent(new_event,evnet_id=False,new=False,detail = False):
    
    res={}
    if evnet_id:
        res  = cache.get('event_app_%s' % evnet_id)
    else:
        if new_event:
            res  = cache.get('event_app_%s' % (new_event.old_event_id,)) 
    if not res or new:
        
        res={}
        if not new_event:
            if evnet_id:
                try:                    
                    new_event=NewEventTable.objects.get(old_event_id=evnet_id)
                except:
                    new_event=NewEventTable.objects.get(id=evnet_id)
                    #new_event = oldEventToNewEvent(evnet_id)
                    #return res
            else:
                return res

        if not new_event:
            return res
        
        #getEventHead(event_li,event,navigationList)
        #updata_cache(new_event) 
        res['isshow']=new_event.isshow_id    
        res['id']=new_event.id
        res['event_id'] =  new_event.old_event_id if new_event.old_event_id else new_event.id
        res['title'] = new_event.fname if new_event.fname else new_event.name
        
        res['sponsor']= [{'pic': '%s%s' % (sp.pic.server.name, sp.pic.urls) if sp.pic else '','name':sp.name,'des':sp.intro} for sp in NewSponsor.objects.filter(events=res['id']).all()]
        try:
            fe=feelnum.objects.get(event_id=new_event.id)
            res['feel'] = fe.feel.name
            res['feelnum'] = fe.feelnum
            res['feeltitle'] = fe.title
            if  fe.content:
                res['detail'] = fe.content
        except:
            res['feelnum'] =random.randint(7, 9)
            res['feel']='活动指数'
            
        try:  
            cats=new_event.cat.filter(type=None).order_by('-id')[0] 
            res['cat_id'] = cats.cat_id
            res['catid'] = cats.id
            
            res['event_cat1'] = cats.parent.cat_id
            res['cat_name'] = cats.name
            res['cat_ename'] = cats.ename
            res['cat_img'] = None
            try:
                if cats.img:
                    c={}
                    imgs=cats.img
                    #print 'imgs yes'
                    if imgs.server:
                        c['img'] = imgs.server.name+imgs.urls
                    else:
                        if re.match('/',imgs.urls):
                            c['img']='http://pic.huodongjia.com'+imgs.urls
                        else:
                            c['img']='http://pic.huodongjia.com/'+imgs.urls
                    
         
                    c['width']=imgs.width
                    c['height']=imgs.height
                    res['cat_img']=c
            except:
                pass
            
        except:
            res['cat_name']=None
            res['cat_ename']=None
            res['catid']=None
            res['cat_id'] = None
            res['cat_img'] = None
            res['event_cat1']=None
        #res['all_cat']=[ca.id for ca in new_event.cat.all()]

        '''
        try: 
            ci=new_event.city.all()[0]         
            res['district_id'] = ci.id
            res['district_title'] =ci.title   
            res['district_name'] = ci.district_name  
        except:
            res['district_id'] =''
            res['district_title'] =''
            res['district_name'] = ''
        '''
        try:
            addrs=new_event.addr.all()[0]
        #if addrs:
            
            res['district_id'] = addrs.city.id
            res['district_title'] =addrs.city.title   
            res['district_name'] = addrs.city.district_name    
            
            res['event_venue'] = addrs.title if addrs else '' 
            res['event_address'] = addrs.address if addrs else ''
            res['position']='%s,%s' % (addrs.longitude_baidu if addrs.longitude_baidu else '',addrs.latitude_baidu  if addrs.latitude_baidu else '')
            '''
            res['district_id'] = addrs.city.id
            res['district_title'] =addrs.title   
            res['district_name'] = addrs.district_name  
            '''
        
        except:   
            res['event_venue'] = '' 
            res['event_address'] =new_event.old_event.event_address if new_event.old_event else '' 
            res['position']=''
            try: 
                ci=new_event.city.all()[0]         
                res['district_id'] = ci.id
                res['district_title'] =ci.title   
                res['district_name'] = ci.district_name  
            except:
                res['district_id'] =''
                res['district_title'] =''
                res['district_name'] = ''
        res['event_content']=[]
        res['des']=new_event.content
        try:  
         
            for con in new_event.paragraph.all().order_by('-txt_order','id'):

                res['event_content'].append((con.cat_name.name,con.txt.replace('pic1.qkan.com','pic.huodongjia.com')))

            #res['event_content'] = [(con.cat_name.name,con.txt.replace('pic1.qkan.com','pic.huodongjia.com')) for con in new_event.paragraph.all().order_by('-txt_order','id')]   
        except:
            pass
             
        

        res['event_tag'] = [tag.name  for tag in  new_event.tag.all()] 
        try:
            imgs=new_event.img.filter(order=9999)[0]
        
            res['has_picture'] = True
            #pic.huodongjia.com
            if imgs.server:
                res['event_img'] =imgs.server.name+imgs.urls
            if re.match('/',imgs.urls):
                res['event_img'] ='http://pic.huodongjia.com'+imgs.urls
            else:
                res['event_img'] ='http://pic.huodongjia.com/'+imgs.urls
        except:
            res['has_picture'] = False
            res['event_img']=''

        img_s=[]
        #for imgs in new_event.img.filter(height__in=(400,),width__in=(640,)).order_by('-order','-id'):       
        for imgs in new_event.img.exclude(order=9999).order_by('-order','-id'):        
            if imgs.server:
                img_s.append(imgs.server.name+imgs.urls)
            else:
                if re.match('/',imgs.urls):
                    img_s.append('http://pic.huodongjia.com'+imgs.urls)
                     
                else:
                    img_s.append('http://pic.huodongjia.com/'+imgs.urls)
        res['img_s']=img_s
            
        res['event_begin_time'] = datetime.datetime.strftime(new_event.begin_time,'%Y-%m-%d') if new_event.begin_time else ''
        start=0
        try:
            start=time.mktime(new_event.begin_time.timetuple())
        except:
            start=0
        res['startdate'] =start      
        
        end=0
        try:
            end=time.mktime(new_event.end_time.timetuple())
        except:
            end=0
        res['enddate'] =end
        res['event_url']='/%s_%s.html' % (datetime.datetime.strftime(new_event.begin_time,'%Y%m%d') if new_event.begin_time else '',new_event.id) 
        res['event_end_time'] = datetime.datetime.strftime(new_event.end_time,'%Y-%m-%d') if new_event.end_time else ''
        res['event_islongtime'] = new_event.state
        res['app_price']=[]
        if new_event.Price:
            
            
            
            res['event_price_unit'] = new_event.Price.Currency.ename if new_event.Price.Currency else "RMB"
            res['event_price_unit_name']=new_event.Price.Currency.name if new_event.Price.Currency else u"人民币"
            res['price_currency']=new_event.Price.Currency.sign if new_event.Price.Currency else u"¥"
            
            new_price=new_event.Price_event_table
            if new_price.all().count():
                pri=[]
                sal=[]
                
                prs=new_price.order_by('begin_time','price')
                #prs=prs.filter(begin_time__lte=datetime.datetime.now())
                #prs=prs.filter(end_time__gte=datetime.datetime.now())
                #prs=prs.filter(stock__gt=0)
                #prs=prs.filter(status=1)
                res['price_unit_info']=[]
                for pr in prs:
                    pt={}                    
                    pt['begin_time']=datetime.datetime.strftime(pr.begin_time,'%Y-%m-%d %H:%M:%S') if pr.begin_time else None
                    pt['end_time']=datetime.datetime.strftime(pr.end_time,'%Y-%m-%d %H:%M:%S') if pr.end_time else None
                    pt['stock']=pr.stock
                    pt['status']=pr.status
                    pt['price']=str(pr.price) if pr.price else ''
                    pt['sale']=str(pr.sale) if pr.sale else ''
                    pt['type']=str(pr.type) if pr.type else ''
                    pt['content']=pr.content if pr.content else ''
                    
                    if  pr.discount:
                        
                        pt['discount']=str(pr.discount)
                        if not pr.sale:
                            pt['sale']=round(float(pr.price)*float(pr.discount),2)
                    elif pr.sale and pr.price:
                        pt['discount']="%.2f" % (float(pr.sale)/float(pr.price) )
                    else:
                        pt['discount']="1.0"
                    
                    res['price_unit_info'].append(pt)
                    if pr.price:
                        pri.append(str(pr.price))
                    if pr.sale:
                        sal.append(str(pr.sale))
                res['event_price'] = '/'.join(pri)  #if pri else new_event.Price.str
                res['event_discount_price'] = '/'.join(sal)  #if sal else   new_event.Price.sale if new_event.Price.sale else ''
            else:
                res['app_price']=formatPrice(new_event.Price)
                res['event_price'] =new_event.Price.str
                res['event_discount_price']=new_event.Price.sale if new_event.Price.sale else ''
                
            event_price_model = new_event.Price.Type_id
            if event_price_model!=1:
                res['event_discount_price'] =''
            if event_price_model==4:        
                res['event_isfree'] = 1
                res['event_price']='免费'
            elif event_price_model==5:
                res['event_price']='收费'
            
            res['event_price_model'] = event_price_model
            if event_price_model == 3:
                try:
                    res['cf'] = Crowfunding.objects.get(event_id = new_event.old_event_id)
                except:
                    pass
            elif event_price_model==7:
                res['event_price'] =''
        cat_s=res['cat_ename'] if res['cat_ename'] else res['catid']        
        navigationList = constructNavigationUrl(res['district_title'],cat_s)
        navigationList.append({'catname':new_event.name,
                               'caturl':'%s.html' % res['event_id'] })
        #res['navigationList']=navigationList
        #res['head']=getEventHead(res,new_event,navigationList) 
        
    if res.has_key('event_id'):
        cache.set('event_app_%s' % res['event_id'],res,86400)
    #print sys.getsizeof(res)    


    if res.has_key('event_price_model') and  res['event_price_model'] in [1,6] and  res.has_key('price_unit_info'):

        res['app_price']={}
        res['app_price']['currency_token']=res['event_price_unit'] if res.has_key('event_price_unit') else "RMB"
        res['app_price']['price_currency']=res['price_currency'] if res.has_key('price_currency') else "¥"
        
        d = {6:0,4:1,7:2,5:3}
        try:
            types = d[res['event_price_model']]
        except:
            types = 0
            
        
        res['app_price']['type']=types# res['event_price_model'] if res.has_key('event_price_model') else 5
        res['app_price']['list']=[]
        
        #price=[]
        
        for i in range(len(res['price_unit_info'])):
            app_price={}
            pt1=res['price_unit_info'][i]
            
            '''
            pri1=str(pt['price'])
            pri2=pri1.split('.')
            if int(pri2[1])==0:
                pri1=pri2[0]
            
            '''
            app_price['sale']=str(pt1['sale'])
            app_price['money']=str(pt1['price'])
            app_price['price_type']=pt1['type']
            
            app_price['number']=int(pt1['stock'])
            app_price['start_date']=pt1['begin_time'] if pt1['begin_time'] else ''
            app_price['end_date']=pt1['end_time'] if pt1['end_time'] else ''
            app_price['discount']=pt1['discount']
            
            app_price['property']=''
            if pt1['begin_time'] and datetime.datetime.strptime(pt1['begin_time'],'%Y-%m-%d %H:%M:%S')>datetime.datetime.now():
                #prr.append(u'待定')
                app_price['property']=u'待定'
                app_price['price_type']=6
            elif pt1['end_time'] and datetime.datetime.strptime(pt1['end_time'],'%Y-%m-%d %H:%M:%S')<datetime.datetime.now():
                #prr.append(u'已过期')
                app_price['property']=u'已过期'
                app_price['price_type']=5
                
            if pt1['stock']<=0:
                app_price['property']=u'售完'
                app_price['price_type']=4
                #prr.append(u'售完')
            if pt1['status']!=1:
                app_price['property']=u'售磬'
                app_price['price_type']=3
                
                
            if not app_price['property']:
                app_price['property']=pt1['content']

            res['app_price']['list'].append(app_price)
            
        #res['event_price']='/'.join(price)        
        #res['app_price']=formatPrice(new_event.Price)


    return res 

def updata_cache(ev):
    for ci in ev.city.all():
        cat_l=NewCatUrl(0,ci.title)
        for ca in ev.cat.all():
            if not cat_l.has_key(ca.id):
                NewCatUrl(0,ci.title,True)
                 
            event_city_cat(ci.id,ca.id,True)
        
        event_city_cat(ci.id,69 ,True )     
        event_city_cat(ci.id,(19,70),True  )   
            
def formatPrice(price):
    res = {}
    
    d = {6:0,4:1,7:2,5:3}
    try:
        type = d[price.Type.id]
    except:
        type = 0
    price_currency = price.Currency.sign
    currency_token = price.Currency.ename
    
    list = []
    price_str = price.str
    for item in price_str.split('/'):
        num = 100
        price_type = 0
        property = ''
        money = 0
        if re.match(r'[\d\.]+?\(.*?\)',item):
            statu = re.findall(r'[\d\.]?\((.*?)\)',item)[0]
            money = re.findall(r'^([\d\.]+)',item)[0]
            if statu in [u'过期',u'结束',u'停止',u'售完']:
                num = 0
            if statu == u'现场':
                price_type = 1
            if statu == u'参展':
                price_type = 2
            else:
                property = statu
        else:
            if  re.match(r'[\d\.]+',item):
                try:
                    money = float(item)
                except:
                    money = 0
        list.append({'money':money,'price_type':price_type,'property':property,'discount':1,'number':num,'start_date':'','end_date':''})
    res = {'type':type,'price_currency':price_currency,'currency_token':currency_token,'list':list}
    return res
       
    #NewformatEvent(ev,ev.id,True)
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                    'lt':'<','60':'<',
                    'gt':'>','62':'>',
                    'amp':'&','38':'&',
                    'quot':'"','34':'"',}

    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
            entity=sz.group()#entity全称，如&gt;
            key=sz.group('name')#去除&;后entity,如&gt;为gt
            try:
                htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
                sz=re_charEntity.search(htmlstr)
            except KeyError:
    #以空串代替
                htmlstr=re_charEntity.sub('',htmlstr,1)
                sz=re_charEntity.search(htmlstr)
    return htmlstr
def search(keyword):
    import sphinxapi
    cl = sphinxapi.SphinxClient()
    cl.SetServer('10.10.64.15',9312)
    #cl.SetConnectTimeout(3)
    cl.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED)
    cl.SetLimits(0,100)
    res = cl.Query(keyword,'mysqlvevent1')
    
    if not res:
        return []
    
    if res.has_key('matches'):
        return [match["id"] for match in res['matches']]
    return []
 

def sendMailAsync(sub,text,html,to_list=['shenghuojia@aliyun.com','252925359@qq.com', '516139718@qq.com','1010478998@qq.com','9682539@qq.com','241617467@qq.com'], cc_list=[]):

    key_name = 'n_mail_host'
    n_mail_host = cache.get(key_name, 0)

    #设置服务器，用户名、口令以及邮箱的后缀
    mail_host_list = [
            {'mail_host': 'smtp.exmail.qq.com', 
             'mail_user': 'order@huodongjia.com', 
             'mail_pass': 'Ve!2013'},
            {'mail_host': 'smtp.exmail.qq.com', 
             'mail_user': 'order1@huodongjia.com', 
             'mail_pass': 'Ve!2013'},
            {'mail_host': 'smtp.exmail.qq.com', 
             'mail_user': 'order2@huodongjia.com', 
             'mail_pass': 'Ve!2013'},
            ]

    #mail_host="smtp.126.com"
    #mail_user="nbwujuan@126.com"
    #mail_pass="0000000000"
    #mail_host="smtp.exmail.qq.com"
    #mail_user="order@huodongjia.com"
    #mail_pass="Ve!2013"

    part1 = MIMEText(text, 'plain', 'utf-8')
    part2 = MIMEText(html, 'html', 'utf-8')

    msg = MIMEMultipart('alternative')
    msg["Accept-Language"]="zh-CN"
    msg["Accept-Charset"]="ISO-8859-1,utf-8"
    msg['Subject'] = sub
    msg['to'] = ';'.join(to_list)
    msg['Cc'] = ';'.join(cc_list)
    msg.attach(part1)
    msg.attach(part2)

    for i in range(len(mail_host_list)):
        n_mail_host = (n_mail_host + 1) % len(mail_host_list)

        author = formataddr((str(Header(u'活动家', 'utf-8')), mail_host_list[n_mail_host]['mail_user']))
        msg['From'] = author
        try:
            s = smtplib.SMTP()
            s.connect(mail_host_list[n_mail_host]['mail_host'])
            #s.esmtp_features["auth"]="LOGIN PLAIN"
            s.login(mail_host_list[n_mail_host]['mail_user'],
                    mail_host_list[n_mail_host]['mail_pass'])
            #s.sendmail(mail_user, to_list.extend(bcc_list), msg.as_string())
            s.sendmail(author, to_list, msg.as_string())
            cache.set(key_name, n_mail_host, 86400*10)
            return True
        except Exception, e:
            pass
            #log.debug('Email Error: %s' %e)

    return False

def sendMail(sub,content,to_list=['252925359@qq.com', '516139718@qq.com','1010478998@qq.com','9682539@qq.com','241617467@qq.com']):
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

def ip_Filter(request,num=10,userID=False,other_ip=['221.237.118.212','127.0.0.1','182.139.33.52','125.70.114.98','125.70.114.60']):
    
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR'] 
        
    re=False
    if ip :
        
        if  ip  in other_ip:
            
            return True
         
        if userID:
            ip='%s:%s' % (ip,userID )  
               
        t_ip=cache.get(ip)
        times=60*1
        
        re=True
        nows=int(time.time())
        if t_ip:
            
            x=nows-t_ip[1]
            n=int(t_ip[0])
            if n>num:
                re=False
            
            elif x>times:
                re=False
            else:
                cache.set(ip,(n+1,t_ip[1] ),x)
            
        else:
            cache.set(ip,(1,nows),times)
    else:
        print ip
            
    if not re :
        cache.set(ip,(1000,nows),3600*24)

    return re

def SendRegisterMsg():
       
    import urllib2,urllib
    #url = 'http://sdk.entinfo.cn:8060/webservice.asmx'
    url='http://211.157.113.39:8060/webservice.asmx'
    #url='http://sdk2.zucp.net:8060/webservice.asmx'
    SN = 'SDK-SRF-010-00554'
    m = hashlib.md5()
    m.update(SN+'85-5C7d-')
    pwd = m.hexdigest().upper()
    #print type(msg)
    #print msg.encode('gbk')
    #msg=re.sub(ur"[^\u4e00-\u9fa5\w]", " ", msg)
    #msg=msg[0:10]
    
    data = {
            #'op':'Register',
            'sn':SN,
                'pwd':pwd,#'855C7d',
                
                'province':u'四川省'.encode('gb2312'),
                'city':u'成都市'.encode('gb2312'),
                'trade':u'IT'.encode('gb2312'),
                'entname':u'云数海量科技有限公司'.encode('gb2312'),
                'linkman':u'刘东'.encode('gb2312'),
                'mobile':u'028-85319761'.encode('gb2312'),
                'phone':u'15371818461'.encode('gb2312'),
                'email':u'1010478998@qq.com'.encode('gb2312'),
                'fax':u'028-85319761'.encode('gb2312'),
                'address':u'成都市高新区元华一巷53号一层'.encode('gb2312'),
                'postcode':u'610000',
                'sign':u'闲时'.encode('gb2312'),
                }
    res = urllib2.urlopen(url,urllib.urlencode(data)).read()
    return res
    print res
    if int(res) > 0:
        
        return True
    else:
        print res
        return False
    
    

def SendOrderMsg(phone=None,msg=''):
    if phone and msg:         
        import urllib2,urllib,hashlib
        url = 'http://sdk.entinfo.cn:8060/z_mdsmssend.aspx'
        
        SN = 'SDK-SRF-010-00554'
        m = hashlib.md5()
        m.update(SN+'85-5C7d-')
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
        #return res
        if int(res) > 0:
            
            return True
        else:
            #return res
            return False
        
    else:
        return  False
def get_time_line(dict_type=0,city_id=None,new=False):
    key_showtime_dict = 'showtime_dict%s' % (city_id if city_id else 'all')
    key_showtime_list = 'showtime_list%s' % (city_id if city_id else 'all')
    key_showtime_Week = 'showtime_Week%s' % (city_id if city_id else 'all')
    
    if not new:
        if dict_type == 0:
            showtime_dict = cache.get(key_showtime_dict)
            if not showtime_dict:
                new=True
        elif dict_type == 1:
            showtime_list = cache.get(key_showtime_list)
            if not showtime_list:
                new=True
        elif dict_type == 2:
            showtime_Week = cache.get(key_showtime_Week)
            if not showtime_Week:
                new=True
    
    
    if new:
        showtime_list=[]
        showtime_dict={}
        showtime_Week=[]
        fe = feelnum.objects.exclude(showtime=None).order_by('-showtime','-feelnum') 
        
        if city_id:
            fe=fe.filter(event__city=int(city_id))
        
        showdate=''
        one_week=None
        week=[]
        
        for f in fe:

            
            f_list={}
            f_list['date'] = datetime.datetime.strftime(f.showtime,'%Y-%m-%d')
            f_list['id']=f.event.old_event_id
            f_list['title'] = f.event.fname if f.event.fname else f.event.name
            f_list['daytitle'] = f.title
            #f_list['city']=[ ci.id  for ci in f.event.city.all()]
            
            if not showtime_dict.has_key(f_list['date']):
                showtime_dict[f_list['date']]=[]
                if showdate:
                    showtime_list.append(showtime_dict[showdate])
                    week.append(showtime_dict[f_list['date']])
                
                if not one_week or one_week>f.showtime:
                    we= f.showtime.weekday()
                    if we==0:
                        we=7
                    one_week=f.showtime+datetime.timedelta(days=-(we-1))
                    if week:
                        showtime_Week.append(week[:])                    
                        week=[]
                        
                
                
                
        
            showtime_dict[f_list['date']].append(f_list)
            
            showdate=f_list['date']
        
        cache.set(key_showtime_dict,showtime_dict,86400*30)
        cache.set(key_showtime_list,showtime_list,86400*30)
             
    if dict_type==0:
        return showtime_dict
    elif  dict_type==1:
        return showtime_list
    elif  dict_type==2:
        if len(week)>0:
            showtime_Week.append(week[:]) 
        
        return showtime_Week
    
def find_img(m):
    try:
        imgs=NewEventImg.objects.get(id=int(re.search(r"\d+",m.group().title()).group().title()))       
        
        return '<img src="%s%s" width="%s" height="%s" ></img>' % (imgs.server.name,imgs.urls,imgs.width,imgs.height)
    except:
        return ''
    
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
            city_code = None #getCityNameByIp(request)
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
                cache.delete(tel)
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
                cache.delete(tel)
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

def captcha_json(func):     
    def _is_captcha_right(request,*arg):
        var = {}
        if not request.POST.get('captcha',False):
            var['success'] = False
            var['description'] = 'captcha'
            return HttpResponse(json.dumps(var), content_type='application/json')
        if not request.session.get('captcha',False):
            var['success'] = False
            var['description'] = 'captcha'
            return HttpResponse(json.dumps(var), content_type='application/json')
        if request.session['captcha'].lower() == request.POST['captcha'].lower():
            return func(request,*arg)
        else:
            var['success'] = False
            var['description'] = 'captcha'
            return HttpResponse(json.dumps(var), content_type='application/json')
