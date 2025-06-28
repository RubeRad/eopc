#! /usr/bin/env python3

import argparse
import re
import sys
import requests


def find_non_ascii(txt):
    # 127 is DEL, 126 is ~ so maybe 126 would be a better limit
    # but this allows 10=LF=\n etc
    return [ch for ch in txt if ord(ch) > 127]


def fetch_esv(ref):
    esv_org_api_key = 'oopxdontpostthisonline'
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


def fetch_tph(ref):
    url = 'https://hymnary.org/hymn/TPH2018/'
    # TBD parse verse numbers like 123v1-3
    url += ref
    #print(url)
    html = requests.get(url)

    mch = re.search(r'<div id="text">(.*?)</div>', html.text, re.DOTALL)
    if mch:
        lyr = mch.group(1)
        # Remove ^A (\x01) and ^M (\r or \x0D)
        lyr = re.sub(r'[\x01\r]', '', lyr)
        lyr = re.sub(r'<p>', '', lyr)
        lyr = re.sub(r'</p>', '\n', lyr)
        lyr = re.sub(r'<br />', '', lyr)
        lyr = re.sub(r'(\d )', r'\n\1', lyr)

        # TBD expand [Refrain]
        return f'Trinity Psalter Hymnal {ref}{lyr}\n\n'

    else:
        with open(f'tph{ref}.html', 'w') as out:
            print(html.text, file=out)
        return f'{ref}\nNot found online\n'
    

amliturgy='''CALL
DOX
LAWGOSPEL
SONG
ESV
SONG
ESV
SERMON
LP
CREED
SUPPER
SONG
OFFERING
TH11
BENE
'''

pmliturgy='''CALL
DOX
CAT
SONG
ESV
SONG
SERMON
SUPPER
SONG
OFFERING
BENE
'''

amdox = '''MORNING DOXOLOGY 567

Praise God from whom all blessings flow;
praise him, all creatures here below;
praise him above, ye heav'nly host:
praise Father, Son, and Holy Ghost.
Amen.'''

pmdox = '''EVENING DOXOLOGY 563

1 May the grace of Christ our Savior
and the Father's boundless love,
with the Holy Spirit's favor,
rest upon us from above.

2 Thus may we abide in union
with each other and the Lord,
and possess, in sweet communion,
joys which earth cannot afford.
Amen.'''

lords_prayer = '''Our Father, who art in heaven
Hallowed by thy name.
Your kingdom come, 
Your will be done,
On earth as it is in heaven.
Give us this day our daily bread,
and forgive us our debts,
as we forgive our debtors.
Lead us not into temptation,
but deliver us from evil.
For thine is the kingdom, the power, and the glory forever, 
Amen

'''

apostles = '''Apostle’s Creed

I believe in God the father almighty,
Maker of heaven and earth

I believe in Jesus Christ, his only begotten son, our Lord;
who was conceived by the Holy Spirit, born of the virgin Mary;
suffered under Pontius Pilate;
was crucified, dead, and buried;
he descended into hell;
the third day he rose again from the dead;
he ascended into heaven,
and sits at the right hand of God the Father Almighty;
from there he shall come to judge the living and the dead.

I believe in the Holy Spirit;
the holy catholic church;
the communion of saints;
the forgiveness of sins;
the resurrection of the body;
and the life everlasting. Amen.

'''

nicene = '''Nicene Creed

I believe in one God, the Father almighty,
Maker of heaven and earth,
and of all things visible and invisible

And in one Lord Jesus Christ, the only begotten Son of God,
begotten of the Father before all worlds;
God of God, Light of Light, very God of very God;
begotten, not made, being of one substance with the Father,
by whom all things were made.
Who, for us men and for our salvation,
came down from heaven
and was incarnate by the Holy Spirit of the virgin Mary
and was made man;
and was crucified also for us under Pontius Pilate;
he suffered and was buried;
and the third day he rose again, according to the Scriptures;
and ascended into heaven, and sits on the right hand of the Father;
and he shall come again, with glory, to judge the living and the dead;
whose kingdom shall have no end.

And I believe in the Holy Spirit, the Lord and Giver of life;
who proceeds from the Father and the Son;
who with the Father and the Son together is worshipped and glorified
who spoke by the prophets.
And I believe in only holy catholic and apostolic church.
I acknowledge one baptism for the remission of sins;
and I look for the resurrection of the dead,
and the life of the world to come. Amen.

'''

th11 = '''Closing Hymn 11

1 Now blessed be the Lord our God
The God of Israel
for he alone does wondrous works
in glory that excel

2 And blessed be his glorious name
to all eternity; 
the whole earth let his glory fill.
Amen, so let it be.

'''



parser = argparse.ArgumentParser('Create a text document of an EOPC service')
parser.add_argument('--pm',     action='store_true', help='PM liturgy')
parser.add_argument('--supper', action='store_true', help="Lord's Supper")
parser.add_argument('refs', nargs='+', help='References to Trinity Psalter Hymnal or ESV')
args = parser.parse_args()


txt = pmliturgy if args.pm else amliturgy

txt = re.sub('CALL', 'Call to worship\n\n', txt)

dox = pmdox if args.pm else amdox
txt = re.sub('DOX', dox+'\n\n', txt)

txt = re.sub('LAWGOSPEL',
             'Reading of the Law / Confession of Sin / Pronouncement of the Gospel\n\n',
             txt)

if args.pm:
    txt = re.sub('SERMON', 'Prayer of Illumination; Sermon; Pastoral Prayer\n\n', txt)
else:
    txt = re.sub('SERMON',
                 "Prayer of Illumination; Sermon; Pastoral Prayer, with the Lord's Prayer:\n",
                 txt)

txt = re.sub('LP', lords_prayer, txt)

creed = nicene if args.supper else apostles
txt = re.sub('CREED', creed, txt)

txt = re.sub('SUPPER', "Lord's Supper\n\n", txt)

txt = re.sub('OFFERING', "Offering\n\n", txt)

txt = re.sub('BENE', "Benediction\n", txt)

txt = re.sub('TH11', th11, txt)

for ref in args.refs:
    if ref[0] == 'h':
        song = fetch_tph(ref[1:])
        txt = re.sub('SONG', song, txt, count=1)
    else:
        pref = re.sub(r'\+', ' ', ref)
        esv = fetch_esv(ref)
        all = f'{pref}\n{esv}'
        txt = re.sub('ESV', all, txt, count=1)



print(txt)



