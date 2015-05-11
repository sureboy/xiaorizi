#! -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from LifeApi.models import NewVenue
#import datetime
from django.utils import timezone
import json
import boring_encode as mess
from admin_self.common import NewformatEvent
import common


#场馆 浏览
def view_venue(request, mess_string):
    try:
        v = NewVenue.objects.get(pk=mess.decode(mess_string))
    except ObjectDoesNotExist:
        v = None

    head = {}
    head['title'] = u"未找到指定场馆"

    if v is None:
        events = None
        old_events = None
    else:
        if v.content is not None:
            v.content = v.content.replace('\n', '<br/>')
        else:
            v.content = ''
        '''
        try:
            s.pic_url = s.pic.server.name + s.pic.urls
        except AttributeError:
            s.pic_url = ""
        '''
        def calculate(e):
            return NewformatEvent(None, e.old_event_id)

        now = timezone.now()
        #检索所有未过期活动，性能假设：每年活动不超过50个
        new_events = v.neweventtable_set.filter(end_time__gt=now) \
                                        .filter(isshow_id__in=[1, 8]) \
                                        .all().order_by('begin_time')

        events = map(calculate, new_events)
        #检索所有过期活动，可能会过滤一部分
        old_events = map(calculate, \
                v.neweventtable_set.filter(end_time__lt=now) \
                .filter(end_time__gte='2014-01-01') \
                .filter(isshow_id__in=[1, 8]) \
                .all().order_by('begin_time') \
                .reverse())

        head = common.venue_page_head(v.title, v.content)

    return render_to_response( \
        'venue.html', \
        {'venue': v, 'events': events, \
		'old_events': old_events, 'head': head}, \
        context_instance=RequestContext(request)
        )

