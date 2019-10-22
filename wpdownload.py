#! py -3.7

import argparse
import os
import re
import time
import urllib3
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser("Download mp3 from WP SermonManager export xml")
parser.add_argument('-t', '--test', action='store_true', help="Print to screen but don't download anything")
parser.add_argument('xml', type=str, help='Wordpress xml export file to process')
args = parser.parse_args()

tree = ET.parse(args.xml)
root = tree.getroot()

for child in root:
    if child.tag == 'channel': # there's only one
        channel = child

http = urllib3.PoolManager()

for item in channel:
    if item.tag != 'item': continue
    for child in item:
        tag = child.tag
        if tag == 'title':
            title = child.text
        if tag == 'category':
            #print(child.attrib['domain'])
            if child.attrib['domain'] == 'wpfc_bible_book':    book = child.text
            if child.attrib['domain'] == 'wpfc_preacher':  preacher = child.text
        if re.search(r'postmeta$', tag):
            if child[0].text == 'sermon_audio':                 url = child[1].text

    if args.test:
        print(title, book, preacher, url)
        continue

    fname = os.path.basename(url)
    print('{:50s}'.format(fname), end='', flush=True)

    dir = 'mp3/' + book
    if not os.path.exists(dir):
        os.mkdir(dir)
    path = os.path.join(dir, fname)

    # download if we don't have it already
    if os.path.exists(path):
        print(' PRESENT')
        continue
    else:
        print(' DOWNLOADING ', end='', flush=True)
        t0 = time.time()
        r = http.request('GET', url)
        dt = time.time() - t0
        if r.status == 200:
            mb = len(r.data)/1024/1024
            with open(path, 'wb') as file:
                file.write(r.data)
            print(' {:.1f}mb  {:.1f}s {:.3f}mb/s'.format(mb, dt, mb/dt))
        else:
            print('FAIL', url)
            continue







