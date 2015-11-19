from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import rethinkdb as r
r.connect( "localhost", 28015).repl()

class TablesHandler(tornado.web.RequestHandler):
    def get(self):
        response = r.db('public').table_list().run()
        self.write(response)
        
class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = { 'version': '3.5.1',
                     'last_build':  date.today().isoformat() }
        self.write(response)
 
class GetGameByIdHandler(tornado.web.RequestHandler):
    def get(self, id):
        response = { 'id': int(id), 
                     'name': 'Crazy Game',
                     'release_date': date.today().isoformat() }
        self.write(response)
 
app = tornado.web.Application([
    (r"/tables/", TablesHandler),
    (r"/getgamebyid/([0-9]+)", GetGameByIdHandler),
    (r"/version", VersionHandler)
])

if __name__ == "__main__":
    
    app.listen(3389)
    tornado.ioloop.IOLoop.current().start()