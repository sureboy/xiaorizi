#coding:utf-8
from django.db import models 
from django.utils.timezone import now
from LifeApi.models import NewEventTable

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, blank=True)
    phone = models.IntegerField()
    password = models.CharField(max_length=100)
    email = models.EmailField()
    register_time = models.IntegerField( blank=True)
    last_login_time = models.IntegerField( blank=True)
    is_temporary = models.IntegerField()
    headphoto_path = models.CharField(max_length=100)
    #push_baidu=models.CharField(max_length=20)
    def __unicode__(self):
        return '%s %s' % (self.id,self.name)      
    
    class Meta:
        db_table = 'user_customer'
        app_label = 'user_center'
        verbose_name = u'用户'
        verbose_name_plural = u'用户'

class UserPushInfo(models.Model):
    st=((1,u'android'),
        (2,u'IOS'),
          )
    user=models.ForeignKey(Customer,verbose_name='用户',related_name='pushUser',blank=True)
    event=models.ManyToManyField(NewEventTable,verbose_name='活动',related_name='pushEvent',blank=True,)
    push_user=models.CharField(u'推送id',max_length=20)
    push_channel=models.CharField(u'channel_id',max_length=20,blank=True)
    app_type=models.IntegerField(u'app类型',choices=st,default=1)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')    
    rel_time = models.DateTimeField(auto_now=True ,verbose_name=u'最后更新时间')
    class Meta:
        db_table = 'user_pushinfo'
        app_label = 'user_center'
        verbose_name = u'用户推送'
        verbose_name_plural = u'用户推送'
        
class Address(models.Model):
    id = models.AutoField(primary_key=True)
    address_name = models.CharField(max_length=100,blank=True)
    name = models.CharField(max_length=40, blank=True)
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(Customer)
    default = models.IntegerField()

    def __unicode__(self):
        return '%s %s' % (self.user, self.address_name)
    
    class Meta:
        managed = False
        db_table = 'user_address'
        app_label = 'user_center'
        verbose_name = u'用户地址'
        verbose_name_plural = u'用户地址'
        

class AppGetui(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    client_id = models.CharField(max_length=50,blank=True)
    token = models.CharField(max_length=50,blank=True)
    update_time = models.IntegerField()
    udid = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'app_getui'
        app_label = 'user_center'
