import requests
import re
import os
base = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../')
def download():
    os.system('mkdir %s.crawler_data' % (base))
    os.system('mkdir %s.crawler_data/seattle_police_internal_affairs_closed_cases/' % (base))
    os.system('mkdir %s.crawler_data/seattle_police_internal_affairs_closed_cases/pdfs/' % (base))
    os.system('mkdir %s.crawler_data/seattle_police_internal_affairs_closed_cases/txts/' % (base))
    html = requests.get('http://www.seattle.gov/opa/closed-case-summaries').text
    os.system('mkdir pdfs')
    files = re.findall('ClosedCaseSummaries/(?P<filename>.*?)\.pdf', html)
    print files
    for f in files:
        if not f+'.pdf' in os.listdir(base+'seattle_police_internal_affairs_closed_cases/pdfs'):
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
    parse_txt_files(new_files)
