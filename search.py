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
from datetime import datetime
import requests
import os
import re
from string import Template 

def is_number_field(field):
    indicators = ['number', 'num', 'views', 'total']
    for indicator in indicators:
        if indicator in field:
            return True
    return False

def get_field(l, field):
    results = []
    for d in l:
        if field in d:
            results.append(d[field])
    return results

def replace_star(d, groups):
    new_d = {}
    for k, v in d.items():
        if isinstance(v, dict):
            new_d[k] = replace_star(v, groups)
        elif isinstance(v, str) or isinstance(v, unicode):
            
            new_d[k] = groups[v[1:]] if v.startswith('*') else v
            print v, new_d[k]
        else:
            new_d[k] = v
    return new_d

def run_query(groups, query):
    print 'GROUPS ***', groups
    print 'before', query
    query = replace_star(query, groups)
    print 'after', query
    return handle_query(query)

def test_rule(not_nones, data):
    for k in not_nones:
        if not data[k]:
            return False
    return True

def global_search(payload):
    for row in r.db('public').table('rules_for_global_search').pluck('id').order_by('order').run(conn):
        m = re.search(row['id'], payload['global_search_query'])
        if m:
            break
    if m:
        rules = r.db('public').table('rules_for_global_search').get(row['id']).run(conn)
        results = run_query(m.groupdict(), rules['query'])
        if len(results['data']) == 1:
            results['data'] = results['data'][0]
        if 'sentences' in rules:

            for sentence_rule in rules['sentences']:
                if test_rule(sentence_rule['not_none'], results['data']):
                    results['sentence'] = Template(sentence_rule['sentence']).safe_substitute(results['data'])
        return results
    else:
        return None

def get_dbobj(payload):
    dbobj = r.db('public').table(payload['table'])
    if 'get' in payload:
        results = {'data': dbobj.get(payload['get']).run(time_format="raw"), 'payload': payload}
        table_data = r.db('public').table('tables').get(payload['table']).run(conn)
        if 'title_template' in table_data:
            d = dict([(item[0].lower().replace(' ', '_'), item[1]) for item in results['data'].items()])
            results['title'] = Template(table_data['title_template']).safe_substitute(d)
        else:
            results['title'] = payload['table'] + ' ' + results['data']['id']
        return results
    for key in payload.keys():
        if key in ['get', 'has_fields', 'doesnt_have_fields', 'match', 'has_string', 'match_any_field', 'has_string_in_any_field']:
            if type(payload[key]) is list and key in ['has_fields']:
                dbobj = getattr(dbobj, key)(*payload[key])
            elif type(payload[key]) is list and key in ['doesnt_have_fields']:
                # 'doesnt_have_fields', 
                dbobj.filter(lambda row: row.pluck(*payload[key]).eq({}))
            elif key in ['doesnt_have_fields']:
                dbobj.filter(lambda row: row.pluck(payload[key]).eq({}))
            elif key == 'match':
                dbobj = getattr(dbobj, 'filter')(lambda case: case[payload['match']['field']].match(payload['match']['value']))
            elif key == 'has_string':
                dbobj = getattr(dbobj, 'filter')(lambda case: case[payload['has_string']['field']].match('.*?'+payload['has_string']['value']+'.*?'))
            elif key == 'match_any_field':
                dbobj = getattr(dbobj, 'filter')(lambda doc: doc.coerce_to('string').match(payload['match_any_field']))
            elif key == 'has_string_in_any_field':
                dbobj = getattr(dbobj, 'filter')(lambda doc: doc.coerce_to('string').match('(?i).*?'+payload['has_string_in_any_field']+'.*?'))
            else:
                dbobj = getattr(dbobj, key)(payload[key])


    if 'filter' in payload:
        key = 'filter'
        if len(payload['filter'].items()) == 1 and payload['filter'].keys()[0] in r.db('public').table(payload['table']).index_list().run(conn):
            print 'using index'
            dbobj = dbobj.get_all(payload['filter'].items()[0][1], index=payload['filter'].items()[0][0])
        else:
            print 'not using index'
            dbobj = getattr(dbobj, key)(payload[key])


    if 'pluck' in payload:
        if type(payload['pluck']) is list:
            dbobj = getattr(dbobj, 'pluck')(*payload['pluck'])
        else:
            dbobj = getattr(dbobj, 'pluck')(payload['pluck'])            
            
    if 'order_by' in payload:
        for o in payload['order_by']:
            if o['direction'] == 'desc':
                dbobj = getattr(dbobj, 'order_by')(r.desc(o['field']), index=r.desc(o['field']))
            else:
                dbobj = getattr(dbobj, 'order_by')(index=o['field'])
    else:
        results = {}
        results['table'] = r.db('public').table('tables').get(payload['table']).run(conn)
        if 'default_order_by' in results['table']:
            field = results['table']['default_order_by']['field']
            if field in r.db('public').table(payload['table']).index_list().run(conn) and not 'filter' in payload and not 'has_string_in_any_field' in payload:
                dbobj = getattr(dbobj, 'order_by')(index=r.desc(field)) 
            else:
                dbobj = getattr(dbobj, 'order_by')(r.desc(field))
                
    
            
    
    if len(payload) < 3 and not 'filter' in payload:
        rows_count = r.db('public').table(payload['table']).info().run(conn)["doc_count_estimates"]
    else:
        rows_count = dbobj.pluck('id').count().run(conn)
            
    #results_for_fields = list(dbobj.run(conn))
    #fields = [row.keys() for row in results_for_fields]
    #fields = list(itertools.chain.from_iterable(fields))
    #fields = sorted(list(set(fields)))
    
    #joined_data = list(r.db("public").table("police_internal_affairs_allegations").eq_join("organization_id", r.db("public").table("organizations")).map({"right":{
    #        "organization_id": r.row["right"]["id"],
    #        "organization_name": r.row["right"]["name"]
    #    }, "left": r.row["left"]}).zip().run(conn))
    #ids_for_other_tables = [field for field in fields if field.endswith('_id')]
    modified_joined_data = [] 
    special_names = {'person': 'people'}
    if not 'do_auto_join' in payload:
        payload['do_auto_join'] = False # turn it off for now due to performance issues
    if payload['do_auto_join']:
        for field in ids_for_other_tables:

            #print field
            #print field[:-3]+'s'
            # get the fields of the table 
            #results_for_fields = r.db('public').table(field[:-3]+'s').run(conn)
            #right_fields = [row.keys() for row in results_for_fields]
            #right_fields = list(itertools.chain.from_iterable(right_fields))
            #right_fields = sorted(list(set(right_fields)))

            t = special_names[field[:-3]] if field[:-3] in special_names else field[:-3]+'s'
            if '__' in t:
                t = t.split('__')[-1]
            if not t in r.db('public').table_list().run(conn):
                continue
            print field, t
            dbobj = dbobj.eq_join(field, r.db("public").table(t))
            #d = {"left": r.row["left"], "right": {}}
            #for right_field in right_fields:
            #    d["right"][field[:-2]+right_field] = r.row["right"][right_field]
            #dbobj = dbobj.map(d)
            dbobj = dbobj.merge(  lambda row: {'left': row['right'].coerce_to('array').map(
                          lambda pair: [r.expr(field[:-2]) + pair[0], pair[1]]
                        ).coerce_to('object')}).without({'right': True}).zip()
            #dbobj = dbobj

    
    if 'page' in payload:
        page = int(payload['page'])
    else:
        payload['page'] = int(1)
        page = int(1)
    if 'rows_per_page' in payload:
        rows_per_page = int(payload['rows_per_page'])
    else:
        rows_per_page = int(10)
    dbobj = dbobj.slice((page - 1) * rows_per_page, page * rows_per_page)
    return dbobj
    
def handle_query(payload, run=True):
    
    conn = r.connect( "localhost", 28015).repl()
    if 'global_search_query' in payload:
        return global_search(payload)
    
    dbobj = get_dbobj(payload)
    
    #fields = [row.keys() for row in results_for_fields]
    #fields = list(itertools.chain.from_iterable(fields))
    #fields = sorted(list(set(fields)))
    print dbobj    
    #for data in joined_data:
    #    d = {}
    #    d.update(data['left'])
    #    new_right_side = data['right'].items()
    #    new_right_side = dict([('organization_'+item[0], item[1]) for item in new_right_side])
    #    d.update(new_right_side)
    #    modified_joined_data.append(d)


    if 'action' in payload:
        if payload['action'] == 'get_fields':
            results = list(dbobj.run(conn))
            fields = [row.keys() for row in results]
            fields = list(itertools.chain.from_iterable(fields))
            results = sorted(list(set(fields)))
        elif payload['action'] == 'count':
            results = {'count': rows_count}
        elif payload['action'] == 'percentage_simple_matching':
            if 'match' in payload:
                base = r.db('public').table(payload['table']).filter(lambda case: case[payload['match']['field']].match(payload['match']['value']))

            else:
                base = r.db('public').table(payload['table']).filter(lambda case: case[payload['has_string']['field']].match('.*?'+payload['has_string']['value']+'.*?'))
            denominator = base.pluck('id').count().run(conn)

            numerator = base.filter({payload['numerator']['field']: payload['numerator']['value']}).pluck('id').count().run(conn) 

            if denominator:
                percentage = float(numerator)/denominator
                percentage = "{:.0%}".format(percentage)+' (%s/%s)' % (numerator, denominator)
            else:
                percentage = 'Error: No denominator'    
            results = {'numerator': numerator, 'denominator': denominator, 'percentage': percentage}
        elif payload['action'] == 'get_list':
            results = [item[payload['field']] for item in list(r.db('public').table(payload['table']).pluck(payload['field']).run(conn))]
        elif payload['action'] == 'get_set':
            results = list(set([item[payload['field']] for item in list(r.db('public').table(payload['table']).pluck(payload['field']).run(conn))]))
        elif payload['action'] == 'do_basic_mapping':
            dbobj = getattr(dbobj, 'pluck')(payload['field_for_key'], payload['field_for_value'])
            items = dbobj.run(conn)
            d = {}
            for item in items:
                if type(item[payload['field_for_key']]) is list:
                    for k in item[payload['field_for_key']]:
                        if not k in d:
                            d[k] = [item[payload['field_for_value']]]
                        else:
                            d[k].append(item[payload['field_for_value']])
                else:
                    if not item[payload['field_for_key']] in d:
                        d[item[payload['field_for_key']]] = [item[payload['field_for_value']]]
                    else:
                        d[item[payload['field_for_key']]].append(item[payload['field_for_value']])
            results = d
        elif payload['action'] == 'do_row_mapping':
            print 'doing ', payload['action']
            items = list(dbobj.run(conn))
            table_fields = [row.keys() for row in items]
            table_fields = list(set(list(itertools.chain.from_iterable(table_fields))))
            d = {}
            for item in items:
                if type(item[payload['field_for_key']]) is list:
                    for k in item[payload['field_for_key']]:
                        if not k in d:
                            d[k] = [item]
                        else:
                            d[k].append(item)
                else:
                    if not item[payload['field_for_key']] in d:
                        d[item[payload['field_for_key']]] = [item]
                    else:
                        d[item[payload['field_for_key']]].append(item)
            results = {'data': d, 'table_fields': table_fields, 'keys': d.keys()}
            return results
    else:
        if not run:
            return dbobj
        # if 'pluck' in payload:
        #if type(payload['pluck']) is list:
        #    dbobj = getattr(dbobj, 'pluck')(*payload['pluck'])
        results = {}
        results['table'] = r.db('public').table('tables').get(payload['table']).run(conn)
        
        special_names_reversed = {value: key for key, value in special_names.items()}
        t = payload['table']
        t = special_names_reversed[t] if t in special_names_reversed else t[:-1]
        t = t + '_id'
        results['data'] = list(dbobj.run(time_format="raw"))
        results['expression'] = str(dbobj)
        if 'linked_tables' in results['table']:

            for linked_table in results['table']['linked_tables']:
                linked_table_data = list(r.db('public').table(linked_table).run(time_format="raw"))
                for i, row in enumerate(results['data']):
                    print i
                    row[linked_table] = [item for item in linked_table_data if item.get(t) == row['id']]
                    # consider using group e.g. r.db('public').table('police_internal_affairs_allegations').group('person_id').run(conn)
                    #row[linked_table] = list(r.db('public').table(linked_table).filter({t: row['id']}).run(time_format="raw"))

        results['fields'] = [row.keys() for row in results['data']]
        results['fields'] = list(set(list(itertools.chain.from_iterable(results['fields']))))
        results['number_of_rows'] = rows_count
        #results['sums_by_field'] = {}
        #for field in results['fields']:
        #    if is_number_field(field):
        #        results['sums_by_field'][field] = r.db('public').table(payload['table']).sum(field).run(conn)
        results['percentages'] = []
        results['group_counts'] = []
        #for field in results['fields']:
        #    if not field.endswith('_id'):
        #        continue
        #    t = special_names[field[:-3]] if field[:-3] in special_names else field[:-3]+'s'
        #    if not t in r.db('public').table_list().run(conn):
        #        continue
        #    g = r.db('public').table(t).group('id').run(conn)
        #    
        #    results['group_counts'].append([t, [[g[item[0]], item[1]] for item in list(sorted(dbobj.group(field).count().run(conn).items(), key=lambda x:x[1], reverse=True))][:10]]) 
        results['group_counts'].sort(key=lambda x:x[0])

        likely_boolean_fields = [field for field in results['fields'] if field.startswith('is_')]
        # remove if the field in a filter
        if 'filter' in payload:
            for field in payload['filter'].keys():
                if field in likely_boolean_fields:
                    likely_boolean_fields.remove(field)
        for field in []:
        #for field in likely_boolean_fields:
            items_in_field = get_field(results['data'], field)
            numerator = items_in_field.count(True)
            denominator = len(items_in_field)
            percentage = float(numerator)/denominator
            percentage = "{:.0%}".format(percentage)+' (%s/%s)' % (numerator, denominator)
            row_name = payload['table'].replace('_', ' ')
            if 'has_string_in_any_field' in payload:
                sentence = '%s of %s mentioning "%s" are %s.' % (percentage, row_name, payload['has_string_in_any_field'], field[3:])
            else:
                sentence = '%s of %s are %s.' % (percentage, row_name, field[3:])
            results['percentages'].append({'field': field, 'value': True, 'percentage': percentage, 'sentence': sentence})
        results['payload'] = payload
        results['name_for_rows'] = payload['table'].split('_')[-1]
        results['field_selectors'] = []
        for field in results['fields']:
            if field == 'id':
                continue
            elif field.startswith('is_'):
                results['field_selectors'].append({'selector': 'checkbox', 'name': field, 'display_name': field[3:].capitalize()})
            else:
                items = sorted(list(set([row[field] if isinstance(row[field], basestring) else '' for row in results['data'] if field in row and len(unicode(row.get(field)).encode('utf-8')) < 50])))
                if len(items) < 100 and not items == ['']:
                    results['field_selectors'].append({'selector': 'dropdown', 'name': field, 'display_name': field.replace('_', ' ').capitalize(), 'items': items})
        if run:
            return results
        return dbobj
        