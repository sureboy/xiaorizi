from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('User.views',
    url(r'^login/$', 'Login'),
    url(r'^quicklogin/$','quickLogin'),
    url(r'^logout/$', 'Logout'),
    url(r'^register/$','Register'),
    url(r'^sendcheckcode/$','SendCheckCode'),
    url(r'^verifycheckcode/$','VerifyCheckCode'),
    url(r'^changepassword/$','ChangePassword'),
    url(r'^getbackpassword/$','GetBackPassword'),
    url(r'^changeuserinfo/$','ChangeUserInfo'),
    url(r'^addaddress/$','AddAddress'),
    url(r'^changeaddress/$','ChangeAddress'),
    url(r'^deleteaddress/$','DeleteAddress'),
    url(r'^showaddress/$','ShowAddress'),
    url(r'^getuicid/$','getCid'),
    url(r'^uploadphoto/$','addPicture'),
    url(r'^delpush/$','delPushInfo'),
    url(r'^addpush/$','addPushInfo'),
    #url(r'^personaltailor/$','addPersonalTailor'),
    #url(r'^getpersonaltailor/$','getPersonalTailor'),
    #url(r'^getcustomevents/$','getEventsInPT'),
#    url(r'^getListInfo/$','getListInfo'),
    )

urlpatterns += patterns('',
(r'^test/$', TemplateView.as_view(template_name='test.html')), 

)