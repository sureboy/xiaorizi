#coding:utf-8
from Ticket.models import InvoiceRecord
from User.models import Customer,Address
from LifeApi.models import NewOrder
from django.http import HttpResponse
from LifeApi.functions import getevent

import json
# Create your views here.
def save_InvoiceRecord(request):
    p={}
    p['code']=0
    
    if request.method != 'GET':
        p['msg']='Only POSTs are allowed'
        return HttpResponse(json.dumps(p), content_type="application/json")
    cds = request.GET
    user_id = cds.get('user_id','')
    if not user_id:
        p['msg']='Post user id is must'
        return HttpResponse(json.dumps(p), content_type="application/json")        
    try:
        user_p = Customer.objects.get(id=user_id)
    except:
        p['msg']='don\'t find user id, err'
        return HttpResponse(json.dumps(p), content_type="application/json")    
    
    
    addr_id = cds.get('addr_id','')   
    if not addr_id:
        try:
            addr_p=AddAddress(request,user_p)
        except:
            p['msg']='addr err'
            return HttpResponse(json.dumps(p), content_type="application/json")
            
    amount_money_p=cds.get('amount_money',0)     
    title_p=cds.get('title','')     
    content_p=cds.get('content','') 
    remarks_p=cds.get('remarks','') 
    if not amount_money_p:
        p['msg']='amount money err'
        return HttpResponse(json.dumps(p), content_type="application/json")    
    if not title_p:
        p['msg']='title err'
        return HttpResponse(json.dumps(p), content_type="application/json")            
    Invoice=InvoiceRecord.objects.create(user=user_p,
                                 addr=addr_p if addr_p else None,
                                 amount_money=amount_money_p,
                                 title=title_p,
                                 content=content_p,
                                 remarks=remarks_p,
                                 )
    orders_d=cds.get('order_number',None) 
    if orders_d:
        for ord in orders_d.split(','):
            err=[]
            try:
                Invoice.orders.add(NewOrder.objects.get(order_number=ord))
            except Exception,e:
                err.append(str(e))
                
            if err:
                return HttpResponse(json.dumps({"code":1,"msg":u"request success","err":err}), content_type="application/json")
    
    return HttpResponse(json.dumps({"code":1,"msg":u"request success"}), content_type="application/json")


def AddAddress(request,user=None):
    if request.method == 'POST':
        cds = request.POST
        #user_id = request.session['user_id']
        if not user:
            user_id = cds.get('userid')
            user = Customer.objects.get(id=user_id)
        name = cds.get('name')
        phone = cds.get('phone')
        address_name = cds.get('address_name')
        if name and phone and address_name:
            if user.address_set.all():
                default = 0
            else:
                default = 1
            newAddress = Address(address_name = address_name,
                                   phone = phone,
                                   name = name,
                                   default = default,
                                   user = user,
                                   )
            newAddress.save()
            return newAddress
            '''
            json_data = {
                        'id':newAddress.id,
                        'name':name,
                        'phone':phone,
                        'address_name':address_name,
                        'default':default, 
                        }
           
            return HttpResponse(json.dumps({"code":1,"msg":'',"data":json_data}), content_type="application/json")
            '''
        else:
            return False  
                
    else:
        return False   


def find_InvoiceRecord(request):
    p={}
    p['code']=0   
    if request.method != 'GET':
        p['msg']='Only POSTs are allowed'
        return HttpResponse(json.dumps(p), content_type="application/json")
    cds = request.GET
    InvoiceRecord_id = cds.get('id','')
    invoi=InvoiceRecord.objects
    if InvoiceRecord_id:
        try:
            inv=invoi.get(id=InvoiceRecord_id)
            p['code']=1
            p['msg']='request success'
            p['data']=[output_invoice(inv)]
            #return HttpResponse(json.dumps(p), content_type="application/json")
        except:
            p['msg']='Don\'d find id'
        return HttpResponse(json.dumps(p), content_type="application/json")
    user_id = cds.get('user_id','')
    if user_id:
        p['code']=1
        p['msg']='request success'
        p['data']=[]
        for inv in invoi.filter(user__id=user_id).order_by('-id'):
            p['data'].append(output_invoice(inv))
            
        return HttpResponse(json.dumps(p), content_type="application/json")
    phone = cds.get('phone','')
    order_number = cds.get('order_number','')
    if phone:
        invoi+=invoi.filter(user__phone=phone)
    if order_number:
        invoi+=invoi.filter(orders__order_number=order_number)
    if phone or order_number:
        p['code']=1
        p['msg']='request success'
        p['data']=[]
        for inv in invoi.order_by('-id'):
            p['data'].append(output_invoice(inv))
        return HttpResponse(json.dumps(p), content_type="application/json") 
    #title_p=cds.get('title','')
def output_invoice(inv):
    return {  'state':inv.state,
              'invoice_number':inv.invoice_number,
              'title':inv.title,
              'content':inv.content,
              'remarks':inv.remarks
              }
def order_invoice(request):
    p={}
    p['code']=0   
    if request.method != 'GET':
        p['msg']='Only POSTs are allowed'
        return HttpResponse(json.dumps(p), content_type="application/json")
    cds = request.GET
    user_id = cds.get('user_id','')
    invoi=NewOrder.objects.filter(order_pay_status = 20)
    if user_id:
        p['code']=1
        p['msg']='request success'
        p['data']=[]
        for inv in invoi.filter(order_userid=user_id).order_by('-id'):
            p['data'].append(output_invoice(inv))
            
        return HttpResponse(json.dumps(p), content_type="application/json")
    phone = cds.get('phone','')
    order_number = cds.get('order_number','')
    if phone:
        invoi+=invoi.filter(order_tel=phone)
    if order_number:
        invoi+=invoi.filter(order_number=order_number)
    if phone or order_number:
        p['code']=1
        p['msg']='request success'
        p['data']=[]
        p['event']=[]
        p['order']=[]
        for inv in invoi.filter(user__id=user_id).order_by('-id'):
            NewOrder.objects
            state=0
            if invoi.invoicerecord_set.count()>0:
                try:
                    ce=invoi.invoicerecord_set.all()[0]
                    state=ce.state
                except:
                    pass
            
            p['data'].append({'event':getevent(inv.event_id),'order':output_order(inv),'state':state,'money':float(inv.order_totalpay)})
            p['order'].append(output_order(inv))
            p['event'].append(getevent(inv.event_id))
        return HttpResponse(json.dumps(p), content_type="application/json") 
def output_order(item):
    order_pay_status="未付款"
    if item.order_pay_status == 20:
        order_pay_status = '已付款'
    elif item.order_pay_status == 30:
        order_pay_status = '退款'
    else:
        pass 
    
    order_status = '未处理'
    if item.order_status == 10:
        order_status = '正在处理'
    return {
        'price':float(item.order_price),
        'order_id':item.order_number,
        'user_id':item.order_userid,
        'addtime':item.order_addtime,
        'name':item.order_user_name,
        'phone':item.order_tel,
        'address':item.order_address,
        'message':item.order_text,
        "total":float(item.order_totalpay),
        "amount":item.order_amount,
        "order_pay_status":order_pay_status,
        "order_status":order_status,
        }