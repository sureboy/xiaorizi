from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^grappelli/', include('grappelli.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/',include('LifeApi.urls_9010')),
    url(r'^weibo/',include('weibo_data.urls')),
    url(r'^user/',include('User.urls')),
    #############################
    url(r'^newevent/get_json_frominfo/(?P<query>[\S\s-]+)/$', 'LifeApi.admin_ajax.frominfo_data',  ),                   
    url(r'^newevent/get_json_city/(?P<query>[\S\s-]+)/$', 'LifeApi.admin_ajax.District_data',  ),
    url(r'^newevent/get_json_cat/(?P<query>[\S\s-]+)/$', 'LifeApi.admin_ajax.Cat_data',  ),
    url(r'^newevent/get_json_cat/$', 'LifeApi.admin_ajax.Cat_data',  ),
    url(r'^newevent/get_json_event_cat/$', 'LifeApi.admin_ajax.get_event_cat',  ),
    url(r'^newevent/get_json_img/(?P<query>[\S\s-]+)/$', 'LifeApi.admin_ajax.img_data',  ),
    url(r'^newevent/get_json_tag/(?P<query>[\S\s-]+)/$', 'LifeApi.admin_ajax.Tag_data',  ),
    url(r'^newevent/get_json_addr/(?P<query>[\S\s-]+)/$', 'LifeApi.admin_ajax.Addr_data',  ),
    url(r'^newevent/get_json_txt/(?P<query>[\S\s-]+)/$', 'LifeApi.admin_ajax.Txt_data_list',  ),
    url(r'^newevent/get_json_addr_str/(?P<query>[\S\s-]+)/$', 'LifeApi.admin_ajax.Addr_data_str',  ),
    url(r'^newevent/get_json_addr_str/$', 'LifeApi.admin_ajax.Addr_data_str',  ),
    url(r'^newevent/save_txt/$', 'LifeApi.admin_ajax.save_txt',  ),
    url(r'^newevent/get_paragraph_tag/(?P<query>[\S\s-]+)/$', 'LifeApi.admin_ajax.get_paragraph_tag',  ),

    url(r'^newevent/get_json_sponsor_str/(?P<query>[\S\s-]+)/$', 'LifeApi.admin_ajax.sponsor_data_str',  ),
    url(r'^newevent/get_json_sponsor_str/$', 'LifeApi.admin_ajax.sponsor_data_str',  ),
    url('^newevent/get_json_event_sponsor/$', 'LifeApi.admin_ajax.get_event_sponsor'),

    url(r'^newevent/show_city_json/$', 'LifeApi.event_edit_ajax.show_city_json',  ),
    url(r'^newevent/show_from_json/(?P<offset>[\d-]+)/(?P<page>[\d-]+)/$', 'LifeApi.event_edit_ajax.show_from_json',  ),
    url(r'^newevent/show_FromType_json/$', 'LifeApi.event_edit_ajax.show_FromType_json', ),
    url(r'^newevent/show_FromClass_json/$', 'LifeApi.event_edit_ajax.show_FromClass_json', ),
    url(r'^newevent/show_img_json/(?P<offset>[\d-]+)/(?P<page>[\d-]+)/$', 'LifeApi.event_edit_ajax.show_img_json',  ),
    url(r'^newevent/show_seo_json/(?P<offset>[\d-]+)/(?P<page>[\d-]+)/$', 'LifeApi.event_edit_ajax.show_seo_json',  ),
    url(r'^newevent/find_seo_json/(?P<offset>[\d-]+)/(?P<query>[\S\s-]+)/$', 'LifeApi.event_edit_ajax.find_seo_json',  ),
    url(r'^newevent/find_from_json/(?P<offset>[\d-]+)/(?P<query>[\S\s-]+)/$', 'LifeApi.event_edit_ajax.find_from_json',  ),
    
    
    url(r'^newevent/save_city/$', 'LifeApi.event_edit_ajax.save_city', ),
    url(r'^newevent/save_from/$', 'LifeApi.event_edit_ajax.save_from', ),
    url(r'^newevent/save_img/$', 'LifeApi.event_edit_ajax.save_img', ),
    url(r'^newevent/save_tag/$', 'LifeApi.event_edit_ajax.save_tag', ),
    url(r'^newevent/save_seo/$', 'LifeApi.event_edit_ajax.save_seo', ),
    #url(r'^newevent/update_save/$', 'LifeApi.views.update_save', name='get_json'),
    url(r'^newevent/send_email/(?P<email>[\S\s-]+)/(?P<content>[\S\s-]+)/(?P<subject>[\S\s-]+)/$', 'LifeApi.event_edit_ajax.send_email', ),
    url(r'^newevent/send_email/$', 'LifeApi.event_edit_ajax.send_email', ),
    url(r'^newevent/del_tag/$', 'LifeApi.event_edit_ajax.del_tag', ),

    url(r'^newevent/show_price/$', 'LifeApi.admin_ajax.price_data',),


)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
