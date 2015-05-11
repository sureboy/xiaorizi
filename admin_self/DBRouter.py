#coding:utf-8
class  Router(object):

    

    def db_for_read(self, model, **hints):

        return 'slave'

 

    def db_for_write(self, model, **hints):

        return 'default'

 

    def allow_relation(self, obj1, obj2, **hints):

        return None

 

    def allow_syncdb(self, db, model):

        return None