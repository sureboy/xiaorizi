#coding:utf-8
import time,re
from LifeApi.common import NewAppEvent,event_city_cat,replaceCharEntity,find_img
from user_activity.models import UserEventMessage
from BeautifulSoup import BeautifulSoup
import bs4
             
def str_html(strs=None):
    strs = strs.replace(' ','').replace('\r','').replace('\n','').replace('<p>','').replace('</p>','\r\n').replace('<br>','\r\n')\
                .replace('<br/>','\r\n').replace('<br />','\r\n').replace('\r\n\r\n','\r\n')
    strs = replaceCharEntity(strs)   
    return strs
    
def dic2text(dic):
    res = ''
    for key,value in dic.items():
        if key == 'csrfmiddlewaretoken':
            continue
        res += key+':'+value+'\n'   
    return res.encode('utf-8')


def find_img_tag(string):

    add_str="</img>"
 
    pos = -2
 
    while True:
        
        pos = string.find("<img", pos+2)
        if pos < 0:
            break
        pos_end=string.find(">", pos)
        if pos_end>0:
            #string[int(pos_end-1)]=string[int(pos_end-2)]
            string = string[:pos_end+1 ] + add_str + string[pos_end+1 :]
        
        
    pos_span=-2
    while True:
        pos_span = string.find("<span", pos_span+2)
        if pos_span < 0:
            break
        pos_span_end=string.find(">", pos_span)
        
        string = string[:pos_span ] + string[pos_span_end+1 :]  
    pos_p=-2      
    while True:
        pos_p = string.find("<p", pos_p+2)
        if pos_p < 0:
            break
        pos_p_end=string.find(">", pos_p)
        
        string=string[:pos_p+2]+string[pos_p_end:]
        
    #return string.replace('style="',' ').replace(':','=').replace('px;',' ').replace('px"', ' ').replace('</span>',' ')
    return string.replace(': ', ':').replace(';"', ';').replace('style="',' ').replace('width:','width=').replace('height:','height=').replace('px;',' ').replace('px"', ' ').replace('</span>',' ').replace('<pre>','').replace('</pre>','').replace('/>', '>')

def add_quote(x):
    pre = x.group('pre')
    fnStr = x.group('post')
    fnStr = fnStr.strip('"')
    return pre + '"' + fnStr + '"'

def get_style_couple(str_in):
    return re.findall('([\w-]+) ?: ?([\w\.-]+);?', str_in)

def remove_tag(html, tag_list=[]):
    '''
    html is bs4.BeautifulSoup
    '''
    if not isinstance(tag_list, (list, tuple)):
        tag_list = [tag_list]
    for tag in tag_list:
        for html_tag in html.find_all(tag):
            html_tag.decompose()
    return html

def unwrap_tag(html, tag_list=[]):
    if not isinstance(tag_list, (list, tuple)):
        tag_list = [tag_list]
    for tag in tag_list:
        for html_tag in html.find_all(tag):
            html_tag.unwrap()
    return html

def xml_fmt_convert(html):
    soup = bs4.BeautifulSoup(html)

    # remove tag and its contents
    soup = remove_tag(soup, ['pre'])

    # remove tag, leave its contents
    soup = unwrap_tag(soup, ['br', 'span'])

    # rename tag: div -> p
    for i in soup.find_all('div'):
        i.name = 'p'

    # deal with the 'style' attributes in <img>
    tag_img = soup.find_all('img')
    for i in tag_img:
        try:
            couple = get_style_couple(i['style'].replace('px', ''))
            for attr, val in couple:
                i[attr] = val
            del i['style']
        except KeyError:
            pass
    
    #soup_fmt = soup.prettify(formatter=None)
    soup_fmt = replaceCharEntity(str(soup))
    soup_fmt = '<body>' + soup_fmt + '</body>'

    # convert <img.../> tag into <img...></img> 
    soup_fmt = soup_fmt.replace('/>', '>')
    soup_fmt = re.sub('<img[^>]+>', lambda x: x.group() + '</img>', soup_fmt)

    return soup_fmt.replace('\r', '').replace('\n', '')

def gettext(strings=None):
    if not strings:
        return ''   
    pattern = re.compile(r"<p>img\d+\</p>")
    con='<body>'
    
    con+=pattern.sub(find_img,replaceCharEntity(strings) )
        
    con+='</body>'

    # add quote before and after the attributes
    pattern = re.compile("(?P<pre>\w+=)(?P<post>\"?[^ \f\n\r\t\v<>]+\"?)")
    con = re.sub(pattern, add_quote, con)
    
    con = re.sub(r":(\S+);",r'="\1"', con)
        
    return re.sub("\r\n",'',con)


class version_dis_for_App():
    def __init__(self,id=None,new=False,ver=''):
        self.version=ver
        self.new=new
        self.id=id
    def output_getevent(self,event_id=None,new=None,ver=''):
        pass
        
    def output(self,id=None,new=False,ver=''):

        if '1.2' in ver:
            #return self.getevent_1_0(self.id,self.new)
            ev= self.getevent_1_2(id,new)
            ev['version']=ver
            return ev
        else:
            ev= self.getevent(id,new)
            ev['version']=ver
            return ev
        
    def getevent_1_2(self,id=None,new=False):
        if not id:
            return {}
        
        event={}
        ca=NewAppEvent(None,id,new)
        #print ca
        event['id']=ca['event_id']
        event['isurl']=True if ca['isshow']==8 else False
        event['title']=ca['title']
        event['imgs']=ca['img_s']
        event['adurl']=ca['event_img']
        
        #del event['imgs'][0]
        event['cat']={'name':ca['cat_name'] if ca['cat_name'] else '',
                      'id':ca['catid'] if ca['catid'] else '',
                      'img':ca['cat_img']['img']  if ca['cat_img'] else ''
                      }
        
        #event['cat_name']=ca['cat_name'] if ca['cat_name'] else ''
        #event['catid']=ca['catid'] if ca['catid'] else ''
        #event['cat_img']=ca['cat_img'] if ca['cat_img'] else ''
        
        if ca.has_key('feeltitle'):
            event['feeltitle']=ca['feeltitle'] if ca['feeltitle'] else ''
        else:
            event['feeltitle']=''
            

        #des1 = ''.join(BeautifulSoup(ca['des']).findAll(text=True))
        #des1 = ''.join(replaceCharEntity(des1))
    
    
        event['tag']=','.join(ca['event_tag'])
        event['price']=ca['app_price']
        
        event['feel']=ca['feel']
        event['feelnum']=ca['feelnum'] if ca['feelnum'] else 0
        event['address']=ca['event_address']
        event['position']=ca['position']
        event['startdate']=ca['startdate']
        event['enddate']=ca['enddate']
        event['islongtime']=ca['event_islongtime']
        event['city']=ca['district_name']
        
        event['detail']=''
        try:
            event['detail']=ca['detail']  
        except:
            pass
        if not event['detail']:        
            event['detail']=ca['des']
            
        if not event['detail']:         
            i=1            
            str_h=  str_html(ca['event_content'][0][1]) 
            
            for de in str_h.split('\n'):
                if event['detail']:
                    event['detail']+='\r\n'
                
                te= BeautifulSoup(de).text
                if te and len(te)>15:            
                    i+=1
        
                    event['detail'] += '%s' % te
                if i>3:
                    break
        
            event['detail']=event['detail'].replace('\r\n\r\n','\r\n')\
                    .replace('\n\n\n\n','\r\n').replace('\n\n\n','\r\n').replace('\n\n','\r\n')
        #event['detail']= BeautifulSoup(ca['event_content'][0][1]).text[0:250]
      
        
    
        for con in ca['event_content']:
            if con[0] in [u'购买须知']:
                event['note']=con[1]
                note=event['note']
                break
    
        try:
            event['note']=str_html(event['note']).replace('\r\n','')
            event['note']=BeautifulSoup(event['note']).text
            o=event['note'].find(u'。')
            if o>0:
                event['note']=event['note'][:o]
            else:
                no=event['note'].split(u'，')
                if len(no)>2:
                    event['note']='%s%s' % (u'，'.join(no[:2]),'...')
        except:
            event['note']='' 
            note=''   
            
        event['comment']={}
        try:        
            com=UserEventMessage.objects.filter(event_id=ca['event_id']).order_by('id')[0]
            event['comment']['id']=com.id
            event['comment']['content']=com.message.txt
            event['comment']['date']=time.mktime(com.end_time.timetuple())
            
            event['comment']['score']=0
            event['comment']['imgs']=[]
            event['comment']['user']={'id':com.user.user_id,'name':com.user.user_name}
    
        except:
            pass
        event['commentTotol']={}
         
        cont=ca['event_content'][0][1]
        
        #cont = cont.replace('\n','').replace('\r','').replace('<br>','').replace('<br/>','').replace('<br />','')
        cont = cont.replace('\n','').replace('\r','').replace('\r\n', '')

        try:
            #note=note.strip().replace('\n','').replace('\r','').replace('<br>','').replace('<br/>','').replace('<br />','')
            note=note.strip().replace('\n','').replace('\r','').replace('\r\n', '')
        except:
            note=''
        
        if event['isurl']:
            event['mobileURL'] = 'http://m.huodongjia.com/app-%s.html'%ca['event_id']
            event['questionURL']='http://m.huodongjia.com/q-%s.html'%ca['event_id']
        else:
            #event['mobileURL']=gettext(find_img_tag(cont)) #'http://m.huodongjia.com/app-%s.html'%ca['event_id']
            #event['questionURL']=gettext(find_img_tag(note))

            event['mobileURL'] = xml_fmt_convert(cont)
            event['questionURL'] = xml_fmt_convert(note)

        
        event['shareURL']='http://m.huodongjia.com/share-%s.html'%ca['event_id']
        
        event['more']=[]
        for ev in event_city_cat(ca['district_id']):
            if ev!=event['id']:
                
                e=NewAppEvent(None,ev)
                even={'id':e['event_id'],'title':e['title'],'price':e['app_price'],'imgs':e['img_s']}
                event['more'].append(even)
                
            if len(event['more'])>3:
                break
        
        return event
    def getevent(self,id=None,new=False):
        if not id:
            return {}
        
        event={}
        ca=NewAppEvent(None,id,new)
        #print ca
        event['id']=ca['event_id']
        #event['isurl']=True if ca['isshow']==8 else False
        event['title']=ca['title']
        event['imgs']=ca['img_s']
        event['cat']={'name':ca['cat_name'] if ca['cat_name'] else '',
                      'id':ca['catid'] if ca['catid'] else '',
                      'img':ca['cat_img']['img']  if ca['cat_img'] else ''
                      }
        
        #event['cat_name']=ca['cat_name'] if ca['cat_name'] else ''
        #event['catid']=ca['catid'] if ca['catid'] else ''
        #event['cat_img']=ca['cat_img'] if ca['cat_img'] else ''
        
        if ca.has_key('feeltitle'):
            event['feeltitle']=ca['feeltitle'] if ca['feeltitle'] else ''
        else:
            event['feeltitle']=''
        event['mobileURL']='http://m.huodongjia.com/app-%s.html'%ca['event_id']
        event['questionURL']='http://m.huodongjia.com/q-%s.html'%ca['event_id']
        event['shareURL']='http://m.huodongjia.com/share-%s.html'%ca['event_id']
        #des1 = ''.join(BeautifulSoup(ca['des']).findAll(text=True))
        #des1 = ''.join(replaceCharEntity(des1))    
    
    
        event['tag']=','.join(ca['event_tag'])
        event['price']=ca['app_price']
        
        event['feel']=ca['feel']
        event['feelnum']=ca['feelnum'] if ca['feelnum'] else 0
        event['address']=ca['event_address']
        event['position']=ca['position']
        event['startdate']=ca['startdate']
        event['enddate']=ca['enddate']
        event['islongtime']=ca['event_islongtime']
        event['city']=ca['district_name']
        
        event['detail']=''
        try:
            event['detail']=ca['detail']  
        except:
            pass
        if not event['detail']:        
            event['detail']=ca['des']
            
        if not event['detail']:         
            i=1            
            str_h=  str_html(ca['event_content'][0][1]) 
            
            for de in str_h.split('\n'):
                if event['detail']:
                    event['detail']+='\r\n'
                
                te= BeautifulSoup(de).text
                if te and len(te)>15:            
                    i+=1
        
                    event['detail'] += '%s' % te
                if i>3:
                    break
        
            event['detail']=event['detail'].replace('\r\n\r\n','\r\n')\
                    .replace('\n\n\n\n','\r\n').replace('\n\n\n','\r\n').replace('\n\n','\r\n')
        #event['detail']= BeautifulSoup(ca['event_content'][0][1]).text[0:250]
      
        
    
        for con in ca['event_content']:
            if con[0] in [u'购买须知']:
                event['note']=con[1]
                break
    
        try:
            event['note']=str_html(event['note']).replace('\r\n','')
            event['note']=BeautifulSoup(event['note']).text
            o=event['note'].find(u'。')
            if o>0:
                event['note']=event['note'][:o]
            else:
                no=event['note'].split(u'，')
                if len(no)>2:
                    event['note']='%s%s' % (u'，'.join(no[:2]),'...')
        except:
            event['note']=''    
            
        event['comment']={}
        try:        
            com=UserEventMessage.objects.filter(event_id=ca['event_id']).order_by('id')[0]
            event['comment']['id']=com.id
            event['comment']['content']=com.message.txt
            event['comment']['date']=time.mktime(com.end_time.timetuple())
            
            event['comment']['score']=0
            event['comment']['imgs']=[]
            event['comment']['user']={'id':com.user.user_id,'name':com.user.user_name}
    
        except:
            pass
        event['commentTotol']={}
        
        event['more']=[]
        for ev in event_city_cat(ca['district_id']):
            if ev!=event['id']:
                
                e=NewAppEvent(None,ev)
                even={'id':e['event_id'],'title':e['title'],'price':e['app_price'],'imgs':e['img_s']}
                event['more'].append(even)
                
            if len(event['more'])>4:
                break
        
        return event
