#coding:utf-8
from LifeApi.models import NewEventTable, NewEventCat,\
                 NewDistrict,NewVenue, NewEventPrice,\
                  NewEventParagraph,NewEventImg,OldEvent,\
                 NewEventTableType, NewEventParagraphTag,\
                 NewEventPriceType,NewEventPriceCurrency,Crowfunding,\
                 NewEventTag, NewEventImgServer,NewDistrict_s,NewEventCat_s,\
                 AdminEventTheme,NewCatInfo, NewArticle,NewEventSeo
from seo_manage.models import FriendlyLink
from dahuodong.models import SysVenue,SysCommonDistrict,SysEvent
from django.db.models import Q 
import HTMLParser
                 
import datetime,time,urllib2
from admin_self.froms import  resolveContent
from django.core.cache import cache
import re,sys,os
import hashlib
from dateutil.relativedelta import relativedelta,MO
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from BeautifulSoup import BeautifulSoup



import logging
log = logging.getLogger('XieYin.app')  



def ip_Filter(request,num=10,userID=False,other_ip=['221.237.118.212','127.0.0.1','182.139.33.52','125.70.114.98','125.70.114.60']):
    
    #if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
    #    ip =  request.META['HTTP_X_FORWARDED_FOR']  
    #else:  
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


def updata_cache(ev):
    for ci in ev.city.all():
        cat_l=NewCatUrl(0,ci.title)
        for ca in ev.cat.all():
            if not cat_l.has_key(ca.id):
                NewCatUrl(0,ci.title,True)
                 
            event_city_cat(ci.id,ca.id,True,True )
        
        event_city_cat(ci.id,69 ,True,True  )     
        event_city_cat(ci.id,(19,70),True,True   )   
            
    #NewformatEvent(ev,ev.id,True)

def show_app(k,un=False): 
    
    def adds(self, request, queryset):
        message_bit=''
        ''' 
        if k.type_id==1:
            try:
                theme=AdminEventTheme.objects.get(id=k.cat_id)
            except:
                theme=AdminEventTheme.objects.create(
                                id=k.cat_id,
                                theme_name=k.name,                                
                                cities=' '.join([ci.district_name   for ci in k.city.all() ]),
                                begin_time=int(time.mktime(k.begin_time)) if k.begin_time else 0,
                                end_time=int(time.mktime(k.end_time)) if k.end_time else 0,
                                picture_web=k.img.urls if k.img else '',
                                picture_server=k.img.server.id if k.img else 0,
                                theme_order=k.order if  k.order else 0,
                                num=0,
                                event_set='',
                                show_pic=0,                                 
                                )
        '''     
        for ev in queryset:
            ev.cat.add(k)
            
            if k.type_id==2:
                ev.old_event.event_cool=k.cat_id-1000
                ev.old_event.save()
            ''' 
            elif k.type_id==1:
                if theme:
                    strs=[]
                    if theme.event_set:
                        for the in theme.event_set.split(';'):
                            if ev.old_event_id!=int(the):
                                strs.append(the)
                    theme.event_set='%s;%s' % (';'.join(strs),ev.old_event_id) if strs else str(ev.old_event_id)
                    theme.num=len(strs) +1 if strs else 1
                    theme.save()
            '''                      
            message_bit += u"《%s》" % (ev.name)
            
            updata_cache(ev)

        self.message_user(request, u"%s 添加到 %s " % (message_bit,k.name))
    adds.short_description = u"加入%s" % (k.name)
    
    def dele(self, request, queryset):
        message_bit=''
        '''
        if k.type_id==1:
            try:
                theme=AdminEventTheme.objects.get(id=k.cat_id)
            except:
                theme=None
        '''
        for ev in queryset:
            ev.cat.remove(k)
             
            if k.type_id==2:
                ev.old_event.event_cool=0
                ev.old_event.save()
            '''
            elif k.type_id==1:
                if theme:
                    strs=[]
                    if theme.event_set:
                        for the in theme.event_set.split(';'):
                            if ev.old_event_id!=int(the):
                                strs.append(the)
                    theme.event_set=';'.join(strs)
                    theme.num=len(strs)-1 if strs else 0
                    theme.save()    
            '''             
            message_bit += u"《%s》" % (ev.name)
            updata_cache(ev)
        self.message_user(request, u"%s 取消 %s" % (message_bit,k.name))
    dele.short_description = u"取消%s" % (k.name)
    
   
    
    
    
    if not un:
        return adds
    else:
        return dele
def ToEventPrice(ids):
    obj=NewEventTable.objects.get(id=ids)
    if not obj:
        return None
    
    if obj.Price:
        if obj.Price.Type.id!=3:
            try:
                pri_arr=obj.Price.str.split('/')
                pri_arr.sort()
                obj.Price.min=pri_arr[0]
                obj.Price.max=pri_arr[-1]
                obj.Price.save()
            except:
                pass
        else:
            
            
            try:
                k=Crowfunding.objects.get(event_id=obj.id)
      
             
                k.cf_total=obj.Price.max
                k.cf_price=obj.Price.str
                k.cf_already=obj.Price.min
                k.save()
            except:
             
                Crowfunding.objects.create(          
                                     cf_total=obj.Price.max,
                                     cf_price=obj.Price.str,
                                     event_id=obj.id,
                                     cf_already_percent=0,
                                     cf_already=obj.Price.min,
                                   
                                     )
    '''
    try:
        con_txt=resolveContent(obj.content)
    except:
        con_txt=[]
        
    if con_txt:
       
        obj.paragraph.all().delete()        
            
        for t in con_txt: 
            try:
                na=NewEventParagraphTag.objects.get(name=t[0])
            except:
                na=None
            if not na:
                na=NewEventParagraphTag.objects.create(
                                                    name= t[0] 
                                                       )
            txt=NewEventParagraph.objects.create(
                                             txt=t[1],
                                             cat_name=na
                                             )
            obj.paragraph.add(txt)
        obj.content=''
    
    '''
    search=obj.name
    search+=','.join([ci.district_name for ci in obj.city.all()])
    search+=','.join([ca.name for ca in obj.cat.all()])
    search+=','.join(["%s,%s" % (addrs.title,addrs.address) for addrs in obj.addr.all()])
    search+=','.join([t.name for t in obj.tag.all()])  
    
    obj.search=search
    obj.save()
            
     
    
def NewEventToOldEvent(ids):
    obj=NewEventTable.objects.get(id=ids)
    
    if not obj:
        print 'not new_event'
        return None
    
    if not obj.old_event:
        #old=OldEvent.objects.create(event_name=obj.name)
        obj.old_event=OldEvent.objects.create(event_name=obj.name,
                                              event_isshow=obj.isshow_id,
                                              event_order=obj.order if obj.order else 0,
                                              )
        obj.old_event.save()
        obj.save()
        #obj.old_event=OldEvent.objects.create(event_name=obj.name)
        #return None
        
        
    search=obj.name
    try:
        img_url=obj.img.order_by('end_time')[0]
        imgs=img_url.urls if img_url else '' 
    except:
        imgs=''
    try:
        citys=obj.city.order_by('id')[0]
        if citys:
             
            #obj.old_event.district_name=citys.district_name
            
            obj.old_event.district_id=citys.district_id#NewDistrict_s.objects.get(district_id=citys.district_id) 
            search+=citys.district_name
        '''
        else:
            obj.old_event.district_id=None
        '''
    except:
        pass
    
    try:
        
        addrs=obj.addr.order_by('venue_id')[0]
        
        if addrs:
            if addrs.venue_id:
                obj.old_event.venue_id=addrs.venue_id 
 
            obj.old_event.event_address=addrs.address
            obj.old_event.district_id=addrs.city.district_id
            #obj.old_event.venue_info=addrs.title
            search+=addrs.title+addrs.address
        '''
        else:
            obj.old_event.venue_id=None
        '''
    except:
        pass
        
    #addrs=addrs.id if addrs else None venue_info
    if obj.Price:
        
        obj.old_event.event_discount_price=obj.Price.sale
        obj.old_event.event_price_model=obj.Price.Type.id if obj.Price.Type.id!=6 else 0
        obj.old_event.cf_total=obj.Price.max
        obj.old_event.event_highprice=obj.Price.max
        obj.old_event.cf_price=obj.Price.str                
        obj.old_event.event_price_currency=obj.Price.Currency.id
        
            
        if obj.Price.Type.id==4:
            obj.old_event.event_price=u'免费'
            obj.old_event.event_isfree=1
            obj.old_event.event_lowprice=0
            obj.old_event.event_discount_price=''
            obj.old_event.event_discount=''
        elif obj.Price.str=='':
            obj.old_event.event_price=obj.Price.Type.name
        else:
            obj.old_event.event_price=obj.Price.str
            

        if obj.Price.Type.id!=3:
            try:
                pri_arr=obj.Price.str.split('/')
                pri_arr.sort()
                obj.Price.min=pri_arr[0]
                obj.Price.max=pri_arr[-1]
                obj.Price.save()
            except:
                pass
        else:  
            
            try:
                k=Crowfunding.objects.get(event_id=obj.id)
      
             
                k.cf_total=obj.Price.max
                k.cf_price=obj.Price.str
                k.cf_already=obj.Price.min
                k.save()
            except:
             
                Crowfunding.objects.create(          
                                     cf_total=obj.Price.max,
                                     cf_price=obj.Price.str,
                                     event_id=obj.id,
                                     cf_already_percent=0,
                                     cf_already=obj.Price.min,
                                   
                                     )
            
                
                
                    
    try:
        cats=obj.cat.filter(type=None).order_by('-cat_id')[0]    
        
        
       
        if cats: 
            print 'cat_id' 
            print cats.cat_id               
            obj.old_event.event_cat=cats.cat_id#NewEventCat_s.objects.get(cat_id=cats.cat_id)
            obj.old_event.event_cat1=cats.parent.cat_id
            #event.event_cat1
            search+=cats.name
    except:
        print 'cat_err'
                       
  
             
    
    obj.old_event.event_name=obj.name
    if obj.tag.count():
        obj.old_event.event_cat_tag=','.join([t.name for t in obj.tag.all()])            
    obj.old_event.event_img=imgs
    obj.old_event.event_img_server=1
    obj.old_event.event_isshow=obj.isshow.id
    obj.old_event.event_app_name=obj.fname
    obj.old_event.event_begin_time=int(time.mktime(obj.begin_time.timetuple())) if obj.begin_time else 0
    obj.old_event.event_islongtime=0
    obj.old_event.event_rank=obj.order
    if obj.end_time:
        obj.old_event.event_end_time=int(time.mktime(obj.end_time.timetuple()))
    else:
        obj.old_event.event_islongtime=1
        obj.old_event.event_end_time=1419955200
    
    search+=obj.old_event.event_cat_tag if obj.old_event.event_cat_tag else ''
    obj.old_event.event_search=search#obj.name+obj.old_event.event_tag+obj.old_event.district_name ;
    if obj.old_event.event_end_time and time.time()>obj.old_event.event_end_time:
        obj.old_event.event_time_expire=2
    else:
        obj.old_event.event_time_expire=0
        
    obj.old_event.event_content=''
          
    for txts in  obj.paragraph.all():
        obj.old_event.event_content+='<h2>'+txts.cat_name.name+'</h2>'
        obj.old_event.event_content+=txts.txt
      
    #obj.old_event.event_content=
    '''
    try:
        con_txt=resolveContent(obj.content)
    except:
        con_txt=[]
        
    if con_txt:
       
        obj.paragraph.all().delete()        
            
        for t in con_txt: 
            try:
                na=NewEventParagraphTag.objects.get(name=t[0])
            except:
                na=None
            if not na:
                na=NewEventParagraphTag.objects.create(
                                                    name= t[0] 
                                                       )
            txt=NewEventParagraph.objects.create(
                                             txt=t[1],
                                             cat_name=na
                                             )
            obj.paragraph.add(txt)
    
    '''
    
    
    try:
        obj.old_event.save()
    except Exception,e:
        print e
    #obj.content=''
    obj.search=search
    obj.save()
    return True
                     
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
        if oldevent.event_begin_time:
            begin_dates = time.localtime(oldevent.event_begin_time)
            begin_dates = datetime.datetime(*begin_dates[:6])
        else:
            begin_dates=''
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
                                       content='',
                                       begin_time=begin_dates,
                                       end_time=end_dates,   
                                       order=oldevent.event_recomend if oldevent.event_recomend else 0,
                                       hot=oldevent.event_rank if oldevent.event_rank else 0,
                                       search=re.sub(ur"[^\u4e00-\u9fa5\w]", " ", oldevent.event_search) if oldevent.event_search else '',
                                      
                                                                           
                                  )
        except Exception,e:
            log.debug('%s' % e) 
 
            try:
                p=NewEventTable.objects.create(
                                   #id=ids,
                               name=re.sub(ur"[^\u4e00-\u9fa5\w]", " ", oldevent.event_name), 
                               fname =oldevent.event_app_name if oldevent.event_app_name else '' ,
                                
                               old_event=oldevent,
                               content='',
                               begin_time=begin_dates,
                               end_time=end_dates,   
                               order=oldevent.event_recomend if oldevent.event_recomend else 0,
                               hot=oldevent.event_rank if oldevent.event_rank else 0,
                               search=re.sub(ur"[^\u4e00-\u9fa5\w]", " ", oldevent.event_search) if oldevent.event_search else '',
                                      
                                                                   
                          )
 
                
            except Exception,e:
                log.debug('%s' % e) 
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
    p.search=re.sub(ur"[^\u4e00-\u9fa5\w]", " ", oldevent.event_search) if  oldevent.event_search else ''   
    try:
        p.save()
    except Exception,e:
        print 'err save'
        print e
    return p

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

def NewCity(type=0,new=False):
    
    baiDuCodeDict = cache.get('NewbaiDuCodeDict') #通过百度代码获取城市信息 元组
    titleDict=cache.get('NewtitleDict')#通过城市名称获取 元组
    districtIdDict=cache.get('NewdistrictIdDict')#通过城市旧id获取 元组
    id_city =cache.get('id_city')#通过城市id获取 字典
    map_city= cache.get('map_city')#城市地图 字典
    map_city_list= cache.get('map_city_list')#城市关系 字典
    if new or not baiDuCodeDict or not titleDict or not districtIdDict or not map_city or not id_city or not map_city_list: 
        log.debug('run city %s' % datetime.datetime.now) 
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
            cache.set('NewbaiDuCodeDict',baiDuCodeDict,86400*10)
            cache.set('NewtitleDict',titleDict,86400*10)
            cache.set('NewdistrictIdDict',districtIdDict,86400*10)
            cache.set('id_city',id_city,86400*10)#通过城市id获取 字典
            cache.set('map_city',map_city,86400*10)#城市地图 字典
            cache.set('map_city_list',map_city_list,86400*10)#城市关系 字典
        
    
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

    cat_x['tag']=[{'id':ta.id,'name':ta.name} for ta in cat.tag.all().order_by('-hot')]
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
def NewCatUrl_edit(type=0,city='',new=False,catename=''):
    f_cat = cache.get('cat_event_map_edit%s' % city) 
    x_cat = cache.get('cat_event_list_edit%s' % city) 
    id_cat= cache.get('cat_event_id_edit%s' % city) 
    
    if new or not f_cat or not x_cat or not id_cat:
        log.debug('run cat %s' % datetime.datetime.now) 
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
                #if not ca.neweventcat.type:                
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
                                    
                if catename:
                    if cat['ename']==catename:
                        id_cat[cat['id']]['flag'] = 'true'
                x_cat[cat['ename']]=id_cat[cat['id']]
                

                
            else:  
                #del id_cat[cat['id']]   
                #continue          
                  
                if city:
                    id_cat[cat['id']]['caturl']= '/%s/%s/' % (city,cat['id'])
                else:
                    id_cat[cat['id']]['caturl']= '/%s/' % (cat['id'])
                    
                if catename:
                    if cat['id']==catename:
                        id_cat[cat['id']]['flag'] = 'true'
                x_cat[cat['id']]=id_cat[cat['id']]

            if id_cat.has_key(cat['fid']):
                id_cat[cat['fid']]['child'].append(id_cat[cat['id']])
            else:
                #if cat['ename']:
                f_cat.append(id_cat[cat['id']])
                                
                
                
         
        
        
        cache.set('cat_event_id_edit%s' % city,id_cat,86400*10)
        cache.set('cat_event_map_edit%s' % city,f_cat,86400*10)
        cache.set('cat_event_list_edit%s' % city,x_cat,86400*10)
        
    
    if catename and x_cat.has_key(catename):        
        x_cat[catename]['flag'] = 'true'
        try:
            id_cat[str(x_cat[catename]['id'])]['flag'] = 'true'
        except:
            id_cat[ x_cat[catename]['id'] ]['flag'] = 'true'
        #id_cat[x_cat[catename]['id']]['flag'] = 'true'
        map_id(f_cat,x_cat[catename])
        
         
 
            
    import copy 
    #f_cat=copy.deepcopy(f_cat)
    f_cat= map_show(copy.deepcopy(f_cat))
    if type==0 or not type:
        return x_cat
    elif type==1:            
        return f_cat
    else:
        return id_cat

#new=True, scan the database
def NewCatUrl(type=0,city='',new=False,catename=''):
    f_cat = cache.get('cat_event_map%s' % city) 
    x_cat = cache.get('cat_event_list%s' % city) 
    id_cat= cache.get('cat_event_id%s' % city) 
 
 


    
    if new or not f_cat or not x_cat or not id_cat:
        #log.debug('run cat %s' % datetime.datetime.now) 
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
                                    
                if catename:
                    if cat['ename']==catename:
                        id_cat[cat['id']]['flag'] = 'true'
                x_cat[cat['ename']]=id_cat[cat['id']]
                

                
            else:  
                #del id_cat[cat['id']]   
                #continue          
                  
                if city:
                    id_cat[cat['id']]['caturl']= '/%s/%s/' % (city,cat['id'])
                else:
                    id_cat[cat['id']]['caturl']= '/%s/' % (cat['id'])
                    
                if catename:
                    if cat['id']==catename:
                        id_cat[cat['id']]['flag'] = 'true'
                x_cat[cat['id']]=id_cat[cat['id']]

            if id_cat.has_key(cat['fid']):
                id_cat[cat['fid']]['child'].append(id_cat[cat['id']])
            else:
                #if cat['ename']:
                f_cat.append(id_cat[cat['id']])
                                
                
                
         
        
        
        cache.set('cat_event_id%s' % city,id_cat,86400*10)
        cache.set('cat_event_map%s' % city,f_cat,86400*10)
        cache.set('cat_event_list%s' % city,x_cat,86400*10)
        
    
    if catename and x_cat.has_key(catename):        
        x_cat[catename]['flag'] = 'true'
        try:
            id_cat[str(x_cat[catename]['id'])]['flag'] = 'true'
        except:
            id_cat[ x_cat[catename]['id'] ]['flag'] = 'true'
        #id_cat[x_cat[catename]['id']]['flag'] = 'true'
        map_id(f_cat,x_cat[catename])
        
         
 
            
    import copy 
    #f_cat=copy.deepcopy(f_cat)
    f_cat= map_show(copy.deepcopy(f_cat))
    if type==0 or not type:
        return x_cat
    elif type==1:            
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
    elif cat_arr.has_key(str(id)):
        id=str(id)
        cat_ll.append(id)
        if cat_arr[id]['child']:
            for ch in cat_arr[id]['child']:
                cat_ll.extend(find_ch(ch['id'], cat_arr))
        
                
    return cat_ll

#通过城市id和tag id获取活动    
def event_city_tag(city_id=None,tag_id=None, new=False,cou=False):
    citys=city_id
    if  type(city_id) == tuple :
        citys=str(city_id).replace('(','').replace( ',' ,'').replace(')' ,'').replace(' ' ,'')  
    cats=tag_id
    if  type(tag_id) == tuple :
        cats= str(tag_id).replace('(','').replace( ',' ,'').replace(')' ,'').replace(' ' ,'')  
    event  = cache.get('event_tag_%s_%s' % (citys,cats)) 
    count  = cache.get('event_tag_%s_%s_con' % (citys,cats)) 
    
    if new or not event or not count :  
    #if new :
        event =[]
        ev=NewEventTable.objects.filter(isshow__in=(1,8)).filter(end_time__gt=datetime.date.today())
        ev=ev.exclude(state=2)
        if city_id:
            if type(city_id) == tuple:
                ev=ev.filter(city__in=city_id)
            else:
                ev=ev.filter(city=city_id)
           
        if tag_id:    
            if type(tag_id) == tuple:
 
                ev=ev.filter(tag__in=list(tag_id))
            else:                
                ev=ev.filter(tag = tag_id)
        
        ev=ev.order_by("-order","-rel_time").distinct()        
        
        
        #event = [NewformatEvent(item) for item in ev[:10] ]
        count=ev.count()
        event=[]
        if count:
            try:
                event = [int(item.old_event_id) for item in ev[:12] ]
            except:
                pass
        
        if event :
            
            cache.set('event_tag_%s_%s' % (citys,cats),event ,86400*10)
            cache.set('event_tag_%s_%s_con' % (citys,cats),count ,86400*10)
        else:
            cache.set('event_tag_%s_%s' % (citys,cats),{'flag':False}  ,86400*10)
            cache.set('event_tag_%s_%s_con' % (citys,cats),{'flag':False} ,86400*10)           
        

    if cou:
        try:
            if not count['flag']:
                return 0
        except:
            
            return count
    else:
        try:
            if not event['flag']:
                return []
        except:

            sk=[]
            for item in event:
                if type(item)==int:
                    sk.append(NewformatEvent(False,item))
                else:
                    sk.append(item)
                    
            return sk

    return []

     
#通过城市id和分类id获取活动    
def event_city_cat(city_id=None,cat_id=None, new=False,cou=False):
    '''
    cou = True, return amount number
    cou = False, return detail info
    '''
    citys=city_id
    if  type(city_id) == tuple :
        citys=str(city_id).replace('(','').replace( ',' ,'').replace(')' ,'').replace(' ' ,'')  
    cats=cat_id
    if  type(cat_id) == tuple :
        cats= str(cat_id).replace('(','').replace( ',' ,'').replace(')' ,'').replace(' ' ,'')  
    event  = cache.get('event_%s_%s' % (citys,cats)) 
    count  = cache.get('event_%s_%s_con' % (citys,cats)) 
    
    if new or not event or not count :  
    #if new :
        event =[]
        ev=NewEventTable.objects.filter(isshow__in=(1,8)).filter(begin_time__gt=datetime.date.today())
        ev=ev.exclude(state=2)
        if city_id:
            if type(city_id) == tuple:
                ev=ev.filter(city__in=city_id)
            else:
                ev=ev.filter(city=city_id)
           
        if cat_id:    
            if type(cat_id) == tuple:
                cat_s=[]
                for id in cat_id:
                    cat_s.extend(find_ch(id,NewCatUrl(2)))
                ev=ev.filter(cat__in=cat_s)
            else:
                ev=ev.filter(cat__in=find_ch(cat_id,NewCatUrl(2)))
        
        ev=ev.order_by("-order","-rel_time").distinct()        
        
        
        #event = [NewformatEvent(item) for item in ev[:10] ]
        count=ev.count()
        event=[]
        if count:
            try:
                event = [int(item.old_event_id) for item in ev[:12] ]
            except:
                pass
        timeout = 86400 
        if event :
            
            cache.set('event_%s_%s' % (citys,cats),event , timeout)
            cache.set('event_%s_%s_con' % (citys,cats),count , timeout)
        else:
            cache.set('event_%s_%s' % (citys,cats),{'flag':False}  , timeout)
            cache.set('event_%s_%s_con' % (citys,cats),{'flag':False} , timeout)           
        

    if cou:
        try:
            if not count['flag']:
                return 0
        except:
            
            return count
    else:
        try:
            if not event['flag']:
                return []
        except:

            sk=[]
            for item in event:
                if type(item)==int:
                    ev=NewformatEvent(False,item)
                    if not ev.has_key('time_expire'):
                        sk.append(ev)
                else:
                    sk.append(item)
                    
            return sk

    return []

     

def get_str_event(str=None,new=False):
    event_str = cache.get('event_str')
    if new or not event_str:
        event_str={}
        for ev in NewEventTable.objects.exclude(ename=''):
            event_str[ev.ename]=ev.id
        cache.set('event_str',event_str,86400*10)
        
    if str:
        try:
            return event_str[str]
        except:
            return None
    else:
        return event_str
    
def get_site_links(new=False):
    site_links = cache.get('site_links')
    if new or not site_links:
        site_links=[]
        for ev in FriendlyLink.objects.exclude(hot__gt=0).order_by('-order'):
            lin=[ev.name,ev.url,ev.page,ev.img]
            #if ev.city:
            lin.append( [city.title for city in ev.city.all()])
            #if ev.cat:
            lin.append( [cat.ename if cat.ename else cat.id for cat in ev.cat.all()])
            site_links.append(lin)
            
        cache.set('site_links',site_links,86400*10)
 
    return site_links
def get_site_hot_links(new=False):
    site_links = cache.get('site_hot_links')
    if new or not site_links:
        site_links=[]
        #.filter(begintime__gt=datetime.datetime.now()).filter(endtime__gt=datetime.datetime.now())
        for ev in FriendlyLink.objects.filter(hot__gt=0).order_by('-hot'):
            
            lin=[ev.name,ev.url,ev.page,ev.img,datetime.datetime.strftime(ev.begintime,'%Y-%m-%d %H:%M:%S') if ev.begintime else None,datetime.datetime.strftime(ev.endtime,'%Y-%m-%d %H:%M:%S') if ev.endtime else None]
            if ev.city:
                lin.append( [city.title for city in ev.city.all()])
            site_links.append(lin)
            
        cache.set('site_hot_links',site_links,86400*10)

    return site_links   
def get_str_singers(event_name=None,new=False):   
    singers_str = cache.get('singers_str')
    if new or not singers_str:
        from LifeApi.models import singers
        singers_str = [item.name for item in singers.objects.all()]
        cache.set('singers_str',singers_str,86400*10)
        
    if event_name:        
        s_name = ''
        for name in singers_str:
            if name in event_name:
                s_name = name
                break
        return s_name
    else:
        return singers_str
    


'''
def GetFormatEvent(query,new=False):
    if query.isdigit():
        try:
            ev = NewEventTable.objects.get(old_event_id= query )
        except:
            try:
                ev = NewEventTable.objects.get(id= query )
            except:                 
                ev=oldEventToNewEvent(query,False)
                
                #ev=None
             
    else:
        try:
            ev = NewEventTable.objects.get(id= get_str_event(query) )
        except:
            return None
    
    format=NewformatEvent(ev,True)         
    city=[(ci.district_id,ci.district_name) for ci in ev.city.all() ]
    cat =[(ca.id,ca.name) for ca in ev.cat.all()]
    
    return 
'''
   
def find_cat_ch(cat_id_li={},cat_id=0,tmp=[]):
    #cat_id_li=NewCatUrl(False,city)
    
    try:
        if cat_id_li.has_key(cat_id):   
            #log.debug(cat_id)         
            tmp.append(cat_id_li[cat_id]['id'])
        elif cat_id_li.has_key(str(cat_id)):
            cat_id=str(cat_id)
            tmp.append(cat_id_li[str(cat_id)]['id'])
        
        if cat_id_li[cat_id]['child']:
            for ch in cat_id_li[cat_id]['child']:
                #tmp.append(ch['id'])
                 
                find_cat_ch(cat_id_li,ch['id'],tmp)
           
    except: 
        pass

def get_event_list( cat=False,city=False,date=False,page=False,offset=False,order=False,new=False):
    '''
    city is a (id,name,title) tuple, name is Chinese, title is Pinyin
    '''
 
    key_name=''
    if not offset:        
        key_name='listcou_%s_%s_%s' % (cat,city,date)        
        key_name = hashlib.md5(key_name).hexdigest()
    else:        
        key_name='list_%s_%s_%s_%s_%s_%s' % (cat,city,date,page,offset,order)
        key_name = hashlib.md5(key_name).hexdigest()
        
        
    list  = cache.get(key_name)   

    if not list or new:
    #if  new:
        #log.debug('run list_show %s' % datetime.datetime.now) 

        args=NewEventTable.objects.filter( isshow__in=(1,8)).filter(end_time__gt=datetime.date.today())
        if date and date != 'latest':
            now = datetime.datetime.now()
            today = datetime.date.today()
            startTime = 0
            endTime = 0
            if 'thisweek' == date:
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
                cat_id=cat_id_li[str(cat)]['id']
            except:
                try:
                    cat_id=cat_id_li[int(cat)]['id']
                except:
                    pass
              
            #log.debug(cat_id)  
            if cat_id:
                #log.debug('%s' % type(cat_id))
                find_cat_ch(NewCatUrl(2,city[2]),cat_id,tmp=tmps)
                
            #log.debug(str(tmps))
            if len(tmps)>0:
                args = args.filter(cat__in=tmps)
            else:
                return None
           
         
        #return render_to_response('base_error.html',{'error_msg':str(cat)})
        
        if city[0]:  
            args =args.filter( city=city[0] )
            #args = args&Q(spot_city=city)
            
           
            
        #log.debug('%s' % key_name) 
        #log.debug('offset run') 
        #log.debug(key_name) 
        #cou=args.distinct().count()
        #if cou>0:
        if not offset:
            list = args.distinct().count()
            #log.debug('count')
        else:
            #return SysSpotInfo.objects.filter(args).order_by(order)[page:offset]
            list = [ev.old_event_id for ev in args.order_by("-order","-rel_time",order).distinct()[page:offset]]    
            #log.debug('list')        
        
        #log.debug(connection.queries) 
        
        
        if not list:
            cache.set(key_name,{'flag':False},60*60)
        else:
            cache.set(key_name,list,60*60)
            
    try:
        if not list['flag']:
            if not offset:
                list=0
            else:
                list=[]
    except:
        pass
            
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
 
            
    
    #navigationDict = dict()
    #navigationDict['catname'] = u'活动网'
    #navigationDict['caturl'] = '/%s/' % (city)
    #new_navigationList.append(navigationDict)
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
        #head['description'] =u"%s%s%s" % (event.search if event.search else '',tags, event.begin_time)
        head['description']=u"%s相关信息，就上【活动家www.huodongjia.com】。活动家活动网为您提供%s的最新信息，包含查询、报名、价格、订票等全方位服务，权威、全面、方便、快捷。了解活动信息，购买活动优惠票，就找活动家，随时随地购票！服务热线:400-003-3879" % (event_li['event_name'],event_li['event_name'])
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
            title=u"%s_【门票-价格-订票】_活动家" % ( event.name)
        
        head['title']=title
        head['keywords']='%s,%s' % (','.join(event_li['event_tag']),','.join(cat_str))
        '''
        head['keywords']='%s,%s' % (','.join(cat_str),tags)
        for tag in event.tag.all():            
            head['keywords']+=tag.name+','
        '''
      
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
                    name_s=''                  
                    #return None
        
        if event.seo.title:            
            head['title']=event.seo.title.replace('(city)', event_li['district_name'])
            try:
                head['title']=head['title'].replace('(name)', event_li['event_name'])
            except:
                pass
            times=event_li['event_begin_time'].split('-')
            if len(times)>=3:                
                    head['title']=head['title'].replace('(year)',times[0])       
                    head['title']=head['title'].replace('(month)',times[1])
                    head['title']=head['title'].replace('(day)',times[2])
            try:
                head['title']=head['title'].replace('(singer)',name_s) 
            except:
                pass
            
            try:
                head['title']=head['title'].replace('(cat)', event_li['cat_name'])
            except:
                pass
            try:
                head['title']=head['title'].replace('(tag)', ','.join(event_li['event_tag']))
            except:
                pass
        else:
            catId=event_li['event_cat1']
            
            if catId == 1:
                title = u'%s-门票-活动家网上订票  '%(event_li['event_name'])
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
                title=u"%s_【门票-价格-订票】_活动家" % ( event.name)
            
            head['title']=title
            
            
            
            
            
            
        if event.seo.keywords:
            head['keywords']=event.seo.keywords.replace('(city)', event_li['district_name'])
            try:
                head['keywords']=head['keywords'].replace('(name)', event_li['event_name'])
            except:
                pass
            times=event_li['event_begin_time'].split('-')
            if len(times)>=3:                
                    head['keywords']=head['keywords'].replace('(year)',times[0])       
                    head['keywords']=head['keywords'].replace('(month)',times[1])
                    head['keywords']=head['keywords'].replace('(day)',times[2])
            try:
                head['keywords']=head['keywords'].replace('(singer)',name_s) 
            except:
                pass
            try:
                head['keywords']=head['keywords'].replace('(cat)', event_li['cat_name'])
            except:
                pass
            try:
                head['keywords']=head['keywords'].replace('(tag)', ','.join(event_li['event_tag']))
            except:
                pass
            #head['keywords']=event.seo.keywords.replace('(city)', event_li['district_name']).replace('(name)', event_li['event_name']).replace('(year)',event_li['event_begin_time'].split('-')[0]).replace('(month)',event_li['event_begin_time'].split('-')[1]).replace('(day)',event_li['event_begin_time'].split('-')[2]).replace('(singer)',name_s)
        else:
            
            cat_str=[]
            for nav in navigationList:           
                cat_str.append( nav['catname'].replace(u'首页',u'活动家'))
            
            head['keywords']='%s,%s' % (','.join(event_li['event_tag']),','.join(cat_str))
            '''
            for tag in event.tag.all():     
                head['keywords']+=tag.name+','   
            '''  
        if event.seo.description:   
            if not event_li['event_end_time']:
                event_li['event_end_time']='2014-12-30'
            try:
                head['description']=event.seo.description.replace('(city)', event_li['district_name']).\
                replace('(name)', event_li['event_name'])
                head['description']=head['description'].replace('(year)',event_li['event_begin_time']\
                .split('-')[0]).replace('(month)',event_li['event_begin_time'].split('-')[1]).\
                replace('(day)',event_li['event_begin_time'].split('-')[2]).\
                replace('(end_year)',event_li['event_end_time'].split('-')[0]).\
                replace('(end_month)',event_li['event_end_time'].split('-')[1]).\
                replace('(end_day)',event_li['event_end_time'].split('-')[2])
                try:
                    head['description']=head['description'].replace('(singer)',name_s)
                except:
                    head['description']=head['description'].replace('(singer)','')
                try:
                    head['description']=head['description'].replace('(venue)',event_li['event_venue'])
                except:
                    head['description']=head['description'].replace('(venue)','')
                    
                try:
                    head['description']=head['description'].replace('(cat)', event_li['cat_name'])
                except:
                    pass
                try:
                    head['description']=head['description'].replace('(tag)', ','.join(event_li['event_tag']))
                except:
                    pass
                
            except Exception,e:
                
                head['description']=u"%s相关信息，就上【活动家www.huodongjia.com】。活动家活动网为您提供%s的最新信息，包含查询、报名、价格、订票等全方位服务，权威、全面、方便、快捷。了解活动信息，购买活动优惠票，就找活动家，随时随地购票！服务热线:400-003-3879" % (event_li['event_name'],event_li['event_name'])
            

        else:
            head['description']=u"%s相关信息，就上【活动家www.huodongjia.com】。活动家活动网为您提供%s的最新信息，包含查询、报名、价格、订票等全方位服务，权威、全面、方便、快捷。了解活动信息，购买活动优惠票，就找活动家，随时随地购票！服务热线:400-003-3879" % (event_li['event_name'],event_li['event_name'])
            
        #return head
 
    
        
 
 
    return head   

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

def str_html(str=None):
    
    str = str.replace(' ','').replace('\r','').replace('\n','').replace('<p>','').replace('</p>','\r\n').replace('<br>','\r\n')\
                .replace('<br/>','\r\n').replace('<br />','\r\n').replace('\r\n\r\n','\r\n')
    str = replaceCharEntity(str)   
    
    #str = str.replace('\r\n','').replace('<p>','').replace('</p>','\r\n').replace('<br>','\r\n')\
                #.replace('<br />','\r\n').replace('\r\n\r\n','\r\n').replace('\n\n','\n')
    #str = replaceCharEntity(str)
    return str    

   
   
   
def NewformatEvent(new_event,evnet_id=False,new=False,detail = False):

    res={}
    if evnet_id:
        res  = cache.get('event_%s' % evnet_id) 
    else:
        if new_event:
            res  = cache.get('event_%s' % (new_event.old_event_id,)) 
    
    if not res or new:
        #log.debug('run event %s' % datetime.datetime.now) 
        #print res
        res={}
        #res['ca']=False
        if not new_event:
            if evnet_id:
                
                try:
                    new_event=NewEventTable.objects.get(old_event_id=evnet_id)
                except:
                    new_event = oldEventToNewEvent(evnet_id)
                    #return res
            else:
                return res
        
        #print 'cache_run'
    
        
        if not new_event:
            return res
        
        #getEventHead(event_li,event,navigationList)
        res['isshow']=new_event.isshow_id    
        res['id']=new_event.id
        res['event_id'] =  new_event.old_event_id if new_event.old_event_id else new_event.id
        res['event_name'] = new_event.name
        res['ename'] = new_event.ename
        res['fname'] = new_event.fname
        res['order'] = new_event.order
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
            if not new_event.edit:
                res['event_address'] =new_event.old_event.event_address if new_event.old_event else '' 
            else:
                res['event_address'] =''
        res['event_content']=[]
        
        #res['event_content_type']=[]
        try:  
         
            for con in new_event.paragraph.all().order_by('-txt_order','id'):
                txt=con.txt.replace('pic1.qkan.com','pic.huodongjia.com').replace('\n','').replace('\r','')#.replace('<br>','')
                
                try:
                    soup = BeautifulSoup(txt)
                    for tag in soup.findAll('img'):
                        tag['class'] = 'img-responsive'
                        try:
                            if tag.has_key('alt'):
                                if not len(tag['alt']):
                                    tag['alt']=res['event_name']
                        except:
                            tag['alt']=res['event_name']
                        #tag['alt']=res['event_name']
      
                    #html_parser = HTMLParser.HTMLParser()
                    txt = str(soup).strip()     
                except:
                    pass
                #res['event_content_type'].append(type(con.cat_name.name))
                if con.cat_name.name==u'会议通知':    
                                 
                    res['event_content'].insert(0,(con.cat_name.name,txt))
                else:
                    res['event_content'].append((con.cat_name.name,txt))

            #res['event_content'] = [(con.cat_name.name,con.txt.replace('pic1.qkan.com','pic.huodongjia.com')) for con in new_event.paragraph.all().order_by('-txt_order','id')]   
        except:
            pass
            
                 

        
        # seems not useful
        ##if new_event.end_time and new_event.end_time<datetime.datetime.today():
        #if new_event.begin_time and new_event.begin_time<=datetime.datetime.today():
        #    #state
        #    res['time_expire'] = 2

        res['event_tag'] = []
        res['event_tag_id'] = []
        for tag in  new_event.tag.all().order_by('-hot','-id'):
            res['event_tag'].append(tag.name)
            res['event_tag_id'].append(tag.id)
            #res['event_tag'] = [tag.name for tag in  new_event.tag.all()] 
            #res['event_tag_id'] = [tag.id for tag in  new_event.tag.all()]
        new_tag=[]
        cat_tag=[]
        des=''
        
        if new_event.content:
            des_s=  new_event.content       
            i=1
            for de in des_s.split('\n'):
                if des:
                    des+='\r\n'
                te= BeautifulSoup(de).text
                if te:
                    i+=1
                    des += '%s' % te
                if i>3:
                    break        
        else:
            if res['event_content']:
                str_h=  str_html(res['event_content'][0][1])
                
        
                i=1
                for de in str_h.split('\n'):
                    if des:
                        des+='\r\n'
                    te= BeautifulSoup(de).text
                    if te:
                        i+=1
                        des += '%s' % te
                    if i>3:
                        break
        res['content']=des     
        for i in range(len(res['event_tag_id'])):
            try:
                new_event.cat.get(tag= res['event_tag_id'][i])
                cat_tag.append(res['event_tag'][i])
            except:
                new_tag.append(res['event_tag'][i])
        res['event_tag'] = new_tag
        res['event_tag'].extend(cat_tag)
        try:
            imgs_logo=new_event.img.get(height=470)
            res['event_img_h330'] =imgs_logo.server.name+imgs_logo.urls
            if re.match('/',imgs_logo.urls):
                res['event_img_h330'] ='http://pic.huodongjia.com'+imgs_logo.urls
            else:
                res['event_img_h330'] ='http://pic.huodongjia.com/'+imgs_logo.urls
        except:
            pass
        
        try:
            imgs=new_event.img.exclude(height__in=(580,470)).order_by('-order')[0]
        
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
        #res['event_url']='/%s_%s.html' % (datetime.datetime.strftime(new_event.begin_time,'%Y%m%d') if new_event.begin_time else '',new_event.id) 
        #res['event_url'] = '/%s-%s.html' %(new_event.ename, res['event_id']) if new_event.ename else '%s-%s.html' %('event', res['event_id'])
        res['event_url'] = '/event-%s.html' %(res['event_id'])
        res['event_end_time'] = datetime.datetime.strftime(new_event.end_time,'%Y-%m-%d') if new_event.end_time else ''
        res['rel_time'] =  datetime.datetime.strftime(new_event.rel_time,'%Y-%m-%d') if new_event.rel_time else ''
        res['event_islongtime'] = new_event.state
        if new_event.Price:            

            event_price_model = new_event.Price.Type_id

            res['event_price_unit'] = new_event.Price.Currency.ename if new_event.Price.Currency else "RMB"
            res['event_price_unit_name']=new_event.Price.Currency.name if new_event.Price.Currency else u"人民币"
            res['event_price_unit_sign']=new_event.Price.Currency.sign if new_event.Price.Currency else u"￥"
            res['event_price_unit_rate']=new_event.Price.Currency.rate
            res['price_unit_info']=[]
            res['price_return_flag'] = False

            # cash return: only business, and exclude medical 
            # catid == 4, medical, catid == 69, business
            fids = wrap_cat_family_id(69, exclude_id=4, new=new)

            if new_event.Price_event_table.all().count():
                pri=[]
                sal=[]
                
                prs=new_event.Price_event_table.filter(Currency=new_event.Price.Currency)
                #prs=prs.filter(begin_time__lte=datetime.datetime.now())
                #prs=prs.filter(end_time__gte=datetime.datetime.now())
                #prs=prs.filter(stock__gt=0)
                #prs=prs.filter(status=1)

                for pr in prs:
                    pt={}
                    
                    pt['begin_time']=datetime.datetime.strftime(pr.begin_time,'%Y-%m-%d %H:%M:%S') if pr.begin_time else ''
                    pt['end_time']=datetime.datetime.strftime(pr.end_time,'%Y-%m-%d %H:%M:%S')  if pr.end_time else ''
                    pt['stock']=pr.stock
                    pt['status']=pr.status
                    pt['price']=float(pr.price)
                    #pr.sale can be None
                    if pr.sale:
                        pt['sale']=float(pr.sale)
                    else:
                        pt['sale']=pr.sale

                    pt['content']=pr.content
       
                    # cash return: only business, and exclude medical 
                    # catid == 4, medical
                    if event_price_model == 6 and res['catid'] in fids:
                        if pr.original_price is not None:
                            # if original_price == price, no cash return
                            if abs(pr.original_price - pr.price) > 1e-3:
                                # pr.original_price, pr.price, etc are Decimal type, so _isinteger(), not is_integer()
                                pt['original_price'] = ('%i' if pr.original_price._isinteger() else '%s') %pr.original_price
                                _tmp = pr.price - pr.original_price
                                pt['price_return'] = ('%i' if _tmp._isinteger() else '%s') %_tmp
                                res['price_return_flag'] = True
                        else:
                            # price greater than & equal to 1000RMB, return about 5% cash
                            if pt['price'] / res['event_price_unit_rate'] >= 1000:
                                pt['price_return'], pt['original_price'] = cash_return(pt['price'], res['event_price_unit_rate'])
                                res['price_return_flag'] = True

                    res['price_unit_info'].append(pt)

                    if pr.price:
                        pri1=str(pr.price)
                        pri2=pri1.split('.')
                        if int(pri2[1])==0:
                            pri.append(pri2[0])
                        else:
                            pri.append(pri1)
                    if pr.sale:
                        pri1=str(pr.sale)
                        pri2=pri1.split('.')
                        if int(pri2[1])==0:
                            sal.append(pri2[0])
                        else:
                            sal.append(pri1)
                        #sal.append(str(int(pr.price)))
                res['event_price'] = '/'.join(pri)  if pri else u'暂停销售'
                res['event_discount_price'] = '/'.join(sal)  #if sal else   new_event.Price.sale if new_event.Price.sale else ''
            else:
             
                res['event_price'] =new_event.Price.str
                res['event_discount_price']=new_event.Price.sale if new_event.Price.sale else ''
                if res['event_discount_price']:

                    res['price_unit_info'] = [{'price': float(i), 'sale': float(j), 
                                               'begin_time': False, 'end_time': False,
                                               'stock': 100, 'status': 1} 
                                               for i,j in zip(res['event_price'].split('/'), 
                                                              res['event_discount_price'].split('/'))]
                else:
                    try:
                        for i in res['event_price'].split('/'):
                            i = float(i)
                            price_return = actual_price = ''
                            # price greater than & equal to 1000RMB, return about 5% cash
                            if event_price_model == 6 and res['catid'] in fids \
                                    and i / res['event_price_unit_rate'] >= 1000:
                                price_return, actual_price = cash_return(i, res['event_price_unit_rate'])
                                res['price_return_flag'] = True
                            
                            res['price_unit_info'].append({
                                'price': float(i), 'price_return': price_return,
                                'original_price': actual_price, 'begin_time': None,
                                'end_time': None, 'stock': 100, 'status': 1
                                })
                    except:
                        res['price_unit_info']=[]
                
            res['price_unit_info'] = sorted(res['price_unit_info'], key=lambda x:x['price'])

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
        #cache.set('event_%s' % res['event_id'],res,86400*10)
        
        if res.has_key('event_id'):
            cache.set('event_%s' % res['event_id'],res,86400*10)
            updata_cache(new_event)
            '''
            for ci in new_event.city.all():
                cat_l=NewCatUrl(0,ci.title)
                for ca in new_event.cat.all():
                    if not cat_l.has_key(ca.id):
                        NewCatUrl(0,ci.title,True)
                         
                    event_city_cat(ci.id,ca.id,True)
                
                event_city_cat(ci.id,69 ,True,True )     
                event_city_cat(ci.id,(19,70),True,True  )   
            '''
    
    if not res.has_key('ename') or not res['ename'] :
        res['ename']='event'
    if not res.has_key('content'):
        des=''
        if res['event_content']:
            str_h=  str_html(res['event_content'][0][1])
            
    
            i=1
            for de in str_h.split('\n'):
                if des:
                    des+='\r\n'
                te= BeautifulSoup(de).text
                if te:
                    i+=1
                    des += '%s' % te
                if i>3:
                    break
            res['content']=des   
        else:
            res['content']=des
    
    #res['event_url'] = '/%s-%s.html' %(res['ename'], res['event_id'])    ##############
    res['event_url'] = '/event-%s.html' %(res['event_id'])

    #print sys.getsizeof(res)    
    if res['event_begin_time']:
        if datetime.datetime.strptime( res['event_begin_time'], "%Y-%m-%d").date() == datetime.date.today():
            if not res.has_key('rel_time'):
                res['rel_time']=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')
                cache.set('event_%s' % res['event_id'],res,86400*10)
            try:
                if datetime.datetime.strptime( res['rel_time'], "%Y-%m-%d").date() != datetime.date.today():
                    n_event=NewEventTable.objects.get(id=res['id'])
                    n_event.rel_time=datetime.datetime.now()
                    n_event.save()
            except:
                pass

    # cat:business id 69
    fids = wrap_cat_family_id(69, new=new)
    if res['catid'] in fids:
        # business using begin_time
        if res['event_begin_time'] and \
            datetime.datetime.strptime( res['event_begin_time'], "%Y-%m-%d").date() <= datetime.date.today():
                res['time_expire'] = 2
    else:
        # others using end_time
        if res['event_end_time'] and \
            datetime.datetime.strptime( res['event_end_time'], "%Y-%m-%d").date() < datetime.date.today():
                res['time_expire'] = 2
            

    if res.has_key('event_price_model') and res['event_price_model'] in (1,6) and res.has_key('price_unit_info'):
        
        #res['event_price']=''
        price=[]
        for i in range(len(res['price_unit_info'])):
            pt=res['price_unit_info'][i]
            prr=[]
            price_status = 1
            if res.get('time_expire') == 2:
                prr.append(u'过期')
                price_status = 0
                price_status_info = u'过期'
            else:
                if pt['begin_time'] and datetime.datetime.strptime(pt['begin_time'],'%Y-%m-%d %H:%M:%S')>datetime.datetime.now():
                    prr.append(u'待定')
                    price_status = 0
                    price_status_info = u'待定'
                elif pt['end_time'] and datetime.datetime.strptime(pt['end_time'],'%Y-%m-%d %H:%M:%S')<datetime.datetime.now():
                    prr.append(u'过期')
                    price_status = 0
                    price_status_info = u'过期'
                if pt['stock']<=0:
                    prr.append(u'售完')
                    price_status = 0
                    price_status_info = u'售完'
                if pt['status']!=1:
                    prr.append(u'无效')
                    price_status = 0
                    price_status_info = u'无效'

            prr_str=''
            if (len(prr)>0):
                prr_str="(%s)" % '|'.join( prr)
            try:
                pri1=str(pt['price'])
    
                pri2=pri1.split('.')
                if int(pri2[1])==0:
                    pri1=pri2[0]
            except:
                break

            res['price_unit_info'][i]['price'] = float_int_str(pt['price'])
            try:
                res['price_unit_info'][i]['status'] = price_status
                res['price_unit_info'][i]['status_info'] = price_status_info
            except:
                pass

            #res['price_unit_info'][i]['price']=pri1            
            #res['price_unit_info'][i]['price'] = '%s%s' %(pri1,prr_str)
            price.append('%s%s'% (pri1,prr_str) )
            res['event_price']='/'.join(price)
        if not len(price):
            res['event_price_model']=5
    
    if 'event_price_model' in res and res['event_price_model'] not in (1,6):
        res['price_unit_info'] = []
        if res['event_price_model'] == 2:
            res['event_price_model_str'] = u'用户出价'
        elif res['event_price_model'] == 3:
            res['event_price_model_str'] = u'用户出价'
        elif res['event_price_model'] == 4:
            res['event_price_model_str'] = u'免费'
        elif res['event_price_model'] == 5:
            res['event_price_model_str'] = u'收费'
        elif res['event_price_model'] == 7:
            res['event_price_model_str'] = u'待定'


    return res
def city_map_xz(new=False):
    pass

def city_ss(new=False):
    map_city_list = cache.get('ss_city_list')
    #print map_city_list
    if not map_city_list or new:
        #print 'return city'
        map_city_list=[]
        
        sf=SysCommonDistrict.objects.filter(upid=0).order_by('-displayorder','district_id')
        for s in sf:
            city_m={}
            city_m['id']=[]
            city_m['district_name']=s.district_name
            city_m['district_id']=[]
            city_m['title']=s.title            
            city_m['child']=[]
            city_m['own_id']=s.district_id
            city=SysCommonDistrict.objects.filter(upid=s.district_id).order_by('-displayorder','district_id')
            for cit in city:
                try:
                    ci=NewDistrict.objects.get(district_name=cit.district_name)
                    c_m={}
                    c_m['id']=ci.id
                    c_m['district_name']=ci.district_name
                    c_m['district_id']=ci.district_id
                    c_m['title']=ci.title
                    city_m['child'].append(c_m)
                    city_m['id'].append(ci.id)
                    city_m['district_id'].append(ci.district_id)
                except:
                    pass
            map_city_list.append(city_m)
            
        if map_city_list:
            cache.set('ss_city_list' ,map_city_list,86400*10)

            
            
    return map_city_list if map_city_list else []
    
#used to find out the 'zhuanti' template in the related directory
def get_html_file_without_extension(drt):
    return ([ '.'.join(i.split('.')[0:-1]) for i in os.listdir(drt)
            if i.split('.')[-1] in ('html', 'htm')])

#def zhuantiDirectory():
#    return os.path.join(os.path.abspath(os.path.dirname(__file__)),
#                '../new_event/templates/zhuanti')
    
#cat_id,city dict,datetime.date,page,offset,order,new,tag_id
#add tag, modified date, compared to get_event_list in admin_self/common.py
def get_event_list_by_ccdt(cat=False,city=False,date=False,page=False,offset=False,order=False,new=False,tag_id=False):
    '''
    Copy from get_event_list, add date & tag filter
    cat is Eng-Pinyin
    city is a (id,name,title) tuple, name is Chinese, title is Pinyin
    '''
 
    key_name=''
    if not offset:        
        key_name='list_count_num_%s_%s_%s_%s' % (cat,city[2],date,tag_id)        
        key_name = hashlib.md5(key_name).hexdigest()
    else:
        
        key_name='list_events_%s_%s_%s_%s_%s_%s_%s' % (cat,city[2],date,page,offset,order,tag_id)

        key_name = hashlib.md5(key_name).hexdigest()
        
        
    ev_list  = cache.get(key_name)   

    if not ev_list or new:
    #if  new:
        #log.debug('run list_show %s' % datetime.datetime.now) 

        args=NewEventTable.objects.filter( isshow__in=(1,8)).filter(begin_time__gt=datetime.date.today())

        if date:
            this_month = datetime.date(date.year, date.month, 1)
            next_month = datetime.date(date.year, date.month+1, 1) if date.month+1 < 13 else datetime.date(date.year+1, 1, 1)

            args=args.filter(begin_time__lt=next_month, end_time__gte=this_month)

        if cat != '':
            
            cat_id_li=NewCatUrl(0,city[2],new=new)
            tmps=[]
            cat_id=None
            try:
                cat_id=cat_id_li[str(cat)]['id']
            except:
                try:
                    cat_id=cat_id_li[int(cat)]['id']
                except:
                    pass
              
            #log.debug(cat_id)  
            if cat_id:
                #log.debug('%s' % type(cat_id))
                find_cat_ch(NewCatUrl(2,city[2],new=new),cat_id,tmp=tmps)
                
            #log.debug(str(tmps))
            if len(tmps)>0:
                args = args.filter(cat__in=tmps)
            else:
                return []
           
         
        #return render_to_response('base_error.html',{'error_msg':str(cat)})
        
        if city[0]:  
            args =args.filter( city=city[0] )
            #args = args&Q(spot_city=city)
            
           
        if tag_id:
            #tag_id_name = cat_id_li[str(cat)]['tag']
            #tag_id_name_dict = {}
            #for i in tag_id_name:
            #    if i[1]:
            #        tag_id_name_dict[i[1]] = i[0]
            #tag_id = tag_id_name_dict[tag]

            args = args.filter(tag=tag_id)
            #if isinstance(tag_id, int):
            #    args = args.filter(tag=tag_id)
            #elif isinstance(tag_id, (list, tuple)):
            #    args = args.filter(tag__in=tag_id)
            
        #log.debug('%s' % key_name) 
        #log.debug('offset run') 
        #log.debug(key_name) 
        #cou=args.distinct().count()
        #if cou>0:
        if not offset:
            ev_list = args.distinct().count()
            #log.debug('count')
        else:
            #return SysSpotInfo.objects.filter(args).order_by(order)[page:offset]
            try:
                ev_list = [ev.old_event_id for ev in args.order_by('-order',order).distinct()[page:offset]]    
            except:
                ev_list = [ev.old_event_id for ev in args.order_by('-order', 'begin_time').distinct()[page:offset]]    
            #log.debug('list')        
        
        #log.debug(connection.queries) 
        
        
        if not ev_list:
            cache.set(key_name,{'flag':False},60*60)
        else:
            cache.set(key_name,ev_list,60*60)
            
    try:
        if not ev_list['flag']:
            if not offset:
                ev_list=0
            else:
                ev_list=[]
    except:
        pass
            
    return ev_list

def city_without_level1(new=False, cat_filter=False):
    '''
    copy from NewCity
    order by the quantity of events in the cat_filter
    cat_filter is used to filter the cities which doesn't hold any event under the specific categories
    '''
    
    key_name = 'map_city_list_without_level1_%s' %cat_filter
    key_name = hashlib.md5(key_name).hexdigest()
    map_city_list= cache.get(key_name) #城市关系 字典

    if new or not map_city_list: 
        log.debug('run city %s' % datetime.datetime.now) 
        map_city_list=[]
        city_ev_count = {}
        if cat_filter:

            city_id_list = []
            ev = NewEventTable.objects.filter(isshow__in=(1,8),
                                              end_time__gte=datetime.date.today(), 
                                              cat__ename__in=cat_filter)

            for i in ev:
                for cities in i.city.all():
                    city_id_list.append(cities.id)
                    city_ev_count[cities.title] = city_ev_count[cities.title] + 1 \
                            if city_ev_count.has_key(cities.title) else 1

                #city_id_list.extend([j.id for j in i.city.all()])

            city_id_list = list(set(city_id_list))
            district_all = NewDistrict.objects.filter(id__in=city_id_list)
        else:
            district_all = NewDistrict.objects.all()

        #.filter(event_count__gte=4)
        for cityObj in district_all:
            city_m={}
            #filter the 1st level district
            if not cityObj.parent_id:
                continue

            city_m['id']=cityObj.id
            #city_m['fid']=cityObj.parent_id
            #city_m['district_id']=cityObj.district_id
            city_m['district_name']=cityObj.district_name
            city_m['title']=cityObj.title
            if cat_filter:
                city_m['event_count'] = city_ev_count[cityObj.title]
            else:
                city_m['event_count']=cityObj.event_count
            #city_m['child']=[]
            #id_city[cityObj.id]=city_m
            map_city_list.append(city_m)

            #if id_city.has_key(ci['fid']):
            #    if ci['event_count']>4:
            #        id_city[ci['fid']]['child'].append(ci)
            #else:
            #    if ci['event_count']>1000:
            #        map_city.append(id_city[ci['id']])
                
        if map_city_list:
            map_city_list = sorted(map_city_list, key=lambda x: x['event_count'], reverse=True)
            cache.set(key_name,map_city_list,60*60)#城市关系 字典
        
    return map_city_list

def get_event_list_for_cal(cat=False,city=False,date=False,new=False,tag_id=False):

    key_name='list_for_cal_%s_%s_%s_%s' % (cat,city[2],date,tag_id)

    key_name = hashlib.md5(key_name).hexdigest()
        
        
    ev_list  = cache.get(key_name)   

    if not ev_list or new:
    #if  new:
        #log.debug('run list_show %s' % datetime.datetime.now) 

        args=NewEventTable.objects.filter(isshow__in=(1,8))

        if date:
            this_month = datetime.date(date.year, date.month, 1)
            next_month = datetime.date(date.year, date.month+1, 1) if date.month+1 < 13 else datetime.date(date.year+1, 1, 1)

            args=args.filter(begin_time__lt=next_month, begin_time__gte=this_month)

        if cat != '':
            
            cat_id_li=NewCatUrl(0,city[2],new=new)
            tmps=[]
            cat_id=None
            try:
                cat_id=cat_id_li[str(cat)]['id']
            except:
                try:
                    cat_id=cat_id_li[int(cat)]['id']
                except:
                    pass
              
            #log.debug(cat_id)  
            if cat_id:
                #log.debug('%s' % type(cat_id))
                find_cat_ch(NewCatUrl(2,city[2],new=new),cat_id,tmp=tmps)
                
            #log.debug(str(tmps))
            if len(tmps)>0:
                args = args.filter(cat__in=tmps)
            else:
                return []
           
         
        #return render_to_response('base_error.html',{'error_msg':str(cat)})
        
        if city[0]:  
            args =args.filter( city=city[0] )
            
           
        if tag_id:
            args = args.filter(tag=tag_id)
            #if isinstance(tag_id, int):
            #    args = args.filter(tag=tag_id)
            #elif isinstance(tag_id, (list, tuple)):
            #    args = args.filter(tag__in=tag_id)
            
        ev_list = [{'id':i.old_event_id, 'begin_time':i.begin_time, 'name':i.name} for i in args.distinct()]
        
        cache.set(key_name,ev_list,60*60)
            
    return ev_list

def get_tag_seo_info(tag_str,new=False):
    key_name='seo_%s' %tag_str
    key_name = hashlib.md5(key_name.encode('utf-8')).hexdigest()
    seo_dict=cache.get(key_name)
    if not seo_dict or new:
        try:
            seo_dict = {}
            ev=NewEventSeo.objects.get(name=tag_str)
            seo_dict['title']=ev.title
            seo_dict['keywords']=ev.keywords
            seo_dict['description']=ev.description
        except ObjectDoesNotExist:
            seo_dict = 'None'
        cache.set(key_name,seo_dict,3600*24*60)
    return seo_dict

def float_int_str(num):
    '''
    1.00 -> '1'
    1.23 -> '1.23'
    '''
    num = float(num)
    return ('%i' if num.is_integer() else '%s') %num
        
def get_cash_return(price, rate, percent=0.05, interval=50.):
    return round(price / rate * 0.05 / 50) * 50 * rate

def cash_return(price, rate):
    cal_prt = get_cash_return(price, rate)
    cal_prt_str = ('%i' if cal_prt.is_integer() else '%s') %cal_prt
    _tmp = price - cal_prt
    actual_price = ('%i' if _tmp.is_integer() else '%s') %_tmp
    return cal_prt_str, actual_price

def cat_iter(parent_id=None, exclude_id=[], new=False, order='order'):
    '''
    parent_id instance is not in the results
    '''
    if isinstance(exclude_id, int):
        exclude_id =  [exclude_id]
    key_name = 'cat_pid_%s_exid_%s' %(parent_id, exclude_id)
    key_name = hashlib.md5(key_name).hexdigest()
    cats_out = cache.get(key_name)
    if new or not cats_out:
        cats = NewEventCat.objects.filter(parent_id=parent_id).exclude(ename=None).exclude(id__in=exclude_id).order_by(order)
        cats_out = []
        for c in cats:
            cats_out.append({'id': c.id, 
                             'name': c.name, 
                             'ename': c.ename, 
                             'parent_id': c.parent_id, 
                             'children': cat_iter(parent_id=c.id, 
                                                  exclude_id=exclude_id, new=new)
                             })

        #for i, cat in enumerate(cats_out):
        #    cats_out[-1]['children'].extend(
        #            cat_iter(parent_id=cat['id'], exclude_id=exclude_id, new=new))

        cache.set(key_name,cats_out,86400*10)
    return cats_out

def format_cat_iter(cat_list, pre_dash=''):
    '''
    business
    --it
    --medical
    travel
    --...
    '''
    format_cat = []
    for cat in cat_list:
        format_cat.append((cat['id'], pre_dash+cat['name']))
        if cat['children']:
            format_cat.extend(format_cat_iter(cat['children'], pre_dash+'--'))

    return format_cat

def family_ids(list_dict):
    '''
    format like:
    [
     {'id':1,
      'children': [{'id':11,
                    'children':[]
                  }]
     }, 
     {'id':2,
      'children': []
     },
    ]
    family_ids(above_list) --> [1,11,2]
    '''
    if list_dict:
        ids = []
        for dic in list_dict:
            ids.append(dic['id'])
            ids.extend(family_ids(dic['children']))
        return ids
    else:
        return []

def wrap_cat_family_id(cat_id, exclude_id=[], new=False):
    key_name = 'wrap_cat_family_id_%s_ex_%s' %(cat_id, exclude_id)
    key_name = hashlib.md5(key_name).hexdigest()
    fids = cache.get(key_name)
    if new or not fids:
        cats = cat_iter(cat_id, exclude_id=exclude_id)
        fids = family_ids(cats) + [cat_id]
        cache.set(key_name, fids, 86400)
    return fids

def sendMailAsync(sub,text,html,to_list=['252925359@qq.com', '241617467@qq.com','1010478998@qq.com','9682539@qq.com','276753659@qq.com'], cc_list=[]):

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
            log.debug('Email Error: %s' %e)

    return False
