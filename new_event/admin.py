#coding:utf-8
from django.contrib import admin
 
from models import  NewEventTable,NewEventTag,NewEventCat,\
                 NewDistrict,NewVenue,NewEventFrom,NewEventPrice,\
                 NewEventSeo,NewEventParagraph,NewEventImg,OldEvent,\
                 NewEventTableType,NewEventTablePoint,NewEventParagraphTag,\
                 NewEventPriceType,NewEventPriceCurrency,Crowfunding,NewOrder,\
                 NewOrderMessage,NewVenueClass,NewNavList,NewEventCatType,\
                 NewEventFromClass,NewEventFromType,NewEventPriceUnit,NewArticle, feelnum,feelType,\
                 AdminEventTheme,PostEvent,RefundRecord
                     
from dahuodong.models import SubscribeInfo
from admin_self.admin_event import EventAdmin,OldEventAdmin,TagAdmin,CatMPTTModelAdmin,ParagraphAdmin,ImgAdmin,testEventAdmin,SubscribeAdmin
from admin_self.admin_operate import DistrictMPTTModelAdmin,VenueAdmin,SeoAdmin,ArticleAdmin,feelnumAdmin
from admin_self.admin_data import adminVenueClass
from admin_self.admin_market import FromAdmin,PriceAdmin,orderAdmin,PriceUnitAdmin,\
                                    orderMessageAdmin,AdminTheme,AdminPostEvent, RefundAdmin

#内容编辑
admin.site.register(NewEventTable,EventAdmin )
admin.site.register(OldEvent, OldEventAdmin)
admin.site.register(NewEventTag,TagAdmin)
admin.site.register(NewEventCat,CatMPTTModelAdmin)
admin.site.register(NewEventParagraph,ParagraphAdmin)
admin.site.register(NewEventImg, ImgAdmin)



#关联参数
admin.site.register(NewEventTableType)
admin.site.register(NewEventPriceType)
admin.site.register(NewEventPriceCurrency)
admin.site.register(NewVenueClass,adminVenueClass)
admin.site.register(NewEventParagraphTag)
admin.site.register(NewNavList)
admin.site.register(NewEventTablePoint)
admin.site.register(NewEventCatType)
admin.site.register(NewEventFromClass)
admin.site.register(NewEventFromType)

#市场运营

admin.site.register(NewEventSeo,SeoAdmin)
admin.site.register(NewDistrict,DistrictMPTTModelAdmin)
admin.site.register(NewVenue,VenueAdmin)
admin.site.register(NewEventFrom,FromAdmin)
#admin.site.register(NewEventPrice,PriceAdmin)
admin.site.register(NewOrder,orderAdmin)
admin.site.register(NewOrderMessage,orderMessageAdmin)
admin.site.register(NewEventPriceUnit,PriceUnitAdmin)
admin.site.register(NewArticle, ArticleAdmin)
admin.site.register(feelnum, feelnumAdmin)
admin.site.register(feelType)
admin.site.register(AdminEventTheme,AdminTheme)
admin.site.register(PostEvent,AdminPostEvent)

admin.site.register(SubscribeInfo, SubscribeAdmin)
admin.site.register(RefundRecord, RefundAdmin)