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

 
#from BeautifulSoup import BeautifulSoup SysSpotInfo
from django.db import models

from django.contrib.auth.models import User,AbstractUser
from mptt.models import MPTTModel,TreeForeignKey
#from admin_self.common import NewCatUrl,event_city_cat
#from admin_self.froms import string_with_title
import datetime
#from settings import MEDIA_ROOT
#from django.db.models.fields.files import ImageFieldFile
 
#from PIL import Image
#from django.db.models.signals import pre_save
'''
class ad_User(User):
    def __unicode__(self):        
        return u'%s%s' % (self.edit.first_name,self.edit.last_name)
'''
class NewNavList(models.Model):
    
    name=models.CharField(u'名称',max_length=100, unique=True)
    app_label=models.CharField(u'标签',max_length=100, )
    app_name=models.CharField(u'app标签',max_length=100, )
    model = models.CharField(u'模型名称',max_length=100, unique=True)
    class Meta:
        db_table='sys_new_nav_list'
        verbose_name = u'后台管理导航排序'
        verbose_name_plural = u'后台管理导航排序'
    def __unicode__(self):
        return self.name

class Crowfunding(models.Model):
    cf_id =  models.AutoField(primary_key=True)
    cf_total = models.IntegerField(blank=True,  )
    cf_price = models.CharField(u'单价',max_length=100,blank=True,   )
    event_id = models.IntegerField( unique=True)
    cf_already = models.IntegerField(blank=True, )
    cf_already_percent = models.FloatField(blank=True,  )
    cf_total_days=models.IntegerField(blank=True )
    class Meta:
        managed = False
        db_table='dahuodong_crowfunding'
        


       
class NewEventPriceCurrency(models.Model):
    name= models.CharField(u'币种',max_length=50,blank=True,unique=True )
    ename= models.CharField(u'币种符号',max_length=10,blank=True,unique=True )
    rate=models.FloatField(u'汇率%',blank=True, null=True )
    sign=models.CharField(u'符号',max_length=50,blank=True, null=True,default=u'￥')
    def __unicode__(self):
        return '%s (%s)' % (self.name,self.rate,)
    class Meta:
        managed = False
        db_table='sys_new_event_price_currency'
        verbose_name = u'币种'
        verbose_name_plural = u'币种'
class NewEventPriceType(models.Model):
    name= models.CharField(u'类型名称',max_length=100,blank=True,unique=True )
    Rule_1=models.CharField(u'规则1',max_length=100,blank=True, null=True)
    Rule_2=models.CharField(u'规则2',max_length=100,blank=True, null=True)
    def __unicode__(self):
        return '%s' % (self.name ,)
    class Meta:
        managed = False
        db_table='sys_new_event_price_type'
        verbose_name = u'销售类型'
        verbose_name_plural = u'销售类型'
    
class NewEventImgServer(models.Model):     
    name=models.CharField(u'服务器地址',max_length=200,blank=True, null=True)
    
        
    def __unicode__(self):
        return self.name 

    class Meta:
        #managed = False
        db_table = 'sys_new_event_img_server'
        verbose_name = u'资源服务器'
        verbose_name_plural = u'资源服务器'
        #app_label = u"活动信息"
class NewEventImg(models.Model):
    
    
    
    name=models.CharField(u'图片名称', max_length=50, blank=True)
    urls = models.CharField(u'图片url', max_length=200, blank=True,null=True,)
    #thumbs = models.ImageField(u'图片缩略图', upload_to = 'thumb', blank=True)
    imgs = models.ImageField(u'图片文件',upload_to = 'temp',blank=True,null=True,) 
    begin_time = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    end_time = models.DateTimeField(auto_now=True ,verbose_name=u'最后编辑时间')
    server=models.ForeignKey(NewEventImgServer,blank=True, null=True,verbose_name=u'服务器地址')
    order=models.IntegerField(u'排序',blank=True,null=True,)
    width=models.IntegerField(u'图片宽度',blank=True,null=True)
    height=models.IntegerField(u'图片高度', blank=True,null=True )
    
     
    def save(self,force_insert=False, force_update=False, using=None,
             update_fields=None):
        #try:
        super(NewEventImg, self).save(force_insert , force_update , using ,
             update_fields )
        
        try:
            if self.imgs:
                import ftplib,time,os
                server1='pic1.qkan.com'
                uid='imga'
                pwd='b@Veryevent'
                s = ftplib.FTP(server1,uid,pwd)
                spot='event'
                try:   
                    s.cwd(spot)   
                except ftplib.error_perm:   
                    s.mkd(spot) 
                #except:
                curTime = time.strftime("%Y-%m-%d", time.localtime(time.time()))
                try:   
                    s.cwd(curTime)   
                except ftplib.error_perm:   
                    s.mkd(curTime)
                    try:                 
                        s.cwd(curTime)  
                    except:
                        pass  
                f = open(self.imgs.path,'rb')   
                #filename=    os.path.basename(self.imgs.path)         # file to send   
                #img_name=self.img_url+"\\"+g.decode('utf-8').replace('/','\\').replace('%20',' ')
                from PIL import Image
                pixbuf = Image.open(self.imgs.path)
                self.width, self.height = pixbuf.size
                
                base, ext = os.path.splitext(os.path.basename(self.imgs.path))
                filename=spot+str(time.time())+ext
                s.storbinary('STOR '+filename, f)   # Send the file   
                f.close()                           # Close file and FTP   
                s.quit()
                self.urls='%s/%s/%s' % (spot,curTime,filename) #os.path.join( spot+'/'+curTime,filename)
                self.server=NewEventImgServer.objects.get(id=1)
                super(NewEventImg, self).save(force_insert , force_update , using ,update_fields )
            
        except:
            pass
    
    
        
        
    def __unicode__(self):
        return "%s%s" % (self.server.name if self.server else 'http://pic1.qkan.com/' ,self.name)
 
    class Meta:
        #managed = False
        db_table = 'sys_new_event_img'
        verbose_name = u'图片'
        verbose_name_plural = u'图片'
        #app_label = u"活动信息"
class NewDistrict_s(models.Model):
    district_id = models.IntegerField(u'旧城市id',primary_key=True)
    id = models.IntegerField(u'id',)
    parent_id= models.IntegerField()
    district_name = models.CharField(u'城市名称',max_length=50, unique=True) 
    event_count=models.IntegerField(u'累计活动',blank=True, null=True)
    def __unicode__(self):
        return self.district_name
    class Meta:
        managed = False
        db_table = 'sys_new_district'
        verbose_name = u'城市'
        verbose_name_plural = u'城市' 
class NewSysEventTag(models.Model):
    tag_id= models.IntegerField(u'id',primary_key=True)
    tag_name=models.CharField(u'标签名称',max_length=50, )
    cat1_id=models.IntegerField()
    class Meta:
        managed = False
        db_table = 'sys_event_tag'

class NewDistrict(MPTTModel):
    district_id = models.IntegerField(u'旧城市id',blank=True,)
    district_name = models.CharField(u'城市名称',max_length=50, unique=True)
    title = models.CharField(u'城市拼音',max_length=30, blank=True,null=True,db_index=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',verbose_name=u'上一级')
    #level = models.IntegerField()
    capital_letter = models.CharField(u'城市首字母',max_length=5, blank=True,null=True)
    usetype = models.IntegerField(blank=True, null=True)
    baidu_code = models.IntegerField(u'百度区域代码',blank=True, null=True)
    displayorder = models.IntegerField(u'排序',blank=True, null=True)
    recomendindex = models.IntegerField(u'建议指数',blank=True, null=True)
    event_count=models.IntegerField(u'累计活动',blank=True, null=True)
    venue_count=models.IntegerField(u'累计场馆',blank=True, null=True)
    img = models.ForeignKey(NewEventImg,blank=True,null=True,verbose_name=u'图片')
    des=models.CharField(u'城市描述',max_length=150, blank=True,null=True)

    class MPTTMeta:
        #parent_attr='upid'
        #level_attr = 'level' 
        order_insertion_by = ['district_name']
    def __unicode__(self):
        return self.district_name
    class Meta:
        #managed = False
        db_table = 'sys_new_district'
        verbose_name = u'城市地区'
        verbose_name_plural = u'城市地区' 
        #app_label = u"活动信息"

class NewVenueClass(models.Model):
    name=models.CharField(u'名称',max_length=50, unique=True)
    venue_count=models.IntegerField(u'累计场馆',blank=True, null=True)
    event_count=models.IntegerField(u'累计活动',blank=True, null=True)
    class Meta:
        #managed = False
        db_table = 'sys_new_venue_class'
        verbose_name = u'地址场馆'
        verbose_name_plural = u'地址场馆' 
 
    def __unicode__(self):
        return self.name 
class NewVenue(models.Model): 
    #district_id = models.IntegerField(u'旧城市id')
    venue_id = models.IntegerField(blank=True, null=True)
    longitude_baidu = models.FloatField(blank=True, null=True)
    latitude_baidu = models.FloatField(blank=True, null=True)
    longitude_google = models.FloatField(blank=True, null=True)
    latitude_google = models.FloatField(blank=True, null=True)  
    city = models.ForeignKey(NewDistrict,verbose_name=u'城市',blank=True,null=True)
    venue_class = models.ForeignKey(NewVenueClass,verbose_name=u'类型',blank=True,null=True)
    address = models.CharField(u'地址',max_length=100 , blank=True, null=True)
    title = models.CharField(u'名称',max_length=300, blank=True, null=True)
    alias = models.CharField(u'别名',max_length=300, blank=True, null=True)
    event_count=models.IntegerField(u'累计活动',blank=True, null=True)
    content=models.TextField(u'内容',blank=True, null=True)
    img = models.ForeignKey(NewEventImg,blank=True,null=True,verbose_name=u'图片')
    class Meta:
        #managed = False
        db_table = 'sys_new_venue'
        verbose_name = u'地址场馆'
        verbose_name_plural = u'地址场馆' 
        #app_label = u"活动信息"

    def __unicode__(self):
             
        return '%s(%s)' % (self.title ,self.address)
    


 
class NewEventTag(models.Model):
    #cat_id = models.AutoField(primary_key=True)
    name = models.CharField(u'名称',max_length=100, blank=True,unique=True)
    hot= models.IntegerField(u'热度', blank=True,null=True)
    def __unicode__(self):
        return self.name

 
    class Meta:
        #managed = False
        db_table = 'sys_new_event_tag'        
        verbose_name = u'标签词库'
        verbose_name_plural = u'标签词库'
        #app_label = u"活动信息"
        
      

''' 
class AuthAdmin(models.Model):
    username = models.CharField(u'用户名',max_length=30, blank=True)
    def __unicode__(self):
        return self.username
    class Meta:
        managed = False
        db_table = 'auth_user'
'''        
class NewEventCatType(models.Model):
    name = models.CharField(u'名称',max_length=100)
    templets = models.CharField(u'模板',max_length=100, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        #managed = False
        db_table = 'sys_new_event_cat_type'
        verbose_name = u'分类类型'
        verbose_name_plural = u'分类类型'

'''    
class Genre(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
         
        order_insertion_by = ['name']
    def __unicode__(self):
        return self.name
'''        
class NewEventSeo(models.Model):   
    name = models.CharField(u'名称',max_length=50,blank=True ,null=True)
    title=models.CharField(max_length=200,blank=True,null=True)
    keywords=models.CharField(max_length=200,blank=True,null=True)#models.ManyToManyField(NewEventTag,blank=True,null=True,verbose_name='标签')
    description=models.CharField(max_length=500,blank=True,null=True)
    def __unicode__(self):
        return '(%s) %s [|] %s' % (self.name,self.title,self.keywords)
    class Meta:
        #managed = False
        #app_label = u'seo_hh' 
        db_table = 'sys_new_event_seo'
        verbose_name = u'SEO管理' 
        verbose_name_plural = u'SEO管理'
        #app_label = u"活动信息"
class NewEventCat_s(models.Model):  
    cat_id = models.IntegerField(u'旧数据id',primary_key=True)   
    id = models.IntegerField(u'id')  
    name = models.CharField(max_length=50,  unique=True  )  
    seo = models.ForeignKey(NewEventSeo,verbose_name=u'seo',blank=True, null=True)
    def __unicode__(self):
        return  self.name    
    class Meta:
        managed = False
        db_table = 'sys_new_event_cat'

class NewEventCat(MPTTModel): 
    st=((1,u'立减'),
              (2,u'折扣'),
              (3,u'限时'),
             )
    name = models.CharField(max_length=50,  unique=True  )
    ename = models.CharField(max_length=10, blank=True,null=True)
    cat_id = models.IntegerField(u'旧数据id', blank=True,null=True)
    tag =  models.ManyToManyField(NewEventTag,blank=True,null=True,verbose_name=u'标签')
    
    parent =TreeForeignKey('self', null=True, blank=True, related_name='children',verbose_name=u'上一级',)# models.ForeignKey('self',verbose_name=u'上一级', null=True, blank=True, related_name='children')
    
    type = models.ForeignKey(NewEventCatType,verbose_name=u'类型',blank=True,null=True)
    
    seo = models.ForeignKey(NewEventSeo,verbose_name=u'seo',blank=True, null=True)
    #path = models.CharField(u'路径', max_length=255, null=True, blank=True, help_text="此项不用填写")
    order = models.IntegerField(u'排序',blank=True,null=True)
    event_count=models.IntegerField(u'活动累计',blank=True,null=True)
    img = models.ForeignKey(NewEventImg,blank=True,null=True,verbose_name=u'图片')
    begin_time = models.DateField( verbose_name=u'开始时间',blank=True,null=True)
    end_time = models.DateField( verbose_name=u'结束时间',blank=True,null=True)
    city = models.ManyToManyField(NewDistrict,blank=True,null=True,verbose_name=u'城市')
    sale=models.IntegerField(u'销售类型',blank=True,null=True,choices=st)
    #txt = models.ManyToManyField(NewDistrict,blank=True,null=True,verbose_name=u'分类文档')
    def __unicode__(self):
        return '__'*self.level+self.name
    class MPTTMeta:
         
        order_insertion_by = ['name']
    
 
    class Meta:
        #managed = False
        db_table = 'sys_new_event_cat'
        verbose_name = u'活动分类' 
        verbose_name_plural = u'活动分类'
        #app_label = u"活动信息"

class NewEventFromType(models.Model):
    name=models.CharField(u'标题',max_length=100, )
    count=models.IntegerField(u'统计',blank=True,null=True)
    def __unicode__(self):
        return '%s' % (self.name,)
    
    class Meta:
        #managed = False
        db_table = 'sys_new_event_from_type'
        verbose_name = u'来源状态' 
        verbose_name_plural = u'来源状态'    
class NewEventFromClass(models.Model):
    name=models.CharField(u'标题',max_length=100, )
    count=models.IntegerField(u'来源累计',blank=True,null=True)
    def __unicode__(self):
        return '%s ' % (self.name,)
    class Meta:
        #managed = False
        db_table = 'sys_new_event_from_class'
        verbose_name = u'来源类型' 
        verbose_name_plural = u'来源类型'   
        #app_label = u"活动信息"            
class NewEventFrom(models.Model):
    f_Class =  models.ForeignKey(NewEventFromClass,verbose_name=u'来源类型' )
    #liaisons= models.CharField(u'联系人',max_length=100,blank=True,null=True, unique=True  )
    Website= models.CharField(u'网址',blank=True,null=True, max_length=500,  )
    email=models.CharField(u'邮箱',blank=True,null=True,max_length=100,   )
    tel=models.CharField(u'电话',max_length=100,blank=True,null=True, )
    #city= models.ManyToManyField(NewDistrict,blank=True,null=True,verbose_name='城市')
    #addr=models.ForeignKey(NewVenue,blank=True,null=True,verbose_name=u'地址')
    content =  models.TextField(u'内容/地址',blank=True)
    type=models.ForeignKey(NewEventFromType,verbose_name=u'来源信息状态',blank=True,null=True,related_name='from_type')
    edit =  models.ForeignKey(User,verbose_name=u'创建编辑',blank=True,null=True,related_name='from_edit')
    last_edit = models.ForeignKey(User,verbose_name=u'最后编辑',blank=True,null=True,related_name='from_last_edit')
    
    
    event_count=models.IntegerField(u'活动累计',blank=True,null=True)
    def __unicode__(self):
        return '%s ' % (self.f_Class,)
    class Meta:
        #managed = False
        db_table = 'sys_new_event_from'
        verbose_name = u'信息来源' 
        verbose_name_plural = u'信息来源'   
        #app_label = u"活动信息"     
class NewEventParagraphTag(models.Model):
    name = models.CharField(u'标签',max_length=50,unique=True, blank=True)
    cat = models.ForeignKey(NewEventCat,blank=True,null=True,verbose_name=u'分类',related_name='pt_tag')
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'sys_new_event_paragraph_tag'
        verbose_name = u'分类标签'
        verbose_name_plural = u'分类标签'

        
class NewEventParagraph(models.Model):
    #id = models.AutoField(u'id',primary_key=True)
    name = models.CharField(u'标题',max_length=100,blank=True )
    txt =  models.TextField(u'内容',blank=True)
    
    tag = models.TextField(u'签名', blank=True)
    cat_name=models.ForeignKey(NewEventParagraphTag,blank=True, null=True,verbose_name=u'分类标签',related_name='Paragraph_tag')
    begin_time = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    end_time = models.DateTimeField(auto_now=True,verbose_name=u'最后编辑时间')
    #txt_hcode = models.ManyToManyField(SysSpotHcode,blank=True,verbose_name='嵌入代码（视频/flash）')
    img = models.ManyToManyField(NewEventImg,blank=True,null=True,verbose_name=u'图片')
    txt_order=models.IntegerField(verbose_name=u'顺序',default=0,blank=True, )
    #spot_info=models.ManyToManyField(SysSpotInfo,blank=True,verbose_name=u'关联在现场报告',through='sys_spot_info_spot_txt')
    def __unicode__(self):
        return '%s %s %s—%s' % (self.id,self.name,self.tag, self.cat_name) 
    
    
    class Meta:
        managed = False
        db_table = 'sys_new_event_paragraph'
        verbose_name = u'文章段落'
        verbose_name_plural = u'文章段落'
        #app_label = u"活动信息"
     
    
    

        #app_label = u"活动信息"
class NewEventPrice(models.Model):
    #name= models.CharField(u'名称',max_length=100,blank=True )
    Currency=models.ForeignKey(NewEventPriceCurrency,blank=True, verbose_name=u'币种',related_name='price_cu')
    Type=models.ForeignKey(NewEventPriceType,blank=True, verbose_name=u'类型',related_name='Price_type')
    #Price = models.ManyToManyField(NewEventPriceUnit,blank=True,verbose_name=u'价格')
    str= models.CharField(u'价格字符串',max_length=100,blank=True )
    min=models.IntegerField(u'最低价格',blank=True)
    max=models.IntegerField(u'最高价格',blank=True)
    points=models.CharField(u'折扣率',max_length=100,blank=True)
    #sale_rate=models.PositiveSmallIntegerField(u'折扣%',blank=True, null=True)
    sale=models.CharField(u'折扣价格字符串',max_length=100,blank=True)
    class Meta:
        #managed = False
        db_table = 'sys_new_event_price'
        #app_label = u"活动信息"
        verbose_name = u'销售管理'
        verbose_name_plural = u'销售管理'
        
    def __unicode__(self):
        return '%s %s %s %s-%s sale:%s' % (self.Type.name,self.Currency.name,self.str,self.min,self.max,self.sale)    
        
  
class NewEventTablePoint(models.Model):
    id= models.IntegerField(u'id',primary_key=True,unique=True)
    name = models.CharField(u'标题',max_length=100, unique=True ) 
    def __unicode__(self):
        return '%s' % (self.name)
    class Meta:
        managed = False
        db_table='sys_new_event_table_point'        
class NewEventTableType(models.Model):
    id= models.IntegerField(u'id',primary_key=True,unique=True)
    name = models.CharField(u'标题',max_length=100, unique=True ) 
    def __unicode__(self):
        return '%s' % (self.name)
    class Meta:
        managed = False
        db_table='sys_new_event_table_type'
        verbose_name = u'活动状态' 
        verbose_name_plural = u'活动状态'        
 
class OldEvent(models.Model):
    st=( (0,u'未处理'),
          (1,u'已发布'),
          (2,u'废弃'),
          (3,u'待完善'),
          (5,u'编辑中'),
          (6,u'过期'),
          (8,u'后备库'),
          )
    event_id = models.AutoField(u'活动id',primary_key=True)
    event_name = models.CharField(u'活动名称',max_length=300, blank=True)
    event_cat_tag = models.CharField(u'活动标签',max_length=150, blank=True)
    event_img = models.CharField(u'活动图片',max_length=100, blank=True)
    event_isshow = models.IntegerField(blank=True, null=True,verbose_name=u'状态',choices=st)#models.ForeignKey(NewEventTableType,verbose_name=u'状态',blank=True,default=True, db_column='event_isshow')
    event_app_name = models.CharField(max_length=300, blank=True)
    district_id = models.IntegerField( default=False,  blank=True)
    province_id = models.IntegerField(blank=True, null=True)
    event_begin_time = models.IntegerField(u'开始时间',blank=True,default=False,)
    event_end_time = models.IntegerField(u'结束时间',blank=True,default=False,)
    event_cat = models.IntegerField(blank=True,default=False,)
    event_cat1 = models.IntegerField(blank=True,default=False,)     
    event_price = models.CharField(u'价格',max_length=300, blank=True)
    event_price_currency = models.IntegerField(blank=True,default=False,)
    event_price_backup = models.CharField(u'价格',max_length=300)
    event_lowprice = models.IntegerField(blank=True, null=True)
    event_highprice = models.IntegerField(blank=True, null=True)
    event_isfree = models.IntegerField(blank=True, null=True)
    event_content = models.TextField(blank=True)
    event_comment = models.CharField(max_length=400, blank=True)
    event_cool = models.IntegerField(blank=True, null=True)
     
    event_img_server = models.IntegerField(blank=True,default=1,)
    venue_id = models.IntegerField( u'地址/场馆',blank=True, default=False,)
    venue_info = models.CharField(u'场馆地址',max_length=200, blank=True)
    event_tag = models.CharField(max_length=150, blank=True)
    
    event_recomend = models.IntegerField(blank=True,default=False,)
    event_point = models.IntegerField(blank=True)
    crawl_url = models.CharField(max_length=700, blank=True)
    crawl_site = models.CharField(u'来源网站',max_length=60, blank=True)
    event_officer = models.CharField(max_length=300, blank=True)
    crawl_title = models.CharField(max_length=300, blank=True)
    event_support = models.CharField(max_length=300, blank=True)
    event_assistant = models.CharField(max_length=300, blank=True)
    event_dep = models.CharField(max_length=300, blank=True)
    event_support_info = models.TextField(u'主办方信息',blank=True)
    event_address = models.CharField(max_length=300, blank=True)
    crawl_time = models.IntegerField(blank=True,default=False,)
    event_order = models.IntegerField(blank=True)
    event_rank = models.IntegerField(blank=True, null=True)
    event_editor = models.CharField(max_length=30, blank=True)
    event_search = models.CharField(max_length=100, blank=True)
    event_random = models.IntegerField(blank=True,default=False,)
    event_like = models.IntegerField(blank=True,default=False,)
    event_longitude_baidu = models.FloatField(blank=True,default=False,)
    event_latitude_baidu = models.FloatField(blank=True,default=False,)
    event_longitude_google = models.FloatField(blank=True,default=False,)
    event_latitude_google = models.FloatField(blank=True,default=False,)
    event_time_expire = models.IntegerField(blank=True,default=False,)
    event_cat_field1 = models.CharField(max_length=100, blank=True)
    event_cat_field2 = models.CharField(max_length=100, blank=True)
    event_cat_field3 = models.CharField(max_length=100, blank=True)
    event_cat_field4 = models.CharField(max_length=100, blank=True)
    event_cat_field5 = models.CharField(max_length=100, blank=True)
    synchronization = models.IntegerField(blank=True)
    event_theme = models.CharField(max_length=100,blank=True)
    event_discount = models.CharField(max_length=100,blank=True)
    event_discount_price = models.CharField(max_length=100,blank=True)
    event_price_model = models.IntegerField(blank=True)
    event_islongtime = models.IntegerField(blank=True)


    #event_cat = models.ForeignKey(SysCat, related_name='event_cat' )
    #event_cat1 = models.ForeignKey(SysCat, related_name='event_cat1' )
     
    
    def __unicode__(self):
        return self.event_name
    class Meta:
        managed = False
        db_table = 'sys_event'
        verbose_name = u'公共活动库' 
        verbose_name_plural = u'公共活动库'
        
        #ordering = ('-event_begin_time',) 
        #app_label='活动家'
        #spotcatUrl()
 

      
class NewEventTable(models.Model):
    ct=(
        (0,u'有效'),
        (1,u'长期'),
        (2,u'无效'),      
      )
    po=(
        (0,u'暂无'),
        (1,u'竞价'),
        (2,u'推广'),      
        (3,u'长期有效'),
      )    
    
    img = models.ManyToManyField(NewEventImg,blank=True,null=True,verbose_name=u'图片')
    cat = models.ManyToManyField(NewEventCat,blank=True,null=True,verbose_name=u'分类')
    tag = models.ManyToManyField(NewEventTag,blank=True,null=True,verbose_name=u'标签')
    city= models.ManyToManyField(NewDistrict,blank=True,null=True,verbose_name=u'城市')
    addr=models.ManyToManyField(NewVenue,blank=True,null=True,verbose_name=u'地址场馆')
        
    relevant=models.ManyToManyField('self',blank=True,null=True,verbose_name=u'相关活动',symmetrical=False)
    from_info=models.ManyToManyField(NewEventFrom,blank=True,null=True,verbose_name=u'来源')   
    paragraph = models.ManyToManyField(NewEventParagraph,blank=True,verbose_name=u'段落')
    
    #app_msg=models.ManyToManyField(UserEventMessage,blank=True,null=True,verbose_name=u'关联留言',through='sys_ac_user_info_event')
    #order=models.ManyToManyField(SysOrder,blank=True,null=True,verbose_name=u'关联订单',)
    #web_msg=models.ManyToManyField(SysOrderMessage,blank=True,null=True,verbose_name=u'关联订单',)
    
    name = models.CharField(u'标题',max_length=100)
    fname = models.CharField(u'app标题',max_length=100,blank=True )
    ename = models.SlugField(u'标题缩写',max_length=10,blank=True,null=True,  )
    content = models.TextField(u'内容简介',blank=True)
    search = models.CharField(u'搜索字段',max_length=200, blank=True,null=True,)
    
    
    
    edit =  models.ForeignKey(User,verbose_name=u'创建编辑',blank=True,null=True,related_name='event_edit')
    last_edit = models.ForeignKey(User,verbose_name=u'最后编辑',blank=True,null=True,related_name='event_last_edit')
    Price = models.OneToOneField(NewEventPrice,verbose_name=u'活动销售',blank=True,null=True,related_name='event_price')
    
    old_event = models.OneToOneField(OldEvent,blank=True,null=True,verbose_name='关联旧数据',related_name='event_old_info')
    seo=models.ForeignKey(NewEventSeo,verbose_name=u'seo',blank=True, null=True)
    #spot = models.ForeignKey(SysSpotInfo,blank=True,null=True,verbose_name=u'在现场')
    
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')    
    rel_time = models.DateTimeField(auto_now=True ,verbose_name=u'最后编辑时间')
    
    begin_time = models.DateTimeField( verbose_name=u'开始时间',blank=True,null=True)
    end_time = models.DateTimeField( verbose_name=u'结束时间',blank=True,null=True)
    
    hot= models.IntegerField(u'热度',blank=True,null=True,default=0)
    order = models.SmallIntegerField(u'排序',blank=True,null=True) 
    isshow = models.ForeignKey(NewEventTableType,verbose_name=u'状态',blank=True,default=5)  
    #point=models.ForeignKey(NewEventTablePoint,verbose_name=u'推广管理',blank=True,default=False) 
    point=models.SmallIntegerField(verbose_name=u'推广管理',db_column='point_id',blank=True,default=0,choices=po,)
    state=models.SmallIntegerField(u'有效状态',blank=True, choices=ct,default=0)
    
    release_time = models.DateTimeField( verbose_name=u'发布时间',blank=True,null=True)
    
    
    def __unicode__(self):
        return '%s %s' % (self.old_event_id,self.name)      
    class Meta:
        managed = False
        db_table = 'sys_new_event_info'
        verbose_name = u'活动管理' 
        verbose_name_plural = u'活动管理'
        #ordering = ["-order"]
        #app_label='活动家'
        #app_label = string_with_title("new_event", u"编辑数据")
    '''     
    def save(self,force_insert=False, force_update=False, using=None,
             update_fields=None):        
        super(NewEventTable, self).save(force_insert , force_update , using ,
             update_fields )
        
        #if self.ename:
            #get_str_event(str
        for ci in self.city.all():
            cat_l=NewCatUrl(0,ci.title)
            for ca in self.cat.all():
                if not cat_l.has_key(cat_l):
                    NewCatUrl(0,ci.title,True)
                     
                event_city_cat(ci.id,ca.id,True)
    '''             
         
 
class NewCatInfo(models.Model):
    id = models.AutoField(u'id',primary_key=True)
    neweventcat=models.ForeignKey(NewEventCat)   
    neweventtable =models.ForeignKey(NewEventTable) 
    class Meta:
        managed = False
        db_table = 'sys_new_event_info_cat'
class NewCityInfo(models.Model):
    id = models.AutoField(u'id',primary_key=True)
    newdistrict=models.ForeignKey(NewDistrict)    
    neweventtable =models.ForeignKey(NewEventTable)
    class Meta:
        managed = False
        db_table = 'sys_new_event_info_city'
class NewEventPriceUnit(models.Model):
    st=( (0,u'无效'),
          (1,u'有效'), 
          )
    st1=( (0,u'标准'),
          (1,u'现场'), 
          (2,u'参展'), 
          )
    #0标准，1现场，2参展
    event=models.ForeignKey(NewEventTable,related_name='Price_event_table',verbose_name=u'关联活动')
    price=models.DecimalField(u'售价',max_digits=10, decimal_places=2)
    sale=models.DecimalField(u'折扣价格 ',max_digits=10, decimal_places=2,blank=True,null=True)
    discount=models.DecimalField(u'折扣率 ',max_digits=7, decimal_places=1,blank=True,null=True)
    original_price=models.DecimalField(u'原价',max_digits=7, decimal_places=2,blank=True,null=True)
    Currency=models.ForeignKey(NewEventPriceCurrency, verbose_name=u'货币单位',default=1)
    begin_time = models.DateTimeField( verbose_name=u'开始时间',blank=True,null=True,default=datetime.datetime.now())
    end_time = models.DateTimeField( verbose_name=u'结束时间',blank=True,null=True,default=datetime.datetime.now())
    stock=models.IntegerField(u'库存',default=100)
    stock_d=models.IntegerField(u'出库等待' ,default=0)
    form_info=models.ForeignKey(NewEventFrom, verbose_name=u'来源',blank=True,null=True)    
    points=models.IntegerField(u'积分',max_length=100,blank=True,null=True)
    status = models.PositiveSmallIntegerField(u'状态',blank=True,null=True,default=1,choices=st )
    type= models.IntegerField(u'状态',blank=True,null=True,default=0,choices=st1 )
    property=models.CharField(u'属性',max_length=45,blank=True,null=True)
    #sale_rate=models.PositiveSmallIntegerField(u'折扣%',blank=True, null=True)
    content=models.CharField(u'价格说明',max_length=255,blank=True,null=True)
    def __unicode__(self):
        return '%s(%s)' % (self.price,self.stock)           
    class Meta:
        #managed = False
        db_table = 'sys_new_event_price_unit'
        verbose_name = u'价格管理' 
        verbose_name_plural = u'价格管理'    

class NewOrder(models.Model):
    
    st=( (0,u'未付款'),
              (10,u'已付订金'),
              (20,u'已付款'),
              (30,u'已退款'),
              )
    
    ct=((0,u'未处理'),
        (10,u'待财务确认'),
        (20,u'正在出库'),
        (30,u'已发货'),
        (50,u'交易完成'),
        (60,u'退货中'),
        (70,u'已退货'),
        (100,u'已取消'),
        (110,u'已作废'),
        )
    pay=(('alipay',u'支付宝'),
         ('bank',u'银行转账'),
         ('weixin',u'微信'),
         
         )
    to=( 
        (0,u'web'),
        (1,u'app'),
        (2,u'Mobile website'),
        (3,u'weixin'),
        (4,u'life app'),
        )
    
    
    order_id = models.AutoField(primary_key=True)
    order_number = models.CharField(u'单号',max_length=20, blank=True)
    order_user_name = models.CharField(u'收货人',max_length=100, blank=True)
    order_tel = models.CharField(u'手机',max_length=100, blank=True)
    order_email = models.CharField(u'邮箱',max_length=100, blank=True)
    order_reg_fields = models.IntegerField()
    order_price = models.DecimalField(u'单价',max_digits=7, decimal_places=2)
    order_totalpay = models.DecimalField(u'订单总额',max_digits=7, decimal_places=2)
    order_amount = models.IntegerField(u'数量')
    order_address = models.CharField(u'地址',max_length=500, blank=True)
    order_payment = models.CharField(u'付款方式',max_length=100, blank=True,choices=pay)
    order_text = models.CharField(u'客户留言',max_length=200, blank=True)
    order_addip = models.CharField(u'客户ip',max_length=20, blank=True)
    order_addtime = models.IntegerField(u'下单时间',blank=True, null=True)
    order_paytime = models.IntegerField(u'交易时间',blank=True, null=True)
    admin_name = models.CharField(u'最后修改',max_length=100, blank=True,null=True)
    admin = models.ForeignKey(User,verbose_name=u'最后修改',blank=True,null=True,related_name='order_edit')
    admin_text = models.TextField(u'管理备注',max_length=200, blank=True,null=True)
    order_telphone = models.CharField(u'固话',max_length=20, blank=True)
    order_pay_status = models.IntegerField(blank=True, null=True,verbose_name=u'支付状态',choices=ct)
    order_status = models.IntegerField(verbose_name=u'订单状态',blank=True, null=True,choices=st)
    event  = models.ForeignKey(NewEventTable,to_field='old_event', verbose_name=u'关联活动',blank=True,related_name='order_event')
    event_name = models.CharField(u'活动名称',max_length=200, blank=True)
    city_title = models.CharField(u'活动城市',max_length=10, blank=True)
    order_userid = models.IntegerField()
    order_pay_info = models.CharField(max_length=200, blank=True)
    event_to = models.IntegerField(u'来源', blank=True, null=True,choices=to)
    addtime=  models.DateTimeField(auto_now_add=True,verbose_name=u'留言时间',blank=True, null=True)
    #order_addip = models.IPAddressField( blank=True)
    def __unicode__(self):
        return '%s —— %s' % (self.order_id,self.order_number)   
    class Meta:
        managed = False
        db_table = 'sys_order'
        verbose_name = u'订单' 
        verbose_name_plural = u'订单'
        #app_label='运营中心'


class NewOrderMessage(models.Model):
    msg_id = models.AutoField(primary_key=True)
    event_id = models.IntegerField(u'活动ID',blank=True)
    event_name = models.CharField(u'活动名称', max_length=300, blank=True)
    msg_name = models.CharField(u'留言姓名',max_length=50, blank=True)
    msg_email = models.CharField(u'Email',max_length=100, blank=True)
    msg_tel = models.CharField(u'手机',max_length=100, blank=True)
    msg_content = models.CharField(u'留言信息',max_length=500, blank=True)
    msg_addtime = models.IntegerField(u'时间')
    msg_addip = models.IPAddressField(u'留言IP',  blank=True)
    type=models.IntegerField(default=0)
    event_to = models.IntegerField(u'来源标识', blank=True, null=True)
    addtime=  models.DateTimeField(auto_now_add=True,verbose_name=u'留言时间',blank=True, null=True)
    def __unicode__(self):
        return '%s —— %s' % (self.msg_id,self.msg_content)   
    class Meta:
        managed = False
        db_table = 'sys_order_message'
        verbose_name = u'留言' 
        verbose_name_plural = u'留言'
        #app_label='运营中心'
        
'''         
class NewCrowfunding(models.Model):
    cf_id =  models.IntegerField(primary_key=True)
    cf_total = models.IntegerField()
    cf_price = models.IntegerField()
    event_id = models.ForeignKey(NewEventTable,verbose_name=u'关联活动',blank=True,related_name='cf_event')
    cf_already = models.IntegerField()
    cf_already_percent = models.FloatField()
    def __unicode__(self):
        return '%s ' % (self.cf_id )   
    class Meta:
        managed = False
        db_table = 'sys_new_Crowfunding'


def inital_category_path(sender, instance,** kwargs):

    if instance.id:

        if instance.parent:

            instance.path = '%s:%s' % (instance.parent.path, instance.id)

        else:

            instance.path = instance.id

pre_save.connect(inital_category_path, sender=Category)
'''
        
class AdminEventTheme(models.Model):
    id = models.IntegerField(primary_key=True)
    theme_name = models.CharField(max_length=100,unique=True)
    num = models.IntegerField(blank=True,  )
    event_set = models.CharField(max_length=300,blank=True,  )
    cities = models.CharField(max_length=300,blank=True,  )
    begin_time = models.IntegerField(blank=True, )
    end_time = models.IntegerField(blank=True,  )
    picture_web = models.CharField(max_length=100,blank=True, )
    show_pic = models.IntegerField(blank=True,  )
    picture_server = models.IntegerField(blank=True,  )
    theme_order = models.IntegerField(blank=True,  )
    class Meta:
        managed = False
        db_table = 'sys_event_theme'
        
class NewArticle(models.Model):
    name=models.CharField(u'标题',max_length=100)
    cat= models.ForeignKey(NewEventCat,blank=True,null=True,verbose_name=u'分类',related_name='ar_tag')
    city=models.ForeignKey(NewDistrict,blank=True,null=True,verbose_name=u'城市',related_name='ar_city')
    content=models.TextField(u'内容')
    begin_time = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    end_time = models.DateTimeField(auto_now=True,verbose_name=u'最后编辑时间')
    img = models.ManyToManyField(NewEventImg,blank=True,null=True,verbose_name=u'图片')
    edit =  models.ForeignKey(User,verbose_name=u'创建编辑',blank=True,null=True,related_name='ar_edit')
    last_edit = models.ForeignKey(User,verbose_name=u'最后编辑',blank=True,null=True,related_name='ar_last_edit')
    def __unicode__(self):
        return '%s' % (self.name) 
    
    
    class Meta:
        #managed = False
        db_table = 'sys_new_article'
        verbose_name = u'网站文章'
        verbose_name_plural = u'网站文章'
        

class singers(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'hot_singers'
        
        
class admin_user(models.Model):
    uid=models.AutoField(primary_key=True)
    u_name=models.CharField(max_length=200)
    
    class Meta:
        managed = False
        db_table = 'sys_admin_user'

class VisitRecord(models.Model):
    event = models.OneToOneField(OldEvent,related_name='event_visit_record',verbose_name=u'关联活动')
    count = models.IntegerField(default=0)
    collection = models.IntegerField(default=0)
    
    class Meta:
        managed = False
        db_table = 'visit_record'

class PostEvent(models.Model):
    to=( 
        (0,u'等待'),
        (1,u'沟通中'),
        (2,u'发布'),
        (3,u'无效'),
        )
    #event_id = models.IntegerField(default=0)
    host_tel=models.CharField(u'电话',max_length=30, blank=True)
    host_mail = models.CharField(u'邮箱',max_length=30, blank=True)
    event_url = models.CharField(u'url',max_length=255, blank=True)
    event_file_path = models.FileField(u'文档路径',max_length=200, upload_to = '/data/user_attach/',blank=True)
    event_priority = models.IntegerField(u'关系',blank=True,choices=to,default=0)
    host_ip = models.CharField(u'ip',max_length=15,blank=True)
    post_time = models.DateTimeField(u'发布时间',auto_now_add=True,)
    last_time = models.DateTimeField(auto_now=True ,verbose_name=u'最后编辑时间')
    qq = models.BigIntegerField(blank=True,)
    begin_time = models.DateTimeField(u'活动开始时间',blank=True,)
    end_time = models.DateTimeField(u'活动结束时间',blank=True,)
    host_name = models.CharField(u'主办方名称',max_length=90,blank=True,)
    title = models.CharField(u'活动名称',max_length=90,blank=True,)
    event=models.ForeignKey(NewEventTable,verbose_name=u'关联活动',related_name='event_Post',blank=True)
    class Meta:
        managed = False
        db_table = 'sys_host_event'
        
class feelType(models.Model):   
    name=models.CharField(max_length=30)
    class Meta:
        db_table='sys_new_feeltype'
    def __unicode__(self):
        return '%s' % (self.name) 
  
class feelnum(models.Model):
  
    event=models.OneToOneField(NewEventTable,verbose_name=u'关联活动',related_name='event_feelnum',)
    title=models.CharField(u'title',max_length=255,blank=True,null=True)
    feel=models.ForeignKey(feelType,verbose_name=u'名称')
    feelnum=models.IntegerField(u'排序',blank=True,null=True)
    showtime=models.DateField(u'展示时间',blank=True,null=True)
    content=models.TextField(u'内容介绍',blank=True,null=True)
    people=models.IntegerField(u'参与最少人数',blank=True,null=True)
    max_people=models.IntegerField(u'参与最多人数',blank=True,null=True)
    class Meta:
        db_table='sys_new_feelnum'

class RefundRecord(models.Model):
    r_type = (
        (0, u'部分退款'),
        (1, u'全额退款'),
        (2, u'其他'),
    )
    s_state = (
        (0, u'等待确认'),
        (1, u'审核'),
        (2, u'退款成功'),
        (3, u'无效'),
    )
    r_method = (
        (0, u'未定'),
        (1, u'支付宝'),
    )

    order = models.ForeignKey(NewOrder, verbose_name = u'原订单')
    refund_method = models.IntegerField(u'退款途径', choices=r_method, default=1)
    alipay_trade_no = models.CharField(u'支付宝订单号', max_length=80, blank=True, null=True)
    refund_fee = models.FloatField(u'退款金额')
    refund_reason = models.CharField(u'退款理由', max_length=200)

    refund_id = models.CharField(u'退款记录编号', max_length=80, blank=True, null=True)
    refund_date = models.DateField(u'退款时间', blank=True, null=True)
    refund_url = models.TextField(u'退款链接', blank=True, null=True)

    refund_type = models.IntegerField(u'退款类型', choices=r_type, default=0)
    refund_state = models.IntegerField(u'退款记录状态', choices=s_state, default=0)

    record_date = models.DateField(u'退款记录时间', blank=True, null=True, default=datetime.date.today())
    edit =  models.ForeignKey(User,verbose_name=u'创建编辑', blank=True, null=True, related_name='refund_record_edit')
    last_edit = models.ForeignKey(User,verbose_name=u'最后编辑', blank=True, null=True, related_name='refund_record_last_edit')

    def __unicode__(self):
        return '%s ' % (self.alipay_trade_no,)

    class Meta:
        db_table = 'sys_order_refund'
        verbose_name = u'退款记录'
        verbose_name_plural = u'退款记录'
