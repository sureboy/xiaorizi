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
from spot.models import SysSpotTxt,SysSpotEvent
from django.db.models.signals import pre_save
#from common import spotcatUrl

class UserInfoEvent(models.Model):
    userinfo_id=models.IntegerField()
    sysspotevent_id=models.IntegerField()
    class Meta:
        managed = False
        db_table = 'sys_ac_user_info_event'
 
 
class UserInfo(models.Model):
    user_id=models.AutoField(primary_key=True )
    user_name = models.CharField(u'用户名称',max_length=100,blank=True )    
    user_cumulative=models.IntegerField(u'累计次数',blank=True )
    user_from =models.CharField(u'来源',max_length=100,blank=True )
    begin_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    end_time = models.DateTimeField(auto_now=True,verbose_name='最后编辑时间')
    event=models.ManyToManyField(SysSpotEvent,blank=True,verbose_name='关联活动') 
    def __unicode__(self):
        return '%s —— %s' % (self.user_id,self.user_name)      
    class Meta:
        #managed = False
        db_table = 'sys_ac_user_info'
        verbose_name = u'用户信息' 
        verbose_name_plural = u'用户信息'
        
class UserEventMessage(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(SysSpotEvent,blank=True,null=True, verbose_name='活动')
    message=models.ForeignKey(SysSpotTxt, verbose_name='留言')    
    user=models.ForeignKey(UserInfo, verbose_name='用户')
    #black_message=models.ForeignKey(SysSpotTxt,blank=True, verbose_name='回复留言')
    black_message=models.ForeignKey('self',null=True,blank=True, verbose_name='留言回复',related_name='children')
    #admin=models.ForeignKey(AdminInfo,blank=True, verbose_name='管理员') 
    path = models.CharField("路径", max_length=255, null=True, blank=True, help_text="此项不用填写")
    examine=models.BooleanField(u'审核',blank=True,default=False)
    begin_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    end_time = models.DateTimeField(auto_now=True,verbose_name='最后编辑时间')
    rel_time = models.DateTimeField(verbose_name='留言时间')
    #last_edit = models.CharField(u'最后编辑',max_length=200,blank=True)
    #edit =  models.CharField(u'创建',max_length=200,blank=False)
  
    
    class Meta:
        #managed = False
        db_table = 'sys_ac_user_message'
        verbose_name = u'留言' 
        verbose_name_plural = u'留言'
        
    def __unicode__(self):
        return self.message.txt


    '''
    def _node(self):

        indent_num = len(self.path.split(':')) -1

        indent = '____' * indent_num

        node = u'%s%s' % (indent, self.message.txt)

        return node

    node = property(_node)
    '''
    
    def has_children(self):        

        return self.children.all().count() > 0 and True or False
    
    def get_parents(self):

        parents_path = self.path.split(":")

        if len(parents_path)> 1:
            path = parents_path[:-1]
        else:
            path = parents_path

        parents = self.model(pk__in=parents_path)

        return parents
  
     
    def save(self, * args, ** kwargs):      

        super(self.__class__, self).save(*args, ** kwargs)
        if not  self.path:
            self.path = self.id     
            
            super(self.__class__, self).save(*args, ** kwargs)
'''
        if self.black_message:

            self.path = '%s:%s' % ( self.id,self.black_message.path,)

        else:

            self.path = self.id

        childrens = self.children.all()

        if len(childrens) > 0:

            for children in childrens:

                children.path = '%s:%s' % ( children.id,self.path)

                children.save()

        super(self.__class__, self).save(*args, ** kwargs)
     
       
def inital_category_path(sender, instance,** kwargs):

    if instance.id:

        if instance.black_message:

            instance.path = '%s:%s' % (instance.id,instance.black_message.path)

        else:

            instance.path = instance.id

pre_save.connect(inital_category_path, sender=UserEventMessage)
'''       
