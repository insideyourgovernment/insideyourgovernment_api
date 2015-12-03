import rethinkdb as r
from tornado import ioloop, gen
from search import handle_query

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
    handle_query = 
        
if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(main)
    ioloop.IOLoop.current().start()