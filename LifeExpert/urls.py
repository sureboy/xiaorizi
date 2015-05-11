from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LifeExpert.views.home', name='home'),
    # url(r'^LifeExpert/', include('LifeExpert.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$','app_manage.views.downAppPage',{'param':'xiaorizi.html'}),    
    url(r'^api/leavemessage/$',view = 'user_activity.app_message_api.get_message',),
    url(r'^api/getusermessage/$',view = 'user_activity.app_message_api.get_user_message',),
    url(r'^api/geteventmessage/$',view = 'user_activity.app_message_api.get_event_message',),
    url(r'^api/',include('LifeApi.urls')),
    url(r'^api/',include('Ticket.urls')),
    url(r'^user/usercollect/$',view = 'user_activity.app_message_api.get_user_collect',),
    
    url(r'^user/',include('User.urls')),
    url(r'^version/',include('app_manage.urls')),
    url(r'^ticket/',include('Ticket.urls')),
    url(r'^app/download','app_manage.views.downAppPage',{'param':'qrcodedownload.html'}),
    url(r'^app/',include('app_manage.urls')),
    url(r'^app/$','app_manage.views.downApp'),
    url(r'^weibo/',include('weibo_data.urls')),
)
