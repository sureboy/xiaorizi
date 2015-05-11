from django.conf.urls import patterns, url
urlpatterns = patterns('app_manage.views',
    url(r'^share-(?P<query>[\S\s-]+).html$','showCont',{'template_name':'share_showEvent.html'}),
    url(r'^app-(?P<query>[\S\s-]+).html$','showCont'),
    url(r'^q-(?P<query>[\S\s-]+).html$','showQ',{'template_name':'q_showEvent.html'}),
    url(r'^update/$','update'),
)