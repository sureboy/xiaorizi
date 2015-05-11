from django import template
from django.conf import settings
from django.utils.datastructures import SortedDict
from LifeApi.models import NewNavList
import datetime
register = template.Library()

class NavNodeList(template.Node):
    def __init__(self):
        super(NavNodeList, self).__init__()


    def render(self, context):
         
        app=[]
        app_list={}
        for nav in NewNavList.objects.all():
            if not app_list.has_key(nav.app_name) :
                app_list[nav.app_name]=[]
                app.append({nav.app_name:app_list[nav.app_name]})
            nav.model=nav.model.lower()
            app_list[nav.app_name].append(nav)
            
             
            
            
        context['nav_node_self'] = app 
        return ''
@register.tag(name="nav_node")
def do_nav_node(parser, token):
    ''' 
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    ''' 
    return NavNodeList()


class CurrentTimeNode2(template.Node):
    def __init__(self, format_string):
        self.format_string = str(format_string)

    def render(self, context):
        now = datetime.datetime.now()
        context['current_time_h'] = now.strftime(self.format_string)
        return ''

@register.tag(name="current_time")
def do_current_time(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return CurrentTimeNode2(format_string[1:-1])






def register_render_tag(renderer):
    """
    Decorator that creates a template tag using the given renderer as the 
    render function for the template tag node - the render function takes two 
    arguments - the template context and the tag token
    """
    def tag(parser, token):
        class TagNode(template.Node):
            def render(self, context):
                return renderer(context, token)
        return TagNode()
    for copy_attr in ("__dict__", "__doc__", "__name__"):
        setattr(tag, copy_attr, getattr(renderer, copy_attr))
    return register.tag(tag)

@register_render_tag
def admin_reorder(context, token):
    """
    Called in admin/base_site.html template override and applies custom ordering 
    of apps/models defined by settings.ADMIN_REORDER
    """
    # sort key function - use index of item in order if exists, otherwise item
    sort = lambda order, item: (order.index(item), "") if item in order else (
        len(order), item) 
    if "app_list" in context:
        # sort the app list
        order = SortedDict(settings.ADMIN_REORDER)
        context["app_list"].sort(key=lambda app: sort(order.keys(), 
            app["app_url"][:-1]))
        for i, app in enumerate(context["app_list"]):
            # sort the model list for each app
            app_name = app["app_url"][:-1]
            if not app_name:
                app_name = context["request"].path.strip("/").split("/")[-1]
            model_order = [m.lower() for m in order.get(app_name, [])]
            context["app_list"][i]["models"].sort(key=lambda model: 
                sort(model_order, model["admin_url"].strip("/").split("/")[-1]))
    return ""


