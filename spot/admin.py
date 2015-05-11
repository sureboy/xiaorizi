#coding:utf-8
from django.contrib import admin
from django import forms
from django.forms.models import ModelMultipleChoiceField
from models import SysSpotInfo, SysSpotTxt, SysSpotHcode,SysSpotImg,SysSpotEvent,SysCity,SysSpotTag,SysSpotfile 
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.contenttypes.models import ContentType
from django.template.response import  TemplateResponse
import time
from admin_self.froms import dhdAdmin,myTextareaWidget
from django.db import models 

 

class MyFilteredSelectMultiple(FilteredSelectMultiple):

    class Media:
        js = (settings.MEDIA_URL + "js/core.js",
              settings.MEDIA_URL + "js/SelectBox.js",
              settings.MEDIA_URL + "js/SelectFilter2.js",
              settings.MEDIA_URL + "js/ajax_spot_list.js",
            
              )


class MyModelMultipleChoiceField(ModelMultipleChoiceField):

    def clean(self, value):
        return [val for val in value]
    
    
class SpotTxtForm(forms.ModelForm):
    txt_img = MyModelMultipleChoiceField(queryset=SysSpotImg.objects.all(), required=False,
        widget=MyFilteredSelectMultiple(verbose_name=u"图片", is_stacked=False))
    txt_hcode = MyModelMultipleChoiceField(queryset=SysSpotHcode.objects.all(), required=False,
        widget=MyFilteredSelectMultiple(verbose_name=u"多媒体代码", is_stacked=False))  
    def __init__(self, *args, **kwargs):
        super(SpotTxtForm, self).__init__(*args, **kwargs)
        try:
            i = kwargs["instance"]
            Spot = SysSpotTxt.objects.get(pk=i.pk)
            qs = Spot.txt_img.all()
 
            cs = Spot.txt_hcode.all()
 
        except:
            qs = SysSpotImg.objects.none()
 
            cs = SysSpotHcode.objects.none()
 

            
        self.fields['txt_img'].queryset = qs
 
        self.fields['txt_hcode'].queryset = cs
    class Meta:
        model = SysSpotInfo    
        widgets = {
            'txt_img': MyFilteredSelectMultiple(verbose_name=u"图片", is_stacked=False),           
            'txt_hcode': MyFilteredSelectMultiple(verbose_name=u"html_hcode", is_stacked=False), 
        }
        
class SysSpotTxtAdmin(dhdAdmin):
    
    #fields = ('name', 'txt','tag','txt_img',)
    #filter_horizontal = ( 'txt_code', 'txt_img', )
    list_display = ('id','name','txt','tag','cat_name','begin_time','end_time','txt_order')
    date_hierarchy = 'end_time'
    ordering = ('-end_time',)
    list_editable=( 'txt_order',)
    raw_id_fields = ['txt_img' ]
    fields =['name','txt','tag','cat_name','txt_img','txt_order']
    #form = SpotTxtForm
    search_fields = ('id','name','txt','tag')
    date_hierarchy = 'begin_time'
    list_filter=('cat_name',)
    formfield_overrides={models.TextField:       {'widget':myTextareaWidget}}
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        opts = self.model._meta
        app_label = opts.app_label
        
        #a = obj.objects.get(first_name='Adrian', last_name='Holovaty')
        try: 
            a=obj.sysspotinfo_set.all()
        except:
            a=False;
        
        #SysSpotTxt.
        #a=obj.name;
        context.update({
            'add': add,
            'change': change,
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, obj),
            'has_delete_permission': self.has_delete_permission(request, obj),
            'has_file_field': True, # FIXME - this should check if form or formsets have a FileField,
            'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
            'form_url': form_url,
            'opts': opts,
            'content_type_id': ContentType.objects.get_for_model(self.model).id,
            'save_as': self.save_as,
            'save_on_top': self.save_on_top,
            'spot_url':a,
        })
        if add and self.add_form_template is not None:
            form_template = self.add_form_template
        else:
            form_template = self.change_form_template

        return TemplateResponse(request, form_template or [
            "admin/%s/%s/change_form.html" % (app_label, opts.object_name.lower()),
            "admin/%s/change_form.html" % app_label,
            "admin/change_form.html"
        ], context, current_app=self.admin_site.name)
    
    
    
    

class SpotForm(forms.ModelForm):
    #spot_img = MyModelMultipleChoiceField(queryset=SysSpotImg.objects.all(), required=False,
        #widget=MyFilteredSelectMultiple(verbose_name=u"图片", is_stacked=False))
    #spot_txt = MyModelMultipleChoiceField(queryset=SysSpotTxt.objects.all(), required=False,
        #widget=MyFilteredSelectMultiple(verbose_name=u"文字", is_stacked=False))
    #spot_hcode = MyModelMultipleChoiceField(queryset=SysSpotHcode.objects.all(), required=False,
        #widget=MyFilteredSelectMultiple(verbose_name=u"多媒体代码", is_stacked=False))   
    #spot_cat = MyModelMultipleChoiceField(queryset=SysCat.objects.all(), required=False,
        #widget=MyFilteredSelectMultiple(verbose_name=u"分类", is_stacked=False)) 
    #spot_city = MyModelMultipleChoiceField(queryset=SysCity.objects.all(), required=False,
        #widget=MyFilteredSelectMultiple(verbose_name=u"城市", is_stacked=False)) 
    spot_event = MyModelMultipleChoiceField(queryset=SysSpotEvent.objects.all(), required=False,
        widget=MyFilteredSelectMultiple(verbose_name=u"关联活动", is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(SpotForm, self).__init__(*args, **kwargs)
        #super(SysSpotEvent, self).__init__(*args, **kwargs)
        try:
            i = kwargs["instance"]
            Spot = SysSpotInfo.objects.get(pk=i.pk)
            #qs = Spot.spot_img.all()
            es = Spot.spot_event.all()
            #ts = Spot.spot_txt.all()
            #cs = Spot.spot_hcode.all()
            #city=Spot.spot_city.all()
            #cat= Spot.spot_cat.all()
        except:
            #qs = SysSpotImg.objects.order_by('-end_time').all()[:20]
           
            es = SysSpotEvent.objects.filter(event_end_time__gte=time.time(),event_isshow=1)[:20]
 
            #ts = SysSpotTxt.objects.order_by('-txt_order').all()[:20]
            #cs = SysSpotHcode.objects.order_by('-end_time').all()[:20]
            #city=SysCity.objects.none()
            
            #cat= SysCat.objects.exclude(cat_ename='')
            
        #self.fields['spot_img'].queryset = qs
        self.fields['spot_event'].queryset = es
        self.fields['spot_event'].label=u'关联活动'
        #self.fields['spot_txt'].queryset = ts
        #self.fields['spot_hcode'].queryset = cs
        #self.fields['spot_city'].queryset = city
        #self.fields['spot_cat'].queryset = cat
        
        

    class Meta:
        model = SysSpotInfo
    
        widgets = {
            #'spot_img': MyFilteredSelectMultiple(verbose_name=u"图片", is_stacked=False),
            'spot_event': MyFilteredSelectMultiple(verbose_name=u"关联活动", is_stacked=False),
            #'spot_txt': MyFilteredSelectMultiple(verbose_name=u"文字", is_stacked=False),
            #'spot_hcode': MyFilteredSelectMultiple(verbose_name=u"多媒体代码", is_stacked=False),
            #'spot_city': MyFilteredSelectMultiple(verbose_name=u"城市", is_stacked=False),
            #'spot_cat': MyFilteredSelectMultiple(verbose_name=u"分类", is_stacked=False),
        }
        



    
class SysSpotInfoAdmin(dhdAdmin):
    
    formfield_overrides={models.TextField:       {'widget':myTextareaWidget}}
    
    def show_url(self, obj):
        return u'<a href="http://www.huodongjia.com/spot/%s.html" target="_blank" >查看</a>' % (obj.id)
    

        
    show_url.short_description = u'页面查看'
    show_url.allow_tags = True
    show_url.admin_order_field = 'id'   
    
    #date_hierarchy = 'spot_end_time'
    #prepopulated_fields = {'spot_name': ('spot_name',)}
    list_display = ( 'id','spot_name','spot_addr', 'spot_begin_time', 'spot_end_time','spot_edit','show_url', 'spot_isshow')
    search_fields = ('spot_name', 'spot_addr','spot_desc')
    filter_horizontal = ('spot_cat', )
    list_editable=( 'spot_isshow',)
    date_hierarchy = 'spot_end_time'
    ordering = ('-spot_end_time',)
    raw_id_fields = ['spot_txt','spot_img', 'spot_city','spot_file']
    
    #raw_id_fields = ('spot_edit',)
    fields = ('spot_name', 'spot_addr','spot_desc','spot_isshow','spot_begin_time','spot_end_time','spot_txt', 'spot_img','spot_event', 'spot_cat','spot_file')
    form = SpotForm    
    
    def save_model(self, request, obj, form, change):
        
        if obj.spot_edit=='':
            obj.spot_edit=request.user.username
        obj.spot_last_edit = request.user.username
        obj.save()
        
        
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        opts = self.model._meta
        app_label = opts.app_label
        
        #a = obj.objects.get(first_name='Adrian', last_name='Holovaty')
        try: 
            a=obj.id  
        except:
            a=False  
            
 
        
        #SysSpotTxt.
        #a=obj.name;
        context.update({
            'add': add,
            'change': change,
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, obj),
            'has_delete_permission': self.has_delete_permission(request, obj),
            'has_file_field': True, # FIXME - this should check if form or formsets have a FileField,
            'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
            'form_url': form_url,
            'opts': opts,
            'content_type_id': ContentType.objects.get_for_model(self.model).id,
            'save_as': self.save_as,
            'save_on_top': self.save_on_top,
            'spot_id':a,
             
        })
        if add and self.add_form_template is not None:
            form_template = self.add_form_template
        else:
            form_template = self.change_form_template

        return TemplateResponse(request, form_template or [
            "admin/%s/%s/change_form.html" % (app_label, opts.object_name.lower()),
            "admin/%s/change_form.html" % app_label,
            "admin/change_form.html"
        ], context, current_app=self.admin_site.name)
    
    
    

    
class SysSpotImgAdmin(admin.ModelAdmin):
    def get_img(self, obj):
        return u'<a href="%s" target="_blank" ><img src="%s" height=100 ></img></a>' % (obj.urls,obj.urls)
        
 
    get_img.short_description = u'图片缩略'
    get_img.allow_tags = True
    get_img.admin_order_field = 'id'     
    
    list_display = ('name','get_img','begin_time','end_time')
    prepopulated_fields = {'imgs': ('urls',)}
    '''
    readonly_fields = ('thumb',) #因为不需要在后台修改该项，所以设置为只读
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
           return self.readonly_fields
        return self.readonly_fields
    
      
    '''
    
    
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        opts = self.model._meta
        app_label = opts.app_label
        
        #a = obj.objects.get(first_name='Adrian', last_name='Holovaty')
        try: 
            a=obj.sysspotinfo_set.all()
            #atxt=obj.systxtinfo_set.all() SysSpotTxt
        except:
            a=False
            
            
        try:
            atxt=obj.sysspottxt_set.all()
        except:
                
            atxt=False
        
        #SysSpotTxt.
        #a=obj.name;
        context.update({
            'add': add,
            'change': change,
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, obj),
            'has_delete_permission': self.has_delete_permission(request, obj),
            'has_file_field': True, # FIXME - this should check if form or formsets have a FileField,
            'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
            'form_url': form_url,
            'opts': opts,
            'content_type_id': ContentType.objects.get_for_model(self.model).id,
            'save_as': self.save_as,
            'save_on_top': self.save_on_top,
            'spot_url':a,
            'txt_url':atxt,
        })
        if add and self.add_form_template is not None:
            form_template = self.add_form_template
        else:
            form_template = self.change_form_template

        return TemplateResponse(request, form_template or [
            "admin/%s/%s/change_form.html" % (app_label, opts.object_name.lower()),
            "admin/%s/change_form.html" % app_label,
            "admin/change_form.html"
        ], context, current_app=self.admin_site.name)

class SpotEventAdmin(dhdAdmin):
    search_fields=('event_name','event_cat_tag')
    
class SpotfileAdmin(dhdAdmin):
    
        
    def spot_gl(self,obj):
        str=''
        for cat in obj.sysspotinfo_set.all():
            str+='<a href="/admin/spot/sysspotinfo/%s"  target="_blank"  >%s</a><br>' % (cat.id,cat.spot_name)
        return str
    spot_gl.short_description = u'关联'
    spot_gl.allow_tags = True
    
    search_fields=('name',)
    list_display = ('name','urls','begin_time','end_time','spot_gl')
     
admin.site.register(SysSpotInfo,SysSpotInfoAdmin)
admin.site.register(SysSpotTxt,SysSpotTxtAdmin)
admin.site.register(SysSpotHcode,)
admin.site.register(SysSpotImg,SysSpotImgAdmin)
admin.site.register(SysSpotTag,)
admin.site.register(SysSpotfile,SpotfileAdmin)
admin.site.register(SysSpotEvent,SpotEventAdmin)
