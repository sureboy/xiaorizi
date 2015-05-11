#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.cache import cache
from admin_self.common import NewCatUrl,NewCity,NewformatEvent,event_city_cat,\
                                oldEventToNewEvent,find_cat_fid ,ip_Filter                           
from django.views.decorators.csrf import csrf_exempt
from new_event.common import find_from_city
from new_event.showlist import showList
from new_event.models import NewEventTable
import json
from django.http import Http404

def indexPage(request,city=None):
    cityObj = find_from_city(request,city)
    
    www={'id':2,'name':'互联网会','img':'http://pic.huodongjia.com/html5/pic/www.png',}
    jinrong={'id':6,'name':'金融会议','img':'http://pic.huodongjia.com/html5/pic/jinrong.png',}
    hospity={'id':23,'name':'医疗会议','img':'http://pic.huodongjia.com/html5/pic/hospity.png',}
    maer={'id':93,'name':'骑马运动','img':'http://pic.huodongjia.com/html5/pic/maer.png',}
    fly={'id':94,'name':'飞行体验','img':'http://pic.huodongjia.com/html5/pic/fly.png',}
    foot={'id':76,'name':'美食烹饪','img':'http://pic.huodongjia.com/html5/pic/foot.png',}
    child={'id':24,'name':'亲子活动','img':'http://pic.huodongjia.com/html5/pic/child.png',}
    snow={'id':24,'name':'滑雪活动','img':'http://pic.huodongjia.com/html5/pic/snow.png',}
    
    hot_cat=[www,jinrong,hospity,maer,fly,foot,child,snow]
    
    m_list=event_city_cat(cityObj[0])
    response = render_to_response('m_home.html',{'city':cityObj[1],
                                           'city_id':cityObj[0],
                                           'city_py':cityObj[2],
                                           'hot_cat':hot_cat,
                                           'list':m_list[:5],
                                           },
                                           context_instance=RequestContext(request))
    response.set_cookie('city_id',cityObj[0])
    response.set_cookie('city_py',cityObj[2])
    response.set_cookie('city',cityObj[1].encode('utf-8'))
    response['Cache-Control'] = 'max-age=300'
    return response    



def showPage(request,query=False,template_name='m_event.html'): 
    event={}
    if query.isdigit():
      
        
        event= NewformatEvent(False,int(query),request.GET.get('new',False))        
 
    if not event.has_key('isshow'):
        return render_to_response('base_error.html',{'error_msg':u'没有该活动  '  })
  
    else:
        if not event['isshow'] in [1,8]:
            return render_to_response('base_error.html',{'error_msg':u'活动没有发布' })       

        city_t=event['district_title']
        city_n=event['district_name']
   
 
        qu=False
           
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


        new=False
        tran_rec_list =event_city_cat(None,event['catid'],new) 
        if event['has_picture']:
            number=4
        else:
            number=6
        
        
        l= len(tran_rec_list)-number
        if l<0:  
            b = event_city_cat(None,None,new )  
            #print b
            tran_rec_list.extend(b [:abs(l)] )
        #tran_rec_list =[]#  [formatEvent(item) for item in recommend_list[randloc:randloc+number]]

                        
                    
                
 
        body={'head':event['head'],
             'event':event,
             'user_viewed_events':tran_rec_list[:number],
             'city':city_n,
             'city_py':city_t,
             'navigationList':event['navigationList']}
        
        
        
        if event.has_key('cf'):
            body['cf']=event['cf']
        
            
        return render_to_response(template_name,body,context_instance=RequestContext(request))
         

def SearchKey_ajax(request):
    cds = request.GET
    keyword = cds.get('keyword',None)
    city = cds.get('city',None)
    cityObj = find_from_city(request,city)
    
    (page,offset) = getPageAndOffset(cds)
    p={}
    if not keyword:
        return HttpResponse(json.dumps({"code":0,"msg":"Only GETs are allowed","list":[]}), content_type="application/json")
    if len(keyword) > 20:
        return HttpResponse(json.dumps({"code":0,"msg":"keyword Fail","list":[]}), content_type="application/json")
    else:
        #events_lis = mc.get(keyword+'_search_lis')
        keyword= keyword.replace('/',' ')
        ids = cache.get('_'.join(keyword.split())+'_search_lis')
        
        p['code']=1
        p['msg']='Request is successful'
        p['keys']=keyword
        p['list'] =[]
        if not ids:
            ids = search(keyword)
        if ids:

            cache.set('_'.join(keyword.split())+'_search_lis',ids,300)
            events_lis = NewEventTable.objects.filter(old_event__in = ids)#.order_by('district_id='+str(district_id),'event_begin_time')
            
            if cityObj:
                events_lis = events_lis.filter(city=cityObj[0])
                
            start = (page-1)*offset
            end = page*offset
            p['list'] = [NewformatEvent(None,item.old_event_id) for item in events_lis[start:end]]
 
    response = json.dumps(p)
    return HttpResponse(response, mimetype="application/json")
            
def SearchKey(request):
    cds = request.GET
    keyword = cds.get('keyword',None)
    city = cds.get('city',None)
    cityObj = find_from_city(request,city)
    (page,offset) = getPageAndOffset(cds)
    
    list_s=[]
    ids=None
    if not keyword:
        return HttpResponse(json.dumps({"code":0,"msg":"Only GETs are allowed","list":[]}), content_type="application/json")
    if len(keyword) > 20:
        return HttpResponse(json.dumps({"code":0,"msg":"keyword Fail","list":[]}), content_type="application/json")
    else:
        #events_lis = mc.get(keyword+'_search_lis')
        keyword= keyword.replace('/',' ')
        ids = cache.get('_'.join(keyword.split())+'_search_lis')
        

        if not ids:
            ids = search(keyword)
            
        if ids:

            cache.set('_'.join(keyword.split())+'_search_lis',ids,300)
            events_lis = NewEventTable.objects.filter(old_event__in = ids)#.order_by('district_id='+str(district_id),'event_begin_time')
            
            if cityObj:
                events_lis = events_lis.filter(city=cityObj[0])
            
            start = (page-1)*offset
            end = page*offset
            list_s = [NewformatEvent(None,item.old_event_id) for item in events_lis[start:end]]
 
    #response = json.dumps(p)
    #return HttpResponse(response, mimetype="application/json")
    return render_to_response('m_list.html',{'list':list_s},context_instance=RequestContext(request))


def list(request,city=None,cat=None,date=None,offset=1):
    
    
    #log.debug('get list')
              
    date = request.GET.get('dat')
    offset = request.GET.get('page')
        
    if not date and not cat:    
        return indexPage(request,city)
        #return False


    
 
    if not city: city='beijing'
    if not cat: cat = 'all'
    if not date: date = 'latest'
    if not offset: 
        offset = 1 
    else: 
        offset = int(offset)
 
    
    
    listDict = showList(request,city,cat,date,offset)
 
    #print connection.queries
    return render_to_response('m_list.html',listDict,context_instance=RequestContext(request))
        
def search(keyword):
    import sphinxapi
    cl = sphinxapi.SphinxClient()
    cl.SetServer('10.10.64.15',9312)
    #cl.SetConnectTimeout(3)
    cl.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED)
    cl.SetLimits(0,100)
    res = cl.Query(keyword,'*')
    
    if not res:
        return []
    
    if res.has_key('matches'):
        return [match["id"] for match in res['matches']]
    return []
 

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


