#coding:utf-8
import datetime,time 
import warnings,csv
import re,json
import os

import django.contrib.admin as admin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.util import quote
from django.contrib.admin.templatetags.admin_static import static
from django.core.urlresolvers import reverse
from django.http import  HttpResponse, HttpResponseRedirect
from django.utils.html import escape, escapejs
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django import forms
from django.db import models 
from django.utils.datastructures import SortedDict

from admin_self.froms import dhdAdmin, MyFilteredSelectMultiple,\
                MyModelMultipleChoiceField,myTextareaWidget,MpttDhdAdmin,fill_topic_tree,\
                fill_topic_tree_city
from LifeApi.models import NewEventTable,NewVenue, NewEventPrice,NewEventPriceType,\
                                NewEventPriceCurrency,NewEventTag,NewEventCat,OldEvent,NewEventSeo,\
                                NewEventFromClass,NewEventFrom,admin_user,VisitRecord,NewEventCat_s,NewEventFromType,\
                                feelType,feelnum,NewEventPriceUnit, NewDistrict,NewEventImg

from admin_self.common import oldEventToNewEvent,NewEventToOldEvent,show_app,\
                                NewCatUrl, NewCity, updata_cache,city_ss,NewCatUrl_edit, \
                                get_html_file_without_extension, \
                                cat_iter, format_cat_iter, city_without_level1

from LifeApi.common import NewAppEvent


from sponsor.models import NewSponsor


import logging
log = logging.getLogger('XieYin.app')  
''' 
from django.utils.decorators import method_decorator
from django.db import  transaction 
from django.views.decorators.csrf import csrf_protect
csrf_protect_m = method_decorator(csrf_protect) 
def find_ch(id=0,cat_arr={}):
    cat_ll=[]
    if cat_arr.has_key(id):
        cat_ll.append(cat_arr[id]['cat_id'])
        if cat_arr[id]['child']:
            for ch in cat_arr[id]['child']:
                cat_ll.extend(find_ch(ch['id'], cat_arr))
                
    return cat_ll
    
    template = 'admin/filter.html'
    
'''
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
            return queryset.filter(edit_id=int(self.value()))

class User_show_new_f(admin.SimpleListFilter):
    title = (u'最后编辑')
    parameter_name = 'last_edit_name'
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [(pt.id,'%s(%s%s)' % (pt.username,pt.first_name,pt.last_name) ) for pt in User.objects.all()]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(last_edit_id=int(self.value()))
            

class EditStateFilter_new(admin.SimpleListFilter):
    title = (u'状态')
 
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
            (1, u'活动编辑'),
            (2, u'活动展示'),
        ) 
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
 
            if int(self.value()) == 1:
                return queryset.filter(isshow=0)
            elif int(self.value()) == 2:
                return  queryset.filter(end_time__gt=datetime.datetime.now()).filter(isshow__in=(1,8,))   
class et_can(admin.SimpleListFilter):
    template = 'admin/filter_time.html'
    title = (u'开始时间')
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'et'     
    def lookups(self, request, model_admin):     
        #return self.value()    
        return (
            (0, self.value()),            
        )
    def queryset(self, request, queryset):
        return
        if self.value():
            date_time=self.value().split('-') 
            if len(date_time)>2:
                begin_dates = datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
                if request.POST.get("et",''):
                    return queryset.filter(begin_time__gte=begin_dates)
class bt_can(admin.SimpleListFilter):
    template = 'admin/filter_time.html'
    title = (u'开始时间')
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'bt'     
    def lookups(self, request, model_admin):     
        #return self.value()    
        return (
            (0, self.value()),            
        )
    def queryset(self, request, queryset):
        return
        if self.value():
            date_time=self.value().split('-') 
            if len(date_time)>2:
                begin_dates = datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
                #if request.POST.get("bt",''):
                return queryset.filter(begin_time__gte=begin_dates)
class begtime_can(admin.SimpleListFilter):
    template = 'admin/filter_time.html'
    title = (u'开始时间')
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'begin'     
    def lookups(self, request, model_admin):     
        #return self.value()    
        return (
            (0, self.value()),            
        )
    def queryset(self, request, queryset):
        if self.value():
            date_time=self.value().split('-') 
            if len(date_time)>2:
                begin_dates = datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
                bt=request.GET.get("bt",'')
                if bt=='1':
                    return queryset.filter(begin_time__lte=begin_dates)                    
                elif bt=='0':
                    return queryset.filter(begin_time__gte=begin_dates)

class endtime_can(admin.SimpleListFilter):
    template = 'admin/filter_time.html'
    title = (u'结束时间')
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'end'     
    def lookups(self, request, model_admin):     
        #return self.value()    
        return (
            (0, self.value()),            
        ) 
    def queryset(self, request, queryset):
        if self.value():
            date_time=self.value().split('-') 
            if len(date_time)>2:
                begin_dates = datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
                #begin_dates = time.mktime(begin_dates.timetuple()) 
                et=request.GET.get("et",'')
                if et=='1':
                    return queryset.filter(begin_time__lte=begin_dates)
                    
                elif et=='0':
                    return queryset.filter(begin_time__gte=begin_dates)
                #return queryset.filter(begin_time__lte=begin_dates)
class Old_event_editor(admin.SimpleListFilter):
    title = (u'编辑')
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'edit_p'    
    def lookups(self, request, model_admin):
        return [(pt.u_name,pt.u_name) for pt in admin_user.objects.all()]
        
    
    def queryset(self, request, queryset):
        if self.value():  
            #self.find_ch(self.value(),NewCatUrl(2))
            return queryset.filter(event_editor__icontains=self.value())       
    

class CatList_old(admin.SimpleListFilter):
    title = (u'分类')
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'cat_p'
    #cats=[]
 
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        ch = [()]
        fill_topic_tree(choices = ch)
        choices = ch[0]
        return ((option_value, option_label) for option_value, option_label in  choices)
    
    def find_ch(self,id=0,cat_arr={}):
        cat_ll=[]
        if cat_arr.has_key(id):
            cat_ll.append(cat_arr[id]['cat_id'])
            if cat_arr[id]['child']:
                for ch in cat_arr[id]['child']:
                    cat_ll.extend(self.find_ch(ch['id'], cat_arr))
            
        return cat_ll
            
            
             
 
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():  
            #self.find_ch(self.value(),NewCatUrl(2))
            return queryset.filter(event_cat__in=self.find_ch(int(self.value()),NewCatUrl_edit(2)))


class SmallIsShowFilter(admin.SimpleListFilter):
    title = u'状态'
    parameter_name = 'edit_state'

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
                return queryset.filter(isshow=0)
            elif self.value() == '-2':
                return  queryset.filter(end_time__gt=datetime.datetime.now()).filter(isshow__in=(1,8,))   
            else:
                return queryset.filter(isshow_id=self.value())
    

class SmallCatList(admin.SimpleListFilter):
    title = u'活动分类'
    parameter_name = 'cat_p'

    cats = cat_iter(exclude_id=[69, 70, 19])
    cats_fmt = format_cat_iter(cats)

    def lookups(self, request, model_admin):
        #return ((option_value, option_label) for option_value, option_label in  self.cats_fmt)
        return self.cats_fmt

    def cat_iter_family_id(self, id_in):
        id_in = float(id_in)
        family_id = [id_in]
        cats_id, cats_label = zip(*self.cats_fmt)
        ind = cats_id.index(id_in)
        n_dash = cats_label[ind].count('-')
        
        while True:
            ind += 1
            try:
                if cats_label[ind].count('-') > n_dash:
                    family_id.append(cats_id[ind])
                else:
                    break
            except IndexError:
                break
        return family_id

    def queryset(self, request, queryset):
        if self.value():
            ids = self.cat_iter_family_id(self.value())
            queryset=queryset.filter(cat__id__in=ids)
            #queryset.query.group_by = ['id']
            return queryset

class CatList(admin.SimpleListFilter):
    title = (u'分类')
        
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'cat_p'
 
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        ch = [()]
        fill_topic_tree(choices = ch)
        choices = ch[0]
        return ((option_value, option_label) for option_value, option_label in  choices)
    
    def find_ch(self,id=0,cat_arr={}):
        cat_ll=[]
        cat_ll.append(id)
        if cat_arr.has_key(id):
            #cat_ll.append(id)
            if cat_arr[id]['child']:
                for ch in cat_arr[id]['child']:
                    cat_ll.extend(self.find_ch(ch['id'], cat_arr))
                    
        return cat_ll  
 
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        
        catinfo.query.group_by = ['id']
        """
        if self.value():            
            queryset=queryset.filter(cat__in=self.find_ch(int(self.value()),NewCatUrl_edit(2))).distinct() 
            #queryset.query.group_by = ['id']
            return queryset
        
        
class cityList_old(admin.SimpleListFilter):
    title = (u'城市')
    
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'city_p'
 
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        ci_ss=city_ss()
        if not ci_ss:
            return ()
        ci_kk=()
        for ci in ci_ss:
            if type(ci['district_id'])==list: 
                            
                strs=('_'.join(map(str,ci['district_id'])),ci['district_name'])
            else:
                strs=( ci['district_id'] ,ci['district_name'])
            ci_kk+=(strs,)
            

            
            if ci['child']:
                for c in ci['child']:
                    if type(c['district_id'])==list:                
                        strs=('_'.join(map(str,c['district_id'])),'__'+c['district_name'])
                    else:
                        strs=( c['district_id'] ,'__'+c['district_name'])
                    ci_kk+=(strs,)
 
        return ci_kk  
        
        
        ch = [()]
        fill_topic_tree_city(choices = ch)
        choices = ch[0]
        return ((option_value, option_label) for option_value, option_label in  choices)
    
    def find_ch(self,id=0,cat_arr={}):
        cat_ll=[]
        if cat_arr.has_key(id):
            cat_ll.append(cat_arr[id]['district_id'])
  
            if cat_arr[id]['child']:
                for ch in cat_arr[id]['child']:
                    cat_ll.extend(self.find_ch(ch['district_id'], cat_arr))
                    
        return cat_ll  

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value(): 
            queryset=queryset.filter(district_id__in=map(int,self.value().split('_'))).distinct()   
            return queryset        
            #return queryset.filter(district_id__in=self.find_ch(int(self.value()),NewCity(1))).distinct()
class InvalidCityList(admin.SimpleListFilter):
    title = u'地区1'
    parameter_name = 'invalid_city'
    def lookups(self, request, model_admin):
        city = city_ss()
        return ((i['district_id'], i['district_name']) for i in city)

    def queryset(self, request, queryset):
        return queryset

class ValidCityList(admin.SimpleListFilter):
    title = u'地区2'
    parameter_name = 'city_p'

    def lookups(self, request, model_admin):
        cat_filter = []
        cat_ename_dict = NewCatUrl(0, '')
        lead_cats = ['business', 'travel', 'fun']
        for lc in lead_cats:
            for i in [cat_ename_dict[lc]] + cat_ename_dict[lc]['child']:
                if i['ename']: cat_filter.append(i['ename'])
        city_ch_py = city_without_level1(False, cat_filter)

        return ((i['id'], i['district_name']) for i in city_ch_py)

    def queryset(self, request, queryset):
        if self.value():    
            queryset=queryset.filter(city__in=self.value().split(','))
            #queryset.query.group_by = ['id']
            return queryset

class EditCity(admin.SimpleListFilter):
    title = (u'使用城市')
 
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'cities'

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
            return queryset.filter(city=int(self.value()))        
class cityList(admin.SimpleListFilter):
    title = (u'城市')
    
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'city_p'
 
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        ci_ss=city_ss()
        if not ci_ss:
            return ()
        ci_kk=()
        for ci in ci_ss:
            if type(ci['id'])==list: 
                            
                strs=('_'.join(map(str,ci['id'])),ci['district_name'])
            else:
                strs=( ci['id'] ,ci['district_name'])
            ci_kk+=(strs,)
            

            
            if ci['child']:
                for c in ci['child']:
                    if type(c['id'])==list:                
                        strs=('_'.join(map(str,c['id'])),'__'+c['district_name'])
                    else:
                        strs=( c['id'] ,'__'+c['district_name'])
                    ci_kk+=(strs,)
 
        return ci_kk        
            
        ch = [()]
        fill_topic_tree_city(choices = ch)
        choices = ch[0]
        return ((option_value, option_label) for option_value, option_label in  choices)
    
 

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():    
    
            
            
            queryset=queryset.filter(city__in=map(int,self.value().split('_'))).distinct()
            #queryset.query.group_by = ['id']
            return queryset
            

class PriceType(admin.SimpleListFilter):
    title = (u'销售状态') 
    parameter_name = 'price_type'
    def lookups(self, request, model_admin):
        '''
        1:折扣价
        2:用户出价
        3:众筹
        4:免费
        5:收费
        6:标准
        7:待定
        '''
        return [(pt.id,pt.name) for pt in NewEventPriceType.objects.exclude(id__in=(2,3))]
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
            return queryset.filter(Price__Type=self.value())           



class DateStateNew(admin.SimpleListFilter):
    title = (u'时间状态') 
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'date_state' 
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (0, u'未开始'),
            (1, u'未过期'),
            (2, u'已经过期'),
        )
 
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            if int(self.value()) == 0:
                return queryset.filter(begin_time__gt=datetime.datetime.now())
            if int(self.value()) == 1:
                return queryset.filter(end_time__gt=datetime.datetime.now())
            if int(self.value()) == 2:
                return queryset.filter(end_time__lt=datetime.datetime.now())  


class EventForm(forms.ModelForm):
    addr = MyModelMultipleChoiceField(queryset=NewVenue.objects.all(), required=False,
        widget=MyFilteredSelectMultiple(verbose_name=u"场馆地址", is_stacked=False))
    
    #cat = MyModelMultipleChoiceField(queryset=NewEventCat.objects.all(), required=False,
        #widget=MyFilteredSelectMultiple(verbose_name=u"分类", is_stacked=False)) 

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        try:
            i = kwargs["instance"]
            event = NewEventTable.objects.get(pk=i.pk)
            qs = event.addr.all()
        except:
            qs = NewVenue.objects.none()
                       
        self.fields['addr'].queryset = qs
        self.fields['addr'].label=u'场馆地址'
        
         
        #self.fields['cat'].label=u'分类'
        #self.fields['addr']
        
   
    class Meta:
        model = NewEventTable    
        widgets = {
            'addr': MyFilteredSelectMultiple(verbose_name=u"场馆地址", is_stacked=False),           
            #'cat': MyFilteredSelectMultiple(verbose_name=u"分类", is_stacked=False), 
        }

class myAdminDateWidget(forms.DateInput):

    @property
    def media(self):
        js = ["calendar.js", "admin/DateTimeShortcuts.js"]
        return forms.Media(js=[static("admin/js/%s" % path) for path in js])

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'vDateField1', 'size': '10'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(myAdminDateWidget, self).__init__(attrs=final_attrs, format=format)
        
class feedshow(admin.SimpleListFilter):
    title = (u'生活家') 
    parameter_name = 'feedshow'
    def lookups(self, request, model_admin):

        return (            
            (1, u'生活家数据'),     
        )
        
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():            
            return queryset.exclude(event_feelnum=None)          



class EventAdmin(dhdAdmin):
    '''
    formfield_overrides={models.TextField:       {'widget':myTextareaWidget},
                         
                         }
    '''

    formfield_overrides = {
            models.DateTimeField: {'widget': None}
    }

    add_form_template = None
    change_form_template = 'admin/new_event/neweventtable/change_form_custom_new.html'
    list_per_page=10
    list_max_show_all=10

    def publish(self, request, queryset):
        for ev in queryset:
            ev.isshow_id = 1
            ev.save()
    publish.short_description = u'发布选中活动'
    
    def mdake_published(self, request, queryset):
        for ev in queryset:
            ev.order=ev.order+1 if ev.order else 1
            ev.old_event.event_rank=1
            ev.old_event.event_order=ev.old_event.event_order+1 if ev.old_event.event_order else 1
            ev.old_event.save()
            ev.save()            
            updata_cache(ev)            
 
            
        
        #queryset.update(status='p')
    mdake_published.short_description = u"推荐活动"    
    
    def Un_published(self, request, queryset):
        for ev in queryset:
            ev.order=ev.order-1 if ev.order else 0
            ev.old_event.event_rank=0
            ev.old_event.event_order=ev.old_event.event_order-1 if ev.old_event.event_order else 0
            ev.old_event.save()
            ev.save()
        pass
        #queryset.update(status='p')
    Un_published.short_description = u"取消推荐活动"   
    
    
    def Download_csv(self, request, queryset):
        #data =queryset
        response = HttpResponse(mimetype="text/csv")
        filename=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d') 
        response['Content-Disposition'] = 'attachment; filename=%s.csv'  % filename
        writer = csv.writer(response)  
        #writer.writerow([u'活动',u'活动id',u'下单时间',u'用户名称',u'手机','详情',u'订单总额'])  
        num=[u'活动',u'活动url',u'地址',u'开始时间',u'结束时间',u'价格']
        for i in range(len(num)):
            if num[i]:
                num[i]=num[i].encode('utf8')  
            
        writer.writerow(num)  
        for item in queryset:  
            #'show_event','begintime','order_user_info','order_totalpay', 'order_price_info','admin_text','order_payment', 'order_status',  'order_pay_status'
            #writer.writerow([item.event_name,item.event.old_event,item.addtime,item.order_user_name,item.order_tel,self.order_user_info(item),item.order_totalpay])  
            items=[item.name.encode('utf8'),u'http://www.huodongjia.com/event-%s.html' % item.old_event_id,
                   self.citys_addr(item).replace('\r\n','|').replace('<br>','|').encode('utf8'),
                   self.begintime(item).encode('utf8'),
                   self.endtime(item).encode('utf8'),
                   self.Price_Type_is(item).replace('\r\n','|').replace('<br>','|').encode('utf8'),                   
                   ]
            '''
            new_ite=[]
            for i in range(len(items)):
                if  type(items[i])==str:
                    items[i]=items[i].encode('utf8')
                #items[i]=items[i].replace('\r\n',',').replace('<br>',',')
                new_ite.extend(str(items[i]).replace('\r\n','|').replace('<br>','|'))
            '''
            writer.writerow(items)
        return response  

        #queryset.update(status='p')
    Download_csv.short_description = u"csv下载"   
    #actions=[Download_csv] 
    
    
    actions=[publish, mdake_published,Un_published,Download_csv] 

    #def __init__(self, model, admin_site):        
    #    self.add_actions()
    #    super(EventAdmin, self).__init__(model, admin_site)    
     
   
    #def add_actions(self):   
    #     
    #    for k in NewEventCat.objects.filter(type_id__in=[3]):
    #        setattr(self.__class__,'%s' % k.ename,staticmethod(show_app(k,False)))          
    #        self.actions.append(k.ename)
    #        setattr(self.__class__,'un%s' % k.ename,staticmethod(show_app(k,True)))          
    #        self.actions.append('un%s' % k.ename)
        
    @staticmethod
    def add_cat(cat):
        def action(modeladmin, request, queryset): 
            for q in queryset:
                q.cat.add(cat)
        name = u"add_cat_id_%s" %cat.id
        return (name, (action, name, u"Add %s" %cat.name))

    @staticmethod
    def remove_cat(cat):
        def action(modeladmin, request, queryset): 
            for q in queryset:
                q.cat.remove(cat)
        name = u"remove_cat_id_%s" %cat.id
        return (name, (action, name, u"Remove %s" %cat.name))
        
    def get_actions(self, request):
        actions = super(EventAdmin, self).get_actions(request)
        _tmp = []
        cats = NewEventCat.objects.filter(type_id__in=[3])
        city = request.GET.get('cities')
        if city:
            cats = cats.filter(city__id=city)
        for cat in cats:
            _tmp.append(self.add_cat(cat))
            _tmp.append(self.remove_cat(cat))
        actions.update(SortedDict(_tmp))

        return actions
            

    '''
    def k(self, request, queryset):
        pass
        #queryset.update(status='p')
    k.short_description = u"推荐选中项" 
    actions = []   
    actions.append(k)  
    '''  

    def add_view(self, request, form_url='', extra_context=None):
        
        #print request.GET.get("id",False)  
        ids=request.GET.get("id",False)  
 
        if ids:
            #print 'OKK'
        #ids=int(ids)
        #if type(ids)==int:
            
            p=oldEventToNewEvent(ids)

            #return qs.filter(models.Q(edit=request.user)|models.Q(last_edit=request.user)) 
            if p:
                
                '''
                if not p.edit:
                    p.edit=request.user
                p.last_edit=request.user
                p.save()  
                '''
                
                      
                return self.change_view(request,str(p.id),  form_url , extra_context  )

        extra_context={}
        extra_context.update({           
                            'pricecurr':NewEventPriceCurrency.objects,
                            'pricetype':NewEventPriceType.objects,  
                            'FromClass':NewEventFromClass.objects,
                            'FromType':NewEventFromType.objects,
                            'feelType':feelType.objects,
                            #'zhuantiList': get_html_file_without_extension(zhuantiDirectory()),
                            'cities':NewDistrict.objects.filter(usetype=1),
                            #'cat_list':choices,
                            })
        return super(EventAdmin, self).add_view(request,  form_url , extra_context  )

 
    def change_view(self, request, object_id, form_url='', extra_context=None):
        #return None
        #extra_context NewEventTable
        #if request.POST
        from django.contrib.admin.util import  unquote 
        obj = self.get_object(request, unquote(object_id))
        '''
        if request.GET.get('tp')=='1':

            self.change_form_template = ''
        '''
        ch = [()]
        fill_topic_tree(choices = ch)
        choices = ch[0]
        extra_context={}
        if request.method == 'POST':
            log.debug(object_id)
            log.debug(request.POST) 
        extra_context.update({'event_id':obj.old_event.event_id if obj.old_event else '',
                              'pr':obj.old_event.event_price_backup if obj.old_event else '',
                              'from_url':obj.old_event.event_officer if obj.old_event else '',
                              'crawl_site':obj.old_event.crawl_site if obj.old_event else '',
                              'crawl_url':obj.old_event.crawl_url if obj.old_event else '',
                              'crawl_title':obj.old_event.crawl_title if obj.old_event else '',
                              'crawl_time':datetime.datetime(*time.localtime(obj.old_event.crawl_time)[:6]) if obj.old_event else '',
                              'tag':NewEventTag.objects.all().order_by('-id')[:20],
                              #'con':con_pr,
                              'addr_old':obj.old_event.venue_info if obj.old_event else '',
                              'event':obj,
                              'cat_list':choices,
                              'pricecurr':NewEventPriceCurrency.objects,
                              'pricetype':NewEventPriceType.objects,
                              'FromClass':NewEventFromClass.objects,
                              'FromType':NewEventFromType.objects,
                              'feelType':feelType.objects,
                              'paragraph':obj.paragraph.all().order_by('-txt_order'),                              
                              #'zhuantiList': get_html_file_without_extension(zhuantiDirectory()),
                              'cities':NewDistrict.objects.filter(usetype=1),                              })

        
        return super(EventAdmin, self).change_view(request, object_id, form_url , extra_context  )
    
 
    def changelist_view(self, request, extra_context=None):
        
        extra_context={}

        extra_context.update({'begin_s': request.GET.get("begin",''),
                              'end_s': request.GET.get("end",''), 
                              'bt': request.GET.get("bt",'0'), 
                              'et': request.GET.get("et",'1'), 
                              'city': json.dumps(city_ss()),
                              'invalid_city': request.GET.get('invalid_city'),
                              'city_p': request.GET.get('city_p'),
                              })  
        
        
        return super(EventAdmin, self).changelist_view(request,  extra_context  )
     
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'test':request.GET.get("begin_s",False),
        }) 
         
        return super(EventAdmin, self).render_change_form(request, context, add , change , form_url , obj )
        
    def response_change(self, request, obj, continue_editing_url=None,save_as_new_url=None, add_another_url=None,hasperm_url=None, noperm_url=None):
        
        if request.method == 'POST':
            ModelForm = self.get_form(request, obj)
            form = ModelForm(request.POST, request.FILES, instance=obj)
            
            if 'tp=1' in request.get_full_path():
                self.save_model_x(request, obj, form, True)
            else:
                self.save_model_s(request, obj, form, True)
            #NewAppEvent(obj, new=True)
            try:
                updata_cache(obj)
            except:
                pass
        #return super(EventAdmin, self).response_change(request, obj, continue_editing_url,save_as_new_url , add_another_url ,hasperm_url , noperm_url )
        try:
            return super(EventAdmin, self).response_change(request, obj, continue_editing_url,save_as_new_url , add_another_url ,hasperm_url , noperm_url )
        except:
            return super(EventAdmin, self).response_change(request, obj  )
    
    def response_add(self, request, obj, post_url_continue='../%s/',
                     continue_editing_url=None, add_another_url=None,
                     hasperm_url=None, noperm_url=None):
        
        if request.method == 'POST':
            ModelForm = self.get_form(request, obj)
            form = ModelForm(request.POST, request.FILES, instance=obj)
            #self.save_model_add(request, obj, form, True)
            self.save_model_s(request, obj, form, True)
            #NewAppEvent(obj, new=True)
            try:
                updata_cache(obj)
            except:
                pass
            
            #updata_cache(obj)
        if post_url_continue != '../%s/':
            warnings.warn("The undocumented 'post_url_continue' argument to "
                          "ModelAdmin.response_add() is deprecated, use the new "
                          "*_url arguments instead.", DeprecationWarning,
                          stacklevel=2)
        opts = obj._meta
        pk_value = obj.pk
        app_label = opts.app_label
        model_name = opts.module_name
        site_name = self.admin_site.name

        msg_dict = {'name': force_text(opts.verbose_name), 'obj': force_text(obj)}

        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if "_continue" in request.POST:
            msg = _('The %(name)s "%(obj)s" was added successfully. You may edit it again below.') % msg_dict
            self.message_user(request, msg)
            if continue_editing_url is None:
                continue_editing_url = 'admin:%s_%s_change' % (app_label, model_name)
            url = reverse(continue_editing_url, args=(quote(pk_value),),
                          current_app=site_name)
            if "_popup" in request.POST:
                url += "?_popup=1"
            return HttpResponseRedirect(url)

        if "_popup" in request.POST:
            return HttpResponse(
                '<!DOCTYPE html><html><head><title></title></head><body>'
                '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script></body></html>' % \
                # escape() calls force_text.
                (escape(pk_value), escapejs(obj)))
        elif "_addanother" in request.POST:
            msg = _('The %(name)s "%(obj)s" was added successfully. You may add another %(name)s below.') % msg_dict
            self.message_user(request, msg)
            if add_another_url is None:
                add_another_url = 'admin:%s_%s_add' % (app_label, model_name)
            url = reverse(add_another_url, current_app=site_name)
            return HttpResponseRedirect(url)
        else:
            msg = _('The %(name)s "%(obj)s" was added successfully.') % msg_dict
            self.message_user(request, msg)

            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            if self.has_change_permission(request, None):
                if hasperm_url is None:
                    hasperm_url = 'admin:%s_%s_changelist' % (app_label, model_name)
                url = reverse(hasperm_url, current_app=site_name)
            else:
                if noperm_url is None:
                    noperm_url = 'admin:index'
                url = reverse(noperm_url, current_app=site_name)
            return HttpResponseRedirect(url)
     
        '''       
        try:
            return super(EventAdmin, self).response_add(request, obj, post_url_continue,\
                         continue_editing_url , add_another_url,\
                         hasperm_url, noperm_url)
        except:
            return super(EventAdmin, self).response_add(request, obj, post_url_continue )
        '''
        

    def save_model_add(self, request, obj, form, change): 
        for ad in obj.addr.all():
            obj.city.add(ad.city)
        '''
        for ta in obj.tag.all():
            for t in ta.neweventcat_set.all():
                obj.cat.add(t)
        '''
                
        obj.save()
              
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'edit', None) is None:
            obj.edit = request.user
        obj.last_edit = request.user

        try:
            old_obj=NewEventTable.objects.get(id=obj.id)
            if old_obj.Price:
                obj.Price= old_obj.Price
                
        except:
            pass
        
        
        obj.save()

        #for ta
        
        if obj.old_event:
            if obj.isshow:      
                obj.old_event.event_isshow=obj.isshow_id          
            #obj.old_event.event_app_name=obj.fname if obj.fname else ''
            
            obj.old_event.event_order= obj.order if obj.order else 0
            try:
                obj.old_event.save()
            except:
                pass
        '''
        else:
            obj.old_event=OldEvent.objects.create(
                                                  event_isshow=obj.isshow_id,
                                                  event_app_name=obj.fname if obj.fname else '',
                                                  event_order=obj.order if obj.order else 0,
                                                  #district_id=NewDistrict_s.objects.get(district_id=45052),
                                                  )
        
 
        
            obj.save()
        '''

        
         
            
        updata_cache(obj)
         
    def save_model_x(self, request, obj, form, change):
        #super(EventAdmin, self).save_model(request, obj, form, change)
        #super(EventAdmin, self).save_related(request, form, formsets=[], False)

        if request.POST.get('state') or not obj.end_time:
            obj.state = 1
            obj.end_time = datetime.datetime.now() + datetime.timedelta(days=365*50)
        else:
            obj.state = 0
        obj.save()
        
        #if not obj.end_time:
        #    obj.state=1
        #    jo= '2015-12-30'
        #    date_time=jo.split('-')         
 
        #    obj.end_time=datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
        #else:
        #    obj.state=0
        
        
        
        
        mi=request.POST.get("min_pr",False)
        mi=mi if mi else 0
        
        ma=request.POST.get("max_pr",False)
        ma=ma if ma else 0
        
        pr_Currency=request.POST.get("pr_Currency",False)
        pr_Currency=pr_Currency if pr_Currency else 1
        
        pr_Type=request.POST.get("pr_Type",False)
        pr_Type=pr_Type if pr_Type else 5
        
        pr_str= request.POST.get("pr_str",'')
        pr_str=pr_str if pr_str else ''

        zpr_str= request.POST.get("zpr_str",'')
        zpr_str=zpr_str if zpr_str else ''        
        
        
        
        if obj.Price:
            
            obj.Price.Currency=NewEventPriceCurrency.objects.get(id=pr_Currency)  
            obj.Price.Type=NewEventPriceType.objects.get(id=pr_Type)  
            obj.Price.str =pr_str   
            obj.Price.sale=zpr_str  

            obj.Price.min=mi
 
            obj.Price.max=ma
            obj.Price.save()
        else:
 
            obj.Price=NewEventPrice.objects.create(
                 Currency=NewEventPriceCurrency.objects.get(id=pr_Currency) ,
                 Type=NewEventPriceType.objects.get(id=pr_Type) ,
                 str =pr_str,
                 sale=zpr_str, 
                 min=mi ,  
                 max=ma ,  
                 
                )
           
      
        
        for ad in obj.addr.all():
            obj.city.add(ad.city)
   
        
        #if obj.cat        
        obj.save()

        updata_cache(obj)
 
        
        
        #ToEventPrice(obj.id) 
         
    


    def save_model_s(self, request, obj, form, change):
        #super(EventAdmin, self).save_model(request, obj, form, change)
        #super(EventAdmin, self).save_related(request, form, formsets=[], False)
        

        if request.POST.get('state') or not obj.end_time:
            obj.state = 1
            obj.end_time = datetime.datetime.now() + datetime.timedelta(days=365*50)
        else:
            obj.state = 0
        obj.save()
        

        # 保存主办方
        sponsor_str = request.POST.get('add_sponsor')
        sponsor_id_org = [i.id for i in NewSponsor.objects.filter(events__in=[obj.id])]
        sponsor_id_now = []
        sponsor_list = []
        if sponsor_str and obj.city.all():
            #sponsor_list = json.loads(sponsor_str.replace('\'', '"'))
            sponsor_list = json.loads(sponsor_str)
            for sponsor_dict in sponsor_list:
                get_flag = False
                try:
                    sponsor_id = sponsor_dict['id']
                except KeyError:
                    sponsor_id = None
                    
                try:
                    sponsor_pic_id = int(sponsor_dict['pic'])
                except:
                    sponsor_pic_id = None
                try:
                    sponsor_intro = sponsor_dict['intro']
                except:
                    sponsor_intro = None
                
                sponsor_verify = True if sponsor_dict['verify'] == 'true' else False
                sponsor_name = sponsor_dict['sponsor_name']
                #如果是原来的主办方
                if sponsor_id:
                    try:
                        v = NewSponsor.objects.get(id=sponsor_id)
                        
                        if sponsor_pic_id:
                            try:
                                objpic = NewEventImg.objects.get(id=sponsor_pic_id)
                                #如果原来的主办方存在则更新
                                v.pic = objpic
                                #get_flag=True则不再新建对象
                                v.save()
                                get_flag = True
                            except:
                                pass
                            
                        if sponsor_intro:
                            v.intro = sponsor_intro
                            get_flag = True
                        
                        get_flag = True
                        
                    except:
                        pass
                    
                
                #如果是新添加的主办方
                if not get_flag and sponsor_name:
                    try:
                        #如果主办方名称相同则不再保存
                        v = NewSponsor.objects.get(name=sponsor_name)
                    except:
                        v = NewSponsor()
                        v.name = sponsor_name
                        v.is_verify = sponsor_verify
                        
                        #如果有图片
                        if sponsor_pic_id:
                            try:
                                objpic = NewEventImg.objects.get(id=sponsor_pic_id)
                                v.pic = objpic
                            except Exception,e:
                                pass
                                    
                        #如果有主办方简介
                        if sponsor_intro:
                            v.intro = sponsor_intro
                        v.save()

                v.events.add(obj)
                sponsor_id_now.append(v.id)

                # 合并多余主办方
                sponsor_same_name = NewSponsor.objects.filter(name=sponsor_name).exclude(id=v.id)
                
                if len(sponsor_same_name) > 0:
                    for sponsor_clone in sponsor_same_name:
                        for sponsor_clone_event in sponsor_clone.events.all():
                            v.events.add(sponsor_clone_event)
                        if sponsor_clone.is_verify:
                            v.is_verify = True
                            v.save()
                        sponsor_clone.delete()
                #----------------

        # 删除以前关联的但现在不关联的主办方
        for del_id in filter(lambda x: x not in sponsor_id_now, sponsor_id_org):
            try:
                NewSponsor.objects.get(id=del_id).events.remove(obj)
            except:

                pass



        # 保存场馆地址
        venue_str = request.POST.get('add_address')
        
        venue_id_org = [i.id for i in obj.addr.all()]
        venue_id_now = []
        if venue_str and obj.city.all():
            #venue_list = json.loads(venue_str.replace('\'', '"'))
            venue_list = json.loads(venue_str)
            for venue_dict in venue_list:

                get_flag = False
                try:
                    venue_id = venue_dict['id']
                except KeyError:
                    venue_id = None
                venue_addr = venue_dict['venue_addr']
                venue_name = venue_dict['venue_name']
                
                try:
                    venue_point = venue_dict['venue_point']
                except:
                    venue_point=None
                                        
                #如果是原来的场馆地址
                if venue_id:
                    try:
                        v = NewVenue.objects.get(id=venue_id)
                        #如果添加了坐标
                        if venue_point:
                            try:
                                po = venue_point.split('-')
                                if len(po) == 2:
                                    v.longitude_baidu = po[0]
                                    v.latitude_baidu = po[1]
                                    v.save()
                                    get_flag = True
                            except:
                                pass
                                
                    except:
                        pass
                #如果是新添加的地址则新建对象并保存
                if not get_flag and venue_addr:
                    try:
                        v = NewVenue.objects.get(address=venue_addr)
                    except:

                        v = NewVenue()
                        v.address = venue_addr
                        v.title = venue_name
                        v.city=obj.city.order_by('-id')[0]
                        
                        if venue_point:
                            po=venue_point.split('-')
                            if len(po)==2:
                                v.longitude_baidu = float(po[0])
                                v.latitude_baidu = float(po[1])
                        
                        v.save()


                obj.addr.add(v)
                venue_id_now.append(v.id)
        
        for del_id in filter(lambda x: x not in venue_id_now, venue_id_org):
            try:
                obj.addr.remove(NewVenue.objects.get(id=del_id))
            except:
                pass
        
        addr_str=request.POST.get("addr_input_z",False)
        if addr_str and not obj.addr.all().count() and obj.city.all().count()>0:

            try:
                v=NewVenue.objects.create(
                            #title=v_i[0],
                            address=addr_str,
                            city=obj.city.order_by('-id')[0],
                            #longitude_baidu=longitude_baidu,
                            #latitude_baidu=latitude_baidu,
                            
                            )
                obj.addr.add(v)
            except:
                v=NewVenue.objects.get(address=addr_str)
                obj.addr.add(v)
         
                
            
             
        
        
        mi=request.POST.get("min_pr",False)
        mi=mi if mi else 0
        
        ma=request.POST.get("max_pr",False)
        ma=ma if ma else 0
        
        pr_Currency=request.POST.get("pr_Currency",False)
        pr_Currency=pr_Currency if pr_Currency else 1
        
        pr_Type=request.POST.get("pr_Type",False)
        pr_Type=pr_Type if pr_Type else 5
        
        #pr_str= request.POST.get("pr_str",'')
        #pr_str=pr_str if pr_str else ''

        zpr_str= request.POST.get("zpr_str",'')
        zpr_str=zpr_str if zpr_str else ''        

        price_str = request.POST.get('pr_str')

        pr_str_list = []
        if price_str:
            #price_list = json.loads(price_str.replace('\'', '"'))
            price_list = json.loads(price_str)
            for price_dict in price_list:
                price_tmp = price_dict['price']

                if price_tmp:
                    price_id_tmp = price_dict['price_id']
                    sale_tmp = price_dict['sale']
                    discount_tmp = price_dict['discount']
                    original_price_tmp = price_dict['original_price']
                    begin_time_tmp = price_dict['begin_time'] if price_dict['begin_time'] else datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                    end_time_tmp = price_dict['end_time'] if price_dict['end_time'] else obj.end_time.strftime('%Y-%m-%d %H:%M')
                    status_tmp = price_dict['status']
                    content_tmp = price_dict['content']

                    pr_str_list.append(price_tmp)
                    if price_id_tmp:
                        price_unit_tmp = NewEventPriceUnit.objects.get(id=price_id_tmp)
                    else:
                        price_unit_tmp = NewEventPriceUnit()
                        price_unit_tmp.event_id = obj.id

                    price_unit_tmp.Currency_id = pr_Currency
                    price_unit_tmp.price = price_tmp
                    price_unit_tmp.begin_time = begin_time_tmp
                    price_unit_tmp.end_time = end_time_tmp
                    price_unit_tmp.status = status_tmp
                    
                    if sale_tmp:
                        price_unit_tmp.sale = sale_tmp
                    if discount_tmp:
                        price_unit_tmp.discount = discount_tmp
                    if original_price_tmp:
                        price_unit_tmp.original_price = original_price_tmp
                    if content_tmp:
                        price_unit_tmp.content = content_tmp
                    
                    price_unit_tmp.save()
                    
        if obj.Price:
            
            obj.Price.Currency=NewEventPriceCurrency.objects.get(id=pr_Currency)  
            obj.Price.Type=NewEventPriceType.objects.get(id=pr_Type)  
            obj.Price.str ='/'.join(pr_str_list)
            obj.Price.sale=zpr_str  

            obj.Price.min=mi
 
            obj.Price.max=ma
            obj.Price.save()
        else:
 
            obj.Price=NewEventPrice.objects.create(
                 Currency=NewEventPriceCurrency.objects.get(id=pr_Currency) ,
                 Type=NewEventPriceType.objects.get(id=pr_Type) ,
                 str ='/'.join(pr_str_list),
                 sale=zpr_str, 
                 min=mi ,  
                 max=ma ,  
                )

        del_price_id = request.POST.get('del_price_id')
        if del_price_id:
            for dpi in del_price_id.split(','):
                try:
                    NewEventPriceUnit.objects.get(id=dpi).delete()
                except:
                    pass
           
# 信息来源保存
        # 如果主办方只有一个，则关联来源信息
        new_sponsor = None

        if len(sponsor_list) == 1:
            sp_name_tmp = sponsor_list[0]['sponsor_name']
            v = NewSponsor.objects.filter(name=sp_name_tmp)
            if v:
                new_sponsor = v[0]
        event_from_str = request.POST.get('message_info')
        if event_from_str:
            #ef_list = json.loads(event_from_str.replace('\'', '"'))
            ef_list = json.loads(event_from_str)
            for ef_dict in ef_list:
                ef_id_tmp = ef_dict['id']
                f_class_tmp = ef_dict['f_class']
                website_tmp = ef_dict['website']
                content_tmp = ef_dict['content']
                type_tmp = ef_dict['type']
                
                try:
                    if ef_id_tmp and ef_id_tmp > 0:
                        ef_obj_tmp = NewEventFrom.objects.get(id=ef_id_tmp)
                    else:
                        ef_obj_tmp = NewEventFrom()
                except:
                    ef_obj_tmp = NewEventFrom()
                    
                ef_obj_tmp.f_Class_id = f_class_tmp
                ef_obj_tmp.content = content_tmp
                ef_obj_tmp.type_id = type_tmp
                ef_obj_tmp.Website = website_tmp
                
                ef_obj_tmp.save()
                obj.from_info.add(ef_obj_tmp)
                
                if new_sponsor:
                    new_sponsor.event_from.add(ef_obj_tmp)
                
# 删除信息来源与该活动的关联
        del_ef_id = request.POST.get('del_info_id')
        if del_ef_id:
            for i in del_ef_id.split(','):
                if i:
                    try:
                        del_ef_obj = NewEventFrom.objects.get(id=i)
                        obj.from_info.remove(del_ef_obj)
                    except:
                        pass


        #_price_unit_list = NewEventPriceUnit.objects.filter(event_id=obj.id)
        #if not _price_unit_list:
        ##if NewEventPriceUnit.objects.filter(event_id=obj.id).count()==0:
        ##if not obj.Price_event_table.all().count():
        #    if obj.Price.Type_id == 6 :
        #        for pr in  pr_str.split('/'):
        #            pr1= re.sub(ur"[^\w]", "", pr)
        #            if pr1:
        #                try:
        #                    NewEventPriceUnit.objects.create(event=obj,
        #                                                     price=pr1,
        #                                                     begin_time=datetime.datetime.now(),
        #                                                     end_time=obj.end_time,
        #                                                     Currency=obj.Price.Currency,
        #                                                     )
        #                except Exception,e:
        #                    log.debug('%s' % e) 
        #            else:
        #                log.debug('%s' % pr)
        #    elif obj.Price.Type_id == 1 :
        #        sale=zpr_str.split('/')
        #        st=pr_str.split('/')
        #        for i in range(len(sale)):
        #            sa1=re.sub(ur"[^\w]", "",sale[i])
        #            pr1=re.sub(ur"[^\w]", "",st[i])
        #            if sa1 and pr1:
        #                #try:
        #                NewEventPriceUnit.objects.create(event=obj,
        #                                                 price=pr1,
        #                                                 sale=sa1,
        #                                                 begin_time=datetime.datetime.now(),
        #                                                 end_time=obj.end_time,
        #                                                 Currency=obj.Price.Currency,
        #                                                 )
        #                #except Exception,e:
        #                    #log.debug('%s' % e) 
        #            else:
        #                log.debug('%s %s' % (pr1,sa1))
        #    else:
        #        log.debug('%s %s %s' % (pr_str,zpr_str,obj.Price.Type_id)) 
        #        
        #else:
        #    for _pu in _price_unit_list:
        #        _pu.Currency = obj.Price.Currency
        #        _pu.end_time = obj.end_time
        #        _pu.save()

        #    log.debug('%s' % obj.Price.Type_id) 
        

        '''
        for ta in obj.tag.all():
            for t in ta.neweventcat_set.all():
                obj.cat.add(t)
        '''
        if not obj.seo:
            for ca in  obj.cat.all():
                try:
                    obj.seo=NewEventSeo.objects.get(name=ca.name)
                    obj.seo.save()
                    break
                except Exception,e:
                    print e,ca.id
                    try:
                        if ca.parent:
                            obj.seo=NewEventSeo.objects.get(name=ca.parent.name)
                            obj.seo.save()
                            break
                        
                    except Exception,e:
                        print e,ca.parent.id
                    
        '''       
        txt_list=request.POST.get("txt_list",False)
        if txt_list:
            txt_list=json.loads(txt_list)
            
            for t in txt_list:
                if t.has_key('txt'):
                    txts=t['txt']
                else:
                    txts=''
                if t.has_key('order'):
                    txt_orders=t['order']
                else:
                    txt_orders=''
                    
                if t.has_key('tabname'):
                    try:
                        na=NewEventParagraphTag.objects.get(name=t['tabname'])
                    except:
                        try:
                            na=NewEventParagraphTag.objects.create(
                                                                name= t['tabname'] 
                                                                   )
                        except:
                            na=NewEventParagraphTag.objects.get(id=2317)
                        
                if na:
                    pa=None
                    if t.has_key('id'):
                        if na:
                            try:
                                pa=NewEventParagraph.objects.get(id=t['id'])
                                pa.txt=txts
                                pa.txt_order=txt_orders
                                    
                                pa.save()
                    

                            except:
                                print 'not txt %s' % t[0]
                                
                        else:
                            print 'not%s' % t[0]
                    else:
                        NewEventParagraph.objects.create(
                                                         
                                                         )
        '''

        # 自动保存feelnum
        try:
            feelnum.objects.get(event=obj)
        except:
            feelnum.objects.create(event=obj, feel_id=1, feelnum=0)
                        
        #if obj.cat    
        search= obj.name
        if obj.fname:
            search+=obj.fname
        search+=','.join([ci.district_name for ci in obj.city.all()])
        search+=','.join([ca.name for ca in obj.cat.all()])
        
        search+=','.join([t.name for t in obj.tag.all()])  
        addr_s=[]
        try:
            for ad in obj.addr.all():
                obj.city.add(ad.city)
                addr_s.append("%s,%s" % (ad.title,ad.address))
        except Exception,e:
            log.debug('%s' % e) 
        if addr_s:
            search+=','.join(addr_s)
        obj.search=search
        try:    
            obj.save()
        except  Exception,e:
            log.debug('%s' % e) 
            

        try:
            if not NewEventToOldEvent(obj.id):
                #print 'new to old err'
                log.debug('new to old err') 

        except Exception,e:
            log.debug('new to old err') 
            log.debug('%s' % e) 

        #updata_cache(obj)
 
        
        
        #ToEventPrice(obj.id) 
         
         
    def queryset(self, request):
        qs = super(EventAdmin, self).queryset(request)
        qs.order_by("-rel_time")
        
        
        # If super-user, show all comments
        if request.user.is_superuser :
            
            return qs
        
        ids=request.GET.get("id",False)  
 
        if ids: 
            return qs
        bt=request.GET.get("bt",False)  
        try:
            if int(bt)==99:
                return qs
        except:
            pass
        return qs.filter(models.Q(edit=request.user)|models.Q(last_edit=request.user)) 
    
  
    def citys(self, obj):
        ch=()
        try:
            
            for ci in obj.city.all():
                ch+=(ci.district_name,)
        except:
            pass
            
        return u'%s' % ( "<br>".join(ch))
    citys.short_description = u'城市'
    citys.allow_tags = True

    def citys_addr(self, obj):
        ch=()
 
        try:            
            for ci in obj.cat.all():
                ch+=(ci.name,)
        except:
            pass

        try:
            
            for ci in obj.city.all():
                ch+=(ci.district_name,)
        except:
            pass
        
        str='<br>'
        for addrs in  obj.addr.all():
            ve = addrs.title if addrs else '' 
            add = addrs.address if addrs else ''
            str+=ve[:10] if ve else add[:10]
            str+='<br>'
 
            
        return u'%s%s' % ( "<br>".join(ch),str)
    citys_addr.short_description = u'城市/地址'
    citys_addr.allow_tags = True  
    citys_addr.admin_order_field = 'addr'  
    
    def cats(self, obj):
        ch=()
        try:            
            for ci in obj.cat.all():
                ch+=(ci.name,)
        except:
            pass
            
        return u'%s' % ( "<br>".join(ch))
    cats.short_description = u'分类'
    cats.allow_tags = True

    def froms(self,obj):
        ch=()
        try:            
            for ci in obj.from_info.all():
                info='<a href="%s" target="_blank">%s%s%s</a>' % (ci.Website,ci.name,ci.tel,ci.email)
                ch+=(info,)
        except:
            pass
            
        return u'%s' % ( "/".join(ch))
    froms.short_description = u'来源'
    froms.allow_tags = True

    def show_url(self,obj):
        str=''
        str+='<a href="/admin/new_event/neweventtable/%s/"  target="_blank" >编辑</a><br>' % (obj.id,)
        if obj.old_event:
            
            str+= '<a href="http://www.huodongjia.com/event-%s.html?new=1"  class="event_edit" target="_blank">%s</a>' % (obj.old_event_id,obj.old_event_id)
        else:
            str+= '<a href="http://www.huodongjia.com/event-%s.html?new=1"  class="event_edit" target="_blank">%s</a>' % (obj.id,obj.id)
         
        return str
    show_url.short_description = u'编辑/查看'   
    show_url.allow_tags = True 
    show_url.admin_order_field = 'id'
    
    def isshow_p(self,obj):
        str=''
        try:
            str+='%s' % obj.isshow.name
        except:
            str=''
            
        return str
    isshow_p.short_description = u'状态'
    isshow_p.allow_tags = True      
    
    def show_new(self,obj):
        str=''
        if obj.old_event_id:
            str+='<a href="http://life.huodongjia.com/api/eventinfoapi/?eventid=%s&new=1"  >刷新</a><br>' % (obj.old_event_id,)
        return str
    show_new.short_description = u'生活家刷新'
    show_new.allow_tags = True
    
    def img_is(self,obj):
        str=''
        if obj.img.all().count()>0:
            str+= u'<span style="color:green">有图</span>'
        else:
            str+= u'<span  >无图</span>'
            
        
        if obj.seo:
            if str:
                str+='<br>'
            str+= u'<span style="color:green">有seo信息</span>'
            
    
        try:
            str+='<br>%s' % obj.isshow.name
        except:
            pass
        '''
        try:
            str+='<br>%s' % obj.point.name
        except:
            pass    
        '''
        return str
         
                
    img_is.short_description = u'其他信息'   
    img_is.allow_tags = True     
    
    def addr_is(self,obj):
        str=''
        for addrs in  obj.addr.all():
            ve = addrs.title if addrs else '' 
            add = addrs.address if addrs else ''
            str+=ve[:10] if ve else add[:10]
            str+='<br>'
            return str
    
        else:
            return str
    addr_is.short_description = u'地址/场馆'   
    addr_is.allow_tags = True    
    
    def Price_Type_is(self,obj):
        
        if obj.Price:
            st=''
            if obj.Price.str:
                st+=u'%s' % obj.Price.str
            else:
                st+=u'%s' % (obj.Price.Type.name)
            return st
        else:
            return u'无价格'
    Price_Type_is.short_description = u'销售'   
    Price_Type_is.allow_tags = True 
    Price_Type_is.admin_order_field = 'Price__max'  
    
    def begintime(self,obj):
        return u'%s' % (obj.begin_time)
    
    begintime.short_description = u'开始时间'   
    #Price_Type_is.allow_tags = True 
    begintime.admin_order_field = 'begin_time'      
    
    def endtime(self,obj):
        return u'%s' % (obj.end_time)
    
    endtime.short_description = u'结束时间'   
    endtime.admin_order_field = 'end_time'     
    
    def cEdit(self,obj):
    
        str=''   
        str= u'%s' % (obj.old_event.event_editor if obj.old_event else '') 
        if not str:
            if obj.edit:
                str=u'%s%s' % (obj.edit.first_name,obj.edit.last_name)
                if not str:
                    str=u'%s' % (obj.edit)
            
            
            
            
        return str
    
    cEdit.short_description = u'创建编辑'   
    cEdit.admin_order_field = 'edit'
    
    def lastEdit(self,obj):
        if obj.isshow_id in [1,8]:
            edit=u'rel:'
        else:
            edit=u'edit:' 
        if obj.edit:
            str=u'%s%s' % (obj.edit.first_name,obj.edit.last_name)
            if not str:
                str=u'%s' % (obj.edit)            
        else:
            str= u'%s' % (obj.old_event.event_editor if obj.old_event else '')
        lstr=''
        if obj.last_edit:
            lstr=u'%s%s' % (obj.last_edit.first_name,obj.last_edit.last_name)
            if not lstr:
                lstr=u'%s' % (obj.last_edit) 
        str= '%s%s' % (edit,str)
        if lstr:
            str +=u'<br>last:%s' % lstr
            
        return str
    
    lastEdit.short_description = u'编辑'   
    lastEdit.admin_order_field = 'last_edit'  
    lastEdit.allow_tags = True 
    
    def reltime(self,obj):
        str=''
        if obj.release_time:
            str+='rel:%s<br>' % (obj.release_time)
        return u'%sup:%s' % (str,obj.rel_time)    
    reltime.short_description =u'更新时间'  
    reltime.admin_order_field = 'rel_time' 
    reltime.allow_tags = True      

    def rel_time_fmt(self, obj):
        return u'%s' %obj.rel_time
    rel_time_fmt.short_description = u'最后更新时间'
    rel_time_fmt.admin_order_field = 'rel_time' 

    def last_edit_fmt(self, obj):
        if obj.last_edit:
            lstr=u'%s%s' % (obj.last_edit.first_name,obj.last_edit.last_name)
            if not lstr:
                lstr=u'%s' % (obj.last_edit) 
            return lstr
        else:
            return None
    last_edit_fmt.short_description = u'最后编辑'   
    last_edit_fmt.admin_order_field = 'last_edit'  

    def addr_fmt(self, obj):
        return '<br>'.join([addr.address for addr in obj.addr.all() if addr.title])
    addr_fmt.short_description = u'地址'   
    addr_fmt.allow_tags = True    

    def venue_fmt(self, obj):
        return '<br>'.join([venue.title for venue in obj.addr.all() if venue.title ])
    venue_fmt.short_description = u'场馆'   
    venue_fmt.allow_tags = True    
    
    
    def createtime(self,obj):
        return u'%s' % (obj.create_time)    
    createtime.short_description =  u'创建时间'    
    createtime.admin_order_field = 'create_time'         
    
    def visitrecord(self,obj):
        try:
            vi=VisitRecord.objects.get(event=obj.old_event_id)
            return '%s' % vi.count
        except:
            return ''
    
    
    visitrecord.short_description = u'app访问次数'   
    #Price_Type_is.allow_tags = True 
    visitrecord.admin_order_field = 'old_event__event_visit_record__count'   
    
    #list_select_related = True
    
    
    #date_hierarchy = 'rel_time'
    #date_hierarchy = 'create_time'
    date_hierarchy = 'release_time'
    #list_display = ('id','show_url', 'name','citys_addr', 'Price_Type_is','begintime','endtime','lastEdit', 'reltime','img_is',  'order' ,'hot','point')
    # 2015.3
    
    #def pushMsg(self,obj):
    #    '''
    #    百度云消息推送
    #    '''
    #    
    #    id = obj.old_event.event_id
    #    
    #    return "<a href='http://life.huodongjia.com/BaiduPushSDK/sample/pushmsg.php?id=%s&type=0'>推送到IOS</a>|<a href='http://life.huodongjia.com/BaiduPushSDK/sample/pushmsg.php?id=%s&type=0'>推送到ANDROID</a>" %(id,id)
    #pushMsg.short_description = u'消息推送'
    #pushMsg.allow_tags = True
    
    list_display = ('name', 'show_url', 'cats', 'citys', 'addr_fmt', 'venue_fmt','Price_Type_is','begintime','endtime','last_edit_fmt', 'rel_time_fmt','img_is','order')
    #list_display = ('name',  'isshow', 'order' )
    
    raw_id_fields = ['relevant','from_info','paragraph', 'tag','Price','img' ,'seo','addr']
    #search_fields = ('name', 'ename','fname','city__district_name','cat__name','tag__name','addr__address','old_event__event_id','id')
    #list_filter = [CatList,'isshow',DateStateNew,cityList,User_show_new,User_show_new_f,'point',PriceType,EditStateFilter_new, begtime_can ,endtime_can,('begin_time',admin.DateFieldListFilter),bt_can,et_can,feedshow ]
    # 2015.3
    list_filter = [SmallCatList,SmallIsShowFilter,EditCity,User_show_new,PriceType,begtime_can ,endtime_can,bt_can,et_can]
    list_editable=(  'order', )
    search_fields = ('name', 'ename','fname', 'old_event__event_id','id','city__district_name','Price__str')
    #fields = ('name','fname','ename','addr','cat', 'tag' ,'Price','begin_time','end_time','img', 'content','paragraph', 'from_info','seo','isshow','city')
    #filter_horizontal =['cat']
    #form = EventForm
    #list_display_links = ('cats',)
    list_display_links = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'fname','ename')}),
        (None, {'fields': ('city','from_info','addr','cat', 'tag')}),
        (None, {'fields': ('Price','begin_time','end_time',)}),
        (None, {'fields': ('content','img','paragraph')}),
        (None, {'fields': ('seo','isshow','relevant','order',)}),
    )

class testEventAdmin(dhdAdmin):   
     
    #list_select_related = True
    date_hierarchy = 'rel_time'
    #list_display = ('name','cats' ,'citys', 'froms' ,'Price_Type_is','begintime','endtime','cEdit','lastEdit','createtime','reltime','img_is','seo_is','isshow','show_url','order' )
    list_display = ('name',  'isshow', 'order' )
    
    raw_id_fields = ['relevant','from_info','paragraph', 'tag','Price','img' ,'seo','city','relevant']
    #search_fields = ('name', 'ename','fname','city__district_name','cat__name','tag__name','addr__address','old_event__event_id','id')
    #list_filter = ['isshow','point','last_edit',cityList,CatList,DateStateNew,PriceType, begtime_can ,endtime_can,('begin_time',admin.DateFieldListFilter),bt_can,et_can ]
    #list_editable=( 'isshow','order' )
    search_fields = ('name', 'ename','fname', 'old_event__event_id','id')
    #fields = ('name','fname','ename','addr','cat', 'tag' ,'Price','begin_time','end_time','img', 'content','paragraph', 'from_info','seo','isshow','city')
    #filter_horizontal =['cat']
    form = EventForm
    #list_display_links = ('cats',)
    fieldsets = (
        (None, {'fields': ('name', 'fname','ename')}),
        (None, {'fields': ('city','from_info','addr','cat', 'tag')}),
        (None, {'fields': ('Price','begin_time','end_time',)}),
        (None, {'fields': ('img','paragraph')}),
        (None, {'fields': ('seo','isshow','relevant')}),
    )

class EditStateFilter(admin.SimpleListFilter):
    title = (u'编辑状态')
 
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
   
            (1, u'活动编辑'),
            (2, u'活动展示'),
        ) 
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
 
            if int(self.value()) == 1:
                return queryset.filter(event_isshow=0)
            elif int(self.value()) == 2:
                return queryset.filter(event_end_time__gt=int(time.time())).filter(event_isshow__in=(1,8,))        
            
class DateStateFilter(admin.SimpleListFilter):
    title = (u'时间状态')
 
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'date_state'
 
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (0, u'未开始'),
            (1, u'活动中'),
            (2, u'已经过期'),
        ) 
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            if int(self.value()) == 0:
                return queryset.filter(event_begin_time__gt=int(time.time()))
            if int(self.value()) == 1:
                return queryset.filter(event_end_time__gt=int(time.time()))
            if int(self.value()) == 2:
                return queryset.filter(event_end_time__lt=int(time.time()))   
            
            
class et_can_old(admin.SimpleListFilter):
    template = 'admin/filter_time.html'
    title = (u'开始时间')
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'et'     
    def lookups(self, request, model_admin):     
        #return self.value()    
        return (
            (0, self.value()),            
        )
    def queryset(self, request, queryset):
        return
        if self.value():
            date_time=self.value().split('-') 
            if len(date_time)>2:
                begin_dates = datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
                if request.POST.get("et",''):
                    return queryset.filter(begin_time__gte=begin_dates)
class bt_can_old(admin.SimpleListFilter):
    template = 'admin/filter_time.html'
    title = (u'开始时间')
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'bt'     
    def lookups(self, request, model_admin):     
        #return self.value()    
        return (
            (0, self.value()),            
        )
    def queryset(self, request, queryset):
        return
        if self.value():
            date_time=self.value().split('-') 
            if len(date_time)>2:
                begin_dates = datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
                #if request.POST.get("bt",''):
                return queryset.filter(begin_time__gte=begin_dates)
class begtime_can_old(admin.SimpleListFilter):
    template = 'admin/filter_time.html'
    title = (u'开始时间')
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'begin'     
    def lookups(self, request, model_admin):     
        #return self.value()    
        return (
            (0, self.value()),            
        )
    def queryset(self, request, queryset):
        if self.value():
            date_time=self.value().split('-') 
            if len(date_time)>2:
                begin_dates = datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
                bt=request.GET.get("bt",'')
                begin_dates=time.mktime(begin_dates.timetuple())
                if bt=='1':
                    return queryset.filter(event_begin_time__lte=begin_dates)                    
                elif bt=='0':
                    return queryset.filter(event_begin_time__gte=begin_dates)

class endtime_can_old(admin.SimpleListFilter):
    template = 'admin/filter_time.html'
    title = (u'结束时间')
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'end'     
    def lookups(self, request, model_admin):     
        #return self.value()    
        return (
            (0, self.value()),            
        ) 
    def queryset(self, request, queryset):
        if self.value():
            date_time=self.value().split('-') 
            if len(date_time)>2:
                begin_dates = datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
                #begin_dates = time.mktime(begin_dates.timetuple()) 
                begin_dates=time.mktime(begin_dates.timetuple())
                et=request.GET.get("et",'')
                if et=='1':
                    return queryset.filter(event_begin_time__lte=begin_dates)
                    
                elif et=='0':
                    return queryset.filter(event_begin_time__gte=begin_dates)
                #return queryset.filter(begin_time__lte=begin_dates)

                 
class OldEventAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        
        extra_context={}
        extra_context.update({'begin_s': request.GET.get("begin",''),
                              'end_s': request.GET.get("end",''), 
                                 'bt': request.GET.get("bt",'0'), 
                              'et': request.GET.get("et",'1'), 
                              })  
        
        return super(OldEventAdmin, self).changelist_view(request,  extra_context  )
    
    
    list_per_page=10
    list_max_show_all=10
        
    def get_save_url(self, obj):
        return u'<a href="/admin/new_event/oldevent/%s/" target="_blank" >%s</a>' % (obj.event_id,obj.event_id)
    get_save_url.short_description = u'查看'
    get_save_url.allow_tags = True
    #get_save_url.admin_order_field = 'event_begin_time'   
    def begintime(self,obj):    
            
        dates = time.localtime(obj.event_begin_time)
        
        dates = datetime.datetime(*dates[:3]).strftime('%Y-%m-%d ')
        return dates
    begintime.short_description = u'开始时间'
    begintime.allow_tags = True
    begintime.admin_order_field = 'event_begin_time'

    def guanlian_new_event(self,obj):
        if not obj.event_old_info:
            return '无'
        else:
            return u'<span style="color:green;font-weight:bold">%s</span>' % (u"有",)
            #return ''
    guanlian_new_event.short_description = u'新数据'
    guanlian_new_event.allow_tags = True

    def endtime(self,obj):
        
        dates = time.localtime(obj.event_end_time)
        dates = datetime.datetime(*dates[:3]).strftime('%Y-%m-%d ')
        return dates
    endtime.short_description = u'结束时间'
    endtime.allow_tags = True
    endtime.admin_order_field = 'event_end_time'   
    
    def crawl(self,obj):
        
        dates = time.localtime(obj.crawl_time)
        dates = datetime.datetime(*dates[:3]).strftime('%Y-%m-%d ')
        return dates
    crawl.short_description = u'采集时间'
    crawl.allow_tags = True
    crawl.admin_order_field = 'crawl_time'   
         
    def queryset(self, request):
        qs = super(OldEventAdmin, self).queryset(request)   
        
        begin=request.POST.get("begin",False)    
        end=request.POST.get("end",False)
        
        if begin:    
            date_time=begin.split('-') 
            begin_dates = datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
            begin_dates = time.mktime(begin_dates.timetuple())
    
            qs.filter(event_begin_time__lte=begin_dates)
        
        if end:
            date_time=end.split('-') 
            end_dates=datetime.datetime(int(date_time[0]),int(date_time[1]),int(date_time[2]))
            end_dates = time.mktime(end_dates.timetuple())
            qs.filter(event_begin_time__gte=end_dates)
        
        
        
        #request
            
        return qs#.exclude(event_isshow=5)
    
    def get_date_state(self, obj):
        if obj.event_begin_time > int(time.time())  :
            return u'<span style="color:green;font-weight:bold">%s</span>' % (u"未开始",)
 
        elif obj.event_end_time > int(time.time())  :
            return u'<span style="color:orange;font-weight:bold">%s</span>' % (u"未过期",)
        else:
            return u'<span style="color:red;font-weight:bold">%s</span>' % (u"已经过期",)
    get_date_state.short_description = u'时间状态'
    get_date_state.allow_tags = True
    get_date_state.admin_order_field = 'event_end_time'  
    
    def show_event_info(self,obj):
        str=''
        
        str+= u'<a href="/admin/new_event/neweventtable/add/?id=%s" target="_blank" >%s</a><br>' % (obj.event_id,obj.event_name if obj.event_name else 'None')
        str+= u'<a href="http://www.huodongjia.com/event-%s.html?new=1" class="event_edit" target="_blank" >%s</a>' % (obj.event_id,obj.event_id)
        return str
    show_event_info.short_description = u'提取编辑'
    show_event_info.allow_tags = True
    show_event_info.admin_order_field = 'event_id'

    def show_cat(self,obj):
        try:
            cat=NewEventCat_s.objects.get(cat_id=obj.event_cat)
            return cat.name
        except:
            return ''
    show_cat.short_description = u'分类'
    #show_cat.short_description = u'分类'    

    #date_hierarchy = 'event_begin_time'
    list_display = ('show_event_info','event_address','show_cat','event_price','begintime','endtime','crawl','get_date_state','event_isshow' , 'event_editor'  )
    #list_filter =[cityList_old,  DateStateFilter ,'crawl_site','event_isshow',CatList_old,'event_editor',begtime_can_old ,endtime_can_old,bt_can_old,et_can_old]
    list_filter =[CatList_old,'event_isshow',DateStateFilter,cityList_old,  Old_event_editor, EditStateFilter,begtime_can_old ,endtime_can_old,bt_can_old,et_can_old]
    
    search_fields=('event_name','venue_info','event_support_info','event_id')
    #date_hierarchy = 'crawl' 
    

class TagAdmin(dhdAdmin):
    search_fields = ['name']
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
    
    
    list_display = ('id','name','hot','cat_gl','event_gl')
    list_editable=('hot', )
    search_fields=('name',)
    #list_filter=('neweventcat_set',)
    '''
    list_display = ('name','cats' ,'citys', 'froms' ,'Price_Type_is','begintime','endtime','lastEdit','createtime','reltime','img_is','isshow','show_url','order' )
    raw_id_fields = ['relevant','from_info','paragraph', 'tag','Price','img' ,'seo','city']
    search_fields = ('name', 'ename','fname','city__district_name','cat__name','tag__name','addr__address','old_event__event_id','id')
    list_filter = ['isshow','point','last_edit', 'city',CatList,DateStateNew,PriceType]
    list_editable=( 'isshow','order' )
    '''
    
class CatMPTTModelAdmin(dhdAdmin):
    def tag_show(self,obj):
        str=[]
        for t in obj.tag.all():
            str.append(t.name)
        return ','.join(str)
    tag_show.short_description = u'标签'
    tag_show.allow_tags = True    
    # speficfy pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    mptt_indent_field = "name"
    list_filter = ['type']
    list_display = ('id','name','ename','order','tag_show')
    list_editable=( 'order', )
    search_fields = ('id','name','ename','tag__name')
    raw_id_fields=['seo','img','city']
    filter_horizontal = ('tag', )
    fields = ('name', 'ename', 'cat_id', 'tag' ,'parent','type','seo','order','begin_time','end_time','img', 'event_count','city','sale' )

class ParagraphVideoFilter(admin.SimpleListFilter):
    title = u'类别'
    parameter_name = 'if_video'
    
    def lookups(self, request, model_admin):
        return (
                ('video', u'视频'),
                ('paragraph', u'段落'),
                )

    def queryset(self, request, queryset):
        if self.value() == 'video':
            return queryset.filter(cat_name_id=17543)
        else:
            return queryset.exclude(cat_name_id=17543)

    
    
class ParagraphAdmin(admin.ModelAdmin):
    list_per_page=20
    list_max_show_all=40
    def show_tab(self,obj):
        if obj.cat_name:
            return '%s' % (obj.cat_name.name)
        else:
            return ''
    show_tab.short_description = u'tab'
    show_tab.allow_tags = True
    #show_tag.admin_order_field = 'id' 
    
    
    
    def show_txt(self,obj):
        return '<span style="height:100px;width:500px;display:block; white-space:pre-wrap;word-wrap : break-word ;overflow: hidden ;">%s</span>' % (obj.txt)
    show_txt.allow_tags = True
    show_txt.short_description = u'文字'
    
    def show_event(self,obj):
        str=''
        for n in  obj.neweventtable_set.all():
            str+='<a href="http://www.huodongjia.com/event-%s.html?new=1" target="_blank" >%s</a>' % (n.old_event_id,n.name)
        return str
    show_event.allow_tags = True
    show_event.short_description = u'活动' 

    def if_video(self,obj):
        return u'视频' if obj.cat_name_id == 17543 else u'段落'
    if_video.short_description = u'类别'
    
    list_display = ('id','show_tab', 'show_txt','show_event','begin_time','end_time','if_video',)
    list_filter = (ParagraphVideoFilter,)
    raw_id_fields=['img','cat_name']
    search_fields=('id',)

class img_cat(admin.SimpleListFilter):
    title = (u'上传')
        
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'img_p'
 
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (1, u'上传'),
            (2, u'外链'),

        )
 
    
 
 
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        
        catinfo.query.group_by = ['id']
        """
        if self.value(): 
            if self.value()=='1':
                queryset=queryset.exclude(imgs='')  
            elif self.value()=='2':
                queryset=queryset.filter(imgs='')         
            #queryset=queryset.filter(cat__in=self.find_ch(int(self.value()),NewCatUrl(2))).distinct() 
            #queryset.query.group_by = ['id']
            
            return queryset
        else:
            return queryset
        
        



class ImgAdmin(admin.ModelAdmin):
    def get_img(self, obj):
        #obj.urls="%s/%s" % obj.urls
        try:
            return u'<a href="%s%s" target="_blank" ><img src="%s%s" height=100 ></img></a>' % (self.server.name ,obj.urls, self.server.name ,obj.urls)
        except:
            return u'<a href="http://pic1.qkan.com/%s" target="_blank" ><img src="http://pic1.qkan.com/%s" height=100 ></img></a>' % (  obj.urls,  obj.urls)
        
 
    get_img.short_description = u'图片缩略'
    get_img.allow_tags = True
    get_img.admin_order_field = 'id'     
    
    list_display = ('id','name','get_img','begin_time','end_time')
    prepopulated_fields = {'imgs': ('urls',)}
    search_fields=('name','id')
    date_hierarchy = 'begin_time'
    list_filter = [img_cat]
    
    list_per_page=10
    list_max_show_all=10
    
    
class SubscribeAdmin(admin.ModelAdmin):

    def _str_to_int_list(self, string):
        ret = []
        try:
            for i in string.split(','):
                if i:
                    ret.append(int(i))
        except ValueError:
            pass
        return ret

    def tags_in_name(self, obj):
        tag_ids = self._str_to_int_list(obj.keywords)
        return ','.join([i.name for i in NewEventTag.objects.filter(id__in=tag_ids)])
    tags_in_name.short_description = u'订阅标签'

    def cats_in_name(self, obj):
        cat_ids = self._str_to_int_list(obj.cats)
        return ','.join([i.name for i in NewEventCat.objects.filter(id__in=cat_ids)])
    cats_in_name.short_description = u'订阅分类'

    list_per_page = 20
    list_display = ('id', 'email', 'cats', 'cats_in_name', 'keywords', 'tags_in_name')

class OldDistrict(admin.ModelAdmin):
    def parent_name(self, obj):
        if obj.upid:
            return SysCommonDistrict.objects.get(district_id=obj.upid).district_name
        else:
            return ''
    list_per_page = 40
    list_display = ('district_id', 'district_name', 'level', 'parent_name')
    search_fields = ('district_id', 'district_name')
    
