#coding:utf-8
#from mptt.models import MPTTModel

from new_event.models import NewDistrict,NewEventCat,NewEventTag,NewEventSeo,NewVenue,NewVenueClass,NewSysEventTag,\
                                OldEvent,NewDistrict_s,NewEventTable,NewEventParagraphTag,NewEventParagraph,AdminEventTheme,\
                                NewEventTag
from dahuodong.models import SysEventCat,SysCommonDistrict,PubEventCat,SysVenue
from django.http import HttpResponse
from django.utils import simplejson as json
from admin_self.common import oldEventToNewEvent,NewEventToOldEvent
import time,datetime
from django.db.models import Q
from django.core.cache import cache
import re
def test_save(i=0):
    p=oldEventToNewEvent(240356)
    print NewEventToOldEvent(p.id)

def update_app_event_rank():
    event=OldEvent.objects.filter(event_rank__gt=0).exclude(event_time_expire=2)
    for old_event in event:
        p=oldEventToNewEvent(old_event.event_id,False)
        if p:
            print p.id,p.old_event_id
        
        else:
            print old_event.event_id
def find_newevent_update():
    for ev in NewEventTable.objects.filter(Q(end_time__gt=datetime.date.today())|Q(end_time=None)):
        #time.sleep( 0.1 )
        p=oldEventToNewEvent(ev.old_event_id,False)
        

            
            
        if not p:            
            print 'err %s' % ev.id
        else:
            if not p.cat.all().count():
                print 'cat err %s' % p.id
                
            if not p.city.all().count():
                print 'city err %s' % p.id
                
 
        
        

def test_txt():
    i=0
    for event in NewEventTable.objects.all():
        if not event.paragraph.all().count():
            i+=1
            if event.old_event:
                p=oldEventToNewEvent(event.old_event.event_id,False)
                print p.name,p.id,p.old_event_id
                if p.paragraph.all().count():
                    print 'OK'
                else:
                    print 'err'
    print i
    

def update_cat():    
    for cat in SysEventCat.objects.all():
        seo_arr=cat.cat_seo.split('[|]')
        if seo_arr[0]:
            tit=seo_arr[0].replace(u'大活动网',u'活动家')
        else:
            tit=''
        if seo_arr[1]:
            key=seo_arr[1].replace(u'大活动网',u'活动家')
        else:
            key=''
        if seo_arr[2]:
            des=seo_arr[2].replace(u'大活动网',u'活动家')
        else:
            des='' 
            
            
            
            
        
        try:
            new_cat=NewEventCat.objects.get(cat_id=cat.cat_id)
            
            if tit:
                if new_cat.seo:
                    new_cat.seo.title=tit
                    new_cat.seo.keywords=key
                    new_cat.seo.description=des
                    new_cat.seo.save()
                else:
                    new_cat.seo=NewEventSeo.objects.create(
                           name=new_cat.name+u'_seo',
                           title=tit,
                           keywords=key,
                           description=des,
                           )
                    new_cat.save()
            
            for e in cat.cat_tag.split(','):
               
                if e:
                    try:
                        pe=NewEventTag.objects.create(name=e)
                        new_cat.tag.add(pe)  
                        print e
                    except:
                        pass
                
        except:
            pass
        
       
    
    pass
def k_tag():
    tag=(3526,5018,6565)
    for ne in NewEventParagraph.objects.filter(cat_name_id__in=tag):
        ne.cat_name.delete()
        ne.delete()

    

def del_tag():
    #t_ip=cache.get(ip)
    #cache.set(ip,(n+1,t_ip[1] ),x)
    
    tag_n={}
    for t in NewEventParagraphTag.objects.all():
        if not tag_n.has_key(t.name):
            tag_n[t.name]=t
        else:
            par=NewEventParagraph.objects.get(cat_name=t) 
            par.cat_name=tag_n[t.name]
            par.save()
    for t in NewEventParagraphTag.objects.all():
        #k=t.neweventparagraph_set.all().count()
        if not t.Paragraph_tag.all().count():
            t.delete()
        else: 
            print t.name
            print t.id
      
     
def test_event():
    ev=OldEvent.objects.get(event_id=224332)
    nev=NewEventTable.objects.get(id=121)
    print ev.event_name
    print type(ev.event_name)
    print nev.name
    print type(nev.name)
    
def find_city_OldToNewEvent():
  
    dis=NewDistrict_s.objects.all()

    for citys in dis:
        num=0
        ev=OldEvent.objects.filter(event_isshow__in=(1,8))
        ev=ev.filter(Q(event_end_time__gt= int(time.time()))|Q(event_islongtime=1) )
         
        for e in ev.filter(district_id=citys.district_id):
            p=oldEventToNewEvent(e.event_id)
            if not p:
                print "%s err" % e.event_id
            else:                
                num+=1
        print '%s %s' % (citys.district_name,num)
  

def OldToNewEvent():
    ev=OldEvent.objects.filter(event_isshow__in=(1,3,5,8))
    ev=ev.filter(event_end_time__gt= int(time.time()) )
    for e in ev:
        p=oldEventToNewEvent(e.event_id)
        if not p:
            print "%s err" % e.event_id
        #else:
            #print p.name
     

def display(foods):
    display_list = []
 
    for food in foods:
        display_list.append(food.title)
 
        children = food.children.all()
        if len(children) > 0:
            display_list.append(display(food.children.all()))
         
    return display_list
   
def find_city_addr():
    dis=NewDistrict.objects.all()
    for citys in dis:
        ve=SysVenue.objects.filter(district_id=citys.district_id)
        for v in ve:
            #time.sleep( 0.5 )
            try:
                p=NewVenue.objects.get(venue_id=v.venue_id) 
                #p=NewVenue.objects.get(venue_id=v.venue_id) 
          
                p.longitude_baidu=v.venue_longitude_baidu
                p.latitude_baidu=v.venue_latitude_baidu
                p.longitude_google=v.venue_longitude_google
                p.latitude_google=v.venue_latitude_google
                                        
                                       
                p.address=v.venue_address #re.sub(ur"[^\u4e00-\u9fa5\w]", " ", v.venue_address) 
                p.title=v.venue_title #re.sub(ur"[^\u4e00-\u9fa5\w]", " ", v.venue_title) 
                p.alias=v.venue_alias
                
                
            except:
                p=NewVenue.objects.create(
                                   venue_id=v.venue_id,
                                   longitude_baidu=v.venue_longitude_baidu, 
                                   latitude_baidu=v.venue_latitude_baidu, 
                                   longitude_google=v.venue_longitude_google,
                                   latitude_google=v.venue_latitude_google,                                            
                                   address=v.venue_address,#re.sub(ur"[^\u4e00-\u9fa5\w]", " ", v.venue_address) ,
                                   title=v.venue_title,#re.sub(ur"[^\u4e00-\u9fa5\w]", " ", v.venue_title) ,
                                   alias=v.venue_alias,
                                   
                                   
                                   )
                print 'new %s' % (v.venue_id)
                
                 
 
            try:
                vc=NewVenueClass.objects.create(
                                             name=v.venue_class
                                             )
            except:
                try:
                    vc=NewVenueClass.objects.get(name=v.venue_class) 
                except:
                    vc=False
            p.city=citys
            if vc:
                p.venue_class=vc
            try:
                p.save()
            except Exception,e:
                print e
                #p.address= re.sub(ur"[^\u4e00-\u9fa5\w]", " ", v.venue_address) 
                #p.save()
                       
            '''
            try:
                print p.title
            except:
                print p.venue_id
            ''' 
        
    
def find_city(cid=0,obj=None):
    
     
    dis=SysCommonDistrict.objects.filter(upid=cid)
    #dis=dis.exclude(title='')
    if dis.count()>0:
        for city in  dis:
            if city.capital_letter:
                try:
                    if obj:
                        p=NewDistrict.objects.create(
                                                   district_id=city.district_id,
                                                   district_name=city.district_name,
                                                   title=city.title,
                                                   parent=obj,
                                                   usetype=city.usetype,
                                                   capital_letter=city.capital_letter,
                                                   baidu_code=city.baidu_code,
                                                   displayorder=city.displayorder,
                                                   recomendindex=city.recomendindex
                                                   )
                        find_city(city.district_id,p) 
                    else:
                        p=NewDistrict.objects.create(
                                                   district_id=city.district_id,
                                                   district_name=city.district_name,
                                                   title=city.title,
                                                   usetype=city.usetype,
                                                   capital_letter=city.capital_letter,
                                                   baidu_code=city.baidu_code,
                                                   displayorder=city.displayorder,
                                                   recomendindex=city.recomendindex
                                                   )  
                        find_city(city.district_id,p)   
                except:
                    print city.district_id
                    try:
                        p=NewDistrict.objects.get(district_id=city.district_id) 
                        find_city(city.district_id,p) 
                    except:
                        pass
            else:
                find_city(city.district_id,None) 
                 
                
            
         
        
    return 
def tag_x():
    print NewEventTag.objects.all().distinct('name').count()
    print NewEventTag.objects.all().count()
def save_new_cat(cid=0,obj=None):
    dis=PubEventCat.objects.filter(cat_fid=cid)
    if dis.count()>0:
        for cat in dis:
            try:
                p=NewEventCat.objects.get(cat_id=cat.cat_id_map)
                p.ename=cat.cat_ename
                p.name=cat.cat_name
                p.cat_id=cat.cat_id_map
                if obj:
                    p.parent=obj
                     
                p.save()
                
                    
                print p.name
            except:  
                try:
                    p=NewEventCat.objects.get(name=cat.cat_name) 
                    p.ename=cat.cat_ename 
                    p.cat_id=cat.cat_id_map 
                    if obj:
                        p.parent=obj
                    p.save()         
                    
                except:
                    try:
                        p=NewEventCat.objects.create(
                                       cat_id=cat.cat_id_map,
                                       name=cat.cat_name,
                                       ename=cat.cat_ename,
                                       #parent=obj,
                                       #seo=cat.cat_seo,
                                       #order=cat.cat_order,
                                       )
                    except:
                        print '----'
                        print cat.cat_id_map
                        print '----'
                    
                
                
                if obj and p:
                    
                    p.parent=obj
                    try:
                        p.save()
                    except:
                        print p.name
   
            ''' 
            if obj and p:
                p.move_to(obj, position='first-child')
                #p.parent=obj
                #p.save()
            if cat.cat_son_id1:
                 
                p_arr=NewEventCat.objects.filter(cat_id__in=cat.cat_son_id1.split(','))
                for ps in p_arr:
                    #ps.parent=p
                    ps.move_to(p, position='first-child')
                    #ps.save()
            if cat.cat_son_id2:
                 
                p_arr=NewEventCat.objects.filter(cat_id__in=cat.cat_son_id2.split(','))
                for ps in p_arr:
                    #ps.parent=p
                    #ps.save
                    ps.move_to(p, position='first-child')
            
            '''
            if p:
                save_new_cat(cat.cat_id,p)
             
    return

def save_cat_event_fid_tag():
    dis=NewEventCat.objects.all()
    for cat in dis:
        for new_tag in NewSysEventTag.objects.filter(cat1_id=cat.cat_id):
            #if not NewEventTag.objects.exclude(id=new_tag.tag_id).filter(name=new_tag.tag_name):
            try:
                tagss=NewEventTag.objects.create(name=new_tag.tag_name)
            except:
                try:
                    tagss=NewEventTag.objects.get(name=new_tag.tag_name)
                except:
                    print new_tag.tag_name
            
                
                
            if tagss:
                try:
                    cat.tag.add(tagss)
                    
                except:
                    print new_tag.tag_name
    
    #NewSysEventTag
   

#删除重复标签
def save_cat_tag():
    dis=NewEventCat.objects.all()
    for cat in dis:
        #b.authors.remove(a) 或者 b.authors.filter(id=1).delete()
        for tags in cat.tag.all():
             
            if NewEventTag.objects.exclude(id=tags.id).filter(name=tags.name).count()>0:
                cat.tag.remove(tags)
                NewEventTag.objects.filter(id=tags.id).delete()
                 
             
             


def find_cat(cid=0,obj=None):
    
     
    dis=SysEventCat.objects.filter(cat_fid=cid)
    #dis=dis.exclude(title='')
    if dis.count()>0:
        for cat in  dis:
            
            try:
                if obj:
                    p=NewEventCat.objects.create(
                                               cat_id=cat.cat_id,
                                               name=cat.cat_name,
                                               ename=cat.cat_ename,
                                               parent=obj,
                                               #seo=cat.cat_seo,
                                               order=cat.cat_order,
                                                
                                               )
                    seo_arr=cat.cat_seo.split('[|]')
                    if seo_arr[0]:
                        tit=seo_arr[0]
                    else:
                        tit=''
                    if seo_arr[1]:
                        key=seo_arr[1]
                    else:
                        key=''
                    if seo_arr[2]:
                        des=seo_arr[2]
                    else:
                        des=''
                    try:
                        seo=NewEventSeo.objects.create(
                                                   name=p.name+u'_seo',
                                                   title=tit,
                                                   keywords=key,
                                                   description=des,
                                                   )
                        p.seo=seo
                        p.save()
                    except:
                        pass
                    
                    for e in cat.cat_tag.split(','):
                        print '>>'+e
                        if e:
                            try:
                                pe=NewEventTag.objects.create(name=e)
                                p.tag.add(pe)   
                            except:
                                pass
                     
                    find_cat(cat.cat_id,p) 
                else:
                    p=NewEventCat.objects.create(
                                               cat_id=cat.cat_id,
                                               name=cat.cat_name,
                                               ename=cat.cat_ename,
                                               #parent=obj,
                                               #seo=cat.cat_seo,
                                               order=cat.cat_order,
                                               )
                    seo_arr=cat.cat_seo.split('[|]')
                    if seo_arr[0]:
                        tit=seo_arr[0]
                    else:
                        tit=''
                    if seo_arr[1]:
                        key=seo_arr[1]
                    else:
                        key=''
                    if seo_arr[2]:
                        des=seo_arr[2]
                    else:
                        des=''
                    try:
   
                        seo=NewEventSeo.objects.create(
                                                   name=p.name+u'_seo',
                                                   title=tit,
                                                   keywords=key,
                                                   description=des,
                                                   )
                        p.seo=seo
                        p.save()
                    except:
                        pass
                    for e in cat.cat_tag.split(','):
                        print '>>'+e
                        if e:
                            try:
                                pe=NewEventTag.objects.create(name=e)
                                p.tag.add(pe)  
                            except:
                                pass                     
                    find_cat(cat.cat_id,p)   
            except:
                print cat.cat_tag
                try:
                    p=NewEventCat.objects.get(cat_id=cat.cat_id) 
                    
                    
                    
                    seo_arr=cat.cat_seo.split('[|]')
                    if seo_arr[0]:
                        tit=seo_arr[0]
                    else:
                        tit=''
                    if seo_arr[1]:
                        key=seo_arr[1]
                    else:
                        key=''
                    if seo_arr[2]:
                        des=seo_arr[2]
                    else:
                        des=''
                    try:
                        seo=NewEventSeo.objects.get(name=p.name+u'_seo')
                        seo.title=tit 
                        seo.keywords=key 
                        seo.description=des
                        seo.save()
                    except: 
                        seo=NewEventSeo.objects.create(
                                                   name=p.name+u'_seo',
                                                   title=tit,
                                                   keywords=key,
                                                   description=des,
                                                   )
                        p.seo=seo
                        p.save()
            
                    
                    
                    for e in cat.cat_tag.split(','):
                        print '>>'+e
                        if e:
                            try:
                                pe=NewEventTag.objects.create(name=e)
                                p.tag.add(pe)  
                            except:
                                pass
                    
                    
                    find_cat(cat.cat_id,p) 
                except:
                    pass

                 
                
            
         
        
    return 

def District_data(request):
    
    
    p={}
    '''
    rock = NewDistrict.objects.create(name="Rock")
    blues = NewDistrict.objects.create(name="Blues")
    NewDistrict.objects.create(name="Hard Rock", parent=rock)
    NewDistrict.objects.create(name="Pop Rock", parent=rock)
    '''
    find_city(0,None)
    '''
    obj=False  
    dis=NewCommonDistrict.objects.filter(upid=0)
    for city in dis:
        #NewDistrict.objects.create(name="Rock")
        if obj:
            NewDistrict.objects.create(
                                       district_id=city.district_id,
                                       district_name=city.district_name,
                                       title=city.title,
                                       parent=obj,
                                       usetype=city.usetype,
                                       capital_letter=city.capital_letter,
                                       baidu_code=city.baidu_code,
                                       displayorder=city.displayorder,
                                       recomendindex=city.recomendindex
                                       )
        else:
            NewDistrict.objects.create(
                                       district_id=city.district_id,
                                       district_name=city.district_name,
                                       title=city.title,
                                       usetype=city.usetype,
                                       capital_letter=city.capital_letter,
                                       baidu_code=city.baidu_code,
                                       displayorder=city.displayorder,
                                       recomendindex=city.recomendindex
                                       )       
        
         
            
    '''
    for node in NewDistrict.objects.all():
        p[node.district_id]=node.district_name
    
    
    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")

