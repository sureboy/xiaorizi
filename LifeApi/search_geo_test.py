#!coding=utf-8
import re
import math
import json

from django.http import HttpResponse
from LifeApi.functions import getevent
from LifeApi.common import getPageAndOffset

import sphinxapi

def search_dis(lat, lon, kw='', radius=10000.):
    '''
    search from NewEventTable by the circle
    whose center is ('lat', 'lon'), half radius is 'radius'
    lat & lon: float; unit:radians
    radius: float; unit:meter
    '''
    
    cl = sphinxapi.SphinxClient()
    cl.SetServer('10.10.43.180',9313)
    cl.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED)
    #cl.SetMatchMode(sphinxapi.SPH_MATCH_FULLSCAN)
    cl.SetGeoAnchor('lat', 'lon', lat, lon)
    cl.SetSortMode(sphinxapi.SPH_SORT_EXTENDED, '@geodist asc')
    cl.SetFilterFloatRange('@geodist', 0.0, radius)
    cl.SetLimits(0,100)
    res = cl.Query(kw, '*')

    if res.has_key('matches'):
        return [match["id"] for match in res['matches']]
    else:
        return []

def search_geo(request):
    var = {}
    var['code'] = 1
    var['msg'] = ''
    var['list'] = []
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    kw = request.GET.get('keywords', '')
    radius = float(request.GET.get('rad', 10000.))

    (page,offset) = getPageAndOffset(request.GET)
    start = (page-1)*offset
    end = page*offset

    if kw:
        kw = re.sub(r'[-~!@#$%^&*()_=+\[\]{};\':",.<>/?]+', ' ', kw)
    kw = '|'.join(kw.split())

    if lat and lon:
        lat = math.radians(float(lat))
        lon = math.radians(float(lon))
        ids = search_dis(lat, lon, kw, radius)
        var['list'] = [getevent(old_id,
                                request.GET.get('new',False),
                                request.GET.get('version',''))
                                for old_id in ids[start:end]]
    else:
        var['msg'] = u'没有经纬度'

    return HttpResponse(json.dumps(var), content_type="application/json")
    
