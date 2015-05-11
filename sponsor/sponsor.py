#! -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from models import NewSponsor
#import datetime
from django.utils import timezone
import json
import boring_encode as mess
from admin_self.common import NewformatEvent
from LifeApi.models import NewOrderMessage
import time
import common

#主办方 浏览
def view_sponsor(request, mess_string):
    try:
        s = NewSponsor.objects.get(pk=mess.decode(mess_string))
    except ObjectDoesNotExist:
        s = None

    head = {}
    head['title'] = u"未找到指定主办方"

    if s is None:
        events = None
        old_events = None
    else:
        s.intro = s.intro.replace('\n', '<br/>')
        if s.like_count == None:
            s.like_count = 0
        try:
            s.pic_url = s.pic.server.name + s.pic.urls
        except AttributeError:
            s.pic_url = ""

        def calculate(e):
            """
            try:
                #只选取第一个关联地址为展示的地址
                e.place = e.city.all()[0].district_name
            except IndexError:
                e.place = ""
            if e.begin_time and e.end_time:
                e.time_range = str(e.begin_time.month) + "." + str(e.begin_time.day) + "-" + str(e.end_time.day)
            else:
                e.time_range = ''
            return e
            """
            return NewformatEvent(None, e.old_event_id)

        #now = datetime.datetime.now()
        now = timezone.now()
        #检索所有未过期活动，性能假设：每年活动不超过50个
        new_events = s.events.filter(end_time__gt=now) \
                            .filter(isshow_id__in=[1, 8]) \
                            .all().order_by('begin_time')
        events = map(calculate, new_events)
        #检索所有过期活动，可能会过滤一部分
        old_events = map(calculate, s.events.filter(end_time__lt=now) \
                                            .filter(isshow_id__in=[1, 8]) \
                                            .all().order_by('begin_time') \
                                            .reverse())
        s.event_count = s.events.count()

        head = common.sponsor_page_head(s.name, s.intro)

    return render_to_response( \
        'sponsor.html', \
        {'sponsor': s, 'events': events, \
		'old_events': old_events, 'head': head}, \
        context_instance=RequestContext(request)
        )

#主办方 点赞 api
#返回json
def like_sponsor(request, mess_string):
    try:
        s = NewSponsor.objects.get(pk=mess.decode(mess_string))
    except ObjectDoesNotExist:
        s = None
    result = {}
    if s is None:
        result['success'] = False
    else:
        if s.like_count == None:
            s.like_count = 0
        s.like_count += 1
        s.save()
        result['success'] = True
        result['like'] = s.like_count
    return HttpResponse(json.dumps(result))


#主办方 认领 api
#返回json
def claim_sponsor(request, mess_string):
    sponsor_id = mess.decode(mess_string)
    try:
        s = NewSponsor.objects.get(pk=sponsor_id)
    except ObjectDoesNotExist:
        s = None
    result = {}
    name = request.POST.get('name', None)
    cellphone = request.POST.get('cellphone', None)
    email = request.POST.get('email', None)
    message = request.POST.get('message', None)
    if not s or \
    not name or \
    not cellphone or \
    not email or \
    not message:
        result['success'] = False
    else:
        NewOrderMessage.objects.create(event_id = sponsor_id, \
                                        event_name = s.name, \
                                        msg_name = name, \
                                        msg_tel = cellphone, \
                                        msg_email = email, \
                                        msg_content = message, \
                                        msg_addtime = time.time(), \
                                        type=6)
        result['success'] = True
    return HttpResponse(json.dumps(result))
