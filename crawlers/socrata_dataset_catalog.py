from joblib import Parallel, delayed  
import multiprocessing
import traceback
import requests

num_cores = multiprocessing.cpu_count()*50
import rethinkdb as r

import dateutil
import dateutil.parser
from pytz import timezone
from datetime import date
from datetime import datetime
tz = timezone('America/Los_Angeles')

def run_count(i, theid, api_url, app_token, tables_list, d):
    conn = r.connect( "localhost", 28015).repl()
    #table = 'socrata_dataset_'+theid.replace('-', '_') # rethinkdb doesn't allow -
    #if not table in tables_list:
        
    #    t = r.db('public').table_create(table).run(conn, noreply=True)
    #    t = r.db('public').table('tables').insert({'id': table, 'name': d['name'], 'categories': ['Socrata datasets']}).run(conn, noreply=True)
    count_url = '%s?$select=count(*)&$$app_token=%s' % (api_url, app_token)
    try:
        count_data = requests.get(count_url, verify=False).json()
        number_of_rows = int(count_data[0][count_data[0].keys()[0]]) # sometimes key is count_1 instead of count
        
        r.db('public').table('datasets').get(theid).update({"number_of_rows": int(number_of_rows), "number_of_rows_error": False}).run(conn, noreply=True)
        print i, theid, int(number_of_rows)
        #return number_of_rows
    except Exception, err:
        r.db('public').table('datasets').get(theid).update({"number_of_rows_error": True}).run(conn, noreply=True)
        print count_url
        print traceback.print_exc()
        #return None
    

def do():
    import rethinkdb as r
    import traceback
    conn = r.connect( "localhost", 28015).repl()
    import requests
    app_token = r.db('nonpublic').table('third_party_creds').get('socrata').run()['app_token']
    results = []
    for i in range(10):
        results.extend(requests.get('http://api.us.socrata.com/api/catalog/v1?only=datasets&limit=10000&offset='+str(10000*i)).json()['results'])
    data = results
    print 'number_of_datasets', len(data)
    modified_data = []
    inputs = []
    tables_list = r.db('public').table_list().run(conn)
    for i, row in enumerate(data):
        d = {}
        d.update(row)
        for key in d.keys():
            if isinstance(d[key], dict):
                d.update(d[key])    
        #d.update(row['resource'])
        #d.update(row['resource']['view_count'])
        #d.update(row['classification'])
        # https://data.cityofnewyork.us/Public-Safety/Disposition-Of-Offensive-Language-Allegations-2007/xah7-gu5w
        # https://data.cityofnewyork.us/resource/xah7-gu5w.json
        # use permalink
        d['api_url'] = d['permalink'].replace('/d/', '/resource/') + '.json'
        d['api_url'] = d['api_url'][:-14]+d['id']+'.json'
        # ?$select=count(*)&$$app_token=%s' 
        
        inputs.append([i, d['id'], d['api_url'], app_token, tables_list, d])
        modified_data.append(d)
    print 'trying insert'
    for i in range(len(data)/200+1):
        t = r.db('public').table('datasets').insert(modified_data[i*200:(i+1)*200]).run(conn, conflict='update', noreply=True)
    results = Parallel(n_jobs=num_cores)(delayed(run_count)(*inp) for inp in inputs)
    
while True:
    do()