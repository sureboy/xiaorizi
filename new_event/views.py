#coding:utf-8
import re
import  time ,datetime
from django import template
from django.template import RequestContext
from django.shortcuts import render_to_response,render
from new_event.models import   NewOrderMessage, NewDistrict_s,OldEvent,PostEvent,\
                                NewDistrict, NewEventCat, NewEventTable, NewEventTag, \
                                NewEventParagraph
 
from new_event.common import sendMail,sendMailForPostEvent,captcha,SendOrderMsg,Telcaptcha,Telcaptcha_ajax
 
from django.db.models import Q
from django.core.urlresolvers import reverse

from admin_self.common import NewCatUrl,NewCity,NewformatEvent,event_city_cat,get_site_links,\
                                oldEventToNewEvent,find_cat_fid ,ip_Filter,event_city_tag, \
                                get_event_list_by_ccdt, city_without_level1, get_event_list_for_cal

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
import json
from django.core.files.base import ContentFile
from django.core.cache import cache

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError, ObjectDoesNotExist


def show_order_url(request,order_id=False):
    body={}
    
    if order_id:
        info=cache.get('order_%s' % order_id)
        url_list=[]
        for i in range(len(info[0])):
            k=info[0][i].split('|')
            if not 'http://' in k[0]:
                k[0]='http://www.huodongjia.com%s' % k[0]
            if len(k)==1:
                k=info[0][i].split()
            url_list.append(k)
        body={'url_list':url_list,'ip':info[1],'order':order_id}
    return render_to_response('show_order_url.html',body,context_instance=RequestContext(request))
def show_post_html(request,query=False,new=False):
    
    #return render_to_response('show_post.html',{'error_msg':u'活动 没有发布' })
    if not query:
        query=58823
    
    p={} 
    p['begin']=False
    event= NewformatEvent(False,query,new)
    if event['event_begin_time']:
        if datetime.datetime.strptime( event['event_begin_time'], "%Y-%m-%d").date() == datetime.date.today():
            p['begin']=True
            #n_event=NewEventTable.objects.get(id=event['id'])
            #n_event.rel_time=datetime.datetime.now()
            #n_event.save()
    
    #p['ca']=new
    p['info']=event    
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json") 
    
def send_msg_text(request):
    #msg = u'您好,您的验证码%s,10分钟内有效,请及时校验【大活动网】'% (2111)
    #msg=u'您好测试,utf8短信[签名]'
    msg= u'您好，你在活动家(huodongjia.com)预订了极限运动活动，还未支付，请你尽快支付，我们好为你出票。你可以在huodongjia.com上查询订单号2121支付即可。谢谢！【大活动网】'

    SendOrderMsg('18628175526',msg)
    #getMsgU()
    ph=[msg]
    response = json.dumps(ph)
    return HttpResponse(response, mimetype="application/json")    


def update_info(request):
    ph=[]
    dis=NewDistrict_s.objects.all()   
    for citys in dis:
        num=0
        ev=OldEvent.objects.filter(event_isshow__in=(1,8))
        #ev=ev.filter(event_cool__gt=0)
        ev=ev.filter(Q(event_end_time__gt= int(time.time()))|Q(event_islongtime=1) )
         
        for e in ev.filter(district_id=citys.district_id):
            p=oldEventToNewEvent(e.event_id,True)
            if not p:
                info="%s err" % e.event_id
                #print info
                ph.append( info)
            else:                
                num+=1
        if citys.parent_id:
            citys.event_count=num
        #else:
            #citys.event_count=999
        citys.save()
        info='%s %s' % (citys.district_name,num)
        #print info
        ph.append(info)   
    response = json.dumps(ph)
    return HttpResponse(response, mimetype="application/json")       
 
def test_data(request):
     
    #ca=NewCatUrl(0,'',True)
    p=[]
    city=NewCity(3,True)
    for k in city.keys():
        if k:
            NewCatUrl(1,k,True)
            
            event_city_cat(city[k][0],(19,70),True,True)
            event_city_cat(city[k][0],69,True,True)
                
        #print k
        #print cal
            #p.append(city[k][0])
            
            '''
            try:
                ne=NewDistrict_s.objects.get(id=city[k][0])    
                if ne.parent_id:    
                    ne.event_count=event_city_cat(city[k][0],None,True,True)
                #else:
                    #ne.event_count=10000
                #event_city_cat()
                ne.save()
            
                #p.append(event_city_cat(city[k][0],None,False,True))
            except:
                pass
            '''
            
        
    
    #NewCity(3,True)   
    
    p=NewCatUrl(0,'',True)

    
    
    
    
    '''
    event_city_cat(city[k][0],74 ,True )     
    event_city_cat(city[k][0],75 ,True )    
    #return render_to_response('base_error.html',{'error_msg':left}) 
    event_city_cat(city[k][0],70 ,True )  
    event_city_cat(city[k][0],(19,69) ,True ) 
    ev=NewEventTable.objects.filter(city=99).filter(end_time__lt=datetime.datetime.now()).filter(isshow__in=(1,8))
    cat=NewCatInfo.objects.filter(neweventtable_id__in=[e.id for e in ev]) 
    cat.query.group_by = ['neweventcat_id'] 
    cat_id={}
    f_id=[]
    for ca in cat:   
        p.append(ca.neweventcat_id)      
        find_cat(ca.neweventcat , cat_arr=f_id, cat_k=cat_id)
    #p.append(cat_id)    
    
    for cit in NewCityInfo.objects.filter(newdistrict_id=99):
        for event in cit.neweventtable__set.filter(end_time__lt=datetime.datetime.now()).filter(isshow__in=(1,8)):
            p.append(event.id)
 
    url=request.META['PATH_INFO']
    if url[-1]=="/":
        url=url[:-1]
    '''
    #for k,c in ca.items():
        #p.append(k)
        #NewCatUrl(1,'',True)
        
     
    #tmps=[]
 
    #cat_id=cat_id_li['fun']['id']
    #find_cat_ch(NewCatUrl(2,'beijing'),cat_id,tmp=tmps)
    
    #p=constructNavigationUrl('beijing',23)
    #p=event_city_cat(54,70 ,True )
    #p=find_ch(70,NewCatUrl(2,'',True))
    #p=NewCatUrl(2)    
      
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
#from django.db import connection

@csrf_exempt
def showPage(request, query=False):
#def showPage(request,query=False,template_name='show_event.html'): 
    event={}

    if query.isdigit():
                event= NewformatEvent(False,int(query),request.GET.get('new',False))        
 
    if not event.has_key('isshow'):
        return render_to_response('base_error.html',{'error_msg':u'没有该活动  '  })
  
    else:
        if not event['isshow'] in [1,8]:
            return render_to_response('base_error.html',{'error_msg':u'活动没有发布' })       
        ##################
        #2015.1.28
        tp_prt_dir = 'zhuanti/'
        #template_name = tp_prt_dir + event['ename'] + '.html'
        #url_name = tp_prt_dir + zhuanti + '.html'
        #if template_name == url_name:
        #    try:
        #        template.loader.get_template(template_name)
        #    except template.TemplateDoesNotExist:
        #        template_name = tp_prt_dir + 'event.html'
        #else:
        #    raise Http404
        template_name = tp_prt_dir + event['ename'] + '.html'
        ################

        #city_t=event['district_title']
        #city_n=event['district_name']
        city_t = ''
        city_n = ''
   
        console_success = False
        if saveConsult(request,event['event_id'],event['event_name']) == True:
            console_success = True
            
        suggestion_success = False
        if saveSuggestion(request,event['event_id'],event['event_name']) == True:
            suggestion_success = True
        
        qu=False
        
        '''
        for i in range(len(event['event_content'])):
            if event['event_content'][i][0]==u'会议通知':
                ko=event['event_content'][i]
                del event['event_content'][i]
                event['event_content'].insert(0,ko)
                    
            if event['event_content'][i][0]==u'会议门票':
                ko=event['event_content'][i]
                del event['event_content'][i]
                event['event_content'].insert(1,ko)
        '''       
                        
        for con in event['event_content']:
            if con[0]==u'常见问题':
                qu=True
                break
        if not qu:
            fid=find_cat_fid(NewCatUrl(2),event['catid'],city_t) 
            ark=False
            for f in fid:
                if f['article']:
                    for ar in f['article']:
                        if ar['name']==u'常见问题':
                            event['event_content'].append((ar['name'],ar['content'].replace('pic1.qkan.com','pic.huodongjia.com'),))
                            ark=True
                            qu=True
                            break
                if ark:
                    break

                        
                
                 
        
        '''
        
        if cache.has_key('rec_with_cat_%s'%event['event_cat']):
            recommend_list = cache.get('rec_with_cat_%s'%event['event_cat'])
        else:
        '''
        #recommend_list = NowEvent.objects.filter(Q(event_isshow=1)|Q(event_isshow=8),event_cat=event['event_cat']).exclude(event_id = event['event_id']).exclude(event_time_expire = 2).order_by('event_begin_time')
        #randloc = randint(0,len(recommend_list)/2)
        #number = 6
        #event_city_tag
        new=False
        if event.has_key('event_tag_id'):
            tran_rec_list=event_city_tag(event['district_id'],tuple(event['event_tag_id']),new)
        else:
            
            tran_rec_list =event_city_cat(None,event['catid'],new) 
        if event['has_picture']:
            number=4
        else:
            number=6
        
        
        l= len(tran_rec_list)-number
        if l<0:  
            b = event_city_cat(None,None,new )  
            #print b
            tran_rec_list.extend(b [:abs(l)+1] )
        #tran_rec_list =[]#  [formatEvent(item) for item in recommend_list[randloc:randloc+number]]

        tran_rec_list_new=[]
        for tr in tran_rec_list:
            if tr['event_id']!=event['event_id']:
                tran_rec_list_new.append(tr)

                
          
 
        body={'head':event['head'],
             'event':event,
             'user_viewed_events':tran_rec_list_new[:number],
             'city':city_n,
             'console_success':console_success,
             'suggestion_success':suggestion_success,
             'city_py':city_t,
             'navigationList':event['navigationList']}
        
        
        
        if event.has_key('cf'):
            body['cf']=event['cf']
        
        return render_to_response(template_name,body,context_instance=RequestContext(request))
         
 
 
        

        

'''  
def getEventHead(event_li,event,navigationList):
    head={}
     
    tags=','.join([ev.name for ev in event.tag.all()])
    
 
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

 
'''
@captcha
def saveSuggestion(request,eventId,eventName):
    try:
        if request.method == 'POST':
            cds = request.POST
            if cds.get('msg_type') != 'suggestion':
                return False
            if cds.get('name',False) and cds.get('email',False) and cds.get('where',False):
                timeNow = time.time()
                msg_content = cds.get('where','')+'\n'+cds.get('suggestion','')
                NewOrderMessage.objects.create(event_id = eventId,
                                               event_name = eventName,
                                               msg_name = cds.get('name',''),
                                               msg_tel = cds.get('phone',''),
                                               msg_email = cds.get('email',''),
                                               msg_content = msg_content,
                                               msg_addtime = timeNow,
                                               type=1,
                                               ) 
                subject ='活动家-新的纠错,活动名:%s'%eventName.encode('utf-8')
                content = '客户姓名:%s\n联系邮箱:%s\n联系电话:%s\n活动id:%s\n活动名:%s\n活动链接:%s\n纠错内容:%s\n纠错时间:%s'%(cds.get('name','').encode('utf-8'),
                                                                                                   cds.get('email','').encode('utf-8'),
                                                                                                   cds.get('phone','').encode('utf-8'),
                                                                                                   eventId,
                                                                                                   eventName.encode('utf-8'),
                                                                                                   'http://www.huodongjia.com/event-%s.html'%eventId,
                                                                                                   msg_content.encode('utf-8'),
                                                                                                   time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timeNow))
                                                                                                   ) 
                sendMail(subject,content)
                return True
            else:
                return False
        else:
            return False
    except Exception,e:
        print e
        return False

@captcha
def saveConsult(request,eventId,eventName):
    try:
        if request.method == 'POST':
            cds = request.POST
            if cds.get('name',False) and (cds.get('email',False) or cds.get('phone',False)) and cds.get('content',False):
                timeNow = time.time()
                NewOrderMessage.objects.create(event_id = eventId,
                                               event_name = eventName,
                                               msg_name = cds.get('name',''),
                                               msg_tel = cds.get('phone',''),
                                               msg_email = cds.get('email',''),
                                               msg_content = cds.get('content',''),
                                               msg_addtime = timeNow
                                               ) 
                subject ='活动家-留言咨询,活动名:%s,客户:%s'%(eventName.encode('utf-8'),cds.get('name','').encode('utf-8'))
                content = '活动id:%s\n活动名:%s\n'%(eventId,eventName.encode('utf-8'))+dic2text(cds)+'留言时间:%s'%time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timeNow)) 
                sendMail(subject,content)
                return True
            else:
                return False
        else:
            return False
    except:
        return False
    
def dic2text(dic):
    res = ''
    for key,value in dic.items():
        if key == 'csrfmiddlewaretoken':
            continue
        res += key+':'+value+'\n'   
    return res.encode('utf-8')

def writeUpLoadFile(f,fname):
    dest = open('/data/user_attach/'+fname,'wb')
    for chunk in f.chunks():
        dest.write(chunk)
    dest.close()

@csrf_exempt
@Telcaptcha_ajax
def postEvent(request):
    import logging
    log = logging.getLogger('XieYin.app')  
    head = {'title':u'会议活动发布平台_活动家亚洲最大的活动活动聚合平台-免费发布',
        'keywords':u'信息发布平台,免费发布,活动发布,会议发布,活动家',
        'description':u'活动家亚洲最大的活动聚合平台，免费为你发布、推广活动！服务热线:400-003-3879'
        }
    if request.method == 'POST':
        if not ip_Filter(request,10):
            return render_to_response('publish.html',{'city_py':'','head':head})
        else:
            title = request.POST.get('title',False)
            telephone = request.POST.get('telephone',False)
            mail = request.POST.get('mail',False)
            #url = request.POST.get('url',False)
            qq = request.POST.get('qq',False)
            begin_time = request.POST.get('begin_time',False)
            end_time = request.POST.get('end_time',False)
            host_name = request.POST.get('host_name',False)
            last_time = '2015-1-12 16:30:00'
            url = ''
            log.debug('postevent eee')
            try:
                if 0 == len(request.FILES):
                    url = request.POST.get('url',False)
                    m = PostEvent(last_time=last_time,host_tel=telephone,host_mail=mail,event_url=url,title=title,qq=qq,begin_time=begin_time,end_time=end_time,host_name=host_name)
                    m.save()
                else:
                    if 2000000 >= request.FILES['uploadDataField'].size:
                        filename = str(int(time.time()))+request.FILES['uploadDataField'].name
                        writeUpLoadFile(request.FILES['uploadDataField'],filename)
                        m = PostEvent(last_time=last_time,host_tel=telephone,host_mail=mail,event_file_path='/data/user_attach/'+filename,title=title,qq=qq,begin_time=begin_time,end_time=end_time,host_name=host_name)
                        #file_content = ContentFile(request.FILES['file_content'].read())
                        m.save()
                    else:
                        return HttpResponse(json.dumps({'code':0,'city_py':'','head':head}), content_type="text/html")
                        #return render_to_response('publish.html',{'flag':0})
            except Exception,e:
                #print e
                log.debug('postevent error:%s',e)
                return HttpResponse(json.dumps({'code':0,'city_py':'','head':head}), content_type="text/html")
                #return render_to_response('publish.html',{'flag':0})
            
            subject ='主办方有新活动发布'
            content = '主办方电话:%s\n邮箱:%s\n标题:%s\nurl:%s'%(telephone.encode('utf8'),mail.encode('utf8'),title.encode('utf8'),url.encode('utf8')) 
            sendMailForPostEvent(subject,content)
            return HttpResponse(json.dumps({'code':1,'city_py':'','head':head}), content_type="text/html")
            #return render_to_response('publish.html',{'flag':1})
    else:
        return render_to_response('publish.html',{'city_py':'','head':head})

def dispatchsitemap(request,param):
    return render_to_response('xmlsitemap/'+param+'.xml',mimetype="application/xml")

def site_links(request):
    title = request.COOKIES.get('city_py', '')
    city_name = request.COOKIES.get('city', '')
    head = {'title':u'友情链接_活动家',
        'keywords':u'友情链接,活动家',
        'description':u'这里是活动家的友情链接页面，欢迎活动、会议、旅游、娱乐相关行业与本站进行友链交换，请联系QQ：3062279918'
        }
 
    return render_to_response('site_links.html',{'city':city_name,'city_py':title,'site_links':get_site_links(),'head':head},context_instance=RequestContext(request))



def show_video(request, video_id=None):
    var = {}
    new = False
    today = datetime.date.today()
    key_name = 'video_%s_%s_%s' %(today.year, today.month, today.day)
    video = cache.get(key_name)

    if new or not video:
        video = NewEventParagraph.objects.filter(cat_name_id=17543).order_by('-end_time')
        cache.set(key_name, video, 60*60)

    validate = URLValidator()
    var['video'] = []


    #video_id = request.GET.get('id')
    if video_id:
        try:
            video_main = [video.get(id=int(video_id))]
            video_main.extend(video.exclude(id=int(video_id))[:4])
            video = video_main
        except ObjectDoesNotExist:
            video = video[:5]
    else:
        video = video[:5]

    var['id'] = video[0].id
    var['intro'] = video[0].tag
    var['name'] = video[0].name

    var['script'] = video[0].txt
    ############################
    #add isAutoPlay=True       #
    #at the end of 'src=...'   #
    #if the video is from YouKu#
    ############################
    pattern = re.compile('(?P<src>.+src=".+youku[\.\?\=\w/]+")')
    var['script'] = re.sub(pattern, video_add_autoplay, var['script'])


    for i in video:
        img = i.img.all()[0]
        imgurl = img.server.name + img.urls
        try:
            validate(i.txt)
            var['video'].append({'id':i.id, 'name':i.name, 'url':i.txt, 
                                 'img':imgurl, 'v_flag':0})
        except ValidationError:


            var['video'].append({'id':i.id, 'name':i.name, 
                                 'url':reverse('new_event:video_detail', args=(i.id,)),
                                 'img':imgurl, 'v_flag':1,
                                 'play': 1 if i.id == var['id'] else '0'
                                 })
    
    var['business_list'] = event_city_cat('',69)[:4]
    var['video'] = sorted(var['video'], key=lambda x:x['v_flag'], reverse=True)

    var['head'] = {'title':u'%s_在线观看_活动家高清视频' %var['name'],
                   'keywords':u'%s，%s在线观看，%s高清视频' %(var['name'], var['name'], var['name']), 
                   'description':u'%s高清视频在线观看，就在【活动家www.huodongjia.com】。视频简介：%s' %(var['name'], var['intro'] if len(var['intro']) <= 100 else var['intro'][:100] + '......')
        }

    return render(request, 'show_video.html', var)

def video_url(id):
    return '/video-%s.html' %id

def video_add_autoplay(x):
    fnStr = x.group("src")
    pt_sym = re.compile('.+src=".+youku[\.\=\w/]+\?[\=\w]+"')
    if pt_sym.match(fnStr):
        return fnStr[:-1] + '&isAutoPlay=true"'
    else:
        return fnStr[:-1] + '?isAutoPlay=true"'
