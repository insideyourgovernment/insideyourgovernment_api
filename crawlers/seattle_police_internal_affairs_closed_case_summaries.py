import requests
import re
import os
base = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../')
os.system('mkdir %s.crawler_data' % (base))
os.system('mkdir %s.crawler_data/base/' % (base))
if False:
    html = requests.get('http://www.seattle.gov/opa/closed-case-summaries').text
    os.system('mkdir pdfs')
    files = re.findall('ClosedCaseSummaries/(?P<filename>.*?)\.pdf', html)
    print files
    for f in files:
        if not f+'.pdf' in os.listdir('/home/ubuntu/redactvideodotorg/opa_closed_case_summaries/pdfs'):
            os.system('wget -O /home/ubuntu/redactvideodotorg/opa_closed_case_summaries/pdfs/%s.pdf http://www.seattle.gov/Documents/Departments/OPA/ClosedCaseSummaries/%s.pdf' % (f, f))
    import os
    #os.system('rm /home/ubuntu/redactvideodotorg/opa_closed_case_summaries/txts/*')
    os.system('mkdir /home/ubuntu/redactvideodotorg/opa_closed_case_summaries/txts')
    files = sorted([f for f in os.listdir('/home/ubuntu/redactvideodotorg/opa_closed_case_summaries/pdfs')])
    new_files = []
    for filename in files:
        print filename
        #os.system('pdf2txt.py pdfs/%s > txts/%s' % (filename, filename[:-4]+'.txt'))
        if not filename[:-4]+'.txt' in os.listdir('/home/ubuntu/redactvideodotorg/opa_closed_case_summaries/txts'):
            print 'converting'
            os.system('pdf2txt.py -A /home/ubuntu/redactvideodotorg/opa_closed_case_summaries/pdfs/%s > /home/ubuntu/redactvideodotorg/opa_closed_case_summaries/txts/%s' % (filename, filename[:-4]+'.txt'))
            new_files.append(filename[:-4]+'.txt')
    import re
    import os
    files = sorted([f for f in os.listdir('/home/ubuntu/redactvideodotorg/opa_closed_case_summaries/txts')])
    #print files[:10]
    opa_files = []
    for filename in new_files:
    #for filename in files:
        f = open('txts/'+filename, 'r')

        opa_file = str(f.read()).replace('\n', ' ').replace('  ', ' ')
        if not opa_file:
            continue
        print opa_file
        opa_file_dict = {}
        regex =  re.search('Complaint Number(?P<num>.*?)Issued', opa_file)

        opa_file_dict['Complaint number'] = regex.group('num').strip(' :').replace(' ', '') if regex else filename[:filename.find('ccs')]
        regex = re.search('Issued Date(?P<date>.*?)Named', opa_file)
        opa_file_dict['Issued date'] = regex.group('date').strip(' :') if regex else None
        regex = re.search('lssued Date(?P<date>.*?)Named', opa_file)
        if regex:
            opa_file_dict['Issued date'] = regex.group('date').strip(' :')

        regex = re.search('OPA Finding(?P<findings>.*?)Final', opa_file)
        opa_file_dict['OPA finding'] = regex.group('findings').strip(' :') if regex else None

        regex = re.search('FINDINGS(?P<findings>.*?)NOTE', opa_file,  re.MULTILINE|re.DOTALL)
        if regex:
            opa_file_dict['Findings'] = regex.group('findings').strip(' :\n').replace('\n', '')
        regex = re.search('Final Discipline\s*(?P<discipline>.*?)INCIDENT', opa_file)
        opa_file_dict['Final discipline'] = regex.group('discipline').strip(' :') if regex else None
        regex = re.search('INCIDENT SYNOPSIS(?P<synopsis>.*?)(Complaint|COMPLAINT)', opa_file,  re.MULTILINE|re.DOTALL)
        opa_file_dict['Incident synopsis'] = regex.group('synopsis').strip(' :\n').replace('\n', '') if regex else None
        regex = re.search('COMPLAINT(?P<complaint>.*?)(Complaint|INVESTIGATION)', opa_file,  re.MULTILINE|re.DOTALL)
        opa_file_dict['Complaint'] = regex.group('complaint').strip(' :\n').replace('\n', '') if regex else None
        regex = re.search('INVESTIGATION(?P<investigation>.*?)(Complaint|ANALYSIS)', opa_file,  re.MULTILINE|re.DOTALL)
        opa_file_dict['Investigation'] = regex.group('investigation').strip(' :\n').replace('\n', '') if regex else None
        regex = re.search('ANALYSIS AND CONCLUSION(?P<analysis>.*?)(Complaint|FINDINGS)', opa_file,  re.MULTILINE|re.DOTALL)
        opa_file_dict['Analysis and conclusion'] = regex.group('analysis').strip(' :\n').replace('\n', '') if regex else None
        opa_file_dict['txt'] = filename
        opa_file_dict['pdf'] = filename[:-4]+'.pdf'
        try:
            # Get the entire findings section
            f = open('txts/'+filename, 'r')

            opa_file2 = f.read()
            import re
            m = re.search('Issued(.*?)Complaint', opa_file2,  re.MULTILINE|re.DOTALL)
            if m:
                section = m.group()
                lines = section.split('\n')[3:-3]
                structured_version = []
                current = None
                opa_file_dict['is_sustained'] = False 
                for i, line in enumerate(lines):
                    if line.startswith('Named Employee'):
                        if current:
                            structured_version.append(current)
                        current = {'heading': line.strip(), 'allegations': []}
                    if line.startswith('Allegation'):
                        allegation_structure = {'heading': line.strip()}
                        allegation_structure['allegation'] = lines[i+2].strip()
                        j = 0
                        while True:
                            j += 1
                            the_line = lines[i + 2 + j]
                            if not the_line:
                                break
                            allegation_structure['allegation'] += ' '+the_line.strip()

                        current['allegations'].append(allegation_structure)
                    if line.startswith('OPA Finding'):
                        current['allegations'][-1]['opa_finding'] = lines[i+2].strip() 
                        if current['allegations'][-1]['opa_finding'] == 'Sustained':
                            opa_file_dict['is_sustained'] = True
                    if line.startswith('Final Discipline'):
                        current['final_discipline'] = lines[i+2].strip()               
                structured_version.append(current)
            opa_file_dict['Summarized results'] = structured_version
        except:
            pass
        opa_files.append(opa_file_dict)
        f.close()
    import sys  

    reload(sys)  
    sys.setdefaultencoding('utf8')
    print opa_files
    import rethinkdb as r
    conn = r.connect( "localhost", 28015).repl()
    db = r.db('opa')
    try:
        db.table_create('closed_case_summaries', primary_key='Complaint number').run(conn)
    except:
        pass
    try:
        db.table_create('closed_case_summaries_subscribers', primary_key='email').run(conn)
    except:
        pass
    db.table('closed_case_summaries').insert(opa_files, conflict='update').run(conn)
    the_html = '<table style="font-size:.9em;vertical-align:top;">'
    columns = ['Issued date', 'Complaint number', 'Complaint', 'Incident synopsis', 'Investigation', 'Analysis and conclusion', 'OPA finding', 'Final discipline']
    from dateutil.parser import parse
    import datetime
    mindate = datetime.date(datetime.MINYEAR, 1, 1)
    opa_files = sorted(opa_files, key=lambda x: parse(x['Issued date']).date() if '/' in x['Issued date'] else mindate, reverse=True)
