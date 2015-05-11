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
from django.core.cache import cache
import os
 

import ftplib,time 
from PIL import Image
#from BeautifulSoup import BeautifulSoup
from django.db import models
#from common import spotcatUrl


class SysSpotfile(models.Model):
    
    
    
    name=models.CharField(u'文件名称', max_length=50, blank=True)
    urls = models.CharField(u'文件url', max_length=200, blank=True)
    #thumbs = models.ImageField(u'图片缩略图', upload_to = 'thumb', blank=True)
    file = models.FileField(u'文件',upload_to = 'temp',blank=True) 
    begin_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    end_time = models.DateTimeField(auto_now=True ,verbose_name='最后编辑时间')
    
    '''
    def make_thumb(self,path, size = 200):
        pixbuf = Image.open(path)
        width, height = pixbuf.size
    
        if height > size:
            delta = height / size
            width = int(width / delta)
            pixbuf.thumbnail((size, width), Image.ANTIALIAS)
    
        return pixbuf
    
    def save(self):
        super(SysSpotImg, self).save() #将上传的图片先保存一下，否则报错
        base, ext = os.path.splitext(os.path.basename(self.imgs.path))
        thumbs_pixbuf = self.make_thumb(os.path.join(MEDIA_ROOT, self.imgs.name))
        relate_thumb_path = os.path.join( 'thumb/', base + '.thumb' + ext)
        thumb_path = os.path.join(MEDIA_ROOT , relate_thumb_path)
        thumbs_pixbuf.save(thumb_path)
        self.thumbs = ImageFieldFile(self, self.thumbs, relate_thumb_path)
        self.urls=os.path.join('/site_media/',relate_thumb_path)
        super(SysSpotImg, self).save() #再保存一下，包括缩略图等
    '''
    def save(self):
        #try:
        super(SysSpotfile, self).save()   
        try:
            
            server='pic1.qkan.com'
            uid='imga'
            pwd='b@Veryevent'
            s = ftplib.FTP(server,uid,pwd)
            spot='spotfile'
            try:   
                s.cwd(spot)   
            except ftplib.error_perm:   
                s.mkd(spot)   
            #except:
            curTime = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            curTime=str(curTime)
            try:   
                s.cwd(curTime)   
            except ftplib.error_perm:   
                s.mkd(curTime)  
                
            f = open(self.file.path,'rb')   
            #filename=    os.path.basename(self.imgs.path)         # file to send   
            base, ext = os.path.splitext(os.path.basename(self.file.path))
            filename=spot+str(int(time.time()))+ext
            s.storbinary('STOR '+filename, f)   # Send the file   
            f.close()                          # Close file and FTP   
            s.quit()
            self.urls=os.path.join('http://'+server+'/'+spot+'/'+curTime,filename)
            self.urls=self.urls.replace('\\', '/')
            super(SysSpotfile, self).save() 
        except:
            False
            
        
        
        
    def __unicode__(self):
        return self.name 
 
    class Meta:
        #managed = False
        db_table = 'sys_spot_file'
        verbose_name = u'文档'
        verbose_name_plural = u'文档'





 
        
         

class SysSpotTag(models.Model):
    name = models.CharField(u'标签',max_length=50, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        #managed = False
        db_table = 'sys_spot_tag'
        verbose_name = u'分类标签'
        verbose_name_plural = u'分类标签'


 

class SysSpotImg(models.Model):
    
    
    
    name=models.CharField(u'图片名称', max_length=50, blank=True)
    urls = models.CharField(u'图片url', max_length=200, blank=True)
    #thumbs = models.ImageField(u'图片缩略图', upload_to = 'thumb', blank=True)
    imgs = models.ImageField(u'图片文件',upload_to = 'temp',blank=True) 
    begin_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    end_time = models.DateTimeField(auto_now=True ,verbose_name='最后编辑时间')
    cat_name=models.ForeignKey(SysSpotTag,blank=True, null=True,verbose_name='分类标签')
    '''
    def make_thumb(self,path, size = 200):
        pixbuf = Image.open(path)
        width, height = pixbuf.size
    
        if height > size:
            delta = height / size
            width = int(width / delta)
            pixbuf.thumbnail((size, width), Image.ANTIALIAS)
    
        return pixbuf
    
    def save(self):
        super(SysSpotImg, self).save() #将上传的图片先保存一下，否则报错
        base, ext = os.path.splitext(os.path.basename(self.imgs.path))
        thumbs_pixbuf = self.make_thumb(os.path.join(MEDIA_ROOT, self.imgs.name))
        relate_thumb_path = os.path.join( 'thumb/', base + '.thumb' + ext)
        thumb_path = os.path.join(MEDIA_ROOT , relate_thumb_path)
        thumbs_pixbuf.save(thumb_path)
        self.thumbs = ImageFieldFile(self, self.thumbs, relate_thumb_path)
        self.urls=os.path.join('/site_media/',relate_thumb_path)
        super(SysSpotImg, self).save() #再保存一下，包括缩略图等
    '''
    def save(self):
        #try:
        super(SysSpotImg, self).save()   
        try:
            
            server='pic1.qkan.com'
            uid='imga'
            pwd='b@Veryevent'
            s = ftplib.FTP(server,uid,pwd)
            spot='spot'
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
                
            f = open(self.imgs.path,'rb')   
            #filename=    os.path.basename(self.imgs.path)         # file to send   
            base, ext = os.path.splitext(os.path.basename(self.imgs.path))
            filename=spot+str(int(time.time()))+ext
            s.storbinary('STOR '+filename, f)   # Send the file   
            f.close()                          # Close file and FTP   
            s.quit()
            self.urls=os.path.join('http://'+server+'/'+spot+'/'+curTime,filename)
            super(SysSpotImg, self).save() 
        except:
            False
            
        
        
        
    def __unicode__(self):
        return self.name 
 
    class Meta:
        #managed = False
        db_table = 'sys_spot_img'
        verbose_name = u'图片'
        verbose_name_plural = u'图片'

class SysSpotHcode(models.Model):
    name=models.CharField(u'视频名称',max_length=50, blank=True)
    hcode = models.TextField(u'视频代码',blank=True)
    cat_name=models.ForeignKey(SysSpotTag,blank=True, null=True,verbose_name='分类标签')
    begin_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    end_time = models.DateTimeField(auto_now=True,verbose_name='最后编辑时间')
    def __unicode__(self):
        return self.name
 
    class Meta:
        #managed = False
        db_table = 'sys_spot_hcode'
        verbose_name = u'多媒体代码'
        verbose_name_plural = u'多媒体代码'

 
        
class SysSpotTxt(models.Model):
    id = models.AutoField(u'id',primary_key=True)
    name = models.CharField(u'标题',max_length=100,blank=True )
    txt =  models.TextField(u'内容',blank=True)
    tag = models.CharField(u'签名',max_length=100, blank=True)
    cat_name=models.ForeignKey(SysSpotTag,blank=True, null=True,verbose_name='分类标签')
    begin_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    end_time = models.DateTimeField(auto_now=True,verbose_name='最后编辑时间')
    txt_hcode = models.ManyToManyField(SysSpotHcode,blank=True,verbose_name='嵌入代码（视频/flash）')
    txt_img = models.ManyToManyField(SysSpotImg,blank=True,verbose_name='图片')
    txt_order=models.IntegerField(verbose_name='顺序',default=0,blank=True, )
    #spot_info=models.ManyToManyField(SysSpotInfo,blank=True,verbose_name=u'关联在现场报告',through='sys_spot_info_spot_txt')
    def __unicode__(self):
        return '%s—%s' % (self.id,  self.cat_name)  
    class Meta:
        #managed = False
        db_table = 'sys_spot_txt'
        verbose_name = u'段落'
        verbose_name_plural = u'段落'
        ordering = ('-txt_order',) 
class SysCat(models.Model):
    cat_id = models.AutoField(u'分类id',primary_key=True)
    cat_name = models.CharField(u'分类名称',max_length=300, blank=True)
    cat_ename = models.CharField(u'分类标记',max_length=300, blank=True)
    cat_fid= models.IntegerField(u'fid')
    def __unicode__(self):
        return self.cat_name
    class Meta:
        managed = False
        db_table = 'sys_event_cat'
                
class SysSpotEvent(models.Model):
    event_id = models.AutoField(u'活动id',primary_key=True)
    event_name = models.CharField(u'活动名称',max_length=300, blank=True)
    event_cat_tag = models.CharField(u'活动标签',max_length=150, blank=True)
    event_img = models.CharField(u'活动图片',max_length=100, blank=True)
    event_isshow = models.IntegerField()
    event_end_time=models.IntegerField()
    event_begin_time=models.IntegerField()
    event_time_expire = models.IntegerField()
    #event_cat = models.ForeignKey(SysCat, related_name='event_cat' )
    #event_cat1 = models.ForeignKey(SysCat, related_name='event_cat1' )
    
    
    def __unicode__(self):
        return self.event_name
    class Meta:
        managed = False
        db_table = 'sys_event'
        #ordering = ('-event_begin_time',) 

        #spotcatUrl()
           

        

        
class SysCity(models.Model):
    district_id = models.AutoField(u'城市id',primary_key=True)
    district_name = models.CharField(u'城市名称',max_length=300, blank=True)
    title = models.CharField(u'城市拼音',max_length=30, blank=True)
    def __unicode__(self):
        return self.district_name
    class Meta:
        managed = False
        db_table = 'sys_common_district'

class SysSpotInfo(models.Model):
    #id = models.AutoField(primary_key=True)
    spot_txt = models.ManyToManyField(SysSpotTxt,blank=True,verbose_name='段落')
    spot_hcode = models.ManyToManyField(SysSpotHcode,blank=True,verbose_name='嵌入代码（视频/flash）')
    spot_img = models.ManyToManyField(SysSpotImg,blank=True,verbose_name='图片')
    
    spot_event = models.ManyToManyField(SysSpotEvent,blank=True,verbose_name='关联活动')
    spot_cat = models.ManyToManyField(SysCat,blank=True,verbose_name='关联分类')    
    spot_city=  models.ManyToManyField(SysCity,blank=True,verbose_name='关联城市')
    
    spot_file = models.ForeignKey(SysSpotfile,blank=True,null=True,verbose_name='文件')
    spot_name = models.CharField(u'标题',max_length=100, )
    spot_addr = models.CharField(u'副标题',max_length=200,blank=True)    
    spot_begin_time = models.DateTimeField( verbose_name="开始时间")
    spot_end_time = models.DateTimeField( verbose_name='结束时间')
    spot_isshow = models.BooleanField(u'显示/隐藏',blank=True,default=True)  
    #spot_edit = models.ForeignKey(AuthAdmin,verbose_name='创建',blank=True)
    spot_last_edit = models.CharField(u'最后编辑',max_length=200,blank=True)
    spot_edit =  models.CharField(u'创建',max_length=200,blank=False)
    spot_desc = models.TextField(u'描述')
    #spot_order=models.IntegerField(verbose_name='顺序')
    
 

 
        
    def __unicode__(self):
        return self.spot_name#'<a href="/spot/%s">%s</a>' % (self.id,self.spot_name)
    class Meta:
        #managed = False
        db_table = 'sys_spot_info'
        verbose_name = u'在现场报告' 
        verbose_name_plural = u'在现场报告'
    def save(self):
        #try:
        super(SysSpotInfo, self).save()
        cache.delete('cat_spot_map')
        
 
        
class SysSpotCatInfo(models.Model):
    id = models.AutoField(u'id',primary_key=True)
    syscat=models.ForeignKey(SysCat)
    
    
    
    class Meta:
        managed = False
        db_table = 'sys_spot_info_spot_cat'

    
            

