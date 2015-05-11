__author__ = 'alexander'
import os
import sys

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

import ConfigParser
import string

from django.conf import settings 

_HERE = os.path.dirname(os.path.abspath(__file__))

define("port", default=8888, help="run on the given port", type=int)

sys.path.append(_HERE)
sys.path.append(os.path.join(_HERE, '..'))
sys.path.append(os.path.join(_HERE, '../contrib'))
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"


def simple_app(environ, start_response):
    status = "200 OK"
    response_headers = [("Content-type", "text/plain")]
    start_response(status, response_headers)
    return ["Hello world!\n"]




class BaseHandler(tornado.web.FallbackHandler):

    '''
    def initialize(self, fallback):
        self.fallback = fallback
    '''
    def prepare(self):
        
        super(BaseHandler, self).prepare()    
        

        
class WSGIContainer_self(tornado.wsgi.WSGIContainer):
    cf = ConfigParser.ConfigParser()

    def __call__(self, request):
        get_uri= request.uri
        
        ver=''
        
        pos=get_uri.find('version=',2)
        if pos>0:
            pos+=8
        
            pos_end=get_uri.find('&',pos)
            
            ver=get_uri[pos:pos_end] if pos_end>0 else get_uri[pos:]
            if ver:
                settings.ROOT_URLCONF = ''
                settings.INSTALLED_APPS=(
                         'app_manage',
                         )
                try:
                    ver=  '_'+'_'.join(ver.split('.')[:2])
                except:
                    ver=''
                    
                
                
            else:
                pass
                settings.ROOT_URLCONF = 'LifeExpert.urls'
        
        ver="conf/ver%s.conf" % ver
        try:
            self.cf.read(ver)
            
            for k,v in self.cf.items("settings"):

                exec('settings.%s=%s' % (string.upper(k),v))
            #print settings.INSTALLED_APPS
            
        except Exception,e:
            print e
        
        print settings.INSTALLED_APPS
        
        
        
        super(WSGIContainer_self, self).__call__(request)
        #os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
        
        

        
class Application(tornado.web.Application):
    def __call__(self, request):
        # Legacy HTTPServer interface
 
        #return super(Application, self).__call__(request)
        
        dispatcher = tornado.web._RequestDispatcher(self, None)
        dispatcher.set_request(request)
        print request.uri
        return dispatcher.execute()
    def __init__(self):
        
        wsgi_app = tornado.wsgi.WSGIContainer(
                django.core.handlers.wsgi.WSGIHandler())
        wsgi_app_test = WSGIContainer_self(django.core.handlers.wsgi.WSGIHandler())
        handlers = [
            
            #(r"/test/.*", BaseHandler,dict(fallback=wsgi_app)),
            ('.*', BaseHandler, dict(fallback=wsgi_app_test)),
            #('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ]
        tornado.web.Application.__init__(self, handlers)
        
    
    pass
def main(port):
    '''
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        [('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    '''
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    try:
        main(int(sys.argv[1]))
    except:
        main(options.port)