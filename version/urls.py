from django.conf.urls import patterns, url

urlpatterns = patterns('version.views',
   #url(r'^update/$','update'),
   url(r'^update_test/$','update_test'),   
                       )