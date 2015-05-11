#! -*- coding:utf-8 -*-
from django.contrib import admin
from models import NewSponsor, ImageAds
from LifeApi.models_admin import NewVenue
import boring_encode as mess
from common import update_image_ads

class SponsorAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'edit', None) is None:
            obj.edit = request.user
        obj.last_edit = request.user
        obj.save()


    def show_url(self, obj):
        mess_str = mess.encode(int(obj.id), 6)
        return u'<a href="http://www.huodongjia.com/sponsor-%s.html" target="_blank">跳转</a>' \
            % (mess_str)

    show_url.short_description = u'页面预览'
    show_url.allow_tags = True

    
    def other_url(self, obj):
        mess_str = mess.encode(int(obj.id), 6)
        return u'<a href="http://www.huodongjia.com/sponsor-%s-dig.html?action=count" target="_blank">关系发现</a>' \
            % (mess_str)

    other_url.short_description = u'其他功能'
    other_url.allow_tags = True

    def events_info(self, obj):
        result = []
        for event in obj.events.all():
            result.append(event.name)
        return u'%s' % ('<br/>'.join(result))

    events_info.short_description = u'关联活动'
    events_info.allow_tags = True

    def from_info(self, obj):
        result = []
        for f in obj.event_from.all():
            result.append(str(f.id))
        return u'%s' % ('<br/>'.join(result))

    from_info.short_description = u'关联来源'
    from_info.allow_tags = True

    exclude = ('like_count', 'event_count', 'edit', 'last_edit', 'feature')
    raw_id_fields = ['pic', 'event_from', 'events']
    list_display = ['id', 'name', 'show_url', 'edit', 'last_edit', \
            'events_info', 'from_info', 'other_url']

class VenueAdmin(admin.ModelAdmin):
    def show_url(self, obj):
        mess_str = mess.encode(int(obj.id), 6)
        return u'<a href="http://www.huodongjia.com/venue-%s.html" target="_blank">%s</a>' \
            % (mess_str, mess_str)

    show_url.short_description = u'页面预览'
    show_url.allow_tags = True

    list_display = ['id', 'title', 'address', 'show_url']

class ImageAdsAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'edit', None) is None:
            obj.edit = request.user
        obj.last_edit = request.user
        obj.save()
        update_image_ads(obj.position)

    def image_preview(self, obj):
        try:
            pic_url = obj.pic.server.name + obj.pic.urls
        except AttributeError:
            if obj.pic is not None:
                pic_url = u"http://pic1.qkan.com/" + obj.pic.urls
            else:
                pic_url = u""

        return u'<img src="%s" width="500"/>' \
            % (pic_url)

    image_preview.short_description = u'图片广告预览'
    image_preview.allow_tags = True

    exclude = ('edit', 'last_edit')
    raw_id_fields = ['pic', 'edit', 'last_edit']
    list_display = ['id', 'state', 'position', 'rank', 'title', 'url', \
            'image_preview', 'edit', 'last_edit']

admin.site.register(NewSponsor, SponsorAdmin)
admin.site.register(ImageAds, ImageAdsAdmin)
#admin.site.register(NewVenue, VenueAdmin)
