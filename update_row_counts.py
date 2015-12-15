import rethinkdb as r
from tornado import ioloop, gen
from search import handle_query
from utils import get_dt

r.set_loop_type("tornado")
def changed_keys(change):
    ck = []
    new_val = change.get('new_val', {})
        if not new_val:
            new_val = {}
    old_val = change.get('old_val', {}) # ugh default = {} not working
        if not old_val:
            old_val = {}
    for key in new_val:
        
        print 'old_val', old_val
        if not key in old_val:
            ck.append(key)
        elif change['new_val'][key] != change['old_val'][key]:
            ck.append(key)
    for key in old_val:
        
        print 'new_val', new_val
        if not key in change.get('new_val', {}):
            ck.append(key)
        elif change['new_val'][key] != change['old_val'][key]:
            ck.append(key)
    return ck

@gen.coroutine
def update_row_counts(table):
    conn = yield r.connect(host="localhost", port=28015)
    first_part = r.db('public').table(table).changes(squash=True)
    feed = yield first_part.run(conn)
    while (yield feed.fetch_next()):
        change = yield feed.next()
        if table == 'tables':
            if not change.get('old_val'):
                ioloop.IOLoop.current().add_callback(update_row_counts, change['new_val']['id'])
        print 'table', table, changed_keys(change)
        if not table == 'changes' and not (table == 'tables' and changed_keys(change) == 'number_of_rows'):
            c = {'table': table, 'datetime': get_dt(), 'change': change}
            #print 'added change', r.db('public').table('changes').insert(c).run(conn)
        print table, change
        if change.get('new_val'):
            indexes = yield r.db('public').table(table).index_list().run(conn)
            table_data = yield r.db('public').table('tables').get(table).run(conn)
            fields = table_data.get('fields')
            for key in change['new_val']:
                if not key in indexes and not key == 'id':
                    r.db('public').table(table).index_create(key).run(conn)
            if not fields:
                r.db('public').table('tables').get(table).update({'fields': change['new_val'].keys()}).run(conn)
            else:
                for key in change['new_val']:
                    if not key in fields:
                        fields.append(key)
                        #print r.db('public').table(table).get(table).update({'fields': fields}).run(conn)
        if not change['new_val'] or not change['old_val']:
            number_of_rows = r.db('public').table(table).count()
            number_of_rows = yield number_of_rows.run(conn)
            query = r.db('public').table('tables').get(table).update({'number_of_rows': number_of_rows})
            q = yield query.run(conn)
            #print table, query, q

@gen.coroutine
def main():
    conn = yield r.connect(host="localhost", port=28015)
    table_list = r.db('public').table_list()
    table_list = yield table_list.run(conn)
    for table in table_list:
        print table
        ioloop.IOLoop.current().add_callback(update_row_counts, table)

if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(main)
    ioloop.IOLoop.current().start()