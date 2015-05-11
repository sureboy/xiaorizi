__author__ = 'sooshian'
from django.conf.urls import patterns, url

urlpatterns = patterns('Ticket.views',
    url(r'^coupon/use/$', 'coupon_use'),
    url(r'^coupon/mine/$', 'coupon_mine'),
    url(r'^coupon/get/$', 'coupon_get'),

)



urlpatterns += patterns('Ticket.invoice',
    url(r'^invoice_find/$', 'find_InvoiceRecord'),
    url(r'^invoice_submit/$', 'save_InvoiceRecord'),
    url(r'^order_invoice/$', 'order_invoice'),
    
    )
