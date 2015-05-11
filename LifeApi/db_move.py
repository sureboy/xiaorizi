#coding:utf-8
from django.contrib.auth.models import User

from LifeApi.models import feelnum, NewEventTable, NewEventImg, NewEventCat, NewEventTag, \
                           NewDistrict, NewVenue, NewEventFrom, NewEventParagraph,  \
                           NewEventPrice, OldEvent, NewEventSeo, NewEventTableType, \
                           NewEventTablePoint, NewEventImgServer, NewEventPriceUnit
                           

def move_database():
    '''
    使用：根目录下的manage_tmp.py指向LifeExpert.settings_tmp，
    LifeExpert/settings_tmp.py，使用LifeExpert.DBRouter_tmp.Router，
    LifeExpert/DBRouter_tmp.Router设置：
        db_fore_read:一个数据库, db_for_write:另一个数据库
    另外把LifeApi.models里的NewEventImg中的save方法注释掉
    >>>python manage_tmp.py shell
    >>>from LifeApi.db_move import move_database
    >>>move_database()
    '''
    xianshi = feelnum.objects.all()
    for xs in xianshi:
        # read feelnum
        event = xs.event
        print(event)
        imgs = event.img.all()
        for img in imgs:
            # create image data
            img.save()
            #NewEventImg.object.create(
            #        id=img.id, name=img.name, urls=img.urls,
            #        imgs=img.imgs, begin_time=img.begin_time, end_time=img.end_time,
            #        server_id=img.server_id, order=img.order, width=img.width,
            #        height=img.height
            #        )

        cat = event.cat.all()
        for i in cat:
            if i.img:
                i.img.save()
        tag = event.tag.all()
        city = event.city.all()
        for i in city:
            if i.img:
                i.img.save()
        addrs = event.addr.all()
        for add in addrs:
            add.save()
            #NewVenue.objects.create(
            #        id=add.id, venue_id=add.id, 
            #        longitude_baidu=add.longitude_baidu, latitude_baidu=add.latitude_baidu, 
            #        longitude_google=add.longitude_google, latitude_google=add.latitude_google,
            #        city_id=add.city_id, venue_class_id=add.venue_class_id,
            #        address=add.address, title=add.title, alias=add.alias
            #        )

        relevant = event.relevant.all()
        from_infos = event.from_info.all()
        for fi in from_infos:
            fi.edit=None
            fi.last_edit=None
            fi.save()
            #NewEventFrom.objects.create(
            #        id=fi.id, f_Class_id=fi.f_Class_id, Website=fi.Website,
            #        email=fi.email, tel=fi.tel, content=fi.content,
            #        type_id=fi.type_id
            #        )

        paragraphs = event.paragraph.all()
        for para in paragraphs:
            para_tag = para.cat_name.save()
            para_imgs = para.img.all()
            for para_img in para_imgs:
                para_img.save()
                #NewEventImg.object.create(
                #        id=para_img.id, name=para_img.name, urls=para_img.urls,
                #        imgs=para_img.imgs, begin_time=para_img.begin_time, end_time=para_img.end_time,
                #        server_id=para_img.server_id, order=para_img.order, width=para_img.width,
                #        height=para_img.height
                #        )

            para.save()
            #NewEventParagraph.objects.create(
            #        id=para.id, name=para.name, txt=para.txt, tag=para.tag,
            #        cat_name_id=para.cat_name_id, begin_time=para.begin_time,
            #        end_time=para.end_time, txt_order=para.txt_order
            #        )
            for para_img in para_imgs:
                para.img.add(para_img)

        price = event.Price
        price.save()
        old_event = event.old_event
        old_event.save()
        #NewEventPrice.objects.create(
        #        id=price.id, Currency_id=price.Currency_id, Type_id=price.Type_id,
        #        str=price.str, min=price.min, max=price.max, points=price.points,
        #        sale=price.sale
        #        )

        event.edit = None
        event.last_edit = None
        event.save()
        #ev = NewEventTable.objects.create(
        #        name=event.name, fname=event.fname, ename=event.ename,
        #        content=event.content, search=event.search, Price_id=price.id,
        #        create_time=event.create_time, rel_time=event.rel_time,
        #        begin_time=event.begin_time, end_time=event.end_time,
        #        hot=event.hot, order=event.order, isshow=event.isshow_id,
        #        point=event.point_id, state=event.state, release_time=event.release_time
        #        )

        for i in imgs:
            i.save()
            event.img.add(i)
        for i in cat:
            i.save()
            event.cat.add(i)
        for i in tag:
            i.save()
            event.tag.add(i)
        for i in city:
            i.save()
            event.city.add(i)
        for i in addrs:
            i.save()
            event.addr.add(i)
        for i in relevant:
            i.save()
            event.relevant.add(i)
        for i in from_infos:
            i.save()
            event.from_info.add(i)
        for i in paragraphs:
            i.save()
            event.paragraph.add(i)

        price_units = NewEventPriceUnit.objects.filter(event_id=event.id)
        for pu in price_units:
            pu.save()
            #NewEventPriceUnit.objects.create(
            #        event_id=pu.event_id, price=pu.price, sale=pu.sale,
            #        discount=pu.discount, original_price=pu.original_price,
            #        Currency_id=pu.Currency_id, begin_time=pu.begin_time,
            #        end_time=pu.end_time, stock=pu.stock, stock_d=pu.stock_d,
            #        form_info_id=pu.form_info_id, points=pu.points,
            #        status=pu.status, type=pu.type, content=pu.content
            #        )

        xs.save()

