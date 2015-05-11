#coding:utf-8
import django.contrib.admin as admin
import datetime,time
import operator
import csv
from django.http import HttpResponse

from django.contrib.admin.views.main import ChangeList,lookup_needs_distinct
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured
from django.contrib.admin.options import IncorrectLookupParameters
from django.db import models
from django.core.cache import cache

class AdminPostEvent(admin.ModelAdmin):    
    
    list_editable=( 'event_priority' , )
    def post_mail(self,obj):
        
        st=''
        if obj.host_tel:
            st+='%s<br />' % obj.host_tel
        if obj.host_mail:
            content=u'感谢您对我们活动家的支持，我们将尽心竭力为你服务。您的信息我们将尽快整理发布到活动家网站上，\r\n请关注活动家网站 http://www.huodongjia.com'
            subject=u'来自活动家的问候'
            st+='%s<br><a href="/newevent/send_email/%s/%s/%s/" target="_blank" >可以发布活动发送邮件</a>' % (obj.host_mail,obj.host_mail,content,subject)
            content1=u'感谢您对我们活动家的支持，我们将尽心竭力为你服务。您提供的信息我们无法帮你发布，非常抱歉。\r\n关注活动家网站 http://www.huodongjia.com'
            subject1=u'来自活动家的问候'            
            st+='<br><a href="/newevent/send_email/%s/%s/%s/" target="_blank" >不能</a>' % (obj.host_mail,content1,subject1)
        return st
    post_mail.short_description=u'联系'
    post_mail.allow_tags = True
    def show_event_file_path(self,obj):
        #event_url
        st=''
        if obj.event_url:
            if not 'http://' in obj.event_url:
                obj.event_url='http://%s' % obj.event_url
            st+='<a href="%s"  target="_blank">%s</a><br />' % (obj.event_url,obj.event_url[0:20]+'...')
        if obj.event_file_path:
            file='%s' % obj.event_file_path
            st+='<a href="http://pic.huodongjia.com/%s"  target="_blank" >%s</a>' % (file,file[0:20]+'...')
        return st
    show_event_file_path.short_description=u'文件查看'
    show_event_file_path.allow_tags = True   
    def show_event(self,obj):
        if obj.event:
            str=u'<a href="http://www.huodongjia.com/event-%s.html?new=1" target="_blank" >web:%s</a></br>' % (obj.event.old_event_id,obj.event.old_event_id)
            str+=u'<a href="/admin/new_event/neweventtable/%s" target="_blank" >edit:%s</a>' % (obj.event.id,obj.event.name)
        else:
            str=''
        return str
    show_event.short_description = u'关联活动'
    show_event.allow_tags = True
    raw_id_fields = ['event']  
    list_display =['id','show_event','post_mail','show_event_file_path','event_priority', 'host_ip','post_time','last_time']
    
class ChangeList_self(ChangeList):    
    def get_query_set(self, request):
        # First, we collect all the declared list filters.
        (self.filter_specs, self.has_filters, remaining_lookup_params,
         use_distinct) = self.get_filters(request)

        # Then, we let every list filter modify the queryset to its liking.
        qs = self.root_query_set
        for filter_spec in self.filter_specs:
            new_qs = filter_spec.queryset(request, qs)
            if new_qs is not None:
                qs = new_qs
 
        try:
            # Finally, we apply the remaining lookup parameters from the query
            # string (i.e. those that haven't already been processed by the
            # filters).
            qs = qs.filter(**remaining_lookup_params)
        except (SuspiciousOperation, ImproperlyConfigured):
            # Allow certain types of errors to be re-raised as-is so that the
            # caller can treat them in a special way.
            raise
        except Exception as e:
            # Every other error is caught with a naked except, because we don't
            # have any other way of validating lookup parameters. They might be
            # invalid if the keyword arguments are incorrect, or if the values
            # are not in the correct type, so we might get FieldError,
            # ValueError, ValidationError, or ?.
            raise IncorrectLookupParameters(e)

        # Use select_related() if one of the list_display options is a field
        # with a relationship and the provided queryset doesn't already have
        # select_related defined.
        if not qs.query.select_related:
            if self.list_select_related:
                qs = qs.select_related()
            else:
                for field_name in self.list_display:
                    try:
                        field = self.lookup_opts.get_field(field_name)
                    except models.FieldDoesNotExist:
                        pass
                    else:
                        if isinstance(field.rel, models.ManyToOneRel):
                            qs = qs.select_related()
                            break

        # Set ordering.
        ordering = self.get_ordering(request, qs)
        qs = qs.order_by(*ordering)

        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name
        
        if self.search_fields and self.query:
            orm_lookups = [construct_search(str(search_field))
                           for search_field in self.search_fields]
            or_queries=[]
            ''' 
            if self.query.isdigit():
 
                
                qs = qs.filter(models.Q(id=self.query)|models.Q(old_event__event_id=self.query))
                    
 
            else:    
            '''                      
                #import jieba
            for bit in self.query.split():
                #seg_list = jieba.cut_for_search(bit)
                #for se in seg_list:
                for se in bit:
                    or_queries += [models.Q(**{orm_lookup: se})
                                  for orm_lookup in orm_lookups]
            qs = qs.filter(reduce(operator.or_, or_queries))
            if not use_distinct:
                for search_spec in orm_lookups:
                    if lookup_needs_distinct(self.lookup_opts, search_spec):
                        use_distinct = True
                        break

        if use_distinct:
            return qs.distinct()
        else:
            return qs



class orderMessageAdmin(admin.ModelAdmin): 
    def event_n(self,obj):
        return '<a href="/event-%s.html" target="_blank" >%s</a>' % (obj.event_id,obj.event_name)
    event_n.short_description = u'活动'
    event_n.allow_tags = True
    def begintime(self,obj):
        
        dates = time.localtime(obj.msg_addtime)
        dates = datetime.datetime(*dates[:6]).strftime('%Y-%m-%d %H:%M:%S')
        #dates = datetime.datetime(*dates[:3]).strftime('%Y-%m-%d ')
        return dates
    begintime.short_description = u'留言时间'
    begintime.allow_tags = True
    begintime.admin_order_field = 'msg_addtime' 
       
    list_display =['event_n','msg_name','msg_email','msg_tel','msg_content','begintime']
    

    
    
    
    
class FromAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'edit', None) is None:
            obj.edit = request.user
        obj.last_edit = request.user
        
        if getattr(obj, 'type', None) is None:
            obj.type_id=1
        obj.save()
    
    def event_info(self,obj):
        ch=()
        try:            
            for ev in obj.neweventtable_set.all():
                ch += ('<a href="http://admin5.huodongjia.com/event-%s.html" target="_blank">'+ev.name[:20]+'</a>',)
        except:
            pass
            
        return u'%s' % ( "<br>".join(ch))
    event_info.short_description = u'关联活动'
    event_info.allow_tags = True
    
    def site_url(self,obj):
        return u'<a href="%s" target="_blank">%s</a>' % (obj.Website,obj.Website)
    site_url.short_description = u'网站查看'
    site_url.allow_tags = True
    
    def email_url(self,obj):
        return u'<a href="%s" target="_blank">%s</a>' % (obj.email,obj.email)
    email_url.short_description = u'电子邮箱'
    email_url.allow_tags = True
    
    fields = ('f_Class','Website','email','tel','content','type')
    list_display =['id','f_Class','site_url','email_url','tel','content','edit','type','event_info']
    list_editable=(  'type',)
    list_filter = ['f_Class','type','edit',]
    search_fields = ['Website','content','neweventtable__id','neweventtable__old_event__event_id']

class PriceAdmin(admin.ModelAdmin): 
    pass

class PriceUnitAdmin(admin.ModelAdmin):
    '''
    def get_changelist(self, request, **kwargs):
 
        return ChangeList_self
    '''
    def show_event(self,obj):
        str=u'<a href="http://www.huodongjia.com/event-%s.html?new=1" target="_blank" >web:%s</a></br>' % (obj.event.old_event_id,obj.event.old_event_id)
        str+=u'<a href="/admin/new_event/neweventtable/%s" target="_blank" >edit:%s</a>' % (obj.event.id,obj.event.name)
        return str
    show_event.short_description = u'查看'
    show_event.allow_tags = True
    raw_id_fields = ['event','form_info'] 
    search_fields = ['event__name','event__id','event__old_event__event_id']
    list_filter=['status']
    list_editable=( 'price','status','stock','content')
    list_display=['id','show_event','price','Currency','begin_time','end_time','stock','status','content']



class orderAdmin(admin.ModelAdmin): 
    list_per_page=20
    list_max_show_all=30
    
    def order_url(self,obj):
        k=cache.get('order_%s' % obj.order_number)
        if k:
            return '<a  href="/newevent/show_order_url/%s/" target="_blank" >查看</a>' % (obj.order_number)
        else:
            return ''

    order_url.allow_tags = True
    order_url.short_description = '访客浏览'      
    def begintime(self,obj):
        
        dates = time.localtime(obj.order_addtime)
        dates = datetime.datetime(*dates[:6]).strftime('%Y-%m-%d %H:%M:%S')
        dates=u'下单时间:%s' % dates
        #dates = datetime.datetime(*dates[:3]).strftime('%Y-%m-%d ')
        if obj.order_paytime:
            paytime=time.localtime(obj.order_paytime)
            paytime=datetime.datetime(*paytime[:6]).strftime('%Y-%m-%d %H:%M:%S')
            dates+=u'<br>支付时间:%s' % paytime
        else:
            dates+='\r\n'
        return dates
    begintime.short_description = u'下单时间'
    begintime.allow_tags = True
    begintime.admin_order_field = 'order_addtime'  
    
    def order_user_info(self,obj):
        str=obj.order_user_name+'<br>'
        str+=u'tel:'+obj.order_tel+'<br>' if obj.order_tel else '\r\n'  
        str+=u'Fix:%s<br>' % obj.order_telphone  if obj.order_telphone else '\r\n'  
        str+=u'Email:%s<br>' % obj.order_email  if obj.order_email else '\r\n'  
            
        #str+=obj.city_title +' ' if obj.city_title else ''  
        str+=u'%s<br>' %  obj.order_address  if obj.order_address else '\r\n'  
        str+='%s' % obj.order_text.replace('\r\n','').replace(',',' ') if obj.order_text else '' 
        return str
    order_user_info.short_description=u'客户信息'
    order_user_info.allow_tags = True
    
    def order_from_info(self,obj):
        str=''
        for fr in obj.event.from_info.all():
            str+=fr.f_Class.name+'<br>'
            str+=fr.Website+'<br>' if fr.Website else '\r\n'
            str+=fr.email+'<br>' if fr.email else '\r\n'
            str+=fr.tel+'<br>' if fr.tel else '\r\n'
            str+=fr.content+'<br>' if fr.content else '\r\n'
            str+=fr.type.name+'  ' if fr.type else '\r\n'
            str+=u'<a href="/admin/new_event/neweventfrom/%s/" target="_blank">查看编辑</a>' % fr.id
            
        return str
    order_from_info.short_description=u'来源信息'
    order_from_info.allow_tags = True    
    
    def paytime(self,obj):
        if obj.order_paytime>0:
            dates = time.localtime(obj.order_paytime)
            dates = datetime.datetime(*dates[:6]).strftime('%Y-%m-%d %H:%M:%S')
        else:
            dates=''
        return dates
    paytime.short_description = u'支付时间'
    paytime.allow_tags = True
    paytime.admin_order_field = 'order_paytime' 
    def order_price_info(self,obj):
        str=''        
        str+=u'支付:%s<br>' % obj.order_payment
        str+=u'<已付款>%s<br>' % obj.order_pay_info if obj.order_pay_info else '\r\n'   
        str+=u'单号：%s<br>' % obj.order_number     
        str+=u'单价：%s × %s <br>' % (obj.order_price,obj.order_amount)
        #str+=u'数量：%s<br>' % obj.order_amount
        str+=u'总额：%s<br>' %  obj.order_totalpay
        if obj.event_to==0:
            str+=u'订单来自web<br>'
            
        elif obj.event_to==1:
            str+=u'订单来自app<br>'
            
        elif obj.event_to==2:
            str+=u'订单来自Mobile website<br>'
        elif obj.event_to==3:
            str+=u'订单来自weixin<br>'
        elif obj.event_to==4:
            str+=u'订单来自life app<br>'
        else:
            str+='\r\n'
        try:
            if obj.admin:
                str+='%s%s' % (obj.admin.first_name,obj.admin.last_name)
            else:
                str+=''
        except:
            pass

        
        
        
        
        return str
    order_price_info.short_description = u'订单详情'
    order_price_info.allow_tags = True    
    raw_id_fields=['event']
 
    def show_event(self,obj):
        str=u'%s<br>' % obj.city_title
        try:
            str+=u'<a href="/admin/new_event/neweventtable/%s/" target="_blank" >%s</a>' % (obj.event.id,obj.event_name)
        except:
            str+='%s' % obj.event_name
        return str;   
    show_event.short_description = u'活动'
    show_event.allow_tags = True
    date_hierarchy = 'addtime'
    list_editable=( 'order_status', 'order_pay_status','order_payment','admin_text', )    
    list_filter = ['order_status', 'order_pay_status',('addtime',admin.DateFieldListFilter),'order_payment','event_to']
    search_fields=('order_id','order_number','order_tel','order_telphone','order_email','order_address','order_user_name', 'event_name','event__id','event__old_event__event_id')        
    list_display =['order_id','show_event','begintime','order_user_info', 'order_price_info','admin_text','order_payment', 'order_status',  'order_pay_status','order_url']
    #list_display =['order_id']
    
    ''' 
    def changelist_view(self, request, extra_context=None):
        """
        The 'change list' admin view for this model.
        """
        
        from django.core.exceptions import PermissionDenied


        if not self.has_change_permission(request, None):
            raise PermissionDenied

        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = self.get_list_filter(request)

        # Check actions to see if any are available on this changelist
        actions = self.get_actions(request)
        if actions:
            # Add the action checkboxes if there are any actions available.
            list_display = ['action_checkbox'] +  list(list_display)

        ChangeList = self.get_changelist(request)
        try:
            cl = ChangeList(request, self.model, list_display,
                list_display_links, list_filter, self.date_hierarchy,
                self.search_fields, self.list_select_related,
                self.list_per_page, self.list_max_show_all, self.list_editable,
                self)
        except IncorrectLookupParameters:
            pass

        # If the request was POSTed, this might be a bulk action or a bulk
        # edit. Try to look up an action or confirmation first, but if this
        # isn't an action the POST will fall through to the bulk edit check,
        # below.
        self.re_list=cl.get_query_set(request)
        return super(orderAdmin, self).changelist_view(request,  extra_context  )
    '''
    def Download_csv(self, request, queryset):
        #data =queryset
        response = HttpResponse(mimetype="text/csv")
        filename=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d') 
        response['Content-Disposition'] = 'attachment; filename=%s.csv'  % filename
        writer = csv.writer(response)  
        #writer.writerow([u'活动',u'活动id',u'下单时间',u'用户名称',u'手机','详情',u'订单总额'])  
        num=[u'活动',u'活动id',u'下单时间',u'支付时间',u'联系人',u'手机',u'固话',u'邮箱',u'地址',u'留言',u'付款方式',u'付款状态',u'订单号',u'单价数量',u'总额',u'订单提交',u'最后编辑',u'管理备注',u'付款方式']
        for i in range(len(num)):
            if num[i]:
                num[i]=num[i].encode('utf8')  
            
        writer.writerow(num)  
        for item in queryset:  
            #'show_event','begintime','order_user_info','order_totalpay', 'order_price_info','admin_text','order_payment', 'order_status',  'order_pay_status'
            #writer.writerow([item.event_name,item.event.old_event,item.addtime,item.order_user_name,item.order_tel,self.order_user_info(item),item.order_totalpay])  
            items=[item.event_name,item.event_id,self.begintime(item).replace('\r\n',',').replace('<br>',','),self.order_user_info(item).replace('\r\n',',').replace('<br>',','),self.order_price_info(item).replace('\r\n',',').replace('<br>',','),item.admin_text.replace('\r\n','').replace(',',' ') if item.admin_text else '',item.order_payment]
            new_ite=[]
            for i in range(len(items)):
                if  type(items[i])==str:
                    items[i]=items[i].encode('utf8')
                #items[i]=items[i].replace('\r\n',',').replace('<br>',',')
                new_ite.extend(str(items[i]).replace('\r\n',',').replace('<br>',',').split(','))
            writer.writerow(new_ite)
        return response  

        #queryset.update(status='p')
    Download_csv.short_description = u"csv下载"   
    actions=[Download_csv] 
    '''
    def save_model(self, request, obj, form, change): 
        
        #if not obj.admin:
         
        if getattr(obj, 'admin', None) is None:
            
            obj.admin = request.user
            obj.save()
        
        
        #super(orderMessageAdmin, self).save_model(request, obj, form, change)
    '''
class AdminTheme(admin.ModelAdmin):
    
    list_editable=( 'event_set' , )    
    #list_filter = ['order_status', 'order_pay_status',('addtime',admin.DateFieldListFilter),'order_payment','event_to']
    #search_fields=('order_id','order_number','order_tel','order_telphone','order_email','order_address','order_user_name', 'event_name','event__id','event__old_event__event_id')        
    list_display =['theme_name','num','event_set','cities', 'begin_time','end_time','picture_web', 'show_pic',  'picture_server','theme_order']

    
