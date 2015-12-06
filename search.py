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


def get_field(l, field):
    results = []
    for d in l:
        if field in d:
            results.append(d[field])
    return results

def handle_query(payload, run=True):
    if run:
        r.db('public').table('queries').insert({'datetime': r.expr(datetime.now(r.make_timezone('-07:00'))), 'payload': payload}).run()
    dbobj = r.db('public').table(payload['table'])
    for key in payload.keys():
        if key in ['get', 'has_fields', 'doesnt_have_fields', 'match', 'has_string', 'match_any_field', 'has_string_in_any_field']:
            if type(payload[key]) is list and key in ['has_fields']:
                dbobj = getattr(dbobj, key)(*payload[key])
            elif 
                # 'doesnt_have_fields', 
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

    if 'pluck' in payload:
        if type(payload['pluck']) is list:
            dbobj = getattr(dbobj, 'pluck')(*payload['pluck'])
        else:
            dbobj = getattr(dbobj, 'pluck')(payload['pluck'])

    results_for_fields = list(dbobj.run())
    fields = [row.keys() for row in results_for_fields]
    fields = list(itertools.chain.from_iterable(fields))
    fields = sorted(list(set(fields)))

    #joined_data = list(r.db("public").table("police_internal_affairs_allegations").eq_join("organization_id", r.db("public").table("organizations")).map({"right":{
    #        "organization_id": r.row["right"]["id"],
    #        "organization_name": r.row["right"]["name"]
    #    }, "left": r.row["left"]}).zip().run())
    ids_for_other_tables = [field for field in fields if field.endswith('_id')]
    modified_joined_data = []
    special_names = {'person': 'people'}
    for field in ids_for_other_tables:
        #print field
        #print field[:-3]+'s'
        # get the fields of the table 
        #results_for_fields = r.db('public').table(field[:-3]+'s').run()
        #right_fields = [row.keys() for row in results_for_fields]
        #right_fields = list(itertools.chain.from_iterable(right_fields))
        #right_fields = sorted(list(set(right_fields)))

        t = special_names[field[:-3]] if field[:-3] in special_names else field[:-3]+'s'
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

    if 'filter' in payload:
        key = 'filter'
        dbobj = getattr(dbobj, key)(payload[key])
    print dbobj    
    #for data in joined_data:
    #    d = {}
    #    d.update(data['left'])
    #    new_right_side = data['right'].items()
    #    new_right_side = dict([('organization_'+item[0], item[1]) for item in new_right_side])
    #    d.update(new_right_side)
    #    modified_joined_data.append(d)

    if 'order_by' in payload:
        for o in payload['order_by']:
            if o['direction'] == 'desc':
                dbobj = getattr(dbobj, 'order_by')(r.desc(o['field']))
            else:
                dbobj = getattr(dbobj, 'order_by')(o['field']) 
    
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
                base = r.db('public').table(payload['table']).filter(lambda case: case[payload['has_string']['field']].match('.*?'+payload['has_string']['value']+'.*?'))
            denominator = base.count().run()

            numerator = base.filter({payload['numerator']['field']: payload['numerator']['value']}).count().run() 

            if denominator:
                percentage = float(numerator)/denominator
                percentage = "{:.0%}".format(percentage)+' (%s/%s)' % (numerator, denominator)
            else:
                percentage = 'Error: No denominator'    
            results = {'numerator': numerator, 'denominator': denominator, 'percentage': percentage}
        elif payload['action'] == 'get_list':
            results = [item[payload['field']] for item in list(r.db('public').table(payload['table']).pluck(payload['field']).run())]
        elif payload['action'] == 'get_set':
            results = list(set([item[payload['field']] for item in list(r.db('public').table(payload['table']).pluck(payload['field']).run())]))
        elif payload['action'] == 'do_basic_mapping':
            dbobj = getattr(dbobj, 'pluck')(payload['field_for_key'], payload['field_for_value'])
            items = dbobj.run()
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
            items = list(dbobj.run())
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
        results['table'] = r.db('public').table('tables').get(payload['table']).run()
        if 'default_order_by' in results['table']:
            dbobj = getattr(dbobj, 'order_by')(r.desc(results['table']['default_order_by']['field']))
        special_names_reversed = {value: key for key, value in special_names.items()}
        t = payload['table']
        t = special_names_reversed[t] if t in special_names_reversed else t[:-1]
        t = t + '_id'
        results['data'] = list(dbobj.run(time_format="raw"))
        if 'linked_tables' in results['table']:

            for linked_table in results['table']['linked_tables']:
                linked_table_data = list(r.db('public').table(linked_table).run(time_format="raw"))
                for i, row in enumerate(results['data']):
                    print i
                    row[linked_table] = [item for item in linked_table_data if item.get(t) == row['id']]
                    # consider using group e.g. r.db('public').table('police_internal_affairs_allegations').group('person_id').run()
                    #row[linked_table] = list(r.db('public').table(linked_table).filter({t: row['id']}).run(time_format="raw"))

        results['fields'] = [row.keys() for row in results['data']]
        results['fields'] = list(set(list(itertools.chain.from_iterable(results['fields']))))
        results['number_of_rows'] = len(results['data'])
        results['percentages'] = []
        results['group_counts'] = []
        for field in results['fields']:
            if not field.endswith('_id'):
                continue
            t = special_names[field[:-3]] if field[:-3] in special_names else field[:-3]+'s'
            g = r.db('public').table(t).group('id').run()
            results['group_counts'].append([t, [[g[item[0]], item[1]] for item in list(sorted(dbobj.group(field).count().run().items(), key=lambda x:x[1], reverse=True))][:10]])
        results['group_counts'].sort(key=lambda x:x[0])

        likely_boolean_fields = [field for field in results['fields'] if field.startswith('is_')]
        # remove if the field in a filter
        if 'filter' in payload:
            for field in payload['filter'].keys():
                if field in likely_boolean_fields:
                    likely_boolean_fields.remove(field)
        for field in likely_boolean_fields:
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
        