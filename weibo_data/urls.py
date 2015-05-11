from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^show/$', 'weibo_data.views.showWeibo'),
    url(r'^page/$', 'weibo_data.views.showpage'),
    url(r'^table/$', 'weibo_data.views.showtable'),
)
