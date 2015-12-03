import rethinkdb as r
from tornado import ioloop, gen

r.set_loop_type("tornado")

@gen.coroutine
def print_changes(table):
    conn = r.connect(host="localhost", port=28015)
    feed = r.db('public').table(table).changes().run(conn)
    while (feed.fetch_next()):
        change = feed.next()
        print(change)

conn = yield r.connect(host="localhost", port=28015)
for table in r.db('public').table_list().run():
    ioloop.IOLoop.current().add_callback(print_changes, table)