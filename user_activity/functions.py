#coding:utf-8
import datetime,time
from user_activity.models import UserEventMessage,UserInfo,UserInfoEvent
from spot.models import SysSpotEvent,SysSpotTxt
from django.core.cache import cache
from User.models import Customer
from LifeApi.functions import getevent
from LifeApi.common import getPageAndOffset



#from django.db import connection


def ip_Filter(request,num=10,userID=False):
    
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR'] 
        
    re=False
    if ip:
        if userID:
            ip='%s:%s' % (ip,userID )  
               
        t_ip=cache.get(ip)
        times=60*5
        
        
        
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
            
    if not re :
        cache.set(ip,(11,nows),times)
        
            
 
            
    #return {'code':n,'message':re}
        #cache.set('cat_spot_list',x_cat,60*5)
        #x_cat=cache.get('cat_spot_list')     
    
    
    
    return re



def admin_black_message(messageid=0,question=None,date=None,userid=0,username=None,userfrom=None,ex=False):
    if not question:
        return {'code':-1,'message':'无留言信息'}
    if not userid:
        return {'code':-2,'message':'用户id不正确'}
     
    try:
        date = time.strptime(date,"%Y-%m-%d %H:%M:%S")
        date=datetime.datetime(* date[:6])
    except:
        date = time.localtime(int(date))
         
        date=datetime.datetime(* date[:6])
    else:
        return {'code':-3,'message':'留言时间不正确'}     
        
    
    try:
        e=UserEventMessage.objects.get(id=int(messageid))
    except :
        return {'code':-4,'message':'回复留言id不正确'}
 
    try:
        u=UserInfo.objects.get(user_id=int(userid))
        u.user_cumulative = u.user_cumulative+1
        #u.event.add(e.event)
        u.save()
    
    except:
        if not username:
            username='app用户'
        if not userfrom:
            userfrom='app'
            
        u = UserInfo(user_name=username,
                      user_id=int(userid),
                      user_cumulative=1,
                      user_from=userfrom,
                       
                     )
        #u.event.add(e.event)
        u.save()
        
    
    #u=UserInfo.objects.get(user_id=int(userid))
    tx=SysSpotTxt(
                   
                   txt=question,
                   tag=username,
                   )
    tx.save()

      
    b=UserEventMessage(
                       #event=e.event,
                       message=tx,
                       user=u,
                       rel_time=date, 
                       #black_message=e,     
                       examine=ex,
                       
                              
                       
                       )
    b.save()
    
    
    #e=find_children(e.id)
    
    b.path='%s:%s' % (e.path,b.path )
    b.save()
    
    e.examine=ex
    e.black_message=b
    e.save()
    arr={'code':1,'message':'保存成功'}
    
    
     
    return arr
 
    return {'code':0,'message':'错误请求'}



def black_message(messageid=0,question=None,date=None,userid=0,username=None,userfrom=None):
    if not question:
        return {'code':-1,'message':'无留言信息'}
    if not userid:
        return {'code':-2,'message':'用户id不正确'}
     
    try:
        date = time.strptime(date,"%Y-%m-%d %H:%M:%S")
        date=datetime.datetime(* date[:6])
    except:
        date = time.localtime(int(date))
         
        date=datetime.datetime(* date[:6])
    else:
        return {'code':-3,'message':'留言时间不正确'}     
        
    
    try:
        e=UserEventMessage.objects.get(id=int(messageid))
    except :
        return {'code':-4,'message':'回复留言id不正确'}
 
    try:
        u=UserInfo.objects.get(user_id=int(userid))
        u.user_cumulative = u.user_cumulative+1
        u.event.add(e)
        u.save()
    
    except:
        if not username:
            username='app用户'
        if not userfrom:
            userfrom='app'
            
        u = UserInfo(user_name=username,
                      user_id=int(userid),
                      user_cumulative=1,
                      user_from=userfrom,
                       
                     )
        #u.event.add(e)
        u.save()
        
    
    #u=UserInfo.objects.get(user_id=int(userid))
    tx=SysSpotTxt(
                   
                   txt=question,
                   tag=username,
                   )
    tx.save()

    try:    
        b=UserEventMessage(
                           event=e.event,
                           message=tx,
                           user=u,
                           rel_time=date, 
                           black_message=e             
                           
                           )
        b.save()
        
        arr={'code':1,'message':'保存成功'}
        
        
         
        return arr
    except:
        return {'code':-3,'message':'错误信息'}  
        
    return {'code':0,'message':'错误请求'}
def save_message(eventid=0,question=None,date=None,userid=0,username=None,userfrom=None):

 
    if not question:
        return {'code':-1,'message':'无留言信息'}
    if not userid:
        return {'code':-2,'message':'用户id不正确'}
     
    try:
        date = time.strptime(date,"%Y-%m-%d %H:%M:%S")
        date=datetime.datetime(* date[:6])
    except:
        #date = time.localtime(int(date))
         
        date=datetime.datetime.now()
    else:
        return {'code':-3,'message':'留言时间不正确'}     
        
    
    try:
        e=SysSpotEvent.objects.get(event_id=int(eventid))
    except :
        return {'code':-4,'message':'活动id不正确'}
    
    if not username:
        username='app用户'
    if not userfrom:
        userfrom='app'
        
    try:
        user=Customer.objects.get(id=int(userid))
    except:
        return {'code':-5,'message':'无此用户'}
 
    try:
        
        u=UserInfo.objects.get(user_id=user.id)
        u.user_cumulative = u.user_cumulative+1
        u.user_name=username
        u.user_from=userfrom
        u.save()
        u.event.add(e)
    
    except:

            
        u = UserInfo(user_name=username,
                      user_id=user.id,
                      user_cumulative=1,
                      user_from=userfrom,
                      #event=e
                     )
        
        
        u.save()
        u.event.add(e)
    
    #u=UserInfo.objects.get(user_id=int(userid))
     
    tx=SysSpotTxt(
                   
                   txt=question,
                   tag='%s %s' %(username,userfrom),
                   )
    tx.save()

    
    b=UserEventMessage(
                       event=e,
                       message=tx,
                       user=u,
                       rel_time=date,              
                       
                       )
    b.save()
    #b.path=b.id
    #b.save
    
    arr={'code':1,'message':'保存成功'}
    
    event={}
    
    event['id']=b.id
    event['event']={'event_id':b.event.event_id,'event_name':b.event.event_name}
    event['data']=[]
    
     
    msg={}
    msg['id']=b.id
    msg['question']=b.message.txt
    msg['date']=int(time.mktime(b.rel_time.timetuple()))#datetime.datetime.strftime(b.rel_time,'%Y-%m-%d %H:%M:%S')
    msg['user']=b.user.user_name
    event['data'].append(msg)
    arr['list']=[];
    arr['list'].append(event)
     
    return arr
   
            

        
        
    return {'code':0,'message':'错误请求'}

def find_children(m_id=0):
    
    try:
        e=UserEventMessage.objects.get(id=int(m_id))
        try:
            return find_children(e.black_message.id)
        except:
            return e
    except :
        return False
    
    return False

def find_user_message(userid,offset=5,page=1):
    try:    
        u=UserInfo.objects.get(user_id=int(userid))
        arr={'code':1,'message':'查询成功'}
        arr['list']=[];
        pag1=(page-1)*offset;
        if not pag1:
            pag1=0
        
        for bm in u.event.all()[pag1:offset]:
            event={}
            event['event']= {'id':bm.event_id,'title':bm.event_name}
            event['data']= []
            
            for b in u.usereventmessage_set.filter(event=bm).order_by('-rel_time')[:15]:
              
                msg={}
                msg['id']=b.id
                msg['question']=b.message.txt
                msg['date']=int(time.mktime(b.rel_time.timetuple()))#datetime.datetime.strftime(b.rel_time,'%Y-%m-%d %H:%M:%S')
                user=Customer.objects.get(id=b.user.user_id)
                #msg['user']={'name':b.user.user_name,'id':b.user.user_id}        
                msg['user']={'name':user.name,'id':user.id,'headphoto':user.headphoto_path}    
                if b.black_message:
                    an=b.black_message
                    msg['an_id']=an.id
                    msg['answer']=an.message.txt
                    msg['an_date']=int(time.mktime(an.rel_time.timetuple()))#datetime.datetime.strftime(an.rel_time,'%Y-%m-%d %H:%M:%S')
                    msg['an_user']={'name':an.user.user_name,'id':an.user.user_id}
                event['data'].append(msg)   
        
            
        
        
            arr['list'].append(event)
        return arr
    
    except :
        return {'code':-4,'message':'活动id不正确'}
    
    return {'code':-3,'message':'错误信息'}

def find_user_collect(request,userid):
    if not userid:
        return {'code':-1,'message':'没有用户id'}
    try: 
        
        
        #u=UserInfo.objects.get(user_id=int(userid))
        arr={'code':1,'message':'查询成功'}
        #arr['list']=[];
        cds = request.GET
        (page,offset) = getPageAndOffset(cds)
        #event_id_u=[]
        arr['list']=[]
        for bm in UserInfoEvent.objects.filter(userinfo_id=userid).order_by('-id')[offset*(page-1):offset*page]:
            #event_id_u.append(bm.sysspotevent_id)
            try:
                arr['list'].append(getevent(bm.sysspotevent_id))
            except:
                pass
            #arr['list']=[eventDic(item) for item in NewEventTable.objects.get(old_event_id=bm.sysspotevent_id)[offset*(page-1):offset*page]]
        
        return arr
    except:
        return {'code':1,'message':'无数据'}
        

def find_user_time_message(userid=0,times=None):
 
    try:
        u=UserInfo.objects.get(user_id=int(userid))
        arr={'code':1,'message':'查询成功'}
        arr['list']=[];
        
        arr['begin']=int(times)
        
        
        event_id_u=[]
        for bm in u.event.all():
            event_id_u.append(bm.event_id)
         
        msg=UserEventMessage.objects.filter(user=int(userid))
        msg=msg.filter(event__in=event_id_u).order_by('-end_time')
        if times:
            dates = time.localtime(int(times))
            dat =datetime.datetime(*dates[:6]) 
            msg=msg.filter(end_time__gt=dat)
            #arr['tim']=times
        
        
        
        #.order_by('-end_time')
        
        event_id_t={}
        event_x=[]
        
        for bm in msg:
            ti=int(time.mktime(bm.end_time.timetuple()))
            if arr['begin']<ti:
                arr['begin']=ti
            msg={}
            user=Customer.objects.get(id=bm.user.user_id)
            
            msg['id']=bm.id
            msg['question']=bm.message.txt
            msg['date']=int(time.mktime(bm.end_time.timetuple()))#datetime.datetime.strftime(b.rel_time,'%Y-%m-%d %H:%M:%S')
            msg['user']={'name':user.name,'id':user.id,'headphoto':user.headphoto_path}        
           
            if bm.black_message:
                an=bm.black_message
                msg['an_id']=an.id
                msg['answer']=an.message.txt
                msg['an_date']=int(time.mktime(an.rel_time.timetuple()))#datetime.datetime.strftime(an.rel_time,'%Y-%m-%d %H:%M:%S')
                msg['an_user']={'name':an.user.user_name,'id':an.user.user_id}
            #event['data'].append(msg)   
            
            
            if not event_id_t.has_key(bm.event.event_id):
                event_id_t[bm.event.event_id]=[]
                event={}
                event['event']= {'id':bm.event.event_id,'title':bm.event.event_name}
                event['data']= event_id_t[bm.event.event_id]
                #event['data'].append(event_id_t[bm.event.event_id])
                event_x.append(event)
                
            event_id_t[bm.event.event_id].append(msg)
    
        for ev in event_x:
        
            arr['list'].append(ev)
            
            
        return arr
    except:
        return {'code':-4,'message':'错误信息'}
    return {'code':-3,'message':'错误信息'}

'''
def msg_black(objects):
    
    return False
    

def find_event_user_message(userid,eventid,offset=5,page=1):
    
'''   

def find_event_message(eventid,offset=5,page=1):
    
    #.sysspotinfo_set.all()
    try:
        e=SysSpotEvent.objects.get(event_id=int(eventid))
        #m=e.usereventmessage_set.all()
        arr={'code':1,'message':'查询成功'}
        
        #event={}
        
        #arr['id']=b.id
        arr['event']={'event_id':e.event_id,'event_name':e.event_name}
        arr['list']=[]
        pag1=(page-1)*offset;
        if not pag1:
            pag1=0
        for b in e.usereventmessage_set.filter(examine=True).order_by('-rel_time')[pag1:offset]: 
            msg={}
            msg['id']=b.id
            msg['question']=b.message.txt
            msg['date']=int(time.mktime(b.rel_time.timetuple()))#datetime.datetime.strftime(b.rel_time,'%Y-%m-%d %H:%M:%S')
            msg['user']={'name':b.user.user_name,'id':b.user.user_id}    
            user=Customer.objects.get(id=b.user.user_id)
                #msg['user']={'name':b.user.user_name,'id':b.user.user_id}        
            msg['user']={'name':user.name,'id':user.id,'headphoto':user.headphoto_path}      
            
            if b.black_message:
                an=b.black_message
                msg['an_id']=an.id
                msg['answer']=an.message.txt
                msg['an_date']=int(time.mktime(an.rel_time.timetuple()))#datetime.datetime.strftime(an.rel_time,'%Y-%m-%d %H:%M:%S')
                msg['an_user']={'name':an.user.user_name,'id':an.user.user_id} 
            arr['list'].append(msg)
                
 
        
        return arr
        
        
    except :
        return {'code':-4,'message':'活动id不正确'}
    
    return {'code':-3,'message':'错误信息'}
