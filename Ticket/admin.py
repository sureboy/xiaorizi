# -*- coding:utf-8 -*-
from django.contrib import admin
from Ticket.models import Coupon, InvoiceRecord, CouponRecord, CouponOwnRecord
from User.models import Customer
from LifeApi.models import NewEventTable

class CouponAdmin(admin.ModelAdmin):
    raw_id_fields = ['for_events', 'owners', 'used_for']
    list_display = ('id', 'coupon_type', 'coupon_value', 
                    'begin_time', 'end_time', 'is_general')

class InvoiceRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_number', 'amount_money', 
                    'title', 'type', 'state', 'remarks')

class CouponOwnRecordAdmin(admin.ModelAdmin):
    def show_coupon(self, obj):
        c = Coupon.objects.get(pk=obj.coupon_id)
        return u'%d - %.2f' % (c.id, c.coupon_value)

    show_coupon.short_description=u'优惠券'
    show_coupon.allow_tags = True

    def show_customer(self, obj):
        c = Customer.objects.get(pk=obj.customer_id)
        return u'%s' % c.name

    show_customer.short_description=u'持有人'
    show_customer.allow_tags = True

    list_display = ('id', 'show_coupon', 'show_customer',  'amount', 'begin_time', 'end_time')

class CouponRecordAdmin(admin.ModelAdmin):
    def show_coupon(self, obj):
        c = Coupon.objects.get(pk=obj.coupon_id)
        return u'%d - %.2f' % (c.id, c.coupon_value)

    show_coupon.short_description=u'优惠券'
    show_coupon.allow_tags = True

    def show_customer(self, obj):
        c = Customer.objects.get(pk=obj.customer_id)
        return u'%s' % c.name

    show_customer.short_description=u'使用者'
    show_customer.allow_tags = True

    def show_event(self, obj):
        e = NewEventTable.objects.get(pk=obj.event_id)
        return u'%s' % e.name

    show_event.short_description=u'活动'
    show_event.allow_tags = True

    readonly_fields = ['id', 'order_id', 'coupon_id', 'customer_id', 'event_id', 'price', 'cost',  'valid', 'time']
    list_display = ('id', 'show_coupon', 'show_customer', 'show_event', 'price', 'cost', 'valid', 'time')

# Register your models here.
admin.site.register(Coupon, CouponAdmin)
admin.site.register(InvoiceRecord, InvoiceRecordAdmin)
admin.site.register(CouponOwnRecord, CouponOwnRecordAdmin)
admin.site.register(CouponRecord, CouponRecordAdmin)
