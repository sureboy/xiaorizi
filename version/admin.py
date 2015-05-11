#coding:utf-8
from django.contrib import admin
from version.models import AppVersion
class AppVersionAdmin(admin.ModelAdmin):
    pass
    list_display = ('id','platform', 'must_update','version', 'url','update_info','update_time')
    #list_editable=( 'platform', 'must_update','version', 'url','update_info','update_time')
    

admin.site.register(AppVersion,AppVersionAdmin) 
