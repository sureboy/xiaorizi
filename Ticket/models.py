# -*- coding:utf-8 -*-
__author__ = 'sooshian'

from django.db import models
from LifeApi.models import NewEventTable, NewOrder
from User.models import Customer, Address

class Coupon(models.Model):
    c_type = (
        (0, u'------'),
        (1, u'抵价券'),
        (2, u'体验券'),
    )
    coupon_type = models.IntegerField(u'优惠券类型', blank=True, choices=c_type, default=2)
    coupon_value = models.FloatField(u'优惠券面值', blank=True, null=True)

    begin_time = models.DateTimeField( verbose_name=u'开始时间',blank=True,null=True)
    end_time = models.DateTimeField( verbose_name=u'结束时间',blank=True,null=True)

    is_general = models.BooleanField(u'是否通用')
    for_events = models.ManyToManyField(NewEventTable, blank=True, null=True, verbose_name=u'适用活动')
    cost_threshold = models.FloatField(u'价格阈值', blank=True, null=True)
    other_threshold = models.FloatField(u'其他阈值', blank=True, null=True)

    range_comment = models.TextField(u'使用条件说明', blank=True, null=True)
    owners = models.ManyToManyField(Customer, blank=True, null=True, verbose_name=u'持券人')
    used_for = models.ManyToManyField(NewOrder, blank=True, null=True, verbose_name=u'已使用于')

    def __unicode__(self):
        return u"%.2f" % self.coupon_value

    class Meta:
        #managed = False
        db_table = 'sys_coupon_manage'
        app_label = 'user_center'
        verbose_name = u'优惠券管理'
        verbose_name_plural = u'优惠券管理'

class InvoiceRecord(models.Model):
    st = (
        (0, u'普通发票（纸质）'),
        (1, u'增值税发票'),
    )
    sta = (
        (0, u'未开发票'),
        (1, u'开发票中'),
        (2, u'已开发票'),
    )
    invoice_number = models.CharField(u'发票编号', max_length=100, blank=True)
    amount_money = models.DecimalField(u'发票金额',max_digits=15, decimal_places=2)
    title = models.CharField(u'发票抬头', max_length=100)
    content = models.CharField(u'发票内容', max_length=500, blank=True)
    type = models.IntegerField(u'发票类型', default=0, choices=st)
    state = models.IntegerField(u'开票状态', default=0, choices=sta)
    remarks = models.CharField(u'备注', max_length=500, blank=True)
    orders = models.ManyToManyField(NewOrder, blank=True, null=True, verbose_name=u'涉及订单')
    user = models.ForeignKey(Customer, verbose_name=u'购买方', blank=True, null=True, related_name='customer')
    addr = models.ForeignKey(Address, verbose_name=u'收票地址', blank=True, null=True, related_name='logistics_address')
    template = models.ForeignKey(Customer, verbose_name=u'发票模板', blank=True, null=True, related_name='template')

    class Meta:
        #managed = False
        db_table = 'sys_invoice_record'
        app_label = 'user_center'
        verbose_name = u'发票记录'
        verbose_name_plural = u'发票记录'

class CouponRecord(models.Model):
    coupon_id = models.IntegerField(u'优惠券编号', blank=True, null=True)
    customer_id = models.IntegerField(u'使用者编号', blank=True, null=True)
    event_id = models.IntegerField(u'活动编号', blank=True, null=True)
    price = models.FloatField(u'原始价格', blank=True, null=True)
    cost = models.FloatField(u'折后价格', blank=True, null=True)
    valid = models.BooleanField(u'已生效', blank=True, null=True)
    time = models.DateTimeField( verbose_name=u'使用时间',blank=True,null=True)
    order_id = models.IntegerField(u'订单编号', blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'sys_coupon_record'
        app_label = 'user_center'
        verbose_name = u'优惠券使用记录'
        verbose_name_plural = u'优惠券使用记录'

class CouponOwnRecord(models.Model):
    coupon_id = models.IntegerField(u'优惠券编号', blank=True, null=True)
    customer_id = models.IntegerField(u'持有者编号', blank=True, null=True)
    amount = models.IntegerField(u'数量', blank=True, null=True)
    begin_time = models.DateTimeField( verbose_name=u'开始时间',blank=True,null=True)
    end_time = models.DateTimeField( verbose_name=u'结束时间',blank=True,null=True)

    class Meta:
        #managed = False
        db_table = 'sys_coupon_own_record'
        app_label = 'user_center'
        verbose_name = u'优惠券持有记录'
        verbose_name_plural = u'优惠券持有记录'