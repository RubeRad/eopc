#! /usr/bin/env python3

import re
import sys
import requests


def find_non_ascii(txt):
    # 127 is DEL, 126 is ~ so maybe 126 would be a better limit
    # but this allows 10=LF=\n etc
    return [ch for ch in txt if ord(ch) > 127]


def fetch_esv(ref):
    esv_org_api_key = '6b2ebf6f70b95c12e8aea92c80c9291be673d2d8'
    esv_org_api_url = 'https://api.esv.org/v3/passage/text'

    hdr = {'Authorization': f'Token {esv_org_api_key}'}
    par = {'q' : 'Phil+3:4-10',
           'include-headings' : False,
           'include-footnotes' : False,
           'include-verse-numbers': False,
           'include-short-copyright': False,
           'include-passage-references': False,
           'line-length' : 80}

    response = requests.get(esv_org_api_url, params=par, headers=hdr)
    passage  = response.json()['passages'][0]

    # fix "em dashes" -- thx ChatGPT!
    passage = re.sub('\u2014', ' -- ', passage)

    # check for any other non-printable characters
    non_ascii = find_non_ascii(passage)
    if non_ascii:
        print('non-printable! ', non_ascii)

    return(passage)


nt = fetch_esv('Phil+3:4-10')
print(nt)




