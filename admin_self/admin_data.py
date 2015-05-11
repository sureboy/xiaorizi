#coding:utf-8
import django.contrib.admin as admin

class adminVenueClass(admin.ModelAdmin):
    fields =('name',)
    search_fields = ('name',)
    list_display = ['id','name','venue_count','event_count']
    

