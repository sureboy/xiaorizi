# -*- coding:utf-8 -*-
__author__ = 'sooshian'
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from LifeApi.models import NewEventCat, NewDistrict
from seo_manage.models import FriendlyLink
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, RequestContext

# #####################################
# 自动化脚本 页面
# #####################################
# 批量添加友情链接 -
#
@csrf_exempt
def add_friendly_link(request):

    '''
    place = request.GET.get("city")

    all_city = NewDistrict.objects.all()

    result = [ {'name': city.district_name, 'title': city.title } for city in all_city \
               if city.district_name in place or place in city.district_name]
    return HttpResponse(json.dumps(result), mimetype="application/json")
    '''
    if request.method == 'GET':
        result = '''
           <form method='post'>
            请将需要批量添加的友情链接数据在excel中按照如下顺序排列好。然后全选复制后粘贴到下面的文本框中。<br/>
            <span>名称</span>
            <span>URL</span>
            <span>城市(可选)</span>
            <span>分类(可选)</span>
            <br/>
            <textarea name='data' rows="30" cols="150"></textarea>
            <br/><br/><input type="checkbox" name="scan" />勾选则进行城市搜索<br/>
            <input type='submit' />
           </form>
        '''
        return HttpResponse(result)

    elif request.method == 'POST':
        record_line = request.POST.get('num')
        if record_line is None:

            # 新功能 检测是否存在城市
            scan = request.POST.get("scan")
            scan = bool(scan) if scan else False
            if scan:
                # 处理数据
                data = request.POST.get('data')
                result = data.split('\r\n')
                response = []
                # 判断城市是否有冲突
                all_city_list = list(NewDistrict.objects.all())
                for line in result:
                    #line = line.replace('\r', '')
                    if line == '':
                        continue
                    query = [{'name': city.district_name, 'url': 'http://www.huodongjia.com/' + city.title + '/' if city.title else ""} for city in all_city_list \
                             if city.district_name in line or line in city.district_name]
                    response.append({'result': query, 'input': line})
                #return HttpResponse(json.dumps({'result': response, 'input': result, 'origin': [ord(c) for c in data]}))
                return render_to_response( \
                        'friendlylink_scan.html', \
                        {'data': response},\
                        context_instance=RequestContext(request)
                        )


            # 处理数据
            data = request.POST.get('data')
            result = []
            num = 0
            for line in data.split('\n'):
                result.append(line.split())

            # 判断城市是否有冲突
            all_city_list = list(NewDistrict.objects.all())
            for record in result:
                if len(record) != 4:
                    #record.append('error')
                    #break
                    # 如果没有城市数据
                    record.append('')
                    # 如果没有分类数据
                    record.append('')
                    if len(record) != 4:
                        continue

                place = record[2]
                # 如果存在城市，则搜索
                if place:
                    query = [{'name': city.district_name, 'id': city.id } for city in all_city_list \
                             if city.district_name in place or place in city.district_name]

                    record[2] = query
                # 如果存在分类，则搜索
                cat = record[3]
                if cat:
                    q_cat = NewEventCat.objects.filter(name__contains=cat)
                    cat_list = [{'name': cat.name, 'id': cat.id} for cat in q_cat]
                    record[3] = cat_list
                num += 1
            # 返回
            response = []
            for i, record in enumerate(result):
                if len(record) != 4:
                    continue
                city = record[2]
                cat = record[3]
                response.append({'index': i, 'name':record[0] , 'url': record[1], \
                                                   'city': city, 'cat': cat, \
                                                   'city_choose': len(city) != 1, 'cat_choose': len(cat) != 1})

            return render_to_response( \
                'friendlylink.html', \
                {'num': num, 'data': response},\
                context_instance=RequestContext(request)
                )
        else:
            # 数据确认
            data = []
            for i in range(int(record_line)):
                index = str(i)
                data.append({'name': request.POST.get('name_' + index),
                             'url': request.POST.get('url_' + index),
                             'city_id': request.POST.get('city_' + index),
                             'cat_id': request.POST.get('cat_' + index)})
            existed = []
            for d in data:
                # 先判断重复没有
                try:
                    f = FriendlyLink.objects.get(name=d['name'])
                    existed.append(f)
                except ObjectDoesNotExist:
                    # 不存在则添加
                    f = FriendlyLink()
                    f.name = d['name']
                    f.url = d['url']

                    f.save()
                    # 由于数据库读写分离了，所以添加关系的时候两个实体的实例应该以同一方式加载
                    # 因为c是从read中读出来的，而f是新创建的，以write的形式存在，所以要先保存然后再以read的形式读出来
                    # 所以read_f就是read形式的f
                    # 不然会报 Cannot add <NewDistrict > instance is on database "default"  value is on database "slave" 的错
                    read_f = FriendlyLink.objects.get(pk=f.id)

                    if d['city_id']:
                        try:
                            c = NewDistrict.objects.get(pk=d['city_id'])
                        except ObjectDoesNotExist:
                            continue
                        read_f.city.add(c)
                        read_f.save()
                    if d['cat_id']:
                        try:
                            c = NewEventCat.objects.get(pk=d['cat_id'])
                        except ObjectDoesNotExist:
                            continue
                        read_f.cat.add(c)
                        read_f.save()

            return render_to_response( \
                'friendlylink_result.html', \
                {'success_num': len(data) - len(existed),\
                 'fail_num': len(existed),\
                 'fail': len(existed) != 0, \
                 'existed_data': existed},\
                context_instance=RequestContext(request)
                )


        return HttpResponse(json.dumps(result))
