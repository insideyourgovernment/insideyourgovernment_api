from datetime import datetime
import rethinkdb as r

def get_dt():
    return r.expr(datetime.now(r.make_timezone('-07:00')))

def update_all_row_counts():
    tables = list(r.db('public').table('tables').run())
    for table in tables:
        the_count = r.db('public').table(table['id']).count().run()
        print table['id'], r.db('public').table('tables').get(table['id']).update({'number_of_rows': the_count}).run()