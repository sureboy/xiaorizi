#coding:utf-8
class  Router(object):

    

    def db_for_read(self, model, **hints):
        #if model._meta.app_label == 'user_center':
            #return 'user_center_r'

        return 'slave'

 

    def db_for_write(self, model, **hints):
        #if model._meta.app_label == 'user_center':
            #return 'user_center_w'
        return 'default'

 

    def allow_relation(self, obj1, obj2, **hints):

        return None

 

    def allow_syncdb(self, db, model):

        return None