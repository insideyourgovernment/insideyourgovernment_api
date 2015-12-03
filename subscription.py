import rethinkdb as r
from tornado import ioloop, gen

r.set_loop_type("tornado")

@gen.coroutine
def print_changes():
    conn = yield r.connect(host="localhost", port=28015)
    feed = yield r.table("table").changes().run(conn)
    while (yield feed.fetch_next())
        change = yield feed.next()
        print(change)

conn = yield r.connect(host="localhost", port=28015)
for table in 
ioloop.IOLoop.current().add_callback(print_changes)