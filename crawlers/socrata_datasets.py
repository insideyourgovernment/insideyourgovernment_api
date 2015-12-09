import rethinkdb as r
r.connect( "localhost", 28015).repl()
import requests
t = list(r.db('public').table('police_response_events').order_by(r.desc('socrata_created_at'), index=r.desc('socrata_created_at')).limit(int(1)).run())[0]['socrata_created_at'].isoformat()[:-9]
data = requests.get('https://data.seattle.gov/resource/pu5n-trf4.json?$select=:*,*&$limit=2000000&$where=:created_at%%20>%%20"%s"' % (t)).json()
import dateutil
import dateutil.parser
from pytz import timezone
from datetime import date
from datetime import datetime
tz = timezone('America/Los_Angeles')
for row in data:
    row['organization_id'] = 'cfee2384-fb23-450a-90bf-2cbfa2912876'
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
