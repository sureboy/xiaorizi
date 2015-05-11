from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^video/$','new_event.views.show_video'),
    url(r'^video-(?P<video_id>\d+).html$','new_event.views.show_video', name='video_detail'),
    url(r'^list/subscribe/$', 'new_event.list_cal.list_page_subscribe'),

    url(r'^send_check_mesage/$','new_event.order_msg.send_check_mesage', ),
    url(r'^get_check_code_image/$','new_event.order_msg.get_check_code_image', ),
    url(r'^verify_captcha/$', 'new_event.order_msg.verify_captcha'),
    url(r'^verify_tel_captcha/$', 'new_event.order_msg.verify_tel_captcha'),
  
    url(r'^searchorder/$','new_event.order_msg.searchOrder'),
    url(r'^submitorder/$','new_event.order_msg.submitOrder'),
    #url(r'^changecity/$','changeCity'), 
    url(r'^order/(\d+?)/$','new_event.order_msg.writeOrder'),
    url(r'^showorder/(\d+?)/$','new_event.order_msg.showOrder'),
    url(r'^show_order_url/(?P<order_id>[\d-]+)/$', 'new_event.views.show_order_url', ),  
    url(r'^zhuantiorder/$','new_event.order_msg.writeZhuantiOrder'),
    
    url(r'^show_post_html/(?P<query>[\S\s-]+)/(?P<new>[\S\s-]+)/$', 'new_event.views.show_post_html', name='show_post_html'),
    url(r'^show_post_html/(?P<query>[\S\s-]+)/$', 'new_event.views.show_post_html', name='show_post_html'),

    url(r'^send_msg_text/$', 'new_event.views.send_msg_text', name='get_json'),
    url(r'^test_data/$', 'new_event.views.test_data', name='get_json'),
    url(r'^update_info/$', 'new_event.views.update_info', name='get_json'),
    url(r'^update_save/(?P<query>[\S\s-]+)/$', 'new_event.admin_ajax.update_save', ), 
    url(r'^event-(?P<query>[\S\s-]+).html$', 'new_event.views.showPage', name='event_detail'),
    url(r'^app-(?P<query>[\S\s-]+).html$','new_event.m_views.showPage',{'template_name':'app_showEvent.html'}),
    url(r'friendLinks/','new_event.views.site_links'),
    url(r'^post_message_json/$', 'new_event.admin_ajax.CustomMessage',  ),
    
    
    url(r'^$','new_event.showlist.homePage' ),    
    url(r'^xmlsitemap/(.*?).xml$','new_event.views.dispatchsitemap'),
    url(r'^postevent/','new_event.views.postEvent'),

    url(r'^(?P<city>[A-Za-z]+)/$', 'new_event.showlist.list'),    #, name='page'),    
    url(r'^(?P<city>[A-Za-z]+)/(?P<cat>[A-Za-z]+)/$', 'new_event.showlist.list'),    #, name='page'),
 
    url(r'upgrade/(?P<tn>\d+)/(?P<totalpay>[\d\.]+)/(?P<event_name>.+?)/$', view = 'payment.views.upgrade_account', name="payment_upgrade_account"),
    
    #url(r'tag/$','searchKeyword',{'isTag':True}),
    #url(r'tag/(?P<offset>\d*)/(?P<page>\d*)/$','searchKeyword',{'isTag':True}),
    


    url(r'^(?P<cat>[A-Za-z]+)/(?P<month>\d{2})/$', 'new_event.list_cal.list_page'),
    url(r'^(?P<city>[A-Za-z]+)/(?P<cat>[A-Za-z]+)/(?P<month>\d{2})/$', 'new_event.list_cal.list_page'),

)
