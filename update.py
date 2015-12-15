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
    dbs_and_tables = {'nonpublic': ['third_party_creds', 'subscribers', 'subscriptions', 'users', 'sessions'], 'public': ['crawling_instructions', 'apps', 'police_internal_affairs_cases', 'police_internal_affairs_allegations', 'organizations', 'tables', 'queries', 'people', 'datasets', 'police_response_events', 'changes', 'crawler_log']}
    
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
    for table in dbs_and_tables['public']:
        if 'police' in table:
            category = "Policing"
        elif table == 'datasets':
            category = "Information Technology"
        elif 'people' in table:
            category = "Human resources"
        else:
            category = "Inside Your Government"
        r.db('public').table('tables').insert({'id': table, 'name': table.replace('_', ' ').capitalize(), 'number_of_rows': 0, 'categories': [category]}, conflict='update').run()

def update(force=False):
    #fetch_dry_run_results = os.popen('git fetch --dry-run').read()
    
    #if not fetch_dry_run_results and not force:
    #    return
    git_pull = os.popen('git pull').read()
    print git_pull
    os.system('sudo pip install -r requirements.txt')
    setup_rethinkdb()
if 'force' in str(sys.argv):
    update(force=True)
else:
    update()
    update() # to ensure the new tables are created
