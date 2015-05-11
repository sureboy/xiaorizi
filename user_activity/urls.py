from django.conf.urls import patterns, url

urlpatterns = patterns('',


    url(r'^post_message/(?P<eventid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/(?P<username>[\S\s-]+)/(?P<userfrom>[\S\s-]+)/$', 'user_activity.app_message_api.get_message', name='get_json'),
    url(r'^post_message/(?P<eventid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/(?P<username>[\S\s-]+)/$', 'user_activity.app_message_api.get_message', name='get_json'),
    url(r'^post_message/(?P<eventid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/$', 'user_activity.app_message_api.get_message', name='get_json'),
    url(r'^post_message/(?P<eventid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/(?P<username>[\S\s-]+)/(?P<userfrom>[\S\s-]+)$', 'user_activity.app_message_api.get_message', name='get_json'),
    url(r'^post_message/(?P<eventid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/(?P<username>[\S\s-]+)$', 'user_activity.app_message_api.get_message', name='get_json'),
    url(r'^post_message/(?P<eventid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)$', 'user_activity.app_message_api.get_message', name='get_json'),


    url(r'^post_an_message/(?P<messageid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/(?P<username>[\S\s-]+)/(?P<userfrom>[\S\s-]+)/$', 'user_activity.app_message_api.get_an_message', name='get_json'),
    url(r'^post_an_message/(?P<messageid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/(?P<username>[\S\s-]+)/$', 'user_activity.app_message_api.get_an_message', name='get_json'),
    url(r'^post_an_message/(?P<messageid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/$', 'user_activity.app_message_api.get_an_message', name='get_json'),
    url(r'^post_an_message/(?P<messageid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/(?P<username>[\S\s-]+)/(?P<userfrom>[\S\s-]+)$', 'user_activity.app_message_api.get_an_message', name='get_json'),
    url(r'^post_an_message/(?P<messageid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/(?P<username>[\S\s-]+)$', 'user_activity.app_message_api.get_an_message', name='get_json'),
    url(r'^post_an_message/(?P<messageid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)$', 'user_activity.app_message_api.get_an_message', name='get_json'),
 
    url(r'^adm_message/(?P<messageid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/(?P<username>[\S\s-]+)/(?P<userfrom>[\S\s-]+)/(?P<examine>[\w-]+)/$', 'user_activity.app_message_api.get_admin_message', name='get_json'),
    url(r'^adm_message/(?P<messageid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/(?P<username>[\S\s-]+)/$', 'user_activity.app_message_api.get_admin_message', name='get_json'),
    url(r'^adm_message/(?P<messageid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/$', 'user_activity.app_message_api.get_admin_message', name='get_json'),
    url(r'^adm_message/(?P<messageid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/(?P<username>[\S\s-]+)/(?P<userfrom>[\S\s-]+)/(?P<examine>[\w-]+)$', 'user_activity.app_message_api.get_admin_message', name='get_json'),
    url(r'^adm_message/(?P<messageid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)/(?P<username>[\S\s-]+)$', 'user_activity.app_message_api.get_admin_message', name='get_json'),
    url(r'^adm_message/(?P<messageid>[\w-]+)/(?P<question>[\S\s-]+)/(?P<date>[\w-]+)/(?P<userid>[\w-]+)$', 'user_activity.app_message_api.get_admin_message', name='get_json'),
 

    url(r'^get_event_msg/(?P<eventid>[\w-]+)/$', 'user_activity.app_message_api.get_event_message', name='get_json'),
    url(r'^get_event_msg/(?P<eventid>[\w-]+)$', 'user_activity.app_message_api.get_event_message', name='get_json'),
    url(r'^get_event_msg/(?P<eventid>[\w-]+)/(?P<offset>[\d-]+)/(?P<page>[\d-]+)/$', 'user_activity.app_message_api.get_event_message', name='get_json'),
    url(r'^get_event_msg/(?P<eventid>[\w-]+)/(?P<offset>[\w-]+)/(?P<page>[\d-]+)$', 'user_activity.app_message_api.get_event_message', name='get_json'),
 
    url(r'^get_user_msg/(?P<userid>[\w-]+)/(?P<date>[\d-]+)/$', 'user_activity.app_message_api.get_user_message', name='get_json'),
    url(r'^get_user_msg/(?P<userid>[\w-]+)/(?P<date>[\d-]+)$', 'user_activity.app_message_api.get_user_message', name='get_json'),
    url(r'^get_user_msg/(?P<userid>[\w-]+)/$', 'user_activity.app_message_api.get_user_message', name='get_json'),
    url(r'^get_user_msg/(?P<userid>[\w-]+)$', 'user_activity.app_message_api.get_user_message', name='get_json'),

    url(r'^test_ip/$','user_activity.app_message_api.test_ip', name='get_json' )

)