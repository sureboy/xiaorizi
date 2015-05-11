#coding:utf-8
from django.db import models 

class AppVersion(models.Model):
    st=((1,u'活动家iOS'),
        (2,u'活动家Android'),
        (3,u'闲时iOS'),
        (4,u'闲时Android'),
          )
    st1=((0,u'不强制'),
        (1,u'强制'),
          )

    platform = models.IntegerField(u'系统',default=1,choices=st,unique=True)
    must_update = models.IntegerField(u'强制更新',default=0,choices=st1)
    version = models.CharField(u'版本号',max_length=45)
    url = models.CharField(u'链接地址',max_length=100)
    update_info = models.TextField(u'更新信息',max_length=300)
    update_time = models.DateTimeField(u'最后修改时间',auto_now=True)
    
    class Meta:
        db_table = 'app_version'
        verbose_name = u'app版本管理' 
        verbose_name_plural = u'app版本管理'
    
class AppVersionCode(models.Model):
    id = models.AutoField(primary_key=True)
    platform = models.IntegerField(default=1)
    must_update = models.IntegerField(default=0)
    version = models.CharField(max_length=45)
    url = models.CharField(max_length=100)
    update_info = models.CharField(max_length=300)
    update_time = models.IntegerField()
    
    class Meta:
        db_table = 'app_version_copy'