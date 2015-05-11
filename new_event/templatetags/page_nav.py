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
            cat_n=NewCatUrl(1,out[0],False,out[1])
            try:
                if 0==len(cat_n):
                    cat_n=NewCatUrl(1,out[0],True,out[1])
            except:
                cat_n=[]
                
                
            
            fl=out[1]
            
        else:
            try:
                cat_n=NewCatUrl(1,out[0])
                if 0==len(cat_n):
                    cat_n=NewCatUrl(1,out[0],True)
            except:
                cat_n=[]
        context['Show_Nav']=[]
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
        context['time']='20150209'

            
        
        
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
 
