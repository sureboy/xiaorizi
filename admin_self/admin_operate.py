#coding:utf-8
import django.contrib.admin as admin
from admin_self.common import NewCity,updata_cache
from admin_self.froms import  myTextareaWidget
from django.db import models 
from LifeApi.models import NewEventCat,NewEventPriceType
from LifeApi.common import NewAppEvent
import datetime
from django.contrib.auth.models import User
#import sponsor.boring_encode as mess

class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides={models.TextField:       {'widget':myTextareaWidget},}
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'edit', None) is None:
            obj.edit = request.user
        obj.last_edit = request.user
        obj.save()
    raw_id_fields = ['img','cat','city']
    fields = ('name','content','img', 'cat',  'city')
    list_display = ('name','content', 'cat',  'city')

class DistrictMPTTModelAdmin(admin.ModelAdmin):
    
    
    # speficfy pixel amount for this ModelAdmin only:
    list_per_page=10
    list_max_show_all=20
    
    list_display = ('id','district_id','district_name','title','capital_letter','parent')
    raw_id_fields = ['img']
    list_editable=( 'parent','title','capital_letter')
    
    search_fields = ('id' ,'district_id','district_name','title', 'capital_letter')
   
    mptt_level_indent = 20
    def save_model(self, request, obj, form, change):
        ci=NewCity(3)
        if not ci.has_key(obj.title):
            NewCity(3,True)
        
       
        obj.save()
    
class VenueAdmin(admin.ModelAdmin):
    raw_id_fields = ['city','venue_class','img']
    list_display = ('id','city','venue_class','address','title','event_gl',)
            #'show_url')
    
    def event_gl(self,obj):
        str=''
        for cat in obj.neweventtable_set.all():
            str+='<a href="/admin/new_event/neweventtable/%s"  target="_blank"  >%s</a><br>' % (cat.id,cat.name)
        return str
    event_gl.short_description = u'活动'
    event_gl.allow_tags = True    
    
    #def show_url(self, obj):
    #    mess_str = mess.encode(int(obj.id), 6)
    #    return u'<a href="http://test3.huodongjia.com/venue-%s.html" \
    #target="_blank">预览</a>' \
    #        % (mess_str)

    #show_url.short_description = u'页面预览'
    #show_url.allow_tags = True
    

    search_fields=( 'address','title','id','neweventtable__id','neweventtable__old_event__event_id')
    
class cat_seo(admin.SimpleListFilter):
    title = (u'销售状态') 
    parameter_name = 'price_type'
    def lookups(self, request, model_admin):
 
        return (
            (0, u'分类关联'),
            (1, u'活动关联'),
          
        )
        
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():    
            queryset.extend()        
            return queryset.filter(Price__Type=self.value())   

class SeoAdmin(admin.ModelAdmin): 
    list_per_page=20
    list_max_show_all=20
    
    def cat_gl(self,obj):
        str=''
        for cat in obj.neweventcat_set.all():
            str+='<a href="/admin/new_event/neweventcat/%s"  target="_blank"  >%s</a><br>' % (cat.id,cat.name)
        return str
    cat_gl.short_description = u'分类'
    cat_gl.allow_tags = True
    #cat_gl.admin_order_field = 'event_id'  
    
    def event_gl(self,obj):
        str=''
        for cat in obj.neweventtable_set.all():
            str+='<a href="/admin/new_event/neweventtable/%s"  target="_blank"  >%s</a><br>' % (cat.id,cat.name)
        return str
    event_gl.short_description = u'活动'
    event_gl.allow_tags = True
    #event_gl.admin_order_field = 'event_id'  
    
    list_editable=( 'title','keywords','description',)
    list_display = ('id', 'name','title','keywords','description',)
    search_fields=( 'id','name','title','keywords','description',)

class EditCat(admin.SimpleListFilter):
    title = (u'专题')
 
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'cats'
 
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [(pt.id,pt.name) for pt in NewEventCat.objects.filter(parent=91)]
        return (           
            (54, u'成都'),
            (99, u'上海'),
            (101, u'北京'),
        ) 
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(event__cat=int(self.value()))

class PriceType(admin.SimpleListFilter):
    title = (u'销售状态') 
    parameter_name = 'price_type'
    def lookups(self, request, model_admin):
        return [(pt.id,pt.name) for pt in NewEventPriceType.objects.all()]
        '''
        return (
            (0, u'未开始'),
            (1, u'未过期'),
            (2, u'已经过期'),
        )
        '''
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():          
            return queryset.filter(event__Price__Type=self.value())           



class EditStateFilter_new(admin.SimpleListFilter):
    title = (u'过期状态')
 
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'edit_state'
 
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (           
            (1, u'未过期'),
            #(2, u'活动展示'),
        ) 
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
 
            if int(self.value()) == 1:

                return  queryset.filter(event__end_time__gt=datetime.datetime.now())   

class SmallIsShowFilter(admin.SimpleListFilter):
    title = u'状态'
    parameter_name = 'edit_isshow'

    def lookups(self, request, model_admin):
        return (
                ('1', u'已发布'),
                ('2', u'废弃'),
                ('3', u'待完善'),
                ('5', u'编辑中'),
                ('8', u'后备库'),
                (-1, u'活动编辑'),
                (-2, u'活动展示'),
                )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == '-1':
                return queryset.filter(event__isshow=0)
            elif self.value() == '-2':
                return  queryset.filter(event__end_time__gt=datetime.datetime.now()).filter(event__isshow__in=(1,8,))   
            else:
                return queryset.filter(event__isshow_id=self.value())
    

class EditCity(admin.SimpleListFilter):
    title = (u'城市')
 
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'citys'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (           
            (54, u'成都'),
            (99, u'上海'),
            (101, u'北京'),
            (69, u'台北'),
            (98, u'重庆'),
            (501,u'里斯本'),
            (14,u'苏州'),
            (17,u'杭州'),
            (30,u'厦门'),
            (48,u'广州'),
            (62,u'西安'),
            (76,u'迪拜'),
            (186,u'罗马'),
            (220,u'伦敦'),
            (241,u'巴黎'),
            
      
            
            
            
        ) 
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(event__city=int(self.value()))
class User_show_new(admin.SimpleListFilter):
    title = (u'创建/发布')
    parameter_name = 'edit_name'
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [(pt.id,'%s(%s%s)' % (pt.username,pt.first_name,pt.last_name) ) for pt in User.objects.filter(is_staff=True, is_active=True)]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(event__edit_id=int(self.value()))
def show_app_life(k,un=False):
    
    def adds(self, request, queryset):
        message_bit=''
   
        for ev in queryset:
            ev.event.cat.add(k)
            
            if k.type_id==2:
                ev.event.old_event.event_cool=k.cat_id-1000
                ev.event.old_event.save()
                  
            message_bit += u"《%s》" % (ev.event.name)
            
            updata_cache(ev.event)

        self.message_user(request, u"%s 添加到 %s " % (message_bit,k.name))
 
    if k.type_id==3:
        adds.short_description = u"+ t %s" % (k.name)
    else:
        adds.short_description = u"+ %s" % (k.name)
    def dele(self, request, queryset):
        message_bit=''
        for ev in queryset:
            ev.event.cat.remove(k)
             
            if k.type_id==2:
                ev.event.old_event.event_cool=0
                ev.event.old_event.save()
         
            message_bit += u"《%s》" % (ev.event.name)
            updata_cache(ev.event)
        self.message_user(request, u"%s 取消 %s" % (message_bit,k.name))
    dele.short_description = u"- %s" % (k.name)
   
    if not un:
        return adds
    else:
        return dele            
class feelnumAdmin(admin.ModelAdmin):
    
    def __init__(self, model, admin_site):        
        self.add_actions()
        super(feelnumAdmin, self).__init__(model, admin_site)    

    

    def add_actions(self):   
        from django.db.models import Q
        import datetime
        for k in NewEventCat.objects.filter(parent=91).order_by('-type','-id'):
            setattr(self.__class__,'%s' % k.ename,staticmethod(show_app_life(k,False)))          
            self.actions.append(k.ename)
            setattr(self.__class__,'un%s' % k.ename,staticmethod(show_app_life(k,True)))          
            self.actions.append('un%s' % k.ename)
        
    
    list_per_page=20
    list_max_show_all=20
    
    def show_new(self,obj):
        str=''
        if obj.event.old_event_id:
            str+='<a href="http://life.huodongjia.com/api/eventinfoapi/?eventid=%s&new=1"    target="_blank"  >刷新</a><br>' % (obj.event.old_event_id,)
            #str+='<a href="http://www.huodongjia.com/event-%s.html?new=1"    target="_blank"  >查看</a><br>' % (obj.event.old_event_id,)
            str+='<a href="/admin/new_event/neweventtable/%s?tp=1"  target="_blank"   >查看/修改</a><br>' % (obj.event.id,)
        return str
    show_new.short_description = u'生活家刷新'
    show_new.allow_tags = True
    def show_content(self,obj):
        if obj.content:
            return obj.content
        elif obj.event.content:
            return obj.event.content
        else:
            return ''
    show_content.short_description = u'简介'
    show_content.allow_tags = True
    def event_gl(self,obj):

        #st='<a href="http://admin5.huodongjia.com/admin/new_event/neweventtable/%s"  target="_blank"  >%s</a>' % (obj.event.id,obj.event.fname if obj.event.fname else obj.event.name)
        st='<a href="/admin/new_event/neweventtable/%s"  target="_blank"  >%s</a>' % (obj.event.id,obj.event.fname if obj.event.fname else obj.event.name)
        
        for ca in obj.event.cat.all():
            
            st+='<br />'
            st+=ca.name
        
        
        if obj.event.state==1:
            st+='<br />'
            st+=u'长期'
        else:
            st+='<br />%s-%s' % (obj.event.begin_time,obj.event.end_time)
            
            
        return st
    event_gl.short_description = u'活动'
    event_gl.allow_tags = True
    event_gl.admin_order_field = 'event__begin_time'
    def feel_show(self,obj):
        str=''
        if obj.feel:
            str+='%s' % obj.feel.name
        return str
    feel_show.short_description = u'指数'
    def show_city(self,obj):
        str=''
        try:
            for ci in obj.event.city.all():
                if str != '':
                    str+='<br />'
                str+=ci.district_name
        except:
            pass
        try:            
            for addrs in  obj.event.addr.all():
                ve = addrs.title if addrs else '' 
                add = addrs.address if addrs else ''
                
                str+='<br>'
                str+=ve[:10] if ve else add[:10]
        except:
            pass
        return str

    show_city.short_description = u'城市/地址'
    show_city.allow_tags = True
    show_city.admin_order_field = 'event__addr'
    
    def price_show(self,obj):
        if  obj.event.old_event_id:
            ev=NewAppEvent(None,obj.event.old_event_id)
        else:
            ev=NewAppEvent(None,obj.event.id)

    
        return '<a href="/admin/new_event/neweventpriceunit/?q=%s"  target="_blank"  >%s</a>' % (ev['id'],ev['event_price'])
        #pr = obj.event.Price_event_table.filter(Currency=obj.event.Price.Currency).order_by('price')
    price_show.short_description = u'价格'
    price_show.allow_tags = True
    price_show.admin_order_field = 'event__Price_event_table__price'

    def pushMsg(self,obj):
        '''
        百度云消息推送
        '''

        id = obj.event.id

        st= u"广播<br><a target='_blank' href='http://life.huodongjia.com/BaiduPushSDK/sample/pushmsg.php?id=%s&type=0'>IOS</a> <a target='_blank' href='http://life.huodongjia.com/BaiduPushSDK/sample/pushmsg.php?id=%s&type=1'>ANDROID</a><br>" %(id,id)
        
        st+= u"定点<br><a target='_blank' href='http://life.huodongjia.com/BaiduPushSDK/sample/userpushmsg.php?id=%s&type=0'>IOS</a> <a target='_blank' href='http://life.huodongjia.com/BaiduPushSDK/sample/userpushmsg.php?id=%s&type=1'>ANDROID</a><br>" %(id,id)
        st+= u"<a target='_blank' href='/admin/user_center/userpushinfo/?q=%s' >查看发送到用户</a>" %(id, )
        
        return st
    pushMsg.short_description = u'消息推送'
    pushMsg.allow_tags = True



    raw_id_fields = ['event']
    date_hierarchy = 'showtime'
    list_filter = [EditCity,EditCat,PriceType,EditStateFilter_new,User_show_new,SmallIsShowFilter]
    #fields = ('name','content','img', 'cat',  'city')
    list_editable=( 'feelnum','showtime','title')
    
    #list_display = ('id','show_city','price_show', 'event_gl','show_new','title', 'feelnum', 'showtime','show_content','pushMsg')
    list_display = ('id','show_city','price_show', 'event_gl','show_new', 'title', 'feelnum', 'showtime', 'show_content','pushMsg')
    
    search_fields=( 'event__id','event__fname','event__old_event__event_id','event__search')
    #list_filter=['people']
    
