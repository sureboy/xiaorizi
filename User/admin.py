#coding:utf-8
from django.contrib import admin
from User.models import Customer, Address  ,UserPushInfo

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email',
                    'register_time', 'last_login_time', 'is_temporary')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'address_name', 'name', 
                    'phone', 'user', 'default')
    

class UserPushInfoAdmin(admin.ModelAdmin):
    def event_list(self,obj):
        return   '<br>'.join(['<a href="/admin/new_event/neweventtable/%s"  target="_blank"  >%s</a>' % (ev.id,ev.name,) for ev in obj.event.all()  ])
     
    event_list.short_description =  u'活动'    
    event_list.allow_tags = True 
    #event_list.admin_order_field = 'create_time'     
    
    raw_id_fields=['event']
    list_display=['user','push_user', 'create_time','rel_time','app_type','event_list']
    search_fields = ('push_user','event__id','event__old_event__event_id','event__name','user__id' ,'user__name')
    
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserPushInfo, UserPushInfoAdmin)

