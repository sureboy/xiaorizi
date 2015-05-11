#-*-coding:utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from weibo_data.models import WeiboUser
import logging,json
from django.http import Http404

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

def showtable(request):
    '''
    '''
    p={}
    fdct=[]
    ci = request.GET.get('city',None)
    style = request.GET.get('style',None)
    add=request.GET.get('add',None)
    
    (page,offset) = getPageAndOffset(request.GET)
    start = (page-1)*offset
    end = page*offset
    add_sql=""
    if add:
        add_sql=' and address <> "" '

        
    if ci and style:
        sql = 'select * from sys_weibo_user where city_name="%s" and style="%s" %s ' % (ci,style,add_sql)
        
        for item in WeiboUser.objects.raw(sql)[start:end]:
            dctMid = {}
            dctMid['id'] = item.id
            dctMid['name'] = item.name
            dctMid['url'] = item.url
            dctMid['city_name'] = item.city_name
            dctMid['style'] = item.style
            dctMid['vermicelli'] = item.vermicelli
            dctMid['state'] = item.state
            dctMid['address'] = item.address
            dctMid['longitude'] = item.longitude
            dctMid['latitude'] = item.latitude
            fdct.append(dctMid)
        p['data'] = fdct
        
    
    if ci and not style:
        sql = 'select * from sys_weibo_user where city_name="%s" %s ' % (ci,add_sql)
        
        for item in WeiboUser.objects.raw(sql)[start:end]:
            dctMid = {}
            dctMid['id'] = item.id
            dctMid['name'] = item.name
            dctMid['url'] = item.url
            dctMid['city_name'] = item.city_name
            dctMid['style'] = item.style
            dctMid['vermicelli'] = item.vermicelli
            dctMid['state'] = item.state
            dctMid['address'] = item.address
            dctMid['longitude'] = item.longitude
            dctMid['latitude'] = item.latitude
            fdct.append(dctMid)
        p['data'] = fdct
        p['sql']=sql
    
    if style and not ci:
        sql = 'select *from sys_weibo_user where style=%s %s ' % (style ,add_sql)
                
        for item in WeiboUser.objects.raw(sql)[start:end]:
            dctMid = {}
            dctMid['id'] = item.id
            dctMid['name'] = item.name
            dctMid['url'] = item.url
            dctMid['city_name'] = item.city_name
            dctMid['style'] = item.style
            dctMid['vermicelli'] = item.vermicelli
            dctMid['state'] = item.state
            dctMid['address'] = item.address
            dctMid['longitude'] = item.longitude
            dctMid['latitude'] = item.latitude
            fdct.append(dctMid)
        p['data'] = fdct
    
        
    
    return HttpResponse(json.dumps(p),mimetype='application/json')
        

def showWeibo(request):
    '''
    '''
    p={}
    fdct = []
    ci=request.GET.get('city',None)
    style=request.GET.get('style',None)
    
    if not ci and not style:
        sql = 'select id,city_name,count(city_name) as city_count from sys_weibo_user GROUP BY city_name'
        
        city={}
        city['style'] = []
        city['city']='所有城市'
#        city['count']=item.city_count
        sql2 = 'select id, style,count(style) as style_count  from sys_weibo_user  GROUP BY style'  
        
        for item2 in  WeiboUser.objects.raw(sql2):
            city['style'].append({'count':item2.style_count,'name':item2.style})
            
        fdct.append(city)

    
        p['data']=fdct
        
    if style and not ci:
        sql = 'select id,city_name,count(city_name) as city_count from sys_weibo_user where style=%s GROUP BY city_name'
        city={}
        city['style'] = []
        city['city']=style
        
        for item2 in  WeiboUser.objects.raw(sql,style):
            city['style'].append({'count':item2.city_count,'name':item2.city_name})
        
        fdct.append(city)
        p['data']=fdct
        

    
    if ci and not style:
        city={}
        city['style'] = []
        city['city']=ci
        sql = 'select id,count(*) as count from sys_weibo_user WHERE city_name=%s group by city_name'
        
        city['count']=WeiboUser.objects.raw(sql,ci)[0].count
        sql2 = 'select id, style,count(style) as style_count  from sys_weibo_user where city_name=%s GROUP BY style' 
        
        for item2 in  WeiboUser.objects.raw(sql2,ci):
            city['style'].append({'count':item2.style_count,'name':item2.style})
            
        fdct.append(city)
        p['data']=fdct
    
    if ci and style:
        sql = 'select id, style,count(style) as style_count  from sys_weibo_user where city_name=%s group by style'
        city={}
        city['style'] = []
        city['city']=ci
        
        for item2 in  WeiboUser.objects.raw(sql,ci):
            if item2.style==style:
                city['style'].append({'count':item2.style_count,'name':item2.style})
                fdct.append(city)
        p['data']=fdct                                                                                                                                                                          
        
    response = json.dumps(p)
    return HttpResponse(response,mimetype='application/json')
        

def showpage(request):
    '''
    '''
    data = {}
    data['cities'] = []
    data['cats'] = []
    sql = 'select id,city_name from sys_weibo_user group by city_name'
    sql2 = 'select id,style from sys_weibo_user group by style'
    
    for catitem in WeiboUser.objects.raw(sql):
        data['cats'].append(catitem.city_name)
        
    for cititems in WeiboUser.objects.raw(sql2):
        data['cities'].append(cititems.style)
#    return HttpResponse(json.dumps(data),mimetype='application/json')
    
    return render_to_response('showWeibo.html',data)

