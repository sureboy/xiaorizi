#coding:utf-8
from itertools import chain
import operator,re
from django.contrib.admin.widgets import ForeignKeyRawIdWidget,ManyToManyRawIdWidget,AdminTextareaWidget
from django.utils.text import Truncator
from django.utils.html import escape
import django.contrib.admin as admin
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.admin.templatetags.admin_static import static
from django.utils.safestring import mark_safe
from django.conf import settings
from mptt.admin import MPTTModelAdmin
from django.utils.encoding import force_text
from django.contrib.admin.views.main import ChangeList,lookup_needs_distinct
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured
from django.contrib.admin.options import IncorrectLookupParameters
from django.db import models
from django.contrib.admin import AdminSite
from django.utils.text import capfirst
from django.utils import six
from LifeApi.models import NewEventPriceCurrency,NewEventPriceType,NewEventCat,NewDistrict
from django.contrib.admin import widgets
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.models import ModelMultipleChoiceField 
from django.forms import SelectMultiple
from django.utils.encoding import   force_unicode
from django.utils.html import   conditional_escape
from django.utils.translation import ugettext_lazy as _
 

 

def fill_topic_tree(deep = 0, parent_id = 0, choices = [], only_py=False):
    if parent_id == 0:
        ts = NewEventCat.objects.filter(parent = None)
        choices[0] += (('', '--'),)
        for t in ts:
            tmp = [()]
            if (only_py and t.ename) or (not only_py):
                fill_topic_tree(4, t.id, tmp, only_py) 
                choices[0] += ((t.id, '-' * deep + t.name,),)
                for tt in tmp[0]:
                    choices[0] += (tt,)
    else:
        ts = NewEventCat.objects.filter(parent__id = parent_id)
        for t in ts:
            if (only_py and t.ename) or (not only_py):
                choices[0] += ((t.id,'-' * deep + t.name, ),)
                fill_topic_tree(deep + 2, t.id, choices, only_py) 

def fill_topic_tree_city(deep = 0, parent_id = 0, choices = []):
    if parent_id == 0:
        ts = NewDistrict.objects.filter(parent = None)
        choices[0] += (('', '---------'),)
        for t in ts:
            tmp = [()]
            fill_topic_tree_city(4, t.id, tmp)
            choices[0] += ((t.id, '-' * deep + t.district_name,),)
            for tt in tmp[0]:
                choices[0] += (tt,)
    else:
        ts = NewDistrict.objects.filter(parent__id = parent_id)
        for t in ts:
            choices[0] += ((t.id,'-' * deep + t.district_name, ),)
            fill_topic_tree_city(deep + 4, t.id, choices)             
 

class TreeSelect(SelectMultiple):
    def __init__(self, attrs=None):
        super(SelectMultiple, self).__init__(attrs)
        
    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        if option_value in selected_choices:
            selected_html = u' selected="selected"'
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return u'<option value="%s"%s>%s</option>' % (
            escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label)).replace(' ', ' '))
            
    def render_options(self, choices, selected_choices):
        ch = [()]
        fill_topic_tree(choices = ch)
        self.choices = ch[0]
        selected_choices = set(force_unicode(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)).replace(' ', ' '))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append(u'</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output) 

class MyFilteredSelectMultiple(FilteredSelectMultiple):

    class Media:
        js = (
    
              settings.MEDIA_URL + "js/core.js",
              settings.MEDIA_URL + "js/SelectBox.js",
              settings.MEDIA_URL + "js/SelectFilter2.js",
              settings.MEDIA_URL + "js/ajax_msg_s.js",  
      
              )
     
    def render(self, name, value, attrs=None, choices=()):
       
        output = [super(MyFilteredSelectMultiple, self).render(name, value, attrs, choices)]
        output.append('<span id="p_%s" class="c_%s"  > ' % (name,name  ) )
         
        output.append('</span>')
 
        # TODO: "add_id_" is hard-coded here. This should instead use the
        # correct API to determine the ID dynamically.
        '''
        if name=='cat':
            output.append(u'<a href="/admin/new_event/neweventcat/add/" \
            class="add-another" id="add_id_cat" \
            onclick="return showAddAnotherPopup(this);">\
            <img src="/static/admin/img/icon_addlink.gif" alt="添加另一个" height="10" width="10">\
            </a>')
        '''
        if name=='addr':
            output.append(u'<a href="/admin/new_event/newvenue/add/" \
            class="add-another" id="add_id_%s" \
            onclick="return showAddAnotherPopup(this);">\
            <img src="/static/admin/img/icon_addlink.gif" alt="添加另一个" height="10" width="10">\
            </a>'%(name,))        
        
        return mark_safe(''.join(output))


class x_AdminSite(AdminSite):

    def get_app_list(self, request):
        
        app_dict = {}
        user = request.user
        for model, model_admin in self._registry.items():
            app_label = model._meta.app_label
            has_module_perms = user.has_module_perms(app_label)
    
            if has_module_perms:
                perms = model_admin.get_model_perms(request)
    
                # Check whether user has any perm for this module.
                # If so, add the module to the model_list.
                if True in perms.values():
                    info = (app_label, model._meta.module_name)
                    model_dict = {
                        'name': capfirst(model._meta.verbose_name_plural),
                        'object_name': model._meta.object_name,
                        'perms': perms,
                    }
                    if perms.get('change', False):
                        try:
                            model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                        except NoReverseMatch:
                            pass
                    if perms.get('add', False):
                        try:
                            model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                        except NoReverseMatch:
                            pass
                    if app_label in app_dict:
                        app_dict[app_label]['models'].append(model_dict)
                    else:
                        app_dict[app_label] = {
                            'name': app_label.title(),
                            'app_label': app_label,
                            'app_url': reverse('admin:app_list', kwargs={'app_label': app_label}, current_app=self.name),
                            'has_module_perms': has_module_perms,
                            'models': [model_dict],
                        }
    
        # Sort the apps alphabetically.
        app_list = list(six.itervalues(app_dict))
        app_list.sort(key=lambda x: x['name'])
    
        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
    
        
        return app_list
 

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




HORIZONTAL, VERTICAL = 1, 2
get_ul_class = lambda x: 'radiolist%s' % ((x == HORIZONTAL) and ' inline' or '')
class AdminEnhancedFKRawIdWidget(ForeignKeyRawIdWidget):
    '''
    def __init__(self, rel, admin_site, attrs=None, using=None):
        self.rel = rel
        self.admin_site = admin_site
        self.db = using
        super(ForeignKeyRawIdWidget, self).__init__(attrs)

    '''
    class Media:
        js = (
              settings.MEDIA_URL + "js/ajax_msg.js", 
            
              )
         
    def render(self, name, value, attrs=None):
        rel_to = self.rel.to
        if attrs is None:
            attrs = {}
        extra = []
        
        if rel_to._meta.db_table in ('sys_new_event_price' ) :
            #
            extra.append(self.label_for_Price( value  ))
            #output = extra
            return mark_safe(''.join(extra))
        

          
        
        if rel_to in self.admin_site._registry:
            # The related object is registered with the same AdminSite
            related_url = reverse('admin:%s_%s_changelist' %
                                    (rel_to._meta.app_label,
                                    rel_to._meta.module_name),
                                    current_app=self.admin_site.name)

            params = self.url_parameters()
            if params:
                url = '?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.items()])
            else:
                url = ''
            if "class" not in attrs:
                attrs['class'] = 'vForeignKeyRawIdAdminField' # The JavaScript code looks for this hook.
            # TODO: "lookup_id_" is hard-coded here. This should instead use
            # the correct API to determine the ID dynamically.
             
            extra.append('<a href="%s%s" class="related-lookup" id="lookup_id_%s" onclick="return showRelatedObjectLookupPopup(this);"> '
                            % (related_url, url, name))
            extra.append(' <img src="%s" width="16" height="16" alt="%s" /></a> '
                            % ( static('admin/img/selector-search.gif'), ('Lookup') ))
            
            

        output = [super(ForeignKeyRawIdWidget, self).render(name, value, attrs)] + extra
        

        
        
        
        if rel_to._meta.db_table in ('sys_ac_user_message'  ,) :
            output.append(self.label_for_black())
        #elif rel_to._meta.db_table in ('sys_new_event_Price'  ,) :
            #output.append(self.label_for_Price())
        else:
            output.append(self.label_for_value(value))
            #output.append('<div id="%s" >%s </div>' % (rel_to._meta.db_table , value,))
        return mark_safe(''.join(output))

    def label_for_Price(self,value  ):
        key = self.rel.get_related_field().name
        select_c=u'<div id="d_id_Currency"><label for="l_id_Currency">币种：</label><select name="pr_Currency" id="s_id_Currency">'
         
        tpye=u'<div id="d_id_Type"><label for="l_id_Type">销售模式：</label><select name="pr_Type" id="s_id_Type">'
        #tpye+=u'<option value="">收费</option>'
        
        pr_div='<div id="d_id_pr">'
        pr=u'<p id="id_pr"><label for="l_id_pr">价格（￥/￥/￥）</label><input id="pr_str" class="vTextField" name="pr_str" maxlength="100" type="text" value="'
        
        zpr=u'<p id="id_zpr"><label for="l_id_zpr">折扣（￥/￥/￥）</label><input id="zpr_str" class="vTextField" name="zpr_str" maxlength="100" type="text" value="'
        ppr=u'<p id="id_ppr" ><label for="l_id_ppr">折率（0.0/0/0）</label><input id="ppr_str" class="vTextField" name="ppr_str" maxlength="100" type="text" value="'
        max_pr=u'<p id="id_max_pr"><label for="l_id_max_pr">最大价格（众筹总价）</label><input id="max_pr" class="vTextField" name="max_pr" maxlength="100" type="text" value="'
        min_pr=u'<p id="id_min_pr"><label for="l_id_min_pr">最小价格（筹集价格）</label><input id="min_pr" class="vTextField" name="min_pr" maxlength="100" type="text" value="'
     

        Currency=NewEventPriceCurrency.objects.all()
        tpye_s=NewEventPriceType.objects.all()
        curr_id=1
        tpye_s_id=5
        if value :
            #key = self.rel.get_related_field().name NewEventPrice NewEventPriceCurrency NewEventPriceType
            try:
                obj = self.rel.to._default_manager.using(self.db).get(**{key: value})          
                curr_id=obj.Currency.id
                tpye_s_id=obj.Type.id
                if tpye_s_id!=3:
                    if obj.str==u'免费':
                        tpye_s_id=4
                    elif obj.str==u'收费':
                        tpye_s_id=5
                
                    
                try:
                    pr+=obj.str 
                except:
                    pass
                
                try:
                    zpr+=obj.sale 
                except:
                    pass
                try:
                    min_pr+='%s' % obj.min 
                except:
                    pass   
                try: 
                    max_pr+='%s' % obj.max 
                except:
                    pass
                
                try: 
                    ppr+='%s' % obj.points 
                except:
                    pass
            except:
                    pass

 

            
        zpr+='"></p>'    
        pr+='"></p>'
        ppr+='"></p>'
        min_pr+='"></p>' 
        max_pr+='"></p>'
        
        pr_div+=pr+zpr+ppr+max_pr+min_pr
        pr_div+='</div>'
        #return  select_c+'</select>'    
        
        for cu1 in tpye_s:
            se1=''
            if cu1.id==tpye_s_id:
                se1='selected="selected"'                   
     
            tpye+=u'<option value="%s" %s >%s</option>' % (cu1.id,se1,cu1.name) 
        
        for cu in Currency:
            se=''
            if cu.id==curr_id:
                se='selected="selected"'                   
            select_c+=u'<option value="%s" %s >%s</option>' % (cu.id,se,cu.name)    
        
        #return  select_c+'</select>'
        select_c+=u'</select><a href="/admin/new_event/neweventpricecurrency/add/" class="add-another" id="add_id_Currency" onclick="return showAddAnotherPopup(this);"><img src="/static/admin/img/icon_addlink.gif" alt="" height="10" width="10"></a></div>'
        tpye+=u'</select><a href="/admin/new_event/neweventpricetype/add/" class="add-another" id="add_id_Currency" onclick="return showAddAnotherPopup(this);"><img src="/static/admin/img/icon_addlink.gif" alt="" height="10" width="10"></a></div>'
        return  select_c+tpye+pr_div
            
            
         
    def label_for_black(self  ):
        #key = self.rel.get_related_field().name
        try:
            
            html='<br><textarea name="content" rows="10" cols="30"> </textarea>' #% (self.rel.to._meta.db_table,key) 
            return html
        except :
            return ''
   
    
            
    def label_for_value(self, value):
        
        key = self.rel.get_related_field().name
        if value:
            
            try:
                obj = self.rel.to._default_manager.using(self.db).get(**{key: value})
                if key=='event_id':                    
                    return '&nbsp;<a target="_blank" href=\'http://www.huodongjia.com/event-%s.html\'>%s</a>' % (value,escape(Truncator(obj).words(14, truncate='...')))                
                elif self.rel.to._meta.db_table=='sys_spot_txt':
                     
                    #html='<br>'
                    html='<div id="%s" style="" ><textarea rows="10" cols="30">%s</textarea></div>' %(self.rel.to._meta.db_table,obj.txt)
                    return html
                elif self.rel.to._meta.db_table=='sys_new_event_img':
                    html='<div id="%s" style="" ><a target="_blank" href="%s" ><img width="200" src="%s"></img></a></div>' %(self.rel.to._meta.db_table,obj.urls,obj.urls)
                    return html
                    
                else:                 
                    return '&nbsp;<div id="%s" style="" >%s</div>' % (self.rel.to._meta.db_table, escape(Truncator(obj)))
            except (ValueError, self.rel.to.DoesNotExist):
                return '0'
        else:
            return '&nbsp;<div id="%s" style="" ></div>' % (self.rel.to._meta.db_table,)

 
    

class AdminManyToManyRawIdWidget(ManyToManyRawIdWidget):
    """
    A Widget for displaying ManyToMany ids in the "raw_id" interface rather than
    in a <select multiple> box.
    """
    
    
    
    
    
    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
         
        if self.rel.to in self.admin_site._registry:
            # The related object is registered with the same AdminSite
            attrs['class'] = 'vManyToManyRawIdAdminField'
        if value:
            value = ','.join([force_text(v) for v in value])
        else:
            value = ''
        return self.render_s(name, value, attrs)
    
    
    
    def label_for_from(self,value  ):
        
        
        key = self.rel.get_related_field().name
        #self.rel.to._meta.db_table district_name
        # [^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$ 
        # ^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$
        
        html='<div id="%s" class="ManyToManyShow" style="" >'% (self.rel.to._meta.module_name )
        select='<select multiple="multiple"  id="select_%s" style="float: left" >'% (self.rel.to._meta.module_name )
       
        try:
            value=value.split(',')#.join(value) 
            for val in value:
                obj = self.rel.to._default_manager.using(self.db).get(**{key: val})
                
                select+='<option value="%s">%s</option>' %(val,obj)
                #return u'<div id="%s" class="ManyToManyShow" >%s </div>' % (self.rel.to._meta.app_label ,obj.district_name,)
           
         
        
        except:
            pass
        
        select+='</select><div id="con_%s" style="float: left;"></div>' % (self.rel.to._meta.module_name )
        select+='<div class="info_input">'
        sel_name='<textarea rows="3" cols="20"></textarea>'
        #name=u'<p><label for="l_id_pr">来源名称</label><input id="pr_str" class="vTextField" name="pr_str" maxlength="100" type="text"></p>'
        #zpr=u'<p><label for="l_id_zpr">来源网址</label><input id="zpr_str" class="vTextField" name="zpr_str" maxlength="100" type="text"></p>'
        #max_pr=u'<p><label for="l_id_max_pr">联系电话</label><input id="max_pr" class="vTextField" name="max_pr" maxlength="100" type="text"></p>'
        #min_pr=u'<p><label for="l_id_min_pr">电子邮箱</label><input id="min_pr" class="vTextField" name="min_pr" maxlength="100" type="text"></p>'
     
        
         
        return html+select+sel_name+'</div></div>'
    '''
    def label_for_tag(self,value  ):
        html='<div id=tag_list>'
        html+='<input name="tags" id="tags" value="foo,bar,baz" />'
        html+='</div>'
        return html
    '''
    def render_s(self, name, value, attrs=None):
        rel_to = self.rel.to
        if attrs is None:
            attrs = {}
        extra = []
        '''
        if rel_to._meta.db_table in ('sys_new_event_tag' ) :
            #
            extra.append(self.label_for_tag( value  ))
            output = extra
            return mark_safe(''.join(output))
        '''
        if rel_to in self.admin_site._registry:
            # The related object is registered with the same AdminSite
            related_url = reverse('admin:%s_%s_changelist' %
                                    (rel_to._meta.app_label,
                                    rel_to._meta.module_name),
                                    current_app=self.admin_site.name)

            params = self.url_parameters()
            if params:
                url = '?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.items()])
            else:
                url = ''
            if "class" not in attrs:
                attrs['class'] = 'vForeignKeyRawIdAdminField' # The JavaScript code looks for this hook.
            # TODO: "lookup_id_" is hard-coded here. This should instead use
            # the correct API to determine the ID dynamically.
            extra.append('<a href="%s%s" class="related-lookup" id="lookup_id_%s" onclick="return showRelatedObjectLookupPopup(this);"> '
                            % (related_url, url, name))
            extra.append('<img src="%s" width="16" height="16" alt="%s" /></a>'
                            % (static('admin/img/selector-search.gif'), ('Lookup')))
        output = [super(ForeignKeyRawIdWidget, self).render(name, value, attrs)] + extra
        
        '''
        if rel_to._meta.db_table in ('sys_new_event_from' ) :
            #
            output.append(self.label_for_from( value  ))
            
            return mark_safe(''.join(output))
        
        if rel_to._meta.db_table in ('sys_new_event_tag' ) :
            #
            output.append(self.label_for_tag( value  ))
          
            return mark_safe(''.join(output))
        '''
        
        if value:
            output.append(self.label_for_value(value,related_url,name))
        else:
            output.append(self.label_for_value(value,related_url,name))
        return mark_safe(''.join(output))
    
    
    
    class Media:
        js = (
              settings.MEDIA_URL + "js/ajax_msg.js",            
              )
        
        

    def label_for_value(self, value,related_url,name):
        
        key = self.rel.get_related_field().name
        #self.rel.to._meta.db_table district_name
        if related_url:
            add=u'<a href="%sadd/" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"><img src="/static/admin/img/icon_addlink.gif" alt="添加另一个" height="10" width="10"></a>' % (related_url,name, )
        html='<div id="%s" class="ManyToManyShow" style="" >' % (self.rel.to._meta.module_name )
        select='<select multiple="multiple"   id="select_%s" style="float: left;max-width:200px;" >'% (self.rel.to._meta.module_name )
        
        try:
            value=value.split(',')#.join(value) 
            for val in value:
                obj = self.rel.to._default_manager.using(self.db).get(**{key: val})
                
                select+='<option value="%s">%s</option>' %(val,obj)
                #return u'<div id="%s" class="ManyToManyShow" >%s </div>' % (self.rel.to._meta.app_label ,obj.district_name,)
           
         
        
        except:
            pass
        
        select+='</select><div id="con_%s" style="float: left;"></div>' % (self.rel.to._meta.module_name )         
        return add+html+select+'</div>'

 
class myTextareaWidget(AdminTextareaWidget):
    class Media:
        js = (
              settings.MEDIA_URL + 'ckeditor/ckeditor.js',         
              )
        
 
    
    def __init__(self, attrs=None):
        final_attrs = {'class': 'ckeditor'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(myTextareaWidget, self).__init__(attrs=final_attrs)
        
 

        
class dhdAdmin(admin.ModelAdmin):

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'cat':
            return db_field.formfield(widget = TreeSelect(attrs = {'width':120}))
         
    
        return super(dhdAdmin, self).formfield_for_dbfield(db_field, **kwargs) 
        
    
    def changelist_view(self, request, extra_context=None):
        return super(dhdAdmin, self).changelist_view(request, extra_context )


    '''    
    def get_changelist(self, request, **kwargs):
 
        return ChangeList_self
    '''


     
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ForeignKey.
        """
        db = kwargs.get('using')
        if db_field.name in self.raw_id_fields:
            kwargs['widget'] = AdminEnhancedFKRawIdWidget(db_field.rel,
                                    self.admin_site, using=db)
        elif db_field.name in self.radio_fields:
            kwargs['widget'] = AdminEnhancedFKRawIdWidget(attrs={
                'class': get_ul_class(self.radio_fields[db_field.name]),
            })
            kwargs['empty_label'] = db_field.blank and _('None') or None

        return db_field.formfield(**kwargs)
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ManyToManyField.
        """
        # If it uses an intermediary model that isn't auto created, don't show
        # a field in admin.
        if not db_field.rel.through._meta.auto_created:
            return None
        db = kwargs.get('using')

        if db_field.name in self.raw_id_fields:
            kwargs['widget'] = AdminManyToManyRawIdWidget(db_field.rel,
                                    self.admin_site, using=db)
            kwargs['help_text'] = ''
         
        elif db_field.name in (list(self.filter_vertical) + list(self.filter_horizontal)):
            kwargs['widget'] = MyFilteredSelectMultiple(db_field.verbose_name, (db_field.name in self.filter_vertical))
         
        return db_field.formfield(**kwargs)
    

class MpttDhdAdmin(MPTTModelAdmin):
    
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        
        """
        Get a form Field for a ForeignKey.
        """
        
        db = kwargs.get('using')
        if db_field.name in self.raw_id_fields:
            kwargs['widget'] = AdminEnhancedFKRawIdWidget(db_field.rel,
                                    self.admin_site, using=db)
        elif db_field.name in self.radio_fields:
            kwargs['widget'] = AdminEnhancedFKRawIdWidget(attrs={
                'class': get_ul_class(self.radio_fields[db_field.name]),
            })
            kwargs['empty_label'] = db_field.blank and _('None') or None

        return db_field.formfield(**kwargs)    
    
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ManyToManyField.
        """
        # If it uses an intermediary model that isn't auto created, don't show
        # a field in admin.
        if not db_field.rel.through._meta.auto_created:
            return None
        db = kwargs.get('using')

        if db_field.name in self.raw_id_fields:
            kwargs['widget'] = AdminManyToManyRawIdWidget(db_field.rel,
                                    self.admin_site, using=db)
            kwargs['help_text'] = ''
         
        elif db_field.name in (list(self.filter_vertical) + list(self.filter_horizontal)):
            kwargs['widget'] = MyFilteredSelectMultiple(db_field.verbose_name, (db_field.name in self.filter_vertical))
         
        return db_field.formfield(**kwargs)
 
    
 
        
class MyModelMultipleChoiceField(ModelMultipleChoiceField):
    def clean(self, value):
        return [val for val in value]
    
    
def resolveContent(html_content):
    from BeautifulSoup import BeautifulSoup
    import HTMLParser
    html_parser = HTMLParser.HTMLParser()
    content_parts = []        
    soup = BeautifulSoup(html_content.replace('\n','</br>'))
    for tag in soup.findAll('img'):
        tag['class'] = 'img-responsive'
        if 'http' not in tag['src']:
            tag['src'] = 'http://pic1.qkan.com'+tag['src']    
    for item in soup.findAll('h2'):
        parts = ''
        #content_parts[str(item.next).strip()] = ''
        cmd = item.nextSibling
        while cmd and '<h2>' not in str(cmd):
            #content_parts[str(item.next).strip()] += str(cmd).strip()
            parts += str(cmd).strip()
            cmd = cmd.nextSibling
        if parts:
            
            #parts=html_parser.unescape(parts)
            txt = html_parser.unescape(item.text)            
            txt=re.sub(ur"[^\u4e00-\u9fa5\w]", "", txt)
            content_parts.append((txt, parts))
    return content_parts


class selfSimpleListFilter(admin.ListFilter):
    # The parameter that should be used in the query string for that filter.
    parameter_name = None
    template = 'admin/filter_time.html'

    def __init__(self, request, params, model, model_admin):
        super(selfSimpleListFilter, self).__init__(
            request, params, model, model_admin)
        if self.parameter_name is None:
            raise ImproperlyConfigured(
                "The list filter '%s' does not specify "
                "a 'parameter_name'." % self.__class__.__name__)
        lookup_choices = self.lookups(request, model_admin)
        if lookup_choices is None:
            lookup_choices = ''
        self.lookup_choices =  lookup_choices
        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    def has_output(self):
        return self.lookup_choices #len(self.lookup_choices) > 0

    def value(self):
        """
        Returns the value (in string format) provided in the request's
        query string for this filter, if any. If the value wasn't provided then
        returns None.
        """
        return self.used_parameters.get(self.parameter_name, None)

    def lookups(self, request, model_admin):
        """
        Must be overriden to return a list of tuples (value, verbose value)
        """
        raise NotImplementedError

    def expected_parameters(self):
        return [self.parameter_name]

    def choices(self, cl):
        #yield self.value()
        
        #return
        yield {
            'selected': self.value() is None,
            'query_string': cl.get_query_string({}, [self.parameter_name]),
            'display': _('All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }
