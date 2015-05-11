#! -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from models import NewSponsor
from django.utils import timezone
import json
import boring_encode as mess
from contact_picker import contact_picker
from sponsor_feature import sponsor_feature
from LifeApi.models import NewEventTable, NewEventFrom
from django.core.cache import cache

#显示
def dig_show_sponsor(request, mess_string):
    sponsor_id = mess.decode(mess_string)
    #从缓存中读取主办方信息
    is_cached = True
    #
    s = cache.get('dig_sponsor_%d' % sponsor_id)
    if not s:
        #缓存标志
        is_cached = False
        try:
            s = NewSponsor.objects.get(pk=sponsor_id)
        except ObjectDoesNotExist:
            s = None

    e = {}
    events = None
    old_events = None
    possible_event_from = []
    froms = None
    if s is not None:
        action = request.REQUEST.get('action', None)
        if action == 'count' and not is_cached:
            #关系发现
            #
            #
            #
            #检索所有
            all_events = s.events.all()
            events = all_events
            #关联的来源
            froms = s.event_from.all()

            f_visited = []
            #根据关联来源生成主办方特征
            sf = sponsor_feature()
            picker = contact_picker()
            picker.init_char_set()
            for f in froms:
                res = picker.pick(f.content)
                for email in res[contact_picker.email_address]:
                    sf.add_item('email', email)
                for phone in res[contact_picker.phone_number]:
                    sf.add_item('phone', phone)
                f_visited.append(f.id)
            
            s.feature = unicode(sf)
            s.save()

            #匹配所有的来源
            for f in NewEventFrom.objects.all():
                if f.id in f_visited:
                    continue
                
                res = picker.pick(f.content)
                sf_f = sponsor_feature()
                for email in res[contact_picker.email_address]:
                    sf_f.add_item('email', email)
                for phone in res[contact_picker.phone_number]:
                    sf_f.add_item('phone', phone)

                if sf.similarity(sf_f) >= 0.5:
                    possible_event_from.append(f)
                f_visited.append(f.id)

            #取出可能来源的相关活动
            def show_linked_event(froms):
                for f in froms:
                    f.linked_event = []
                    for le in f.neweventtable_set.all():
                        f.linked_event.append(le)

            show_linked_event(froms)
            show_linked_event(possible_event_from)
            e['content'] = json.dumps(s.feature)

        elif action == 'count':
            if is_cached:
                e =  cache.get('dig_sponsor_env_%d' % sponsor_id)
                events =  cache.get('dig_sponsor_events_%d' % sponsor_id)
                froms =  cache.get('dig_sponsor_froms_%d' % sponsor_id)
                possible_event_from = cache.get('dig_sponsor_pef_%d' % sponsor_id)

        e['target'] = s.name
        #e['content'] = s.intro

    e['title'] = 'dig system' 
    
    #进行缓存，前提是没有缓存，以及主办方存在
    if not is_cached and s:
        timeout = 60 * 5
        cache.set('dig_sponsor_%d' % sponsor_id, s, timeout)
        cache.set('dig_sponsor_env_%d' % sponsor_id, e, timeout)
        cache.set('dig_sponsor_events_%d' % sponsor_id, events, timeout)
        cache.set('dig_sponsor_froms_%d' % sponsor_id, froms, timeout)
        cache.set('dig_sponsor_pef_%d' % sponsor_id, possible_event_from, timeout)

    return render_to_response( \
        'dashboard.html', \
        {'env': e, 'events': events, 'froms': froms,\
        'possible_froms': possible_event_from}, \
        context_instance=RequestContext(request)
        )

#
def like_sponsor(request, mess_string):
    try:
        s = NewSponsor.objects.get(pk=mess.decode(mess_string))
        s.pic_url = s.pic.urls
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
    return HttpResponse(json.dumps(result), mimetype="application/json")
