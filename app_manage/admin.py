#coding:utf-8
from django.contrib import admin
from app_manage.models import app_table
from app_manage.common import get_app_list
class AppTableAdmin(admin.ModelAdmin):
    def icon_show(self,obj):
        if obj.icon:
            return '<img width=50 src="/site_media/%s"></img>' % obj.icon
        else:
            return ''
    icon_show.short_description=u'图标'
    icon_show.allow_tags = True
        
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'edit', None) is None:
            obj.edit = request.user
        obj.last_edit = request.user
        obj.save()
        if not obj.icon2:
            try:
                import ftplib,time,os
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
                    
                f = open(obj.icon.path,'rb')   
                #filename=    os.path.basename(self.imgs.path)         # file to send   
                #base, ext = os.path.splitext(os.path.basename(self.file.path))
                base, ext = os.path.splitext(os.path.basename(obj.icon.path))
                filename=app+str(int(time.time()))+ext
                s.storbinary('STOR '+filename, f)   # Send the file   
                f.close()                          # Close file and FTP   
                s.quit()
                #self.urls='%s/%s/%s' % (spot,curTime,filename)
                obj.icon2=os.path.join('http://'+server+'/'+app+'/'+curTime,filename)
                obj.icon2=obj.icon2.replace('\\', '/')
                obj.save()
            except:
                pass 
        
        
        if not obj.link:
            try:
                import ftplib,time,os
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
                    
                f = open(obj.file.path,'rb')   
                #filename=    os.path.basename(self.imgs.path)         # file to send   
                #base, ext = os.path.splitext(os.path.basename(self.file.path))
                base, ext = os.path.splitext(os.path.basename(obj.file.path))
                filename=app+str(int(time.time()))+ext
                s.storbinary('STOR '+filename, f)   # Send the file   
                f.close()                          # Close file and FTP   
                s.quit()
                #self.urls='%s/%s/%s' % (spot,curTime,filename)
                obj.link=os.path.join('http://'+server+'/'+app+'/'+curTime,filename)
                obj.link=obj.link.replace('\\', '/')
                obj.save()
            except:
                pass        
        get_app_list(obj.app_class,True)



    list_editable=['order','rel_time','state','app_class','must_update','version']
    list_display=['name','icon_show','version','must_update','order','rel_time','state','app_class','cat']
    fields=['name','icon','icon2','file','link','content','state','app_class','version','cat','company','website','phone','email','must_update','hot']


admin.site.register(app_table, AppTableAdmin)