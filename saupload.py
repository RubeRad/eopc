from datetime import date, datetime
import glob
import os
import re
import sys
import sermonaudio
from sermonaudio.broadcaster.requests import BroadcasterAPIError, Broadcaster
from sermonaudio.models import SermonEventType

def book2osis(b):
   if   b.lower() == 'judges':  return 'JDG'
   elif b.lower() == 'ezekiel': return 'EZK'
   elif b.lower() == 'joel':    return 'JOL'
   elif b.lower() == 'nahum':   return 'NAM'
   elif b.lower() == 'mark':    return 'MRK'
   elif b.lower() == 'john':    return 'JHN'
   elif b.lower() == 'philippians': return 'PHP'
   elif b.lower() == 'philemon':return 'PHM'
   elif b.lower() == 'james':   return 'JAS'
   elif b.lower() == '1john':   return '1JN'
   elif b.lower() == '2john':   return '2JN'
   elif b.lower() == '3john':   return '3JN'
   elif re.search('song', b, re.IGNORECASE): return 'SNG'
   else:
      return b[:3].upper()


def osis_passage(p):
   # book 1:2-3:4
   mch = re.fullmatch(r'(\d?\w+?)(\d+)v(\d+)-(\d+)v(\d+)', p)
   if mch:
      osis = book2osis(mch.group(1))
      chp1 = mch.group(2)
      vrs1 = mch.group(3)
      chp2 = mch.group(4)
      vrs2 = mch.group(5)
      return '{} {}:{}-{}:{}'.format(osis, chp1, vrs1, chp2, vrs2)

   # book 1:2-3
   mch = re.fullmatch(r'(\d?\w+?)(\d+)v(\d+)-(\d+)', p)
   if mch:
      osis = book2osis(mch.group(1))
      chap = mch.group(2)
      vrs1 = mch.group(3)
      vrs2 = mch.group(4)
      return '{} {}:{}-{}'.format(osis, chap, vrs1, vrs2)

   # book 1-2
   mch = re.fullmatch(r'(\d?\w+?)(\d+)-(\d+)', p)
   if mch:
      osis = book2osis(mch.group(1))
      chp1 = mch.group(2)
      chp2 = mch.group(3)
      return '{} {}-{}'.format(osis, chp1, chp2)

   # book 1
   mch = re.fullmatch(r'(\d?\w+?)(\d+)', p)
   if mch:
      osis = book2osis(mch.group(1))
      chap = mch.group(2)
      return '{} {}'.format(osis, chap)

   # special cases
   if p == 'ezra-nehemiah':
      return 'EZR 1-10; NEH 1-13'
   if p == 'proverbs':
      return 'PRV 1-31'

   # else
   raise ValueError('cant understand passage: '+p)



def nice_passage(p):
   nice = p.title()
   nice = re.sub(r'^([123])', r'\1 ', nice)
   nice = re.sub(r'(\D)(\d)', r'\1 \2', nice, count=1)
   nice = re.sub(r'(\d)V(\d)', r'\1:\2', nice)
   return nice




with open(sys.argv[0]+'.key') as file:
   for line in file:
      sermonaudio.set_api_key(line.rstrip())
      break

mp3s = glob.glob('*/*.mp3')

for path in mp3s:
   base = os.path.basename(path)
   file, mp3 = os.path.splitext(base)
   if mp3 != '.mp3': raise ValueError("Must be mp3")

   date, ampm, pasg, prch = file.split('_')

   if not re.match(r'\d\d\d\d-\d\d-\d\d', date): raise ValueError('Date not formatted correctly')
   if not re.match(r'([apx])?m', ampm): raise ValueError('am/pm/xm not formatted correctly')

   osis = osis_passage(pasg)
   nice = nice_passage(pasg)

   print('{:20}{:30}{}'.format(osis, nice, pasg))

   stophere=1




