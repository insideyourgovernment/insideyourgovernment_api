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
        print(change)
        content = str(change)
        message = sendgrid.Mail()
        message.add_to(email)
        message.add_to('tim@insideyourgovernment.com')
        message.set_subject('Public disclosure request to %s for records created in response to my pdrs' % (city))
        message.set_text(content)
        message.set_html(content.replace('\n', '<br/>'))
        message.set_from('tim@insideyourgovernment.com')
        print sg.send(message)

@gen.coroutine
def main():
    q = handle_query({'table': 'test_table'}, run=False).changes()
    ioloop.IOLoop.current().add_callback(print_changes, q)
    
        
if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(main)
    ioloop.IOLoop.current().start()