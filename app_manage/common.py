from django.core.cache import cache
from models import app_table
import datetime

def get_app_list(app=0,new=False):
    #.objects.exclude(ename='')
    app_str = cache.get('app_table_%s'%app)
    if new or not app_str:
        app_str=[]
        app_t=app_table.objects.filter(app_class=app).order_by('-order','rel_time')
        for ev in app_t:
            st={}
            st['id']=ev.id
            st['name']=ev.name
            st['icon']=ev.icon2 if ev.icon2 else ''
            #st['icon2']=ev.icon2
            #st['icon3']=ev.icon3
            st['link']=ev.link if ev.link else ''
            st['content']=ev.content if ev.content else ''
            st['hot']=ev.hot if ev.hot else ''
            st['order']=ev.order if ev.order else ''
            st['version']=ev.version if ev.version else ''
            st['company']=ev.company if ev.company else ''
            st['website']=ev.website if ev.website else ''
            st['rel_time']=datetime.datetime.strftime(ev.rel_time,'%Y-%m-%d %H:%M:%S') if ev.rel_time else None
            st['state']=str(ev.state)
            app_str.append(st)
            
            
            
        cache.set('app_table_%s'%app,app_str,86400*10)
    new_app=[]
    for i in range(len(app_str)):
        if app_str[i]['state'] is '0':
            if app_str[i]['rel_time']:
                if datetime.datetime.strptime(app_str[i]['rel_time'],'%Y-%m-%d %H:%M:%S')<datetime.datetime.now():
                    new_app.append(app_str[i])
            else:
                app_str[i]['rel_time']=''
                new_app.append(app_str[i])
            
        

    return new_app