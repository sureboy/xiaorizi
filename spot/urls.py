from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^get_json_img/(?P<query>[\w-]+)/$', 'spot.views.get_json_img', name='get_json'),
    url(r'^get_json_txt/(?P<query>[\w-]+)/$', 'spot.views.get_json_txt', name='get_json'),
    url(r'^get_json_code/(?P<query>[\w-]+)/$', 'spot.views.get_json_code', name='get_json'),
    url(r'^get_json_event/(?P<query>[\w-]+)/$', 'spot.views.get_json_event', name='get_json'),
    url(r'^get_json_cat/(?P<query>[\w-]+)/$', 'spot.views.get_json_cat', name='get_json'),
    url(r'^get_json_city/(?P<query>[\w-]+)/$', 'spot.views.get_json_city', name='get_json'),
    url(r'^get_json_img_id/(?P<query>[\S\s-]+)/$', 'spot.views.img_data', name='get_json'),
    url(r'^get_json_txt_x/(?P<query>[\S\s-]+)/$', 'spot.views.Txt_data_list', name='get_json'),
    url(r'^get_json_event_id/(?P<query>[\S\s-]+)/$', 'spot.views.get_json_event_id', name='get_json'),
    
    url(r'^($)($)','spot.list.index' ),
    url(r'^(\w+)($)','spot.list.index' ), 
    url(r'^(\w+)/($)','spot.list.index' ), 
    url(r'^(\w+)/(\d+?)$','spot.list.index' ), 
    url(r'^(\w+)/(\d+?)/$','spot.list.index' ),
    #url(r'(\d+?)/$','spot.page.index' ),   
    url(r'(\d+?).html','spot.page.index' ),   


    

)