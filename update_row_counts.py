import rethinkdb as r
from tornado import ioloop, gen
from search import handle_query

r.set_loop_type("tornado")

@gen.coroutine
def print_changes(q):
    conn = yield r.connect(host="localhost", port=28015)
    feed = yield q.run(conn)
    while (yield feed.fetch_next()):
        change = yield feed.next()
        

@gen.coroutine
def main():
    conn = yield r.connect(host="localhost", port=28015)
    table_list = r.db('public').table_list()
    table_list = yield table_list.run(conn)
    q = handle_query({'table': 'test_table'}, run=False).changes()
    ioloop.IOLoop.current().add_callback(print_changes, q)
    
        
if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(main)
    ioloop.IOLoop.current().start()