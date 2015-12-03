import rethinkdb as r
from tornado import ioloop, gen

r.set_loop_type("tornado")

@gen.coroutine
def print_changes(table):
    conn = yield r.connect(host="localhost", port=28015)
    feed = yield r.db('public').table(table).changes().run(conn)
    while (yield feed.fetch_next()):
        change = yield feed.next()
        print(change)

@gen.coroutine
def main():
    conn = yield r.connect(host="localhost", port=28015)
    for table in r.db('public').table_list().run(conn):
        ioloop.IOLoop.current().add_callback(print_changes, table)
        
if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(main)
    ioloop.IOLoop.current().start()