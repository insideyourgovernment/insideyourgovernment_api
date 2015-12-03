import rethinkdb as r
from tornado import ioloop, gen

r.set_loop_type("tornado")

@gen.coroutine
def print_changes(table):
    conn = yeild r.connect(host="localhost", port=28015)
    feed = yeild r.db('public').table(table).changes().run(conn)
    while (yield feed.fetch_next()):
        change = yield feed.next()
        print(change)

conn = r.connect(host="localhost", port=28015)
for table in r.db('public').table_list().run(conn):
    ioloop.IOLoop.current().add_callback(print_changes, table)
    
@gen.coroutine
def main():
    """ Async main method. It needed to be async due to r.connect is async . """
    parse_command_line()
    db_name = "rechat"
    setup_db(db_name)
    r.set_loop_type("tornado")

    db = yield r.connect("localhost", db=db_name)
    #Single db connection for everything thanks a lot Ben and Jeese
    http_server = httpserver.HTTPServer(RechatApp(db))
    http_server.listen(options.port)

if __name__ == "__main__":
    IOLoop.current().run_sync(main)
    IOLoop.current().start()