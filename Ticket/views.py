# -*- coding:utf-8 -*-
from django.shortcuts import render


# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson as json
from LifeApi.views import submitOrder_with_coupon
from User.models import Customer
from django.core.exceptions import ObjectDoesNotExist
from models import Coupon, CouponRecord, CouponOwnRecord
from LifeApi.models import NewEventTable
from LifeApi.common import getPageAndOffset
import datetime
from LifeApi.functions import getevent
# 优惠券逻辑
def check_coupon(coupon_id, event_id, user_id, price):
    '''
    :param coupon_id:
    :param event_id:
    :param user_id:
    :param price: 总价，非单价
    :return: 返回折后价格 0-N 为正确使用 -1 表示不可用
    '''
    try:
        c = Coupon.objects.get(pk=coupon_id)
    except ObjectDoesNotExist:
        return -1
    try:
        e = NewEventTable.objects.get(pk=event_id)
    except ObjectDoesNotExist:
        return -1
    try:
        u = Customer.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return -1

    '''
    # 成功使用，从持有集合中删除用户，使用集合中添加事件。
    # 若订单没有付款，
    c.used_for.add(e)
    c.owners.remove(u)
    c.save()
    '''
    # 检查是否适用
    state = c.is_general or e in c.for_events.all()
    if not state:
        return -1

    # 检查是否持有
    '''
    state = u in c.owners.all()
    if not state:
        return -1
    '''
    own_record = CouponOwnRecord.objects.filter(coupon_id=coupon_id).filter(customer_id=user_id)
    if len(own_record) == 0 or own_record[0].amount == 0:
        return -1

    old = price

    # 时间检查

    # 不同的优惠券类型有不同的检查条件
    if c.coupon_type == 1:
        # 抵价券
        if price >= c.cost_threshold:
            price -= c.coupon_value

    if c.coupon_type == 2:
        # 免费体验券
        price = 0

    #  创建记录
    cr = CouponRecord()
    cr.coupon_id = coupon_id
    cr.customer_id = user_id
    cr.event_id = event_id
    cr.price = old
    cr.cost = price
    cr.time = datetime.date.today()
    cr.valid = False
    cr.save()

    # c.owners.remove(u)
    own_record[0].amount -= 1
    own_record[0].save()

    return cr


# 优惠券使用
def coupon_use(request):
    coupon_id = request.GET.get('coupon_id')
    event_id = request.GET.get('eventid')
    user_id = request.GET.get('userid')
    price = request.GET.get('price')
    amount = request.GET.get('amount')
    if not coupon_id or not event_id or not user_id or not price or not amount:
        return HttpResponse(json.dumps({'code': 0, 'msg': 'Lost some parameter'}), content_type="application/json")

    # 验证是否有效
    coupon_id = int(coupon_id)
    event_id = int(event_id)
    user_id = int(user_id)
    price = round( float(price),2)
    amount = int(amount)

    coupon_record = check_coupon(coupon_id, event_id, user_id, price * amount)
    if coupon_record == -1:
        return HttpResponse(json.dumps({'code': 0, 'msg': 'Coupon can not be used'}), content_type="application/json")

    # 调用提交订单
    return submitOrder_with_coupon(request, coupon_record)


# 获取优惠券
def coupon_get(request):
    coupon_id = request.GET.get('coupon_id')
    customer_id = request.GET.get('customer_id')
    if not coupon_id or not customer_id:
        return HttpResponse(json.dumps({'code': 0, 'msg': 'Lost some parameter'}), content_type="application/json")

    # 检查优惠券是否存在
    # 检查用户是否存在
    # 检查领取条件
    # 检查是否已经存在记录
    orrd = CouponOwnRecord.objects.filter(coupon_id=coupon_id).filter(customer_id=customer_id)
    if len(orrd) == 0:
        orrd = CouponOwnRecord()
        orrd.customer_id = customer_id
        orrd.coupon_id = coupon_id
        orrd.amount = 0
        # 日期计算
    else:
        orrd = orrd[0]

    orrd.amount += 1
    orrd.save()

    return HttpResponse(json.dumps({'code': 1, 'msg': 'Get!'}), content_type="application/json")

def get_format_coupon(c):
    r = dict()
    r['id'] = c.id
    # 映射 2 -> 0  别问我0怎么办，废了
    r['coupon_type'] =0 if c.coupon_type == 2 else c.coupon_type 
    r['coupon_value'] = c.coupon_value
    r['begin_time'] =datetime.datetime.strftime(c.begin_time,'%Y-%m-%d') if c.begin_time else '' 
    r['end_time'] =datetime.datetime.strftime(c.end_time,'%Y-%m-%d') if c.end_time else ''  
    r['is_general'] = c.is_general
    r['range_comment'] = c.range_comment  if c.range_comment else 0
    r['cost_threshold'] = c.cost_threshold if c.cost_threshold else 0
    r['events'] = list()
    for event in c.for_events.all():
        e = dict()
        e['id'] = event.id
        e['title'] = event.name

        r['events'].append(e)
    return r
def get_event_format(c):
    r = dict()
    r['id'] = c.id
    # 映射 2 -> 0  别问我0怎么办，废了
    r['coupon_type'] = 0 if c.coupon_type == 2 else c.coupon_type 
    r['coupon_value'] = c.coupon_value
    r['start_time'] =datetime.datetime.strftime(c.begin_time,'%Y-%m-%d') if c.begin_time else '' 
    r['end_time'] =datetime.datetime.strftime(c.end_time,'%Y-%m-%d') if c.end_time else ''  
    r['is_general'] = c.is_general
    r['range_comment'] = c.range_comment if c.range_comment else 0
    r['cost_threshold'] = c.cost_threshold if c.cost_threshold else 0
    if c.is_general:
        return r
    events= list()
    for event in c.for_events.all():
        ev_r={}
        ev_r=r
        ev_r['event']=getevent(event.old_event_id)
        
        events.append(ev_r)
    return events
    
# 获取个人优惠券信息
# 无查询条件时候返回限定数量信息
def coupon_mine(request):
    customer_id = request.GET.get('customer_id')
    (page,offset) = getPageAndOffset(request.GET)
    out=[]
    if not customer_id:
        all_coupon =Coupon.objects
        phone= request.GET.get('phone')
        if phone:
            #all_coupon=all_coupon.filter(owners__phone=phone)
            try:
                customer_id = Customer.objects.get(phone=phone).id
            except ObjectDoesNotExist:
                return HttpResponse(json.dumps({'code': 0, 'msg': 'phone number is not exist'}), content_type="application/json")
            all_coupon = []
            own_record = CouponOwnRecord.objects.filter(customer_id=customer_id)
            for record in own_record:
                try:
                    all_coupon.append(Coupon.objects.get(pk=record.coupon_id))
                except ObjectDoesNotExist:
                    pass
        else:
            all_coupon=all_coupon.all()
        
        for cou in all_coupon[offset*(page-1):offset*page]:
            co=get_event_format(cou)
            if type(co)==list:
                out.extend(co)
            else:
                out.append(co)
                
        #out =map(get_event_format, all_coupon[offset*(page-1):offset*page])
        #return HttpResponse(json.dumps({'code': 0, 'msg': 'No customer_id parameter'}), content_type="application/json")
    else:
        #all_coupon = Coupon.objects.filter(owners__in=[int(customer_id)])[offset*(page-1):offset*page]
        all_coupon = []
        own_record = CouponOwnRecord.objects.filter(customer_id=customer_id)
        for record in own_record:
            try:
                all_coupon.append(Coupon.objects.get(pk=record.coupon_id))
            except ObjectDoesNotExist:
                pass
        #out =map(get_event_format, all_coupon[offset*(page-1):offset*page])
        for cou in all_coupon[offset*(page-1):offset*page]:
            co=get_event_format(cou)
            if type(co)==list:
                out.extend(co)
            else:
                out.append(co)
    # 格式化

    count = len(all_coupon) if isinstance(all_coupon, list) else all_coupon.count()
    return HttpResponse(json.dumps({'code': 1, 'msg': '', 'list': out,'count': count}), content_type="application/json")