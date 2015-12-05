import rethinkdb as r
from tornado import ioloop, gen
from search import handle_query

r.set_loop_type("tornado")

@gen.coroutine
def update_row_counts(table):
    conn = yield r.connect(host="localhost", port=28015)
    first_part = yield r.db('public').table(table)
    feed = yield first_part.run(conn)
    while (yield feed.fetch_next()):
        change = yield feed.next()
        q = yield r.table('tables').get(table).update({'number_of_rows': 

@gen.coroutine
def main():
    conn = yield r.connect(host="localhost", port=28015)
    table_list = yield r.db('public').table_list()
    table_list = yield table_list.run(conn)
    for table in table_list:
        q = handle_query({'table': 'test_table'}, run=False).changes()
        ioloop.IOLoop.current().add_callback(print_changes, q)
    
        
if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(main)
    ioloop.IOLoop.current().start()