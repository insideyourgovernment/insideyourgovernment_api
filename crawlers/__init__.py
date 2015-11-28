import requests
import hashlib
import os
from bs4 import BeautifulSoup
import urlparse
import re

base = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../')

def process_url(base_url, url):
    new_url = 'http://'+urlparse.urljoin(urlparse.urlparse(base_url)['netloc'], url) if url.startswith('/') else urlparse.urljoin(base_url, url)
    return new_url
 
def get_text_of_all_pdfs_linked_from(url):
    url_hash = hash_object = hashlib.md5(url)
    url_hash = hash_object.hexdigest()
    os.system('mkdir %s.crawler_data' % (base))
    os.system('mkdir %s.crawler_data/%s/' % (base, url_hash))
    os.system('mkdir %s.crawler_data/%s/pdfs/' % (base, url_hash))
    os.system('mkdir %s.crawler_data/%s/txts/' % (base, url_hash))
    # <base href="http://www.seattle.gov/" />	
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    base_url = url
    m = re.search('<base href="(?P<url>.*?)"', html)
    if m:
        base_url = m.group('url')
    print base_url
    
    docs = [{'url': process_url(base_url, link['href']), 'tag': link.contents[0]} for link in soup.find_all('a', href=True) if link['href'].endswith('.pdf')]
    print docs
    for doc in docs:
        doc['filename'] = doc['url'].split('/')[-1]
    for doc in docs:
        if True:
        #if not doc['filename'] in os.listdir(base+'.crawler_data/'+url_hash+'/pdfs'):
            os.system('wget -O %s.crawler_data/%s/pdfs/%s %s' % (base, url_hash, doc['filename'], doc['url']))
     
            os.system('pdf2txt.py -A %s.crawler_data/%s/pdfs/%s > %s.crawler_data/%s/txts/%s' % (base, url_hash, doc['filename'], base, url_hash, doc['filename'][:-4]+'.txt'))
        with open('%s.crawler_data/%s/txts/%s' % (base, url_hash, doc['filename'][:-4]+'.txt')) as f:
            
             doc['text'] = f.read()
    return docs