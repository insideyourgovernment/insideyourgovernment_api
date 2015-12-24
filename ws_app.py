import tornado.ioloop
import tornado.web
import tornado.websocket
import rethinkdb as r
from tornado.options import define, options, parse_command_line

define("port", default=8888, type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        print 'rendering'
        self.render("ws_index.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        print "New connection"
        self.write_message("Welcome!")

    def on_message(self, message):
        conn = r.connect( "localhost", 28015).repl()
        print "New message {}".format(message)
        response = r.db('public').table(message).limit(10).run(conn)
        response = list(response)
        self.write_message(response)

    def on_close(self):
        print "Connection closed"


app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws/', WebSocketHandler),
])


if __name__ == '__main__':
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()