from joblib import Parallel, delayed  
import multiprocessing



num_cores = multiprocessing.cpu_count()

  

import rethinkdb as r

def run_count(i, theid, api_url):
    
    count_url = '%s?$select=count(*)&$$app_token=%s' % (d['api_url'], app_token)
    try:
        count_data = requests.get(count_url, verify=False).json()
        number_of_rows = count_data[0]['count']
        print i, d['id'], d['number_of_rows']
    except Exception, err:
        print count_url
        print traceback.print_exc()
    conn = r.connect( "localhost", 28015).repl()
    r.db('public').table('datasets').get(theid).update({"number_of_rows": number_of_rows}).run(conn)
    print i
    return number_of_rows

def do():
    import rethinkdb as r
    import traceback
    r.connect( "localhost", 28015).repl()
    import requests
    app_token = r.db('nonpublic').table('third_party_creds').get('socrata').run()['app_token']
    results = []
    for i in range(10):
        results.extend(requests.get('http://api.us.socrata.com/api/catalog/v1?only=datasets&limit=10000&offset='+str(10000*i)).json()['results'])
    data = results
    modified_data = []
    inputs = []
    for i, row in enumerate(data):
        d = {}
        d.update(row)
        d.update(row['resource']) 
        d.update(row['resource']['view_count'])
        d.update(row['classification'])
        # https://data.cityofnewyork.us/Public-Safety/Disposition-Of-Offensive-Language-Allegations-2007/xah7-gu5w
        # https://data.cityofnewyork.us/resource/xah7-gu5w.json
        # use permalink
        d['api_url'] = d['permalink'].replace('/d/', '/resource/') + '.json'
        # ?$select=count(*)&$$app_token=%s' 
        inputs.append([i, d['id'], d['api_url']])
        modified_data.append(d)
    print r.db('public').table('datasets').insert(modified_data).run(conflict='update')
    results = Parallel(n_jobs=num_cores)(delayed(run_count)(*inp) for inp in inputs)
while True:
    do()