import rethinkdb as r
r.connect( "localhost", 28015).repl()
import requests
app_token = r.db('nonpublic').table('third_party_creds').get('socrata').run()['app_token']
t = list(r.db('public').table('police_response_events').order_by(r.desc('socrata_created_at'), index=r.desc('socrata_created_at')).limit(int(1)).run())[0]['socrata_created_at'].isoformat()[:-9]
data = requests.get('https://data.seattle.gov/resource/pu5n-trf4.json?$select=:*,*&$limit=2000000&$where=:created_at%%20>%%20"%s"&$$app_token=%s' % (t, app_token)).json()
import dateutil
import dateutil.parser
from pytz import timezone
from datetime import date
from datetime import datetime
tz = timezone('America/Los_Angeles')
for row in data:
    row['organization_id'] = 'cfee2384-fb23-450a-90bf-2cbfa2912876'
    row['is_cad_event'] = True
    row['is_rms_event'] = False
    for key in row.keys():
        if key.startswith(':id'):
            row['id'] = row[':id']
            del row[':id']
        elif key.startswith(':'):
            row['socrata_'+key[1:]] = row[key]
            del row[key]
    for key in row.keys():
        if not '_at' in key and not 'date' in key and not 'time' in key:
            continue

        row[key] = dateutil.parser.parse(row[key])
        if row[key].tzinfo == None:
            row[key] = row[key].replace(tzinfo = tz)
print r.db('public').table('police_response_events').insert(data).run(conflict='update')

t = list(r.db('public').table('police_response_events').order_by(r.desc('socrata_rms_created_at'), index=r.desc('socrata_rms_created_at')).limit(int(1)).run())[0]['socrata_created_at'].isoformat()[:-9]
data = requests.get('https://data.seattle.gov/resource/y7pv-r3kh.json?$select=:*,*&$limit=2000000&$where=:created_at%%20>%%20"%s"&$$app_token=%s' % (t, app_token)).json()
print 'got the data'
#print data
import dateutil
from pytz import timezone
from datetime import date
from datetime import datetime
tz = timezone('America/Los_Angeles')
for i, row in enumerate(data):
    
    row['organization_id'] = 'cfee2384-fb23-450a-90bf-2cbfa2912876'
    row['is_rms_event'] = True
    #print 'gon', row['general_offense_number']
    try:
        row['id'] = list(r.db('public').table('police_response_events').get_all(row['general_offense_number'], index='general_offense_number').run())[0]['id']
    except:
        #print row.keys()
        row['id'] = row[':id']
    for key in row.keys():
        
        if key.startswith(':'):
            row['socrata_rms_'+key[1:]] = row[key]
            del row[key]
    for key in row.keys():
        if not '_at' in key and not 'date' in key and not 'time' in key:
            continue

        row[key] = dateutil.parser.parse(row[key])
        if row[key].tzinfo == None:
            row[key] = row[key].replace(tzinfo = tz)
    change = r.db('public').table('police_response_events').insert(row).run(conflict='update')
    print change