import datetime
import rethinkdb as r

def get_dt():
    return r.expr(datetime.now(r.make_timezone('-07:00')))