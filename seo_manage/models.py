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
#from django.core.cache import cache
 
#from BeautifulSoup import BeautifulSoup
from django.db import models
from LifeApi.models import NewEventTable,NewEventPrice,NewDistrict,NewEventCat
from django.contrib.auth.models import User



#from common import spotcatUrl
'''
class test_one(models.Model):
    name=models.CharField(u'名称',max_length=100)
    Price_s=models.OneToOneField(NewEventPrice,verbose_name=u'销售s',blank=True,null=True) 
    
    def __unicode__(self):
        return self.name
    class Meta:
        #managed = False
        db_table = 'sys_test_one'
        verbose_name = u'测试' 
        verbose_name_plural = u'测试'
'''        
                
class SiteInfo(models.Model):
    ct=( (0,u'博客'),
      (1,u'百度系'),
      (2,u'论坛|分类信息'),
      (3,u'社交|其他'),
      )
    
    name=models.CharField(u'名称',max_length=100)
    url=models.URLField(u'站点')
    event_count=models.IntegerField(blank=True, null=True,verbose_name=u'回访网站次数统计')
    site_cat=models.IntegerField(u'分类',blank=True, null=True,choices=ct,default=0)
    edit =  models.ForeignKey(User,verbose_name=u'创建编辑',blank=True,null=True,related_name='Site_edit')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间') 
    
    def __unicode__(self):
        return self.name
    class Meta:
        #managed = False
        db_table = 'sys_site_info'
        verbose_name = u'发布站点分类' 
        verbose_name_plural = u'发布站点分类'
    
class PostSeoInfo(models.Model):
    st=( (0,u'待审核'),
          (1,u'审核通过'),
          (2,u'审核不通过'),
          (3,u'人工查看'),
          )
    
    ct=( (0,u'未收录'),
          (1,u'已收录'),
          (2,u'人工测试'),
          )
    
    event=models.ForeignKey(NewEventTable,related_name='Post_event_table',blank=True,null=True,verbose_name=u'关联活动')
    site=models.ForeignKey(SiteInfo,verbose_name=u'站点',blank=True,null=True)
    #site_name=models.CharField(u'站点名称', max_length=100)
    site_url=models.URLField(u'文章地址' ,unique=True)
    
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')    
    rel_time = models.DateTimeField(auto_now=True ,verbose_name=u'最后编辑时间')
    edit =  models.ForeignKey(User,verbose_name=u'创建编辑',blank=True,null=True,related_name='Post_edit')
    last_edit = models.ForeignKey(User,verbose_name=u'最后编辑',blank=True,null=True,related_name='Post_last_edit')

    status = models.IntegerField(blank=True, null=True,verbose_name=u'状态',choices=st)
    baidu_include = models.IntegerField(blank=True, null=True,verbose_name=u'百度收录',choices=ct)
    u360_include = models.IntegerField(blank=True, null=True,verbose_name=u'360收录',choices=ct)
    google_include = models.IntegerField(blank=True, null=True,verbose_name=u'谷歌收录',choices=ct)
    baidu_include_time = models.DateTimeField(blank=True,null=True,verbose_name=u'百度收录时间')
    u360_include_time = models.DateTimeField(blank=True,null=True,verbose_name=u'360收录时间')
    google_include_time = models.DateTimeField(blank=True,null=True,verbose_name=u'google收录时间')
    
    def __unicode__(self):
        return self.site_url
    class Meta:
        #managed = False
        db_table = 'sys_post_info'
        verbose_name = u'发布站点' 
        verbose_name_plural = u'发布站点'
    
class FriendlyLink(models.Model):
    name=models.CharField(u'名称',max_length=100,unique=True)
    url=models.CharField(u'url地址' ,max_length=100,unique=True)
    order=models.IntegerField(u'排序',default=0,blank=True,)
    img=models.CharField(u'图片' ,max_length=200,blank=True)
    page=models.IntegerField(u'page',default=0,blank=True)
    city=models.ManyToManyField(NewDistrict,verbose_name=u'城市',blank=True,null=True,)
    cat=models.ManyToManyField(NewEventCat,verbose_name=u'分类',blank=True,null=True,)
    hot=models.IntegerField(u'热门',default=0, blank=True)
    endtime=models.DateTimeField(u'结束时间',blank=True,null=True)
    begintime=models.DateTimeField(u'结束时间',blank=True,null=True)
    def __unicode__(self):
        return self.name
    class Meta:
        #managed = False
        db_table = 'sys_site_link'
        verbose_name = u'友情链接' 
        verbose_name_plural = u'友情链接'
    
    
