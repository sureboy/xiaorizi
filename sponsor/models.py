#!-*- coding:utf-8 -*-
'''
活动家程序新增模块
主要需求：将活动场馆地址和主办方信息，有针对性的整理展示到网站前页，以及在后台添加编辑查询。
要求：
1、以下有网站系统正在使用的跟新模块相关联的 数据模型（代码为django） 供参考，请在不影响现有系统正常运行的情况下，进行定义设计。
2、针对网站页面展示进行高并发优化处理，优化方案、使用程序框架等请自行定夺优化。
        相关信息说明：网站主体程序基于python-django框架完成，服务器配置方案有两种（nginx+tornado+mysql+memcache）（apache+mysql+memcache）。
3、编辑后台对相关信息进行清晰详细的管理，以及对展示页信息有效推荐等人工操作
4、UI：与现有页面风格尽量相似，信息展示认知度好，界面清晰美观，遵守seo规则呈现html页面
'''
from django.db import models
from django.contrib.auth.models import User
from LifeApi.models_admin import NewEventImg, NewEventFrom, NewEventTable

#主办方
class NewSponsor(models.Model):
    name = models.CharField(u'主办方名称', max_length=200)
    intro = models.TextField(u'主办方简介', blank=True)
    like_count = models.IntegerField(u'喜欢数量', blank=True, null=True)
    is_verify = models.BooleanField(u'是否认证')
    pic = models.ForeignKey(NewEventImg, blank=True, null=True, verbose_name=u'图片')
    #统计量
    event_count = models.IntegerField(u'活动数量', blank=True, null=True)
    #在不修改NewEventFrom的情况下添加1-N关系（不在NewEventFrom中添加外键），最方便的方式是用N-N曲线救国
    event_from = models.ManyToManyField(NewEventFrom, blank=True, null=True, verbose_name=u'信息来源')
    events = models.ManyToManyField(NewEventTable, blank=True, null=True, verbose_name=u'活动')

    #便于编辑
    edit = \
            models.ForeignKey(User,verbose_name=u'创建编辑',blank=True,null=True,related_name='sponsor_edit')
    last_edit = \
            models.ForeignKey(User,verbose_name=u'最后编辑',blank=True,null=True,related_name='sponsor_last_edit')

    feature = models.TextField(u'特征集合', blank=True)

    def __unicode__(self):
        return '%s ' % (self.name,)


    class Meta:
        db_table = 'sys_new_sponsor'
        verbose_name = u'主办方管理'
        verbose_name_plural = u'主办方管理'

class ImageAds(models.Model):
    s = (
        (0,u'有效'),
        (1,u'长期'),
        (2,u'无效'),
        (3,u'审核'),
      )
    ads_pos = (
        (1,u'首页-----顶部轮播'),
        (2,u'首页-----底部位置-----左'),
        (3,u'首页-----底部位置-----右'),
        (4,u'列表页-----轮播'),
    )
      
    state = models.SmallIntegerField(u'状态',blank=True, choices=s, default=3)
    name = models.CharField(u'投放人', max_length=200, blank=True, null=True)
    begin_time = models.DateTimeField(verbose_name=u'投放时间', blank=True, null=True)
    end_time = models.DateTimeField(verbose_name=u'过期时间', blank=True, null=True) 
    
    pic = models.OneToOneField(NewEventImg, blank=True, null=True, verbose_name=u'图片')
    title = models.CharField(u'标题', max_length=200, blank=True, null=True)
    description = models.TextField(u'描述', blank=True, null=True)
    url = models.URLField(u'跳转URL', blank=True, null=True)
    
    rank = models.IntegerField(u'排序', default=0)
    
    position = models.IntegerField(u'投放位置编号', choices=ads_pos, blank=True, null=True)
    position_intro = models.CharField(u'投放位置说明', max_length=200, blank=True, null=True)
    
    pv_total = models.IntegerField(u'总PV', default=0)
    price = models.FloatField(u'价格', blank=True, null=True)
    
    remarks = models.TextField(u'备注', blank=True, null=True)
    edit =  models.ForeignKey(User,verbose_name=u'创建编辑', blank=True, null=True, related_name='image_ads_edit')
    last_edit = models.ForeignKey(User,verbose_name=u'最后编辑', blank=True, null=True, related_name='image_ads_last_edit')
    
    def __unicode__(self):
        return '%s ' % (self.title,)

    class Meta:
        db_table = 'sys_image_ads'
        verbose_name = u'图片广告管理'
        verbose_name_plural = u'图片广告管理'
