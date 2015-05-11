#coding:utf-8
from django import template
from django.conf import settings
from django.utils.datastructures import SortedDict
from new_event.models import NewNavList
from admin_self.common import NewCatUrl,NewCity,get_site_links
import datetime
register = template.Library()

import logging
log = logging.getLogger('XieYin.app')  


class NavMain(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        #log.debug('return nav')
        output = self.nodelist.render(context).replace('\n','').replace('\r','')
        
        out=output.split('|')
        fl=''
        if len(out)>1:
            '''
            cat_n=NewCatUrl(1,out[0],False,out[1])
            try:
                if 0==len(cat_n):
                    cat_n=NewCatUrl(1,out[0],True,out[1])
            except:
                cat_n=[]
                
                
            '''
            fl=out[1]
            cat_n=[]
            cat_n.append({'caturl':'/%s/meeting/' % out[0],'catname':u'商务会议' ,'ename':u'meeting','flag':False})
            cat_n.append({'caturl':'/%s/travel/' % out[0],'catname':u'旅行体验','ename':u'travel','flag':False})
            cat_n.append({'caturl':'/%s/show/' % out[0],'catname':u'娱乐演出','ename':u'show','flag':False})
            cat_n.append({'caturl':'/%s/local/' % out[0],'catname':u'同城活动','ename':u'local','flag':False})
        else:
            out[0]='beijing'
            '''
            try:
                cat_n=NewCatUrl(1,out[0])
                if 0==len(cat_n):
                    cat_n=NewCatUrl(1,out[0],True)
            except:
                cat_n=[]
            '''
            cat_n=[]
            cat_n.append({'caturl':'/beijing/meeting/'  ,'catname':u'会议','ename':u'meeting','flag':False})
            cat_n.append({'caturl':'/beijing/travel/' ,'catname':u'旅行体验','ename':u'travel','flag':False})
            cat_n.append({'caturl':'/beijing/show/'  ,'catname':u'演出','ename':u'show','flag':False})
            cat_n.append({'caturl':'/beijing/local/' ,'catname':u'同城活动','ename':u'local','flag':False})
            #cat_n.append({'caturl':'/beijing/local','catname':u'同城活动','ename':u'local','flag':False})
        context['Show_Nav']=[]
        context['cat_Map']=cat_n

        for cat in cat_n:
            nav={}
            nav['url']=cat['caturl']
            nav['name']=cat['catname']#+cat['flag'] 
            #nav['ename']=cat['caturl'] 
            
            nav['flag']=cat['flag']
            #if cat['flag']=='true':
                #nav['url']='#'
            context['Show_Nav'].append(nav)
        
        nav={}
        nav['url']='/searchorder/'
        nav['name']=u'订单查询'  
        if fl=='searchorder':
            nav['flag']='true'
        else:
            nav['flag']='false'
        nav['rel']="nofollow"
        nav['class']="last"
        context['Show_Nav'].append(nav)
        
        
        context['city_Nav']=NewCity(0)
        

        #context['site_links']=get_site_links(True)
        context['time']='201410181'

        www={'id':2,'name':'互联网会议','img':'http://pic.huodongjia.com/html5/pic/www1.png?time=%s'%context['time'],'url':'/%s/it/' % out[0] }
        jinrong={'id':6,'name':'金融会议','img':'http://pic.huodongjia.com/html5/pic/jinrong1.png?time=%s'%context['time'],'url':'/%s/finance/'  % out[0]}
        hospity={'id':23,'name':'医疗会议','img':'http://pic.huodongjia.com/html5/pic/hospity1.png?time=%s'%context['time'],'url':'/%s/medical/'  % out[0]}
        maer={'id':93,'name':'骑马运动','img':'http://pic.huodongjia.com/html5/pic/maer1.png?time=%s'%context['time'],'url':'/tag/?keyword=骑马运动' }
        fly={'id':94,'name':'飞行体验','img':'http://pic.huodongjia.com/html5/pic/fly1.png?time=%s'%context['time'],'url':'/tag/?keyword=飞行体验' }
        foot={'id':76,'name':'美食烹饪','img':'http://pic.huodongjia.com/html5/pic/foot1.png?time=%s'%context['time'],'url':'/%s/food/' % out[0]}
        child={'id':24,'name':'亲子活动','img':'http://pic.huodongjia.com/html5/pic/child1.png?time=%s'%context['time'],'url':'/tag/?keyword=亲子活动'}
        snow={'id':24,'name':'滑雪活动','img':'http://pic.huodongjia.com/html5/pic/snow1.png?time=%s'%context['time'],'url':'/tag/?keyword=滑雪活动'}
        
        
        context['hot_cat']=[www,jinrong,hospity,maer,fly,foot,child,snow]
        
        
        return ''
 

    '''
    def render(self, context):
        context['Show_Nav']=[]   
        
        cat_n=NewCatUrl(1,self.city_py)  
        for cat in cat_n:
            nav={}
            nav['url']=cat['caturl']
            nav['name']=cat['catname']            
                
            context['Show_Nav'].append(nav)
 
        return ''
    '''

@register.tag(name="cityNav")
def do_cityNav(parser, token):    
    nodelist = parser.parse(('endcityNav',))
    parser.delete_first_token()
    return NavMain(nodelist)
 
