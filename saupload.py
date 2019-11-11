#! /usr/bin/python3.6

from datetime import date, datetime
import dateutil.parser
import glob
import os
import re
import sys
import sermonaudio
from sermonaudio.node.requests import Node, NodeAPIError
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
   mch = re.fullmatch(r'(\d?\w+?)(\d+)\.?v(\d+)-(\d+)', p)
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
   if p == 'deut4v25-40;deut30':
      return 'DEU 4:25-40'
   if p == 'matt3v1-2;matt4v17':
      return 'MAT 3:1-2'

   # else
   raise ValueError('cant understand passage: '+p)


def osis2parts(p):
   mch = re.match(r'(\w+)\s?(\S*)', p)
   book = mch.group(1)
   rest = mch.group(2)
   nums = re.findall(r'\d+', rest)
   if len(nums)==0:
      return (book, None, None, None, None)
   if len(nums)==1:
      return (book, nums[0], None, None, None)
   if len(nums)==2:
      return (book, nums[0], nums[1], None, None)
   if len(nums)==3:
      return (book, nums[0], nums[1], nums[0], nums[2])
   if len(nums)==4:
      return (book, nums[0], nums[1], nums[2], nums[3])



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


preacher = {}
dir = os.path.dirname(sys.argv[0])
piper = os.path.join(dir, 'rename.pipe')
with open(piper) as file:
  for line in file:
    if re.search('Date unknown for', line):
       continue
    words = line.split('|')
    mp3 = words[8].rstrip()
    prch = words[5]
    preacher[mp3] = prch
    stophere=1


mp3s = []
if len(sys.argv) > 1:
   for i in range(1,len(sys.argv)):
      arg = sys.argv[i]
      if re.search(r'\.mp3$', arg):
         mp3s.append(arg)
      else:
         mp3s.extend(glob.glob(arg+'/*.mp3'))
else:
   mp3s = glob.glob('*/*.mp3')

new_sermon = None

for path in mp3s:
   base = os.path.basename(path)
   file, mp3 = os.path.splitext(base)
   if mp3 != '.mp3': raise ValueError("Must be mp3")

   iso, ampm, pasg, prch = file.split('_')

   if not re.match(r'\d\d\d\d-\d\d-\d\d', iso): raise ValueError('Date not formatted correctly')
   if not re.match(r'([apx])?m', ampm): raise ValueError('am/pm/xm not formatted correctly')

   osis = osis_passage(pasg)
   nice = nice_passage(pasg)
   preach = preacher[base]
   d = dateutil.parser.parse(iso).date()

   (b, ch1, vs1, ch2, vs2) = osis2parts(osis)
   #resp = Node.get_sermons(book=b, chapter=ch1, chapter_end=ch2, verse=vs1, verse_end=vs2)

   if   ampm == 'am': typ = SermonEventType.SUNDAY_AM
   elif ampm == 'pm': typ = SermonEventType.SUNDAY_PM
   else:              typ = SermonEventType.SUNDAY_SERVICE


   print('{:20}{:30}{:15}{}   {}'.format(osis, nice, pasg, preach, d))

   stophere=1

   new_sermon = Broadcaster.create_or_update_sermon(
           accept_copyright=True,
           full_title=nice,
           speaker_name=preach,
           preach_date=d,
           publish_timestamp=datetime.now(),
           event_type=typ,
           language_code="en",
           sermon_id=None,
           display_title=nice,
           subtitle=None,
           bible_text=nice,
           more_info_text=None,
           keywords=None,
   )

   if new_sermon is None:
      raise ValueError('Sermon create failed!')

   fullpath = os.path.abspath(path)
   result = Broadcaster.upload_audio(sermon_id=new_sermon.sermon_id,
                                     path=fullpath)

   #result = Broadcaster.delete_sermon(new_sermon.sermon_id)




