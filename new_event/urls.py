from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^video/$','new_event.views.show_video'),
    url(r'^video-(?P<video_id>\d+).html$','new_event.views.show_video', name='video_url'),
    url(r'^list/subscribe/$', 'new_event.list_cal.list_page_subscribe'),

    url(r'^refund_alipay_jump/$', view = 'payment.views.alipay_refund', name='refund_alipay'),

    url(r'^newevent/get_json_frominfo/(?P<query>[\S\s-]+)/$', 'new_event.admin_ajax.frominfo_data',  ),                   
    url(r'^newevent/get_json_city/(?P<query>[\S\s-]+)/$', 'new_event.admin_ajax.District_data',  ),
    url(r'^newevent/get_json_cat/(?P<query>[\S\s-]+)/$', 'new_event.admin_ajax.Cat_data',  ),
    url(r'^newevent/get_json_cat/$', 'new_event.admin_ajax.Cat_data',  ),
    url(r'^newevent/get_json_img/(?P<query>[\S\s-]+)/$', 'new_event.admin_ajax.img_data',  ),
    url(r'^newevent/get_json_tag/(?P<query>[\S\s-]+)/$', 'new_event.admin_ajax.Tag_data',  ),
    url(r'^newevent/get_json_addr/(?P<query>[\S\s-]+)/$', 'new_event.admin_ajax.Addr_data',  ),
    url(r'^newevent/get_json_txt/(?P<query>[\S\s-]+)/$', 'new_event.admin_ajax.Txt_data_list',  ),
    #url(r'^get_json_txt_id/(?P<query>[\d-]+)/$', 'new_event.admin_ajax.Txt_data_id', name='get_json'),
    url(r'^newevent/get_json_addr_str/(?P<query>[\S\s-]+)/$', 'new_event.admin_ajax.Addr_data_str',  ),
    url(r'^newevent/get_json_addr_str/$', 'new_event.admin_ajax.Addr_data_str',  ),
    url(r'^newevent/save_txt/$', 'new_event.admin_ajax.save_txt',  ),
    url(r'^newevent/get_paragraph_tag/(?P<query>[\S\s-]+)/$', 'new_event.admin_ajax.get_paragraph_tag',  ),
    
    url(r'^newevent/show_city_json/$', 'new_event.event_edit_ajax.show_city_json',  ),
    url(r'^newevent/show_from_json/(?P<offset>[\d-]+)/(?P<page>[\d-]+)/$', 'new_event.event_edit_ajax.show_from_json',  ),
    url(r'^newevent/show_FromType_json/$', 'new_event.event_edit_ajax.show_FromType_json', ),
    url(r'^newevent/show_FromClass_json/$', 'new_event.event_edit_ajax.show_FromClass_json', ),
    url(r'^newevent/show_img_json/(?P<offset>[\d-]+)/(?P<page>[\d-]+)/$', 'new_event.event_edit_ajax.show_img_json',  ),
    url(r'^newevent/show_seo_json/(?P<offset>[\d-]+)/(?P<page>[\d-]+)/$', 'new_event.event_edit_ajax.show_seo_json',  ),
    url(r'^newevent/find_seo_json/(?P<offset>[\d-]+)/(?P<query>[\S\s-]+)/$', 'new_event.event_edit_ajax.find_seo_json',  ),
    url(r'^newevent/find_from_json/(?P<offset>[\d-]+)/(?P<query>[\S\s-]+)/$', 'new_event.event_edit_ajax.find_from_json',  ),
    
    
    url(r'^newevent/save_city/$', 'new_event.event_edit_ajax.save_city', ),
    url(r'^newevent/save_from/$', 'new_event.event_edit_ajax.save_from', ),
    url(r'^newevent/save_img/$', 'new_event.event_edit_ajax.save_img', ),
    url(r'^newevent/save_tag/$', 'new_event.event_edit_ajax.save_tag', ),
    url(r'^newevent/save_seo/$', 'new_event.event_edit_ajax.save_seo', ),
    #url(r'^newevent/update_save/$', 'new_event.views.update_save', name='get_json'),
    url(r'^newevent/send_email/(?P<email>[\S\s-]+)/(?P<content>[\S\s-]+)/(?P<subject>[\S\s-]+)/$', 'new_event.event_edit_ajax.send_email', ),
    url(r'^newevent/send_email/$', 'new_event.event_edit_ajax.send_email', ),
    
    url(r'^newevent/del_tag/$', 'new_event.event_edit_ajax.del_tag', ),
    url(r'^del_tag/$', 'new_event.event_edit_ajax.del_tag', ),

    url(r'^send_email/(?P<email>[\S\s-]+)/(?P<content>[\S\s-]+)/(?P<subject>[\S\s-]+)/$', 'new_event.event_edit_ajax.send_email', ),
 
    url(r'^send_email/$', 'new_event.event_edit_ajax.send_email', ),
    
    url(r'^get_json_cat/(?P<query>[\S\s-]+)/$', 'new_event.admin_ajax.Cat_data',  ),
    url(r'^get_json_cat/$', 'new_event.admin_ajax.Cat_data',  ),
    url(r'^show_city_json/$', 'new_event.event_edit_ajax.show_city_json',  ),
    url(r'^show_from_json/(?P<offset>[\d-]+)/(?P<page>[\d-]+)/$', 'new_event.event_edit_ajax.show_from_json',  ),
    url(r'^show_FromType_json/$', 'new_event.event_edit_ajax.show_FromType_json', ),
    url(r'^show_FromClass_json/$', 'new_event.event_edit_ajax.show_FromClass_json', ),
    url(r'^show_img_json/(?P<offset>[\d-]+)/(?P<page>[\d-]+)/$', 'new_event.event_edit_ajax.show_img_json',  ),
    url(r'^show_seo_json/(?P<offset>[\d-]+)/(?P<page>[\d-]+)/$', 'new_event.event_edit_ajax.show_seo_json',  ),
    url(r'^find_seo_json/(?P<offset>[\d-]+)/(?P<query>[\S\s-]+)/$', 'new_event.event_edit_ajax.find_seo_json',  ),
    url(r'^find_from_json/(?P<offset>[\d-]+)/(?P<query>[\S\s-]+)/$', 'new_event.event_edit_ajax.find_from_json',  ),

    url(r'^save_city/$', 'new_event.event_edit_ajax.save_city', ),
    url(r'^save_from/$', 'new_event.event_edit_ajax.save_from', ),
    url(r'^save_img/$', 'new_event.event_edit_ajax.save_img', ),
    url(r'^save_tag/$', 'new_event.event_edit_ajax.save_tag', ),
    url(r'^save_seo/$', 'new_event.event_edit_ajax.save_seo', ),    

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
    
    #api url   city_id=None,cat_id=None, new=False,cou=False
    
    url(r'^newformatevent_json/(?P<eventid>[\d-]+)/(?P<new>[\S\s-]+)/$', 'new_event.json_api.NewformatEvent_json', ),     
    url(r'^newformatevent_json/(?P<eventid>[\d-]+)/$', 'new_event.json_api.NewformatEvent_json', ),     
    url(r'^get_event_list_json/(?P<cat>[\d-]+)/(?P<city>[\d-]+)/(?P<date>[\S\s-]+)/(?P<page>[\d-]+)/(?P<offset>[\d-]+)/(?P<order>[\d-]+)/(?P<new>[\S\s-]+)/$', 'new_event.json_api.get_event_list_json', ),
    url(r'^get_event_list_json/(?P<cat>[\d-]+)/(?P<city>[\d-]+)/(?P<date>[\S\s-]+)/(?P<page>[\d-]+)/(?P<offset>[\d-]+)/(?P<order>[\d-]+)/$', 'new_event.json_api.get_event_list_json', ),
    url(r'^event_city_cat_json/(?P<city_id>[\w-]+)/(?P<cat_id>[\w-]+)/(?P<new>[\S\s-]+)/(?P<cou>[\d-]+)/$', 'new_event.json_api.event_city_cat_json', ),
    
    
    
    url(r'^show_cache/$','new_event.json_test.show_cache', name='get_json'),
    #url(r'^event-(?P<query>[\S\s-]+).html$','new_event.views.showPage', name='get_json'),
    #url(r'^app-(?P<query>[\S\s-]+).html$','new_event.views.showPage',{'template_name':'app_showEvent.html'}),
    #url(r'^zhuanti-(?P<query>[\S\s-]+).html$','new_event.views.showPage',{'template_name':'zhuanti_temp.html'}),
    url(r'^event-(?P<query>[\S\s-]+).html$', 'new_event.views.showPage'),
    #url(r'^(?P<query>[\S\s-]+).html$','new_event.views.showPage', name='page'),
    #url(r'^getevent/(?P<query>[\S\s-]+)/$','new_event.views.getevent'),
    url(r'friendLinks/','new_event.views.site_links'),
    url(r'^post_message_json/$', 'new_event.admin_ajax.CustomMessage',  ),
    
    
    url(r'^$','new_event.showlist.homePage' ),    
    #url(r'^(?P<city>[\w-]+)$', 'new_event.showlist.list', name='page'),
    url(r'^xmlsitemap/(.*?).xml$','new_event.views.dispatchsitemap'),
    url(r'^postevent/','new_event.views.postEvent'),

    url(r'^(?P<city>[A-Za-z]+)/$', 'new_event.showlist.list', name='page'),    
    url(r'^(?P<city>[A-Za-z]+)/(?P<cat>[A-Za-z]+)/$', 'new_event.showlist.list', name='page'),
    #url(r'^(?P<city>[\w-]+)/(?P<cat>[\w-]+)/(?P<date>[\w-]+)/$', 'new_event.showlist.list', name='page'),
    #url(r'^(?P<city>[\w-]+)/(?P<cat>[\w-]+)/(?P<date>[\w-]+)/(?P<offset>[\w-]+)/$', 'new_event.showlist.list', name='page'), 
	 
    url(r'upgrade/(?P<tn>\d+)/(?P<totalpay>[\d\.]+)/(?P<event_name>.+?)/$', view = 'payment.views.upgrade_account', name="payment_upgrade_account"),
    
    #url(r'tag/$','searchKeyword',{'isTag':True}),
    #url(r'tag/(?P<offset>\d*)/(?P<page>\d*)/$','searchKeyword',{'isTag':True}),
    


    url(r'^(?P<cat>[A-Za-z]+)/(?P<month>\d{2})/$', 'new_event.list_cal.list_page'),
    url(r'^(?P<city>[A-Za-z]+)/(?P<cat>[A-Za-z]+)/(?P<month>\d{2})/$', 'new_event.list_cal.list_page'),
    #url(r'meeting/(?P<city>\w+)/(?P<cat>\w+)/(?P<month>\d{2})/$', 'new_event.list_cal.list_page'),
    #url(r'meeting/calendar/test/$', 'new_event.views.calendar_page'),


)
