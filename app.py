from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import rethinkdb as r
r.connect( "localhost", 28015).repl()
import json
import urlparse

class LoginHandler(tornado.web.RequestHandler):
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
        username = userid
        print db.table('sessions').insert({'id': session_id, 'userid': username}).run(conn)
        resp = make_response(redirect('/'))
        resp.set_cookie('session', session_id)
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

class TablesHandler(tornado.web.RequestHandler):
    def get(self):
        response = r.db('public').table_list().run()
        self.write(json.dumps(response))
        
 
app = tornado.web.Application([
    (r"/login/", LoginHandler),
    (r"/tables/", TablesHandler),
])

if __name__ == "__main__":
    
    app.listen(3389)
    tornado.ioloop.IOLoop.current().start()