#coding:utf-8
from django.contrib import admin
from weibo_data.models import WeiboUser
class WeiboUserAdmin(admin.ModelAdmin):
    def show_url(self,obj):
        str=''
        if obj.url:
            str+='<a href="%s"    target="_blank"  >%s</a><br>' % (obj.url,obj.url,)
        return str
    show_url.short_description = u'网址'
    show_url.allow_tags = True
    search_fields = ('name','city_name','style',)
    list_filter = ['city_name','style',]
    list_display = ('name', 'show_url', 'city_name','style','ischeck')
    list_editable=('ischeck',)
 
admin.site.register(WeiboUser,WeiboUserAdmin) 
