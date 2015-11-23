import os
import sys

def setup_rethinkdb():
    import rethinkdb as r
    r.connect( "localhost", 28015).repl()
    try:
        r.db_create("nonpublic").run()
    except:
        pass
    try:
        r.db_create("public").run()
    except:
        pass
    db = r.db("public")
    dbs_and_tables = {'nonpublic': ['third_party_creds', 'subscribers', 'users', 'sessions'], 'public': ['crawling_instructions', 'apps', 'police_internal_affairs_cases', 'organizations', 'tables']}
    
    for database in dbs_and_tables.keys():
        try:
            r.db_create(database).run()
        except:
            pass
        db = r.db(database)
        tables_needed = dbs_and_tables[database]
        existing_tables = db.table_list().run()
        tables_to_create = set(tables_needed) - set(existing_tables) # remove existing tables from what we need
        for table in tables_to_create:
            db.table_create(table).run()
    for table in dbs_and_tables:
        #tables_ids = [item['id'] for item in r.db('public').table('tables').run()]
        #if not table in tables_ids:
        if 'police' in table:
            category = 'policing'
        else:
            category = 'Pe
        r.db('public').table('tables').insert({'id': table, 'name': table.replace('_', ' ').capitalize(), 'categories': [category]}, conflict='update').run()

def update(force=False):
    fetch_dry_run_results = os.popen('git fetch --dry-run').read()
    
    if not fetch_dry_run_results and not force:
        return
    os.popen('git pull').read()
    os.system('sudo pip install -r requirements.txt')
    setup_rethinkdb()
if 'force' in str(sys.argv):
    update(force=True)
else:
    update()
