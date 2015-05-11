#coding:utf-8
from django.shortcuts import render_to_response,render,redirect
from new_event.models import NewDistrict, NewEventCat, NewEventTable, NewEventTag, NewEventParagraph
from spot.models import SysSpotInfo
from dahuodong.models import SubscribeInfo
 
import  time ,datetime

from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt 
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from admin_self.common import NewCatUrl,NewCity,NewformatEvent,event_city_cat,get_site_links,\
                                oldEventToNewEvent,find_cat_fid ,ip_Filter,event_city_tag, \
                                get_event_list_by_ccdt, city_without_level1, get_event_list_for_cal

from django.http import HttpResponse, Http404
import json

import calendar
import math

@csrf_exempt
def list_page_subscribe(request):
    var = {}
    if request.method == 'POST':
        cat_ids = request.POST.get('cat_id', None)
        tag_ids = request.POST.get('tag_id', None)
        email = request.POST.get('email', None)

        if not cat_ids and not tag_ids:
            var['success'] = False
            return HttpResponse(json.dumps(var), content_type='application/json')

        try:
            subinfo = SubscribeInfo.objects.get(email=email)
            if cat_ids:
                subinfo.cats = string_cat(subinfo.cats, cat_ids) + ','
            if tag_ids:
                subinfo.keywords = string_cat(subinfo.keywords, tag_ids) + ','
        except ObjectDoesNotExist:
            subinfo = SubscribeInfo(email=email,keywords=tag_ids+',',cats=cat_ids+',')
        
        subinfo.save()
        
        var['success'] = True

    return HttpResponse(json.dumps(var), content_type='application/json')

def string_cat(string1, string2, sp_by=','):
    '''
    concatenate string, remove the duplicate
    '''
    list1 = filter(lambda x:x, string1.split(sp_by))
    list2 = filter(lambda x:x, string2.split(sp_by))
    return sp_by.join(set(list1.append(list_2)))


def list_page(request,city='city',cat='meeting',month=None,offset=1):
    '''
    cal_flag: return list or calendar
    lead_cat: all the filtering is under this lead_cat category
    city, cat, month : filter the data by this city, category, month
    blank_page_flag: return blank page, if necessary
    '''

    cal_flag = request.GET.get('cal')
    if cal_flag: cal_flag = 1

    lead_cat = 'meeting'

    if request.GET.get('db'):
        new = True
    else:
        new = False

    blank_page_flag = False
    month_int = 0

    if month:
        if month.isdigit():
            month_int = int(month)
        else:
            #return redirect(reverse('new_event.showlist.list', kwargs={'city':city, 'cat':cat}))
            raise Http404

    if month_int not in range(0,13):
        month_int = 0
        month = None
        #return redirect(reverse('rd_page', kwargs={'city':city, 'cat':cat}))

    #in the calendar page, no 'all' option for month selection
    if cal_flag and month_int == 0:
        raise Http404

    #if month before the current, then it means the month of next year
    today = datetime.date.today()
    if month_int == 0:
        date_in = ''
    else:
        date_in = datetime.date(today.year+1 if month_int < today.month else today.year
                            ,month_int,1)
    
    #month = str(month).zfill(2)

    #if city not in the city-dataset or != 'city', raise 404
    city_title_dict = NewCity(3)
    if city == 'city':
        city_info = (0,u'不限','')
    elif city_title_dict.has_key(city):
        city_info = city_title_dict[city]
    else:
        raise Http404
        #blank_page_flag = True
    

    #get all cats by city
    #if cat not in the lead-cats-dataset or != lead_cat, return empty
    cat_ename_dict = NewCatUrl(0, '', new=new)
    cat_ename_list = []
    seo_dict = {}
    if cat_ename_dict.has_key(lead_cat):
#to include category itself and its children
        cat_ename_list += [cat_ename_dict[lead_cat]] + cat_ename_dict[lead_cat]['child']
        try:
            seo_dict = cat_ename_dict[cat]['seo']
        except KeyError:
            pass
    else:
        #raise Http404
        blank_page_flag = True



    cat_id = 0
    if cat not in [i['ename'] for i in cat_ename_list]:
        cat = lead_cat
        
    cat_id = cat_ename_dict[cat]['id']

    #get all tags by cats (how to by cities & cats)
    tag_name = request.GET.get('tag')
    #tag_name is None not in the url
    #set it to '' for the further usage
    if not tag_name: tag_name = ''

    tag_id = 0  #default

    #get all tags under the category
    tag_name_id_dict = {}
    if cat_ename_dict.has_key(cat):
        for i in cat_ename_dict[cat]['tag']:
            if i.has_key('id') and i.has_key('name'):
                tag_name_id_dict[i['name']] = i['id']
    else:
        #blank_page_flag = True
        tag_name = ''


    if tag_name:
        if tag_name_id_dict.has_key(tag_name):
            tag_id = tag_name_id_dict[tag_name]
        else:
            #pass
            tag_name = ''
            #blank_page_flag = True


    offset_str = request.GET.get('page')
    if offset_str:
        try:
            offset = int(offset_str)
            if offset < 1:
                offset = 1
        except TypeError:
            offset = 1
    

    ######################
    #info of current page#
    ######################
    listDict = {}

    listDict['current_city'] = city_info[1]
    #cat == '' indicates the cat_ename_dict is empty
    listDict['current_cat'] = cat_ename_dict[cat]['catname'] if cat != lead_cat and cat else u'不限'
    listDict['current_month'] = month_int2ch(month_int)
    listDict['current_tag'] = tag_name if tag_name else u'不限'

    #do not include 'page='
    url_tail = [['tag', tag_name], ['cal', cal_flag]]
    url_tail_for_cat = [['cal', cal_flag]]


    ################
    #filter options#
    ################
    #nu:name,url
    listDict['city_nu'] = move_to_n_first(
            list_get_city_ch_py_url(lead_cat, cat, month, url_tail, new), 
            city_info[0], 1)

    listDict['cat_nu'] = list_get_cat_ch_py_url(
            lead_cat, cat_ename_list, city, month, url_tail_for_cat, new)

    listDict['month_nu'] = list_get_month_ch_py_url(
            lead_cat, cat, city, today.year, today.month, url_tail, new)

    listDict['tag_nu'] = move_to_n_first(
            list_get_tag_ch_py_url(lead_cat, cat, city, month, tag_name_id_dict, [['cal', cal_flag]], new),
            tag_id, 1)


    listDict['right_news'] = list_get_right_news(today, new)
    listDict['right_news_more'] = '/spot/'

    listDict['right_video'] = list_get_right_video(today, new)
    listDict['right_video_more'] = '/video/'


    ##################
    #list or calendar#
    ##################
    listDict['cal_flag'] = cal_flag

    if cal_flag:
        #remove 'all' option for month-selection in the calendar page
        listDict['month_nu'] = listDict['month_nu'][1:]

        listDict['year'] = date_in.year
        listDict['month'] = date_in.month
        #listDict['switch_link'] = '/' + '/'.join([lead_cat, city, cat, month, '?tag='+ tag_name])
        listDict['switch_link'] = '/' + '/'.join([city, cat, month, '?tag='+ tag_name])
        listDict['calendar_table'] = calendar_page(cat, city_info, date_in, tag_id, new)
        #listDict['reset_link'] = '/' + '/'.join([lead_cat, 'city', lead_cat, str(today.month).zfill(2)]) + '?cal=1'
        listDict['reset_link'] = '/' + '/'.join(['city', lead_cat, str(today.month).zfill(2)]) + '?cal=1'


    else:
        if month:
            #listDict['switch_link'] = '/' + '/'.join([lead_cat, city, cat, month, '?tag='+ tag_name + '&cal=1'])
            listDict['switch_link'] = '/' + '/'.join([city, cat, month, '?tag='+ tag_name + '&cal=1'])
        else:
            listDict['switch_link'] = '/' + '/'.join([city, cat, str(today.month).zfill(2), '?tag='+ tag_name + '&cal=1'])

        #listDict['reset_link'] = '/' + '/'.join([lead_cat, 'city', lead_cat, '00'])
        listDict['reset_link'] = '/' + '/'.join(['city', lead_cat, '00'])


        #do not raise 404
        if blank_page_flag:
            return render(request, 's_list.html', listDict)

        #the amount of the events
        count = get_event_list_by_ccdt(cat=cat,city=city_info,date=date_in,page=False,offset=False,order='',new=new,tag_id='')

        count=count if count else 0

        perpage=12
        pages = count/perpage
        if 0 != (count%perpage): pages = pages + 1
        if offset > pages: offset = pages
        
        listDict.update(show_list(request,city_info,cat,date_in,tag_id,perpage,offset,new))

        listDict['firstPage'],listDict['lastPage'],listDict['prePage'],listDict['nextPage'],listDict['pageList'] \
                = list_page_url(city,cat,month,tag_name,pages,offset)


    #####
    #seo#
    #####
    if city_info[0]:
        html_head_city = city_info[1]
    else:
        #html_head_city = ','.join([i[1] for i in city_title_dict.values()])
        html_head_city = u''

    if cat == lead_cat:
        html_head_cat = ','.join([i['ename'] for i in cat_ename_list])
    else:
        html_head_cat = cat_ename_dict[cat]['ename']

    if month_int:
        html_head_date = u'%s年%s月' %(date_in.year, date_in.month)
    else:
        html_head_date = u'最新'

    if tag_name and cat != lead_cat:
        html_head_tag = ','.join(tag_name_id_dict.keys())
    else:
        html_head_tag = ''

    listDict['head'] = get_list_cal_head(seo_dict, html_head_city, html_head_cat, html_head_date, html_head_tag)


    return render(request, 's_list.html', listDict)

def list_get_right_video(date, new=False):
    key_name = 'list_right_video_%s_%s_%s' %(date.year, date.month, date.day)
    video_list = cache.get(key_name)

    if not video_list or new:

        video = NewEventParagraph.objects.filter(cat_name_id=17543).order_by('-end_time')[:5]
        video_list = []
        validate = URLValidator()

        for i in video:
            try:
                validate(i.txt)
                video_list.append({'name':i.name, 'url':i.txt})
            except ValidationError:
                video_list.append({'name':i.name, 'url':'/video?id=%s' %i.id})

        cache.set(key_name, 86400)

    return video_list


def list_get_right_news(date, new=False):
    key_name = 'list_right_news_%s_%s_%s' %(date.year, date.month, date.day)
    news_list = cache.get(key_name)
    
    if not news_list or new:
        news = SysSpotInfo.objects.filter(spot_isshow=True).order_by('-spot_last_edit')[:5]
        news_list = [{'name':i.spot_name, 'url':'/spot/%s.html' %i.id} for i in news]
        cache.set(key_name, news_list, 86400)
    
    return  news_list

def get_list_cal_head(seo_dict, city_str, cat_str, date_str, tag_str):

    if seo_dict.has_key('title'):
        seo_dict['title']=seo_dict['title'].replace('XX',city_str).replace(u'大活动',u'活动家') 
        seo_dict['title']=seo_dict['title'].replace('(city)',city_str)
        seo_dict['title']=seo_dict['title'].replace('(date)',date_str)
        seo_dict['title']=seo_dict['title'].replace('(cat)',cat_str)
        seo_dict['title']=seo_dict['title'].replace('(tag)',tag_str)
    else:
        seo_dict['title']=u'会议网_活动网_公开课培训_%s展会_活动家'%city_str
    
    if seo_dict.has_key('keywords'):
        seo_dict['keywords']=seo_dict['keywords'].replace('XX',city_str).replace(u'大活动',u'活动家')
        seo_dict['keywords']=seo_dict['keywords'].replace('(city)',city_str)
        seo_dict['keywords']=seo_dict['keywords'].replace('(date)',date_str)
        seo_dict['keywords']=seo_dict['keywords'].replace('(cat)',cat_str)
        seo_dict['keywords']=seo_dict['keywords'].replace('(tag)',tag_str)
    else:
        seo_dict['keywords']=u'会议网,活动网,商务活动,公开课培训,%s展览,%s展会,%s会展,%s会议'%(city_str,city_str,city_str,city_str)
    
    if seo_dict.has_key('description'):
    
        seo_dict['description']=seo_dict['description'].replace('XX',city_str).replace(u'大活动',u'活动家')
        seo_dict['description']=seo_dict['description'].replace('(city)',city_str)
        seo_dict['description']=seo_dict['description'].replace('(date)',date_str)
        seo_dict['description']=seo_dict['description'].replace('(cat)',cat_str)
        seo_dict['description']=seo_dict['description'].replace('(tag)',tag_str)
    else:
        seo_dict['description']=u'活动家www.huodongjia.com为你提供会议报名，会展参展，公开课报名服务。服务热线:400-003-3879'

    return seo_dict

def month_int2ch(month):
    month = int(month)
    dic = {0:u'不限', 1:u'一月', 2:u'二月', 3:u'三月', 4:u'四月', 5:u'五月', 6:u'六月', 7:u'七月', 8:u'八月', 9:u'九月', 10:u'十月', 11:u'十一月', 12:u'十二月'}
    return dic[month]

def url_add_tail(url, tail_list=[]):
    '''
    tail_list like [['tag', 'sd'], ['page', '1']]
    '''
    tail = []
    for (a, b) in tail_list:
        if b:
            #if not isinstance(a, str):
            #    a = str(a)
            #if not isinstance(b, str):
            #    b = str(b)
            tail.append('%s=%s' %(a,b))

    if tail:
        return url + '?' + '&'.join(tail)
    else:
        return url


def url_add_tag_page(url, tag=False, page=False):
    if tag:
        url += '?tag=' + tag
        symbol = '&'
    else:
        symbol = '?'
    if page:
        url += symbol + 'page=' + page

    return url

def move_to_n_first(list_in, id_in, first_n):
    '''
    compared the id
    '''
    if id_in:
        first_part = list_in[:first_n]
        second_part = []
        last_part = []
        for i in list_in[first_n:]:
            ##
            if i['id'] != id_in:
                last_part.append(i)
            else:
                second_part = [i]
        return first_part + second_part + last_part
    else:
        return list_in


def list_get_tag_ch_py_url(cat1_title,cat2_title,city,month,tag_name_id_dict,url_tail,new=False):
    tag_ch_py_url = []
    #tag_pre = '/' + cat1_title + '/' + city + '/' + cat2_title + '/' + month + '/'

    tag_pre = '/' + city + '/' + cat2_title + '/'
    if month:
        tag_pre += month + '/'

    tag_post = ''

    #insert 'all' at the 1st place
    tag_ch_py_url.append({'name':u'不限',
                          'id':0,
                          'url':tag_pre + url_add_tail(tag_post, url_tail)})

    for i in tag_name_id_dict.keys():
        tmp_dict = {}
        tmp_dict['name'] = i
        tmp_dict['id'] = tag_name_id_dict[i]
        tmp_dict['url'] = tag_pre + url_add_tail(tag_post, url_tail + [['tag',i]])
        tag_ch_py_url.append(tmp_dict)

    return tag_ch_py_url

def list_get_month_ch_py_url(cat1_title,cat2_title,city,this_year,this_month,url_tail,new=False):
    month_ch_py_url = []
    #month_pre = '/' + cat1_title + '/' + city + '/' + cat2_title + '/'
    month_pre = '/' + city + '/' + cat2_title + '/'
    month_post = ''

    #month_post = url_add_tag_page(month_post, tag)
    month_post = url_add_tail(month_post, url_tail)

    #for i in range(len(month_ch_py_url)):
    for i in [0] + range(this_month,this_month+12):
        year = this_year if i <= 12 else this_year + 1
        i = i if i <= 12 else i-12
        tmp_dict = {}
        tmp_dict['title'] = str(i).zfill(2)
        tmp_dict['name'] = month_int2ch(i)
        #if month = 0, which means no-limit, do not show in url
        if i:
            tmp_dict['url'] = month_pre + tmp_dict['title'] + month_post
        else:
            tmp_dict['url'] = month_pre + month_post
        if i == 1:
            tmp_dict['year'] = year
        month_ch_py_url.append(tmp_dict)

    return month_ch_py_url


def list_get_cat_ch_py_url(cat1_title,cat2,city,month,url_tail,new=False):
    '''
    get urls on the category links for the new list page
    '''

    cat_ch_py_url = []
    #cat_pre = '/' + cat1_title + '/' + city + '/'
    cat_pre = '/' + city + '/'
    cat_post = '/'
    if month:
        cat_post += month + '/'

    #cat_post = url_add_tag_page(cat_post, tag)
    cat_post = url_add_tail(cat_post, url_tail)
    
    cat_ch_py_url.append({
        'name':u'不限',
        'title':cat1_title,
        'url':cat_pre + cat1_title + cat_post,
        })

    #insert 'all' at the 1st place
    for i in cat2:
        tmp_dict = {}
        if all((i['catname'], i['ename'])):
            #the equal indicates the all(不限)
            if i['ename'] != cat1_title:
                tmp_dict['name'] = i['catname']
                tmp_dict['title'] = i['ename']
                tmp_dict['url'] = cat_pre + tmp_dict['title'] + cat_post
                tmp_dict['tag'] = i['tag']
                tmp_dict['id'] = i['id']
                cat_ch_py_url.append(tmp_dict)

    return cat_ch_py_url

def list_get_city_ch_py_url(cat1_title,cat2_title,month,url_tail,new=False):
    '''
    get urls on the city links for the new list page
    '''

    #-----------------
    #2015.2.4 add 2nd parameter in city_without_level1
    #to filter the cities which doesn't hold any event under the specific categories
    cat_filter = []
    cat_ename_dict = NewCatUrl(0, '', new=new)
    for i in [cat_ename_dict[cat1_title]] + cat_ename_dict[cat1_title]['child']:
        if i['ename']: cat_filter.append(i['ename'])

    #temporary
    city_ch_py = city_without_level1(new, cat_filter)

    city_ch_py_url = []

    city_pre = '/'
    city_post = '/' + cat2_title + '/'
    if month:
        city_post += month + '/'

    #city_post = url_add_tag_page(city_post, tag)
    city_post = url_add_tail(city_post, url_tail)

    #insert 'all' at the 1st place
    city_ch_py_url.append({'name':u'不限',
                           'title':'city',
                           'id':0,
                           'url':city_pre + 'city' + city_post})

    for city_dict in city_ch_py:
        tmp_dict = {}
        tmp_dict['name'] = city_dict['district_name']
        tmp_dict['title'] = city_dict['title']
        tmp_dict['id'] = city_dict['id']
        tmp_dict['url'] = city_pre + tmp_dict['title'] + city_post
        city_ch_py_url.append(tmp_dict)

    return city_ch_py_url

def show_list(request, city, cat, date, tag_id, perpage, offset, new=False):
    '''
    city is tuple
    return a list of event-dict of only one specific page
    '''

    offset = int(offset)
    cout = perpage*(offset-1)
    try:
        url=request.META['PATH_INFO']
        if url[-1]=="/":
            url=url[:-1] 
    except:
        url=''
    

    ####################
    #new = Ture, read from database
    mlist = get_event_list_by_ccdt(cat=cat, city=city, date=date, page=cout, offset=cout+perpage, order='-rel_time', new=new, tag_id=tag_id)

    tmp = []
    if mlist:
        print mlist
        for item in mlist:
            tmp.append(NewformatEvent(False,item))


    listDict = {'list':tmp}

    return listDict

def list_page_url(city,cat,month,tag,amountPages,curpage):

    if curpage > amountPages:
        curpage =  amountPages
    if curpage <= 0 or False == curpage:
        curpage = 1
    pageList = []
    #url = '/'+city+'/'+cat+'/'+date 
    url = '/'+city+'/'+cat+'/'

    if month:
        url += month
    if tag: 
        url += '/?tag='+tag
        symbol = '&'
    else:
        symbol = '?'

    #construct section page
    startPage = 1
    endPage = amountPages
    if 3 <= curpage:
        startPage = curpage-2
    if 2 <= amountPages - curpage:
        endPage =  curpage+2
        
    #first last page
    firstPage = 'false'
    lastPage = 'false'
    if curpage != 1:
        firstPage = url #url+'&page='+'1'
    if curpage != amountPages:
        lastPage = url+symbol+'page='+str(amountPages)
    #prepage nextpage
    prePage = 'false'
    nextPage = 'false'
    if 1 < curpage:
        prePage = url+symbol+'page='+str(curpage-1)
    if curpage < amountPages and 1 < amountPages:
        nextPage = url+symbol+'page='+str(curpage+1)
        
    for i in range(startPage,endPage+1):
        curPageFlg = 'false'
        if curpage == i:
            curPageFlg = 'true'
        if i==1:
            pageDict = {'page':i, 'pageurl':url,'flag':curPageFlg}
        else:
            pageDict = {'page':i, 'pageurl':url+symbol+'page='+str(i),'flag':curPageFlg}
        pageList.append(pageDict)
    return (firstPage,lastPage,prePage,nextPage,pageList)    

#--------------------
#calendar page
def add_empty_dict(dt):
    dt.append(
        {'day':'',
         'n_event':0,
         'event':[]}
        )

def add_sth_dict(dt, date, ev):
    ev_dict_list = []
    for i in ev:
        ev_dict_list.append(
            {'name':i['name'],
             'url':'/event-%s.html' %i['id']}
            )

    dt.append(
        {'day':str(date.day),
         'n_event':len(ev),
         'event':ev_dict_list}
        )

def make_table_str(table_str_in, data):
    table_str = table_str_in
    table_str += '<tr class="table-tr"><td></td>'
    for i in data:
        table_str += '<td>' + str(i['day']) if i['day'] else '<td>'
        table_str += '<div class="blue-div">' + str(i['n_event']) \
                       + u'场活动</div></td>' if i['n_event'] else '</td>'
    table_str += '<td></td>'
    table_str += '</tr><tr class="table-tr table-td">'

    #add empty in the first grid
    table_str += '<td class="first-td"><div class="table_div"></div></td>'
    for i in data:
        table_str += '<td><div class="table_div">'

        if i['event']:
            table_str += '<ul>'
            n_count = 0
            for ev in i['event']:
                n_count += 1
                if n_count == 4: break
                table_str += '<li><a href="' + ev['url'] + '">' + ev['name'] + '</a></li>'
            table_str += '</ul>'
            if n_count == 4: table_str += u'<p>更多></p>'
        table_str += '</div></td>'

    
    #add empty in the last grid
    table_str += '<td class="last-td"><div class="table_div"></div></td>'

    return table_str

#def calendar_page(request):
def calendar_page(cat, city, date, tag_id, new):

    #template_name = 'table_ldstest.html'

    #y_m = time.strptime(request.GET.get('ym'), '%Y%m')
    year = date.year
    month = date.month
    day = 1
    date = datetime.date(year, month, day)

    weekday = date.weekday()
    month_days = calendar.monthrange(year, month)[1]
    n_rows = int(math.ceil((month_days + weekday) / 7.0))
    
    ev = get_event_list_for_cal(cat=cat,city=city,date=date,new=new,tag_id=tag_id)
    
    days_count = 0

    data_dict_table_month = []

    for j in range(n_rows):
        #store data of one week
        data_dict_table_week = []

        s_day = j*7+1-weekday
        e_day = s_day+6 
        if s_day <= 0: s_day = 1
        if e_day > month_days: e_day = month_days

        #ev_week = ev.filter(begin_time__gte=datetime.date(year,month,s_day),
        #                    begin_time__lte=datetime.date(year,month,e_day))
        ev_week = [i for i in ev if datetime.datetime(year, month, s_day) <= i['begin_time'] <= datetime.datetime(year, month, e_day)]
        for i in range(7):
            if (j == 0 and i < weekday) or days_count == month_days:
                add_empty_dict(data_dict_table_week)
            else:
                days_count += 1
                this_day = datetime.date(year,month,days_count)
                #ev_day = ev_week.filter(begin_time=datetime.date(year,month,days_count))
                ev_day = [i for i in ev_week if i['begin_time'] == datetime.datetime(year, month, days_count)]
                add_sth_dict(data_dict_table_week, this_day, ev_day)
        
        data_dict_table_month.append(data_dict_table_week)

    return data_dict_table_month


def ldstest(request):
    from admin_self.common import find_cat_ch
    video = list_get_right_video(datetime.date.today(), True)
    var = {}
    var['video'] = video
    return HttpResponse(json.dumps(var), content_type='application/json')
    new = True
    var = {}
    lead_cat = 'meeting'
    cat = 'finance'
    city = 'beijing'
    month = '02'
    tag_name = u'不限'.encode('utf8')

    cat_ename_dict = NewCatUrl(0, city, new=False)
    cat_ename_list = cat_ename_dict[cat]['child']
    tag_id_name_list = []
    for i in cat_ename_list:
        if i['tag']:
            tag_id_name_list.extend(i['tag'])

    tag_name_id_dict = {}
    for [id, name] in tag_id_name_list:
        tag_name_id_dict[name] = id

    cat_in = 'finance'
    city_info = (0, u'不限', '')
    date_in = datetime.date.today()
    tag_id = ''
    var['calendar_table'] = calendar_page(cat_in, city_info, date_in, tag_id, new)

    return render(request, 'ldstest.html', var)

    cat_ename_dict = NewCatUrl(0, city, new=new)
    cat_ename_list = [i['ename'] for i in cat_ename_dict[lead_cat]['child']]

    ev_tmp=NewEventTable.objects.filter(isshow__in=(1,8)).filter(end_time__gte=datetime.date.today()).filter(cat__ename__in=cat_ename_list)
    ev = ev_tmp[0].city.all()
    return HttpResponse(json.dumps(ev[0]), content_type='application/json')

    #count = get_event_list_by_ccdt(cat=cat,city=[101,u'北京',''],date=datetime.date.today(),page=False,offset=False,order='',new=new,tag_id='')
    #return HttpResponse(count)

#def calendar_page(year,month, city_id, cat_id, tag_id):
#    import calendar
#    import math
#    import time
#
#    template_name = 'table_ldstest.html'
#
#    #y_m = time.strptime(request.GET.get('ym'), '%Y%m')
#    #year = y_m.tm_year
#    #month = y_m.tm_mon
#    day = 1
#    date = datetime.date(year, month, day)
#
#    weekday = date.weekday()
#    month_days = calendar.monthrange(year, month)[1]
#    n_rows = int(math.ceil((month_days + weekday) / 7.0))
#    
#    
#    days_count = 0
#
#    table_str = u'<div class="col-lg-12 col-md-12 col-xs-12 col-sm-12 agenda" id="agenda"> <span class="agenda_title">商务活动&sdot;%s年%s月会议日程安排</span><span class="month">%s年%s月</span> <div class="agenda-hr"></div> <table class="agenda_table" cellpadding="1" cellspacing="1"> <thead> <tr class="table-tr"> <th></th> <th>Mon</th> <th>Tue</th> <th>Wed</th> <th>Thu</th> <th>Fri</th> <th>Sat</th> <th>Sun</th> <th></th> </tr> </thead> <tbody> ' %(year, month, year, month)
#
#    for j in range(n_rows):
#        #store data of one week
#        data_dict_table = []
#
#        s_day = j*7+1-weekday
#        e_day = s_day+6 
#        if s_day < 0: s_day = 1
#        if e_day > month_days: e_day = month_days
#
#        ev_week = NewEventTable.objects.filter(isshow__in=(1,8), 
#                                               begin_time__gte=datetime.date(year,month,s_day),
#                                               begin_time__lte=datetime.date(year,month,e_day))
#        for i in range(7):
#            if (j == 0 and i < weekday) or days_count == month_days:
#                add_empty_dict(data_dict_table)
#            else:
#                days_count += 1
#                this_day = datetime.date(year,month,days_count)
#                ev_day = ev_week.filter(begin_time=datetime.date(year,month,days_count))
#                add_sth_dict(data_dict_table, this_day, ev_day)
#    
#        table_str = make_table_str(table_str, data_dict_table)
#
#    table_str += '</tbody></table></div>'
#
#    return table_str
#
#    #var = {}
#    #var['table'] = table_str
#    ##return HttpResponse(json.dumps(var), content_type='application/json')
#    #return render(request, template_name, var)




#def find_child_cat(ins):
#
#    out = []
#
#    children = NewEventCat.objects.filter(parent_id=ins.id)
#
#    if children:
#        out.extend(children)
#        for i in children:
#            out.extend(find_child_cat(i))
#
#    return out
#
#def find_child_city(ins):
#
#    out = []
#
#    children = NewDistrict.objects.filter(parent_id=ins.id)
#
#    if children:
#        out.extend(children)
#        for i in children:
#            out.extend(find_child_cat(i))
#
#    return out
#
#def get_cat_id(cat):
#    parent_cat = NewEventCat.objects.get(ename=cat)
#    prt_chd_cat = find_child_cat(parent_cat) + [parent_cat]
#    
#    return [i.id for i in prt_chd_cat]
#
#        
#def get_city_id(city):
#    parent_city = NewDistrict.objects.get(title=city)
#    prt_chd_city = find_child_city(parent_city) + [parent_city]
#
#    return [i.id for i in prt_chd_city]
#
#
#def ldstest(request, city='city', cat='cat', month='00'):
#
#    MeetingCat = find_child_cat(NewEventCat.objects.get(ename='meeting'))
#    _tmp = [(i.id,i.ename) for i in MeetingCat]
#    all_cat_dict = {}
#    for i in _tmp:
#        if i[1]:
#            all_cat_dict[i[1]] = i[0]
#
#    if cat == 'cat':
#        cat_id = get_cat_id('meeting')
#    elif cat != 'cat' and cat not in all_cat_dict.keys():
#        raise Http404
#    else:
#        cat_id = get_cat_id(cat)
#
#    _tmp = [(i.id,i.title) for i in NewDistrict.objects.all()] #include None
#    all_city_dict = {}
#    for i in _tmp:
#        if i[1]:
#            all_city_dict[i[1]] = i[0]
#
#    if city == 'city':
#        city_id = all_city_dict.values()
#    elif city != 'city' and city not in all_city_dict.keys():
#        raise Http404
#    else:
#        city_id = get_city_id(city)
#
#
#    month = int(month)
#    if month:
#        today = datetime.date.today()
#        this_month = datetime.date(today.year,month,1)
#        next_month = datetime.date(today.year,month+1,1) if month+1 < 13 else datetime.date(today.year+1,1,1)
#
#        event = NewEventTable.objects.filter(isshow__in=(1,8)).filter(begin_time__lt=next_month).filter(end_time__gte=this_month).filter(cat__in=cat_id).filter(city__in=city_id).filter(end_time__gte=datetime.date.today()).distinct().order_by('-begin_time')
#
#    else:
#        event = NewEventTable.objects.filter(isshow__in=(1,8)).filter(cat__in=cat_id).filter(city__in=city_id).filter(end_time__gte=datetime.date.today()).distinct().order_by('-begin_time')
#
#    ##tag
#    tag = request.GET.get('tag')
#    if tag:
#        _tmp = [(i.id, i.name) for i in NewEventTag.objects.all()]
#        all_tag_dict = {}
#        for i in _tmp:
#            if i[1]:
#                all_tag_dict[i[1]] = i[0]
#        if tag not in all_tag_dict.keys():
#            tag_id = 0
#        else:
#            tag_id = all_tag_dict[tag]
#
#    #####
#    if tag:
#        event = event.filter(tag=tag_id)
#    
#
#    event_count = len(event)
#
#    #tag = request.GET.get('tag')
#    ev_list = []
#    for i in event:
#        ev_list.append(NewformatEvent(False,i.old_event_id))
#
#    paginator = Paginator(ev_list, 10)
#    page = request.GET.get('page')
#    try:
#        ev_list = paginator.page(page)
#    except PageNotAnInteger:
#        ev_list = paginator.page(1)
#    except EmptyPage:
#        ev_list = paginator.page(paginator.num_pages)
#
#    return render(request, 'list.html', {'list':ev_list})

