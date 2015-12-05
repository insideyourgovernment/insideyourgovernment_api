import rethinkdb as r
from tornado import ioloop, gen
from search import handle_query

r.set_loop_type("tornado")

@gen.coroutine
def update_row_counts(table):
    conn = yield r.connect(host="localhost", port=28015)
    first_part = r.db('public').table(table).changes()
    feed = yield first_part.run(conn)
    while (yield feed.fetch_next()):
        change = yield feed.next()
        number_of_rows = r.db('public').table(table).count()
        number_of_rows = yield number_of_rows.run(conn)
        query = r.db('public').table('tables').get(table).update({'number_of_rows': number_of_rows})
        q = yield query.run(conn)
        print table, query, q
@gen.coroutine
def main():
    conn = yield r.connect(host="localhost", port=28015)
    table_list = r.db('public').table_list()
    table_list = yield table_list.run(conn)
    for table in table_list:
        ioloop.IOLoop.current().add_callback(update_row_counts, table)
    
        
if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(main)
    ioloop.IOLoop.current().start()