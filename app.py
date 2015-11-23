from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import rethinkdb as r
r.connect( "localhost", 28015).repl()
import json
import urlparse
import random
import string
import itertools

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_user_info_from_session(session_id):
    userid = r.db('nonpublic').table('sessions').get(session_id).run()['userid']
    user_data = r.db('nonpublic').table('users').get(userid).run().copy()
    del user_data['password']
    return user_data

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "accept, cache-control, origin, x-requested-with, x-file-name, content-type")  
        
    def get(self):
        self.set_header("Content-Type", 'application/json')
        
    def post(self):
        self.set_header("Content-Type", 'application/json')

class SessionHandler(BaseHandler):
    def get(self):
        params = urlparse.parse_qs(self.request.body)
        print params
        self.write(get_user_info_from_session(self.get_argument('session')))

class LoginHandler(BaseHandler):
    def post(self):
        print self.request.body
        params = urlparse.parse_qs(self.request.body)
        email = params['email'][0]
        password = params['password'][0]
        success = False
        user_data = r.db('nonpublic').table('users').get(email).run()
        if password == user_data['password']:
            success = True
        response = {'success': success} 

        session_id = id_generator(30)
        
        r.db('nonpublic').table('sessions').insert({'id': session_id, 'userid': email}).run()
        response['session_id'] = session_id
        #resp = make_response(redirect('/'))
        #resp.set_cookie('session', session_id)
        self.set_cookie("session", session_id)
        self.set_header("Content-Type", 'application/json')
        self.write(json.dumps(response))
        #try:
        #    print tornado.escape.json_decode(self.request.body) 
        #except:
        #    pass
        # it's assumed that a username is an email address
        #if not is_already_account(request.form['username']):
        #    return Response(json.dumps({'msg': '<strong>Error:</strong> Either email or password is incorrect'}), mimetype="application/json")
        #user_data = db.table('users').get(request.form['username']).run(conn)
        #m = hashlib.sha512()
        #salt = user_data['salt']
        #password = request.form['password']
        #m.update(salt+password)
        #hash = m.hexdigest()

        #if user_data['hash'] != hash:
        #    return Response(json.dumps({'msg': '<strong>Error:</strong> Either email or password is incorrect'}), mimetype="application/json")
        #if not (user_data.get('is_approved') or user_data.get('is_admin')):
        #    return Response(json.dumps({'msg': "<strong>Error:</strong> Your account hasn't been approved"}), mimetype="application/json")
        #two_factor_code = id_generator(60)
        #db.table('two_factor_codes').insert({'id': two_factor_code, 'userid': request.form['username']}).run(conn)
        #message = sendgrid.Mail()
        #message.add_to(request.form['username'])
        #message.set_subject('RedactVideo two factor authentication')
        #message.set_html('<a href="http://redactvideo.org/confirm_two_factor/?two_factor_code=%s">Click here</a> to confirm two factor code.' % (two_factor_code))
        #message.set_from('no-reply@redactvideo.org')
        #sg = sendgrid.SendGridClient(get_setting('sendgrid_username'), get_setting('sendgrid_password'))
        #status, msg = sg.send(message)
        #return Response(json.dumps({'msg': 'Two factor authentication email sent'}), mimetype="application/json")
      
        
class TablesHandler(BaseHandler):
    def get(self):
        response = r.db('public').table_list().run()
        self.set_header("Content-Type", 'application/json')
        self.write(json.dumps(response))
        
def table_create(payload):
    return r.db('public').table_create(payload['name']).run()

def insert(payload):
    pass

def update(payload):
    pass

class ModifyDBHandler(BaseHandler):
    def post(self):
        # For now user needs to be an admin
        params = urlparse.parse_qs(self.request.body)
        session = params['session'][0]
        user_info = get_user_info_from_session(session)
        if user_info['is_admin']:
            payload = json.loads(params['payload'])
            action = payload['action']
            actions = {'table_create': create_table,
                       'insert': insert,
                       'update': update}
            self.write(actions[action](payload))
            
class RetriveHandler(BaseHandler):
    def get(self):
        params = urlparse.parse_qs(self.request.body)
        print params
        payload = json.loads(self.get_argument('payload'))
        dbobj = r.db('public').table(payload['table'])
        for key in payload.keys():
            if key in ['get', 'filter', 'has_fields', 'match', 'has_string']:
                if type(payload[key]) is list and key in ['has_fields']:
                    dbobj = getattr(dbobj, key)(*payload[key])
                elif key == 'match':
                    dbobj = getattr(dbobj, 'filter')(lambda case: case[payload['match']['field']].match(payload['match']['value']))
                elif key == 'has_string':
                    dbobj = getattr(dbobj, 'filter')(lambda case: case[payload['has_string']['field']].match('.*?'+payload['has_string']['value']+'.*?'))
                else:
                    dbobj = getattr(dbobj, key)(payload[key])
        if 'pluck' in payload:
            print 'plucking'
            dbobj = getattr(dbobj, 'pluck')(*payload['pluck'])
        
                
        self.set_header("Content-Type", 'application/json')
        if 'action' in payload:
            if payload['action'] == 'get_fields':
                results = list(dbobj.run())
                fields = [row.keys() for row in results]
                fields = list(itertools.chain.from_iterable(fields))
                results = sorted(list(set(fields)))
            elif payload['action'] == 'count':
                results = {'count': dbobj.count().run()}
            elif payload['action'] == 'percentage_simple_matching':
                if 'match' in payload:
                    base = r.db('public').table(payload['table']).filter(lambda case: case[payload['match']['field']].match(payload['match']['value']))
                
                else:
                    base = r.db('public').table(payload['table']).filter(lambda case: case[payload['has_string']['field']].match(payload['has_string']['field']))
                denominator = base.count().run(conn)

                numerator = base.filter({payload['numerator']['field']: payload['numerator']['value']}).count().run(conn) 

                if denominator:
                    percentage = float(numerator)/denominator
                    percentage = "{:.0%}".format(percentage)+' (%s/%s)' % (numerator, denominator)
                else:
                    percentage = 'Error: No denominator'    
                results = {'numerator': numerator, 'denominator': denominator, 'percentage': percentage}
        else:
            results = list(dbobj.run())
        self.write(json.dumps(results))

                        
app = tornado.web.Application([
    (r"/get_session_info/", SessionHandler),
    (r"/login/", LoginHandler),
    (r"/tables/", TablesHandler),
    (r"/modify_db/", ModifyDBHandler),
    (r"/retrive/", RetriveHandler),
])

if __name__ == "__main__":
    
    app.listen(8000) 
    tornado.ioloop.IOLoop.current().start()