import requests
import hashlib
import os
from bs4 import BeautifulSoup
import urlparse

base = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../')

def get_text_of_all_pdfs_linked_from(url):
    url_hash = hash_object = hashlib.md5(url)
    url_hash = hash_object.hexdigest()
    os.system('mkdir %s.crawler_data' % (base))
    os.system('mkdir %s.crawler_data/%s/' % (base, url_hash))
    os.system('mkdir %s.crawler_data/%s/pdfs/' % (base, url_hash))
    os.system('mkdir %s.crawler_data/%s/txts/' % (base, url_hash))
    html = requests.get(url).text
    docs = [{'url': urlparse.urljoin(url, link['href']), 'tag': link.contents[0]} for link in soup.find_all('a', href=True) if link['href'].endswith('.pdf')]
    for doc in docs:
        doc['filename'] = doc['ur'].split('/')[-1]
    for doc in docs:
        if not doc['filename'] in os.listdir(base+'.crawler_data/'+url_hash+'/pdfs'):
            os.system('wget -O %s.crawler_data/%s/pdfs/%s %s' % (base, url_hash, doc['filename'], doc['url']))
     
            os.system('pdf2txt.py -A %s.crawler_data/%s/pdfs/%s > %s.crawler_data/%s/txts/%s' % (base, url_hash, doc['filename'], base, url_hash, doc['filename'][:-4]+'.txt'))
        with open('%s.crawler_data/%s/txts/%s' % (base, url_hash, doc['filename'][:-4]+'.txt')) as f:
            
             doc['text'] = f.read()
    return docs