#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
import datetime
import ftplib,time,os
class app_table(models.Model):   
    ct=(
        (0,u'有效'),
        (1,u'无效'),      
      )
    po=(
        (0,u'html5'),
        (1,u'ios'),
        (2,u'android'),      
      ) 
    cat_t=(
           (0,u'生活服务'),
           (0,u'游戏'),
           )
    st1=((0,u'不强制'),
        (1,u'强制'),
          )
    name = models.CharField(u'名称',max_length=30,unique=True)
    icon = models.FileField(u'图标',upload_to = 'app_file',blank=True) 
    icon2 = models.URLField(u'图标2',blank=True) 
    
    file = models.FileField(u'文件',upload_to = 'app_file',blank=True) 
    link=models.URLField(u'更新地址',blank=True)
    
    content=models.CharField(u'简介',max_length=255,blank=True)
    hot=models.IntegerField(u'下载量',blank=True,default=0)
    order=models.IntegerField(u'排序',blank=True,default=0)
    version=models.CharField(u'版本号',max_length=32,blank=True)
    
    company=models.CharField(u'公司名称',max_length=255,blank=True)
    website=models.URLField(u'网站',blank=True)
    phone  =models.CharField(u'电话',max_length=50,blank=True)
    email=models.EmailField(u'邮箱',blank=True)
    
    
    rel_time=models.DateTimeField(u'发布时间',default=datetime.datetime.now())
    create_time=models.DateTimeField(u'创建时间',auto_now_add=True)
    last_time=models.DateTimeField(u'最后时间',auto_now=True)    
    edit =  models.ForeignKey(User,verbose_name=u'创建编辑',blank=True,null=True, related_name='app_table_edit')
    last_edit = models.ForeignKey(User,verbose_name=u'最后编辑',blank=True,null=True, related_name='app_table_last_edit')
    app_class=models.SmallIntegerField(u'app平台',blank=True, choices=po,default=0)
    state=models.SmallIntegerField(u'有效状态',blank=True, choices=ct,default=0)
    cat=models.SmallIntegerField(u'类别',blank=True,choices=cat_t,default=0)
    must_update = models.IntegerField(u'强制更新',default=0,choices=st1)
    md5=models.CharField(u'客户端验证信息',max_length=32,blank=True)
    update_text=models.CharField(u'更新信息',max_length=255,blank=True)
    class Meta:
        db_table = 'app_manage_table'
        verbose_name = u'app应用管理' 
        verbose_name_plural = u'app应用管理'
    def __unicode__(self):
        return self.name 
    '''    
    def save(self,force_insert=False, force_update=False, using=None,
             update_fields=None):

        #try:
        super(app_table, self).save(force_insert , force_update , using ,
             update_fields )
        
        if self.file:
            try:
                    
                server='pic1.qkan.com'
                uid='imga'
                pwd='b@Veryevent'
                s = ftplib.FTP(server,uid,pwd)
                app='app_file'
                try:   
                    s.cwd(app)   
                except ftplib.error_perm:   
                    s.mkd(app)   
                #except:
                curTime = time.strftime("%Y-%m-%d", time.localtime(time.time()))
                curTime=str(curTime)
                try:   
                    s.cwd(curTime)   
                except ftplib.error_perm:   
                    s.mkd(curTime)  
                    try:
                        s.cwd(curTime)
                    except:
                        pass
                    
                f = open(self.file.path,'rb')   
                #filename=    os.path.basename(self.imgs.path)         # file to send   
                #base, ext = os.path.splitext(os.path.basename(self.file.path))
                base, ext = os.path.splitext(os.path.basename(self.file.path))
                filename=app+str(int(time.time()))+ext
                s.storbinary('STOR '+filename, f)   # Send the file   
                f.close()                          # Close file and FTP   
                s.quit()
                #self.urls='%s/%s/%s' % (spot,curTime,filename)
                self.link=os.path.join('http://'+server+'/'+app+'/'+curTime,filename)
                self.link=self.link.replace('\\', '/')
                super(app_table, self).save(force_insert , force_update , using ,update_fields ) 

            except:
                pass
    '''