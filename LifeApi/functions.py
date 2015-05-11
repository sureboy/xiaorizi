#coding:utf-8
import re,time,datetime
from LifeApi.models import NewEventCat,NewDistrict,NewArticle,NewEventImg
from LifeApi.version_farmt import version_dis_for_App
from LifeApi.common import NewAppEvent,event_city_cat,replaceCharEntity,feelnum,find_img
from user_activity.models import UserEventMessage
from BeautifulSoup import BeautifulSoup
from django.db import connection
from django.db.models import Q
from sgmllib import SGMLParser

def str_html(str=None):
    str = str.replace(' ','').replace('\r','').replace('\n','').replace('<p>','').replace('</p>','\r\n').replace('<br>','\r\n')\
                .replace('<br/>','\r\n').replace('<br />','\r\n').replace('\r\n\r\n','\r\n')
    str = replaceCharEntity(str)   
    return str
    
def dic2text(dic):
    res = ''
    for key,value in dic.items():
        if key == 'csrfmiddlewaretoken':
            continue
        res += key+':'+value+'\n'   
    return res.encode('utf-8')
    
def getevent(id=None,new=False,ver=''):
    ev= version_dis_for_App()
    return ev.output(id ,new ,ver)
    if not id:
        return {}
    
    event={}
    ca=NewAppEvent(None,id,new)
    #print ca
    event['id']=ca['event_id']
    event['isurl']=True if ca['isshow']==8 else False
    event['title']=ca['title']
    event['imgs']=ca['img_s']
    event['cat']={'name':ca['cat_name'] if ca['cat_name'] else '',
                  'id':ca['catid'] if ca['catid'] else '',
                  'img':ca['cat_img']['img']  if ca['cat_img'] else ''
                  }
    
    #event['cat_name']=ca['cat_name'] if ca['cat_name'] else ''
    #event['catid']=ca['catid'] if ca['catid'] else ''
    #event['cat_img']=ca['cat_img'] if ca['cat_img'] else ''
    
    if ca.has_key('feeltitle'):
        event['feeltitle']=ca['feeltitle'] if ca['feeltitle'] else ''
    else:
        event['feeltitle']=''
    event['mobileURL']='http://m.huodongjia.com/app-%s.html'%ca['event_id']
    event['questionURL']='http://m.huodongjia.com/q-%s.html'%ca['event_id']
    event['shareURL']='http://m.huodongjia.com/share-%s.html'%ca['event_id']
    #des1 = ''.join(BeautifulSoup(ca['des']).findAll(text=True))
    #des1 = ''.join(replaceCharEntity(des1))    

    
    event['tag']=','.join(ca['event_tag'])
    event['price']=ca['app_price']
    
    event['feel']=ca['feel']
    event['feelnum']=ca['feelnum'] if ca['feelnum'] else 0
    event['address']=ca['event_address']
    event['position']=ca['position']
    event['startdate']=ca['startdate']
    event['enddate']=ca['enddate']
    event['islongtime']=ca['event_islongtime']
    event['city']=ca['district_name']
    event['city_id']=ca['district_id']
    event['detail']=''
    try:
        event['detail']=ca['detail']  
    except:
        pass
    if not event['detail']:        
        event['detail']=ca['des']
        
    if not event['detail']:         
        i=1            
        str_h=  str_html(ca['event_content'][0][1]) 
        
        for de in str_h.split('\n'):
            if event['detail']:
                event['detail']+='\r\n'
            
            te= BeautifulSoup(de).text
            if te and len(te)>15:            
                i+=1
    
                event['detail'] += '%s' % te
            if i>3:
                break
    
        event['detail']=event['detail'].replace('\r\n\r\n','\r\n')\
                .replace('\n\n\n\n','\r\n').replace('\n\n\n','\r\n').replace('\n\n','\r\n')
    #event['detail']= BeautifulSoup(ca['event_content'][0][1]).text[0:250]
  
    

    for con in ca['event_content']:
        if con[0] in [u'购买须知']:
            event['note']=con[1]
            break

    try:
        event['note']=str_html(event['note']).replace('\r\n','')
        event['note']=BeautifulSoup(event['note']).text
        o=event['note'].find(u'。')
        if o>0:
            event['note']=event['note'][:o]
        else:
            no=event['note'].split(u'，')
            if len(no)>2:
                event['note']='%s%s' % (u'，'.join(no[:2]),'...')
    except:
        event['note']=''    
        
    event['comment']={}
    try:        
        com=UserEventMessage.objects.filter(event_id=ca['event_id']).order_by('id')[0]
        event['comment']['id']=com.id
        event['comment']['content']=com.message.txt
        event['comment']['date']=time.mktime(com.end_time.timetuple())
        
        event['comment']['score']=0
        event['comment']['imgs']=[]
        event['comment']['user']={'id':com.user.user_id,'name':com.user.user_name}

    except:
        pass
    event['commentTotol']={}
    
    event['more']=[]
    for ev in event_city_cat(ca['district_id'],None,new):
        if ev!=event['id']:
            
            e=NewAppEvent(None,ev)
            even={'id':e['event_id'],'title':e['title'],'price':e['app_price'],'imgs':e['img_s']}
            event['more'].append(even)
            
        if len(event['more'])>4:
            break
    
    return event


def FindEvent(catid=None,cityid=None,peoples=None,price_type=None,money_mins=None,money_maxs=None,random=None,page=1,offset=10,ver=None,isshow=None,new=None):
    ev=feelnum.objects.filter(Q(event__end_time__gt=datetime.date.today())|Q(event__end_time=None))
    if not isshow:
        ev=ev.filter( event__isshow=1)
    else:
        ev=ev.filter(event__isshow=isshow)
    if catid:
        if catid.isdigit():        
            ev=ev.filter(event__cat=catid)
        else:
            try:
                cat=catid.split(',')
                if len(cat)>0:
                    ev=ev.filter(event__cat__in=cat)
            except:
                pass

    if cityid:
        if cityid.isdigit():
            ev=ev.filter(event__city=cityid)
        else:
            try:
                ci=cityid.split(',')
                if len(ci)>0:
                    ev=ev.filter(event__city__in=ci)
            except:
                pass
    if price_type:
        if price_type.isdigit():
            ev=ev.filter(event__Price__Type=price_type)
        else:
            try:
                pr=price_type.split(',')
                if len(pr)>0:
                    ev=ev.filter(event__Price__Type__in=price_type)
            except:
                pass
        
        
    
    if peoples:
        ev=ev.filter(Q(people__lte=peoples)|Q(max_people=peoples)).filter(Q(max_people__gte=peoples)|Q(people=peoples))
    if money_mins:
        ev=ev.filter(Q(event__Price__min__gte=money_mins)|Q(event__Price__max__gte=money_mins))
    if money_maxs:
        
        ev=ev.filter(Q(event__Price__min__lte=money_maxs)|Q(event__Price__max__lte=money_maxs))
        #ev=ev.filter(event__Price__max__gte=money_maxs)
    if not random:
        start = (page-1)*offset
        end = page*offset
    else:
        con=ev.count()
        if not con:
            return []
        elif con<offset:
            start=0
        else:    
            import random 
            start=random.randint(1, con-offset-1)
        end = start+offset
        #return [start,end]
        
    
    
    return [getevent(id=e.event.old_event_id,new=new,ver=ver)  for e in ev.order_by('-feelnum', '-event__end_time').distinct()[start:end]]

def getImgUrl(img_id):
    imgs=NewEventImg.objects.get(id=img_id)
    return imgs.server.name+imgs.urls
def getCatArticle(cat_id=None):
    if not cat_id:
        return ''   
    pattern = re.compile(r"<p>img\d+\</p>")
    con='<body>'
    for ar in NewArticle.objects.filter(cat=cat_id):
        con+=pattern.sub(find_img,replaceCharEntity(ar.content) )
        
    con+='</body>'
        
    return re.sub("\r\n",'',con)



def getcat(ty=3,lasttime=None,cityid=None,page=1,offset=10,kw_sep=','):
    
    
    cats=NewEventCat.objects.filter(type=ty)
    if ty==3:
        cats=cats.filter(begin_time__lte=datetime.date.today()).filter(Q(end_time__gt=datetime.date.today())|Q(end_time=None))
    if lasttime:
        
        try:
            lasttime = datetime.datetime.strptime(lasttime, "%Y-%m-%d").date()
            #lasttime=datetime.datetime(* date[:3])
        except:
            date = time.localtime(int(lasttime))        
            lasttime=datetime.datetime(* date[:3]).date()
        '''
        else:
            return lasttime   
        '''
        cats=cats.filter(begin_time__gt=lasttime)
        return cats.count()
    ca=[]
    if cityid:
        ci=cityid.split('_')
        if len(ci)>0:
            cats=cats.filter(city__in=ci)
        else:
            cats=cats.filter(city=ci)
    start = (page-1)*offset
    end = page*offset

    
    for cat in cats.order_by('-begin_time')[start:end]:
        c={}
        c['id']=cat.id
        c['title']=cat.name
        c['keywords']=kw_sep.join([ta.name for ta in cat.tag.all()])
        c['text']=getCatArticle(cat.id)
        c['img']=''
        c['width']=''
        c['height']=''
        c['begin_time']=datetime.datetime.strftime(cat.begin_time, "%Y-%m-%d") if cat.begin_time else 0
        #lasttime=c['begin_time']
        try:
            if cat.img:
                
                imgs=cat.img
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
        except:
            pass
        
        ca.append(c)

    
    return ca

def getTheme(ty=4):

    try:
        cats=NewEventCat.objects.filter(type=ty).order_by('-order')
        ca=[]
        for cat in cats:
            c={}
            c['id']=cat.id
            c['title']=cat.name
            c['hot']=cat.order
            c['type']=cat.sale
            
            c['des']=','.join([ta.name for ta in cat.tag.all()])
  
            
            try:
                if cat.img:
                    
                    imgs=cat.img
                    #print 'imgs yes'
                    if imgs.server:
                        c['img'] = imgs.server.name+imgs.urls
                    else:
                        if re.match('/',imgs.urls):
                            c['img']='http://pic.huodongjia.com'+imgs.urls
                        else:
                            c['img']='http://pic.huodongjia.com/'+imgs.urls
                    
          
            except:
                
                c['img']=''
            ca.append(c)
    except:
        ca=[]
    
    return ca
            
def getCity(id_list=[]):
    #citys=NewDistrict.objects.filter(id__in=[101,99,54,6,14,17,30,48,62,69,76,98,186,220,241,501,502]).order_by('-event_count')
    if id_list:
        citys = NewDistrict.objects.filter(id__in=id_list)
    else:
        citys = NewDistrict.objects.exclude(img__isnull=True).order_by('-event_count')
    #citys=NewDistrict.objects.filter(id__in=[98,69,54]).order_by('-event_count')
    ca=[]
    cc={}
    for city in citys:
        cct={}
        cct['id']=city.id
        cct['name']=city.district_name
        cct['des']=city.des if city.des else ''


        
        try:
            if city.img:
                
                imgs=city.img
                #print 'imgs yes'
                if imgs.server:
                    cct['img'] = imgs.server.name+imgs.urls
                else:
                    if re.match('/',imgs.urls):
                        cct['img']='http://pic.huodongjia.com'+imgs.urls
                    else:
                        cct['img']='http://pic.huodongjia.com/'+imgs.urls
                
      
        except:
            
            cct['img']=''
        #cct['img']=city.img
        
        if city.parent:
            cct['parent_name']=city.parent.district_name
            cct['parent_id']=city.parent.id
            '''
            if not cc.has_key(city.parent.id):
                cc[city.parent.id]=[]
                ca.append(cc)
            cc[city.parent.id].append(cct)
            '''
        #else:
        
        ca.append(cct)
        
        
  
    #c1={'id':101,'name':'北京','des':'皇城根下，国人的灵魂源头','img':'http://pic1.qkan.com/event/2014-11-28/event1417152267.6.jpg'}
    #c2={'id':99,'name':'上海','des':'风情外滩，纸醉金迷不夜城','img':'http://pic1.qkan.com/event/2014-11-28/event1417160142.93.jpg'}
    #c3={'id':54,'name':'成都','des':'国宝川剧，大气休闲而静谧','img':'http://pic1.qkan.com/event/2014-11-28/event1417160108.12.jpg'}
    #ca=[c1,c2,c3]    
    return ca
