from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import rethinkdb as r
r.connect( "localhost", 28015).repl()
import json
class TablesHandler(tornado.web.RequestHandler):
    def get(self):
        response = r.db('public').table_list().run()
        self.write(json.dumps(response))
        
 
app = tornado.web.Application([
    (r"/tables/", TablesHandler),
])

if __name__ == "__main__":
    
    app.listen(3389)
    tornado.ioloop.IOLoop.current().start()