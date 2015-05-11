#coding:utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

from LifeApi.models import NewEventSeo

class PubEventCat(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=30, blank=True)
    cat_ename = models.CharField(max_length=30, blank=True)
    cat_fid = models.IntegerField()
    cat_id_map = models.IntegerField()
    cat_typeid = models.IntegerField()
    cat_order = models.IntegerField()
    cat_son_id1 = models.CharField(max_length=200, blank=True)
    cat_son_id2 = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'pub_event_cat'


class SysCommonDistrict(models.Model):
    district_id = models.IntegerField(primary_key=True)
    district_name = models.CharField(max_length=255)
    title = models.CharField(max_length=30, blank=True,db_index=True)
    capital_letter = models.CharField(max_length=5, blank=True)
    level = models.IntegerField()
    usetype = models.IntegerField()
    upid = models.IntegerField()
    displayorder = models.IntegerField()
    recomendindex = models.IntegerField(blank=True, null=True)
    baidu_code = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'sys_common_district'

class SysEvent(models.Model):
    event_id = models.IntegerField(primary_key=True)
    event_name = models.CharField(max_length=300, blank=True)
    event_app_name = models.CharField(max_length=300, blank=True)
    district_id = models.IntegerField()
    province_id = models.IntegerField(blank=True, null=True)
    event_begin_time = models.IntegerField()
    event_end_time = models.IntegerField()
    event_cat = models.IntegerField()
    event_cat1 = models.IntegerField()
    event_cat_tag = models.CharField(max_length=200, blank=True)
    event_price = models.CharField(max_length=300, blank=True)
    event_price_currency = models.IntegerField()
    event_price_backup = models.CharField(max_length=300)
    event_lowprice = models.IntegerField(blank=True, null=True)
    event_highprice = models.IntegerField(blank=True, null=True)
    event_isfree = models.IntegerField(blank=True, null=True)
    event_content = models.TextField(blank=True)
    event_comment = models.CharField(max_length=400, blank=True)
    event_cool = models.IntegerField(blank=True, null=True)
    event_img = models.CharField(max_length=100, blank=True)
    event_img_server = models.IntegerField()
    venue_id = models.IntegerField()
    venue_info = models.CharField(max_length=200, blank=True)
    event_tag = models.CharField(max_length=150, blank=True)
    event_isshow = models.IntegerField()
    event_recomend = models.IntegerField()
    event_point = models.IntegerField()
    crawl_url = models.CharField(max_length=700, blank=True)
    crawl_site = models.CharField(max_length=60, blank=True)
    event_officer = models.CharField(max_length=300, blank=True)
    crawl_title = models.CharField(max_length=300, blank=True)
    event_support = models.CharField(max_length=300, blank=True)
    event_assistant = models.CharField(max_length=300, blank=True)
    event_dep = models.CharField(max_length=300, blank=True)
    event_support_info = models.TextField(blank=True)
    event_address = models.CharField(max_length=300, blank=True)
    crawl_time = models.IntegerField()
    event_order = models.IntegerField()
    event_rank = models.IntegerField(blank=True, null=True)
    event_editor = models.CharField(max_length=30, blank=True)
    event_search = models.CharField(max_length=100, blank=True)
    event_random = models.IntegerField()
    event_like = models.IntegerField()
    event_longitude_baidu = models.FloatField()
    event_latitude_baidu = models.FloatField()
    event_longitude_google = models.FloatField()
    event_latitude_google = models.FloatField()
    event_time_expire = models.IntegerField()
    event_cat_field1 = models.CharField(max_length=100, blank=True)
    event_cat_field2 = models.CharField(max_length=100, blank=True)
    event_cat_field3 = models.CharField(max_length=100, blank=True)
    event_cat_field4 = models.CharField(max_length=100, blank=True)
    event_cat_field5 = models.CharField(max_length=100, blank=True)
    synchronization = models.IntegerField()
    event_theme = models.CharField(max_length=100)
    event_discount = models.CharField(max_length=100)
    event_discount_price = models.CharField(max_length=100)
    event_price_model = models.IntegerField()
    event_islongtime = models.IntegerField()
    seo_id=models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'sys_event'
        
    #def __unicode__(self):
        #return self.event_id  
    
class Crowfunding(models.Model):
    cf_id =  models.IntegerField(primary_key=True)
    cf_total = models.IntegerField()
    cf_price = models.CharField(max_length=45)
    event_id = models.IntegerField()
    cf_already = models.IntegerField()
    cf_already_percent = models.FloatField()


class SysEventCat(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=100, blank=True)
    cat_ename = models.CharField(max_length=100, blank=True)
    cat_fid = models.IntegerField()
    cat_typeid = models.IntegerField()
    cat_tag = models.CharField(max_length=300, blank=True)
    cat_seo = models.TextField(blank=True)
    cat_templets = models.CharField(max_length=50, blank=True)
    cat_order = models.IntegerField()
    cat_etp_id1 = models.IntegerField(blank=True, null=True)
    cat_etp_id2 = models.IntegerField(blank=True, null=True)
    cat_etp_id3 = models.IntegerField(blank=True, null=True)
    cat_etp_id4 = models.IntegerField(blank=True, null=True)
    cat_etp_id5 = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'sys_event_cat'

class SysEventHot(models.Model):
    id = models.IntegerField(primary_key=True)
    hot = models.IntegerField(blank=True, null=True)
    begin_time = models.IntegerField(blank=True, null=True)
    end_time = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    page_id = models.IntegerField(blank=True, null=True)
    cat_id = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'sys_event_hot'
    

class SysEventNow(models.Model):
    event_id = models.IntegerField(primary_key=True)
    event_name = models.CharField(max_length=300, blank=True)
    district_id = models.IntegerField()
    event_begin_time = models.IntegerField()
    event_end_time = models.IntegerField()
    event_cat = models.IntegerField()
    event_cat_tag = models.CharField(max_length=200, blank=True)
    event_price = models.CharField(max_length=300, blank=True)
    event_content = models.TextField(blank=True)
    event_img = models.CharField(max_length=100, blank=True)
    event_img_server = models.IntegerField()
    venue_id = models.IntegerField()
    venue_info = models.CharField(max_length=200, blank=True)
    event_address = models.CharField(max_length=300, blank=True)
    event_tag = models.CharField(max_length=150, blank=True)
    event_isshow = models.IntegerField()
    crawl_url = models.CharField(max_length=700, blank=True)
    crawl_site = models.CharField(max_length=60, blank=True)
    event_officer = models.CharField(max_length=300, blank=True)
    crawl_title = models.CharField(max_length=300, blank=True)
    event_support = models.CharField(max_length=300, blank=True)
    event_assistant = models.CharField(max_length=300, blank=True)
    event_dep = models.CharField(max_length=300, blank=True)
    event_support_info = models.TextField(blank=True)
    crawl_time = models.IntegerField()
    event_order = models.IntegerField()
    event_editor = models.CharField(max_length=30, blank=True)
    event_search = models.CharField(max_length=300, blank=True)
    event_kid = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'sys_event_now'


class SysEventTheme(models.Model):
    id = models.IntegerField(primary_key=True)
    theme_name = models.CharField(max_length=100)
    num = models.IntegerField()
    event_set = models.CharField(max_length=300)
    cities = models.CharField(max_length=300)
    begin_time = models.IntegerField()
    end_time = models.IntegerField()
    picture_web = models.CharField(max_length=100)
    show_pic = models.IntegerField()
    picture_server = models.IntegerField()
    theme_order = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'sys_event_theme'

class SysEventTui(models.Model):
    id = models.IntegerField(primary_key=True)
    page_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=150, blank=True)
    img_url = models.CharField(max_length=100, blank=True)
    text = models.TextField(blank=True)
    tuijian_order = models.IntegerField(blank=True, null=True)
    begin_time = models.IntegerField(blank=True, null=True)
    end_time = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    dahuodong_ad = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'sys_event_tui'

class SysEventTypeParameter(models.Model):
    etp_id = models.IntegerField(primary_key=True)
    etp_name = models.CharField(max_length=100, blank=True)
    etp_fid = models.IntegerField(blank=True, null=True)
    etp_type = models.IntegerField(blank=True, null=True)
    etp_order = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'sys_event_type_parameter'

class SysLinkTag(models.Model):
    link_id = models.IntegerField(primary_key=True)
    link_http = models.CharField(max_length=50, blank=True)
    link_tag1 = models.CharField(max_length=500, blank=True)
    link_tag2 = models.CharField(max_length=500, blank=True)
    link_tag3 = models.CharField(max_length=500, blank=True)
    link_tag4 = models.CharField(max_length=500, blank=True)
    link_tag5 = models.CharField(max_length=500, blank=True)
    link_tag6 = models.CharField(max_length=500, blank=True)
    link_type = models.IntegerField(blank=True, null=True)
    link_cat = models.IntegerField(blank=True, null=True)
    link_name = models.CharField(max_length=100, blank=True)
    link_begin = models.IntegerField(blank=True, null=True)
    link_end = models.IntegerField(blank=True, null=True)
    link_user = models.CharField(max_length=100, blank=True)
    class Meta:
        managed = False
        db_table = 'sys_link_tag'

class SysOrder(models.Model):
    order_id = models.IntegerField(primary_key=True)
    order_number = models.CharField(max_length=20, blank=True)
    order_user_name = models.CharField(max_length=100, blank=True)
    order_tel = models.CharField(max_length=100, blank=True)
    order_email = models.CharField(max_length=100, blank=True)
    order_reg_fields = models.IntegerField()
    order_price = models.DecimalField(max_digits=7, decimal_places=2)
    order_totalpay = models.DecimalField(max_digits=7, decimal_places=2)
    order_amount = models.IntegerField()
    order_address = models.CharField(max_length=500, blank=True)
    order_payment = models.CharField(max_length=100, blank=True)
    order_text = models.CharField(max_length=200, blank=True)
    order_addip = models.CharField(max_length=20, blank=True)
    order_addtime = models.IntegerField(blank=True, null=True)
    order_paytime = models.IntegerField(blank=True, null=True)
    admin_name = models.CharField(max_length=100, blank=True)
    admin_id = models.IntegerField(blank=True, null=True)
    admin_text = models.CharField(max_length=200, blank=True)
    order_telphone = models.CharField(max_length=20, blank=True)
    order_pay_status = models.IntegerField(blank=True, null=True)
    order_status = models.IntegerField(blank=True, null=True)
    event_id = models.IntegerField(blank=True, null=True)
    event_name = models.CharField(max_length=200, blank=True)
    city_title = models.CharField(max_length=10, blank=True)
    order_userid = models.IntegerField()
    order_pay_info = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'sys_order'


class SysOrderMessage(models.Model):
    msg_id = models.IntegerField(primary_key=True)
    event_id = models.IntegerField()
    event_name = models.CharField(max_length=300, blank=True)
    msg_name = models.CharField(max_length=50, blank=True)
    msg_email = models.CharField(max_length=100, blank=True)
    msg_tel = models.CharField(max_length=100, blank=True)
    msg_content = models.CharField(max_length=500, blank=True)
    msg_addtime = models.IntegerField()
    msg_addip = models.CharField(max_length=20, blank=True)
    type=models.IntegerField(default=0)
    class Meta:
        managed = False
        db_table = 'sys_order_message'

class SysOrderSimple(models.Model):
    order_id = models.IntegerField(primary_key=True)
    order_number = models.IntegerField(blank=True, null=True)
    order_user = models.IntegerField(blank=True, null=True)
    order_contact = models.CharField(max_length=50, blank=True)
    order_reg_fields = models.IntegerField(blank=True, null=True)
    order_text = models.CharField(max_length=500, blank=True)
    order_code = models.CharField(max_length=32, blank=True)
    order_address = models.CharField(max_length=200, blank=True)
    order_tel = models.CharField(max_length=100, blank=True)
    order_email = models.CharField(max_length=100, blank=True)
    order_money_count = models.FloatField(blank=True, null=True)
    order_promotions = models.IntegerField(db_column='order_Promotions', blank=True, null=True) # Field name made lowercase.
    event_id = models.IntegerField(blank=True, null=True)
    venue_id = models.IntegerField(blank=True, null=True)
    venue_title = models.CharField(max_length=100, blank=True)
    order_area = models.IntegerField(blank=True, null=True)
    order_city = models.IntegerField(blank=True, null=True)
    visitor_id = models.IntegerField(blank=True, null=True)
    order_time = models.IntegerField(blank=True, null=True)
    order_status = models.IntegerField(blank=True, null=True)
    order_ip = models.CharField(max_length=10, blank=True)
    admin_name = models.CharField(max_length=20, blank=True)
    admin_text = models.CharField(max_length=500, blank=True)
    admin_edit_time = models.IntegerField(blank=True, null=True)
    cat_id = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'sys_order_simple'

class SysRegExtendInfo(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True) # Field name made lowercase.
    user_id = models.IntegerField()
    reg_field_id = models.IntegerField()
    order_id = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=500)
    class Meta:
        managed = False
        db_table = 'sys_reg_extend_info'


class SysSearchKey(models.Model):
    keyid = models.IntegerField(primary_key=True)
    keyword = models.CharField(max_length=50, blank=True)
    ip = models.IPAddressField()
    search_time = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'sys_search_key'

class SysUsers(models.Model):
    user_uid = models.IntegerField(primary_key=True)
    user_name = models.TextField()
    user_email = models.TextField()
    user_tel = models.TextField(blank=True)
    user_password = models.TextField()
    user_register_date = models.DateField()
    class Meta:
        managed = False
        db_table = 'sys_users'

class SysVenue(models.Model):
    venue_id = models.IntegerField(primary_key=True)
    venue_longitude_baidu = models.FloatField()
    venue_latitude_baidu = models.FloatField()
    venue_longitude_google = models.FloatField()
    venue_latitude_google = models.FloatField()
    venue_class = models.CharField(max_length=30, blank=True)
    district_id = models.IntegerField()
    venue_address = models.CharField(max_length=100, blank=True)
    venue_title = models.CharField(max_length=300, blank=True)
    venue_alias = models.CharField(max_length=300, blank=True)
    venue_damai = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'sys_venue'
        
        
class SubscribeInfo(models.Model):
    id = models.AutoField(primary_key=True)
    #user_name = models.CharField(max_length=100, blank=True)
    #age = models.IntegerField()
    phone = models.CharField(max_length=20,blank=True)
    email = models.CharField(max_length=100, blank=True)
    keywords = models.CharField(max_length=200,blank=True)
    from_app = models.IntegerField(default=0)
    cats = models.CharField(max_length=240,blank=True)
    #cities = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'subscribe_info'
        
class CustomPublishEvent(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    
    event_cat = models.IntegerField()
    event_name = models.CharField(max_length=100)
    event_content = models.CharField(max_length=2000)
    venue_name = models.CharField(max_length=100)
    event_begin_time = models.IntegerField()
    event_end_time = models.IntegerField()
    event_price = models.CharField(max_length=100)
    class Meta:
        db_table = 'sys_custom_publish_event'
        
class singers(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'hot_singers'
