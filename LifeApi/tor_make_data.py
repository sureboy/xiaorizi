#coding:utf-8
import torndb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import sys

define("mysql_host", default="221.236.172.241:3306", help="database host")
define("mysql_database", default="vevent", help="database name")
define("mysql_user", default="vevent", help="database user")
define("mysql_password", default="DFG^&*()sdhf@#nhD", help="database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/homeapi", HomeHandler),
            

        ]
        settings = dict(
            api_title=u"Tornado Test",
            #template_path=os.path.join(os.path.dirname(__file__), "templates"),
            #static_path=os.path.join(os.path.dirname(__file__), "static"),
            #ui_modules={"Entry": EntryModule},
            #xsrf_cookies=True,
            #cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            #login_url="/auth/login",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

class EntryModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)
class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    

class HomeHandler(BaseHandler):
    def get(self):
        p={}
        p['code']=1
        p['msg']='Request is successful'
        p['category']=[]
        '''
        p['category']=self.db.query("SELECT sys_new_event_cat.id, "
            "(select group_concat(sys_new_event_tag.name)"
            " from sys_new_event_tag INNER JOIN `sys_new_event_cat_tag` ON "
            "(`sys_new_event_tag`.`id` = `sys_new_event_cat_tag`.`neweventtag_id`)"
            " WHERE `sys_new_event_cat_tag`.`neweventcat_id` = sys_new_event_cat.id "
            " ORDER BY sys_new_event_tag.hot,sys_new_event_tag.id) as tag ,sys_new_event_cat.name, "
            " CONCAT(`sys_new_event_img_server`.`name` , `sys_new_event_img`.`urls` ) AS img, "
            " `sys_new_event_img`.`width`, `sys_new_event_img`.`height` FROM sys_new_event_cat "
            " INNER JOIN `sys_new_event_img` ON `sys_new_event_cat`.`img_id`=`sys_new_event_img`.`id` "
            " INNER JOIN `sys_new_event_img_server` ON `sys_new_event_img_server`.`id` = `sys_new_event_img`.`server_id` "
            " WHERE sys_new_event_cat.type_id=3 ORDER BY sys_new_event_cat.order  desc"
                ) 
        '''
        p['theme']=[]
        
        cat=self.db.query("SELECT sys_new_event_cat.id, sys_new_event_cat.type_id, "
            "(select group_concat(sys_new_event_tag.name)"
            " from sys_new_event_tag INNER JOIN `sys_new_event_cat_tag` ON "
            "(`sys_new_event_tag`.`id` = `sys_new_event_cat_tag`.`neweventtag_id`)"
            " WHERE `sys_new_event_cat_tag`.`neweventcat_id` = sys_new_event_cat.id "
            " ORDER BY sys_new_event_tag.hot,sys_new_event_tag.id) as des ,sys_new_event_cat.name as title, "
            " CONCAT(`sys_new_event_img_server`.`name` , `sys_new_event_img`.`urls` ) AS img, "
            " `sys_new_event_img`.`width`, `sys_new_event_img`.`height`,sys_new_event_cat.order as `hot` , "
            " sys_new_event_cat.sale as `type` FROM sys_new_event_cat "
            " INNER JOIN `sys_new_event_img` ON `sys_new_event_cat`.`img_id`=`sys_new_event_img`.`id` "
            " INNER JOIN `sys_new_event_img_server` ON `sys_new_event_img_server`.`id` = `sys_new_event_img`.`server_id` "
            " WHERE sys_new_event_cat.type_id in (3,4) ORDER BY sys_new_event_cat.order  desc"
            )
        for ca in cat:
            if ca['type_id'] == 3:
                p['category'].append({'id':ca['id'],
                                      'tag':ca['des'],
                                      'name':ca['title'],
                                      'img':ca['img'],
                                      'width':ca['width'],
                                      'height':ca['height'],
                                      })
            else:
                p['theme'].append({'id':ca['id'],
                                   'des':ca['des'],
                                   'title':ca['title'],
                                   'img':ca['img'],
                                   'hot':ca['hot'],
                                   'type':ca['type'],                                   
                                   })
        p['city']=self.db.query(
            "SELECT `sys_new_district`.`id`,`sys_new_district`.`district_name` AS `name` , `sys_new_district`.`des` , "
            "CONCAT(`sys_new_event_img_server`.`name` , `sys_new_event_img`.`urls` ) AS `img`  FROM `sys_new_district` "
            " INNER JOIN `sys_new_event_img` ON `sys_new_district`.`img_id`=`sys_new_event_img`.`id` "
            "INNER JOIN `sys_new_event_img_server` ON `sys_new_event_img_server`.`id` = `sys_new_event_img`.`server_id` "
            " WHERE `sys_new_district`.`id` IN (101,99,54) "
            )
        
        self.write(p)

        #self.render("home.html", entries=[])

def main(port):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main(int(sys.argv[1]))
