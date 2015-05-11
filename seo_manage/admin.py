#coding:utf-8
from django.contrib import admin
from models import SiteInfo,PostSeoInfo,FriendlyLink
from admin_self.common import get_site_links

class SiteInfoAdmin(admin.ModelAdmin):
    list_display =['name','url','event_count','site_cat','create_time','edit']
    fields=['name','url','site_cat']
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'edit', None) is None:
            obj.edit = request.user
        
        obj.save()
    
    
    pass
'''
class PriceType(admin.SimpleListFilter):
    title = (u'销售状态') 
    parameter_name = 'price_type'
    def lookups(self, request, model_admin):
        return [(pt.id,pt.name) for pt in NewEventPriceType.objects.all()]
        
        return (
            (0, u'未开始'),
            (1, u'未过期'),
            (2, u'已经过期'),
        )
       
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():            
            return queryset.filter(Price__Type=self.value())           

'''
class PostSeoInfoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'edit', None) is None:
            obj.edit = request.user
        obj.last_edit = request.user
        obj.save()
    
    def show_url(self,obj):
        str=''
        if obj.event:
            if obj.event.old_event:
                str+=u'<a href="http://www.huodongjia.com/event-%s.html" target="_blank">%s</a>' % (obj.event.old_event_id,obj.event.name)
            else:
                str+=u'<a href="http://www.huodongjia.com/event-%s.html" target="_blank">%s</a>' % (obj.event.id,obj.event.name)
        
            str+='<br >'
            str+=u'<a href="/admin/new_event/neweventtable/%s/" target="_blank">%s</a>' % (obj.event.id,obj.event.old_event_id if obj.event.old_event else obj.event.id)
        return str
    show_url.short_description = u'页面预览'   
    show_url.allow_tags = True 
    
 
    #/admin/new_event/oldevent/%s/
    def show_site_url(self,obj):
        return u'<a href="%s" target="_blank">%s</a>' % (obj.site_url,obj.site_url)
    show_site_url.short_description = u'链接地址'   
    show_site_url.allow_tags = True         
  
    
    def site_show(self,obj):    
        if obj.site:
            return u'<a href="%s" target="_blank">%s</a>' % (obj.site.url,obj.site.name)
        else:
            return ''
    site_show.short_description = u'网站'
    site_show.allow_tags = True    
    
    list_editable=( 'status','baidu_include','u360_include','google_include' )
    raw_id_fields = ['event']
    list_display =['site_show','show_url', 'show_site_url','create_time','rel_time','edit','last_edit','status','baidu_include','u360_include','google_include']
    fields = ('site_url','event','site','status','baidu_include','u360_include','google_include')
    list_filter = ['status','site','site__site_cat','edit','last_edit','baidu_include','u360_include','google_include']
    search_fields = ('event__name','site_url','site__name')
    
    
class FriendlyLinkAdmin(admin.ModelAdmin):
    def city_show(self,obj):    
        str=''
        for ci in  obj.city.all():
            if str:
                str+='<br>'
            str+= u'%s' % (ci.district_name)
        #else:
        return str
    def cat_show(self,obj):    
        str=''
        for ci in  obj.cat.all():
            if str:
                str+='<br>'
            str+= u'%s' % (ci.name)
        #else:
        return str
    city_show.short_description = u'城市'
    city_show.allow_tags = True    
    raw_id_fields = ['city', 'cat']
    list_display =['name','url','order','img','page','city_show','cat_show','hot']
    list_editable=['order']
    search_fields=('name','url',)
    def save_model(self, request, obj, form, change):
        obj.save()
        get_site_links(True)
        
    
    
admin.site.register(SiteInfo,SiteInfoAdmin )
admin.site.register(PostSeoInfo, PostSeoInfoAdmin)
admin.site.register(FriendlyLink, FriendlyLinkAdmin)
