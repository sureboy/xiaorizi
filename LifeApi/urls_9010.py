from django.conf.urls import patterns, url

urlpatterns = patterns('',    
    url(r'^dateapi/$', 'LifeApi.views_9010.DateApi'),   
    url(r'^catapi/$', 'LifeApi.views_9010.CatApi'),       
    url(r'^homeapi/$', 'LifeApi.views_9010.HomeApi', ),      
    url(r'^eventapi/$', 'LifeApi.views_9010.EventApi'),   
    url(r'^eventinfoapi/$', 'LifeApi.views_9010.EventInfoApi'),   
    url(r'^searchkey/$', 'LifeApi.views_9010.SearchKey'),   
    url(r'^tag_hot/$','LifeApi.views_9010.tag_hot'),
    url(r'^custom_message/$','LifeApi.views_9010.CustomMessage'),
    url(r'^searchorder/$','LifeApi.views_9010.searchOrder'),    
    url(r'^submitorder/$','LifeApi.views.submitOrder'),
    url(r'^collectevent/(\d+?)/$','LifeApi.views_9010.collect'),
    url(r'^collectevent_del/$','LifeApi.views_9010.collect_del'),
    url(r'^app/(.*?)$','LifeApi.views_9010.downloadapp'),
    url(r'^send_msg_text/$','LifeApi.views_9010.send_msg_text'),
    
)
