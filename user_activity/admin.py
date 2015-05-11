#coding:utf-8
from django.contrib import admin
 
from models import UserInfo,UserEventMessage 
from spot.models import   SysSpotTxt
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template.response import  TemplateResponse
from admin_self.froms import AdminEnhancedFKRawIdWidget,dhdAdmin
from  user_activity.functions import admin_black_message
import time

 
from django import forms

class CategoryAdmin(dhdAdmin):
    
    def Message(self, obj):
        try:
            return '%s:%s' % (obj.begin_time,obj.message.txt)
        except:
            return ''
    
    Message.short_description = u'留言'
    Message.allow_tags = True
    #Message.admin_order_field = 'end_time'  
    
    #form = CategoryForm
    
    def event_info(self,obj):
        
        try:
            return obj.event.event_name
        except:
            return ''
    def black_msg(self,obj):
        try:
            return '%s (%s)' % (obj.black_message.message.txt,obj.black_message.begin_time)
        except:
            return ''
    black_msg.short_description = u'回复'
    black_msg.allow_tags = True
    
    event_info.short_description = u'活动'
    event_info.allow_tags = True
    #event_info.admin_order_field = 'end_time'  
    list_display = ('id','treenode', 'black_msg','event_info', 'examine','path')
    #list_display = ['id', 'Message', 'treenode','path', 'direct_link', 'has_keywords', 'has_description', ]

    ordering = ['path']

    list_per_page = 1000

    raw_id_fields = ['black_message','event','message' ]
    #raw_id_fields = ['event']

    list_filter = ['examine',]
    list_editable=( 'examine',)
    date_hierarchy = 'end_time'

    

     


    def treenode(self, obj):

        indent_num = len(obj.path.split(':')) -1

        p = '<div style="text-indent:%spx;">%s (%s)</div>' % (indent_num*25,obj.message.txt,obj.begin_time)

        return p

    treenode.short_description = '留言'

    treenode.allow_tags = True
    
    def save_model(self, request, obj, form, change):
        
        obj.path=obj.id
        obj.save()
        try:
            content=request.POST.get("content",'')  
            if content:        
                admin_black_message(obj.id,content,int(time.time()),99999,'大活动客服','活动小管家',True)
        except:
            pass
        
        #if obj.spot_edit=='':
            #pass
        
    

class userAdmin(admin.ModelAdmin):
    raw_id_fields = ['event' ]

 

admin.site.register(UserInfo,userAdmin) 
admin.site.register(UserEventMessage,CategoryAdmin )