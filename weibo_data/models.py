#coding:utf-8
from django.db import models 
from LifeApi.models import NewDistrict

class WeiboUser(models.Model):
    st=((0,u'活跃'),
        (1,u'暂停'),
          )
    name=models.CharField(u'用户名',unique=True,max_length=100)
    url=models.CharField(u'url',unique=True,max_length=100)
    city_name=models.CharField(u'城市名称',max_length=100,blank=True, null=True)
    city=models.ForeignKey(NewDistrict,verbose_name=u'城市',blank=True,null=True)
    style=models.CharField(u'风格',max_length=100,blank=True,)
    vermicelli=models.IntegerField(u'粉丝',default=0)
    state  = models.IntegerField(u'状态',default=0,choices=st)
    class Meta:
        db_table = 'sys_weibo_user'
        verbose_name = u'微博用户'
        verbose_name_plural = u'微博用户' 
        app_label = 'new_event'

