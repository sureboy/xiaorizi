#coding:utf-8
from new_event.common import find_from_city
from django.template import RequestContext
from django.shortcuts import render_to_response

def searchKeyword(request,offset = 15,page = 1,isTag=False):
    #mc = memcache.Client(['127.0.0.1:11211'])
    cityObj = find_from_city(request)
    title = cityObj[2]
    city_name = cityObj[1] 
    district_id = cityObj[0]
 
    if offset < 1 or page < 1:
        return render_to_response('base_error.html',{'error_msg':u'页码错误'},context_instance=RequestContext(request))
    offset = int(offset)
    page = int(page)
    error = u'你什么都没有输入'
    if request.GET.get('keyword',''):
        keyword = request.GET['keyword']
        #keyword = keyword.encode('utf8')
        #print keyword.encode('utf8')
        if keyword:
            if page == 1 and not isTag:
                        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                            ip =  request.META['HTTP_X_FORWARDED_FOR']
                        else:
                            ip = request.META['REMOTE_ADDR']
                        SysSearchKey.objects.create(keyword = keyword,
                                                    ip = ip,
                                                    search_time = time.time()
                                                    )
            if len(keyword) > 20:
                error = u'关键词的字数不能超过20'
            else:
                #events_lis = mc.get(keyword+'_search_lis')
                keyword= keyword.replace('/',' ')
                events_lis = cache.get('_'.join(keyword.split())+'_search_lis')
                if not events_lis:
                    ids = search(keyword)
                    if ids:
                        events_lis = SysEvent.objects.filter(event_id__in = ids)#.order_by('district_id='+str(district_id),'event_begin_time')
                        cache.set('_'.join(keyword.split())+'_search_lis',events_lis,300)
                if events_lis:
                    events_lis = events_lis.extra(select={'is_top':'district_id='+str(district_id)})
                    events_lis = events_lis.extra(order_by=['-is_top'])
                    #print connection.queries
                    count = events_lis.count()
                    if count%offset:
                        page_number = count/offset+1
                    else:
                        page_number = count/offset
                    rlist = [formatEvent(item) for item in events_lis[offset*(page-1):offset*page]]
                    if not isTag:
                        url = '/search/'+str(offset)+'/page/?keyword='+keyword
                    else:
                        url = '/tag/'+str(offset)+'/page/?keyword='+keyword
                    #print page_number
                    pageList = []
                    for i in range(1,page_number+1):
                        curPageFlg = False
                        if page == i:
                            curPageFlg = True
                        pageDict = {'page':i, 'pageurl':url.replace('page',str(i)),'flag':curPageFlg}
                        pageList.append(pageDict)
                        
                    if page <= 1:
                        firstPage = False
                        prePage = False
                    else:
                        firstPage = pageList[0]
                        prePage = pageList[page-2]
                        
                    if page >= page_number:
                        lastPage = False
                        nextPage = False
                    else:
                        lastPage = pageList[page_number-1]
                        nextPage = pageList[page]
                    #print pageList
                    
                    head = {'title':u'%s_门票预订_报名参加_活动网_活动家'%(keyword),
              'keywords':u'%s'%(keyword),
             'description':u'报名参加购买%s活动门票请上活动家（huodongjia.com）'%(keyword)}
                    return render_to_response('search_results.html',{'list':rlist,
                                                                     'city':city_name,
                                                                     'city_py':title,
                                                                     'keyword':keyword,
                                                                     'firstPage':firstPage,
                                                                     'prePage':prePage,
                                                                     'currentPage':page,
                                                                     'nextPage':nextPage,
                                                                     'lastPage':lastPage,
                                                                     'pageList':pageList,
                                                                     'head':head})
                else:
                    error = u'没能搜索到与"%s"相关的活动，你可以尝试其他搜索'%keyword
                    
                    clist = []
                    for i in [20,21,22,23,89,90]:
                        cl = cache.get('rec_with_cat_%s'%i)
                        if cl:
                            for j in cl:
                                if not random.randint(0,8):
                                    clist.append(j)
                    rlist = [formatEvent(item) for item in clist]
                    
                    if clist:
                        message = u'你可能感兴趣的活动'
                    else:
                        message = ''
                    return render_to_response('search_results.html',{'error_msg':error,'message':message,'city':city_name,'city_py':title,'list':rlist},context_instance=RequestContext(request))

        else:
            error = u'输入不能为空'

    
    return render_to_response('search_results.html',{'error_msg':error,'city':city_name,'city_py':title},context_instance=RequestContext(request))
