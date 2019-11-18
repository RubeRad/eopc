#! /usr/bin/env python3

import argparse
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


def die(msg):
   print(msg)
   print('') # extra blank line improves readability
   exit(0)


def confirm(q, onno):
   yn = input(q + ' [N/y]')
   if re.search(r'^y', yn, re.IGNORECASE):
      return
   else:
      die(onno)


def set_api_key():
   fname = sys.argv[0]+'.key'
   if not os.path.exists(fname):
      die('Must put API key in adjacent text file '+fname)

   with open(fname) as file:
      for line in file:
         key = line.rstrip()
         print('Found sermonaudio API key in', fname, ': ', key)
         sermonaudio.set_api_key(key)
         break


def get_date(iso):
   d = dateutil.parser.parse(iso).date()
   # verify sunday
   if d.weekday() != 6: # 6==sunday
      confirm('That date is not a Sunday, are you sure?',
              'Please specify the correct --date')
   return d


def get_full_speaker(speak):
   # nicknames file has lines formatted sipmply as, for example:
   #   nickname Full Name
   #   pastor The Good and Right Rev Dr First McLasterman, M.A., M. Div., Ph. D.
   #   intern Johnny McLicentiate
   #   # this comment will be ignored
   #   bob Robert Visitor # so will this one
   # etc
   fname = sys.argv[0]+'.speakers'
   if os.path.exists(fname):
      print('Found speaker nicknames file', fname)
   else:
      print('Speaker nicknames file', fname, 'not found')

   nicks = {}
   with open(fname) as file:
      for line in file:
         line = re.sub(r'\#.*', '', line) # strip comments
         line = re.sub(r'\s+$', '', line) # strip trailing whitespace
         if not line:
            continue
         mch = re.fullmatch(r'(\w+)\s+(.*)', line)
         if not mch:
            print(fname, 'must have lines formatted like "nickname  The Full Name"')
         nicks[mch.group(1)] = mch.group(2)

   if speak not in nicks:
      print('Fuller name not found for "' + speak + "'")
      confirm("Does this match exactly the speaker's name in sermonaudio.com?",
              "Please specify exact speaker name or speaker nickname with --speaker")
      return speak # if we don't exit inside confirm

   # else speak is a nickname from saupload.py.speakers
   return nicks[speak]



def check_bibref(p):
   if not p:
      die('Please use like --bibref "Book C:V-V" or "Book C:V-C:V" or "Book C" to specify the sermon text')

   mch = re.search(r'^[123]?\s?([a-z]+)', p, re.IGNORECASE)
   if not mch:
      die("Could not understand bibref '"+p+"'")

   book = mch.group(1)
   if len(book)<=3 and book.lower()!='job':
      die('sermonaudio.com does not accept abbreviated book names')



if __name__ == '__main__':
   parser = argparse.ArgumentParser("Use the sermonaudio API to upload a sermon mp3")
   parser.add_argument('-s', '--speaker', type=str, help='Speaker full name or nickname from saupload.py.speakers file')
   parser.add_argument('-d', '--date',    type=str, help='Date in ISO format: YYYY-MM-DD')
   parser.add_argument('-a', '--am', action='store_true', help='SUNDAY_AM service type')
   parser.add_argument('-p', '--pm', action='store_true', help='SUNDAY_PM service type')
   parser.add_argument('-b', '--bibref',   type=str, help='Bible passage (as per sermonaudio, no abbreviations')
   parser.add_argument('-t', '--title',    type=str, help='Optional sermon title (default to bibref)')
   parser.add_argument('-u', '--subtitle', type=str, help='Optional sermon subtitle')
   parser.add_argument('mp3', type=str, help='mp3 file')
   args = parser.parse_args()


   set_api_key() # from adjacent file saupload.py.key


   if not os.path.exists(args.mp3):
      die("Can't find mp3 file: '"+args.mp3+"'")


   # not defaulting to AM or just SUNDAY_SERVICE, because Christians should worship morning and
   # evening on the Lord's Day. See R. Scott Clark, Recovering the Reformed Confession, ch 8
   if not args.am and not args.pm:
      die('Must specify either --am or --pm')


   if args.am:
      service = SermonEventType.SUNDAY_AM
      svc_str =                'SUNDAY_AM'
   elif args.pm:
      service = SermonEventType.SUNDAY_PM
      svc_str =                'SUNDAY_PM'
   else:
      die('ERROR: Cannot specify both AM and PM')


   # make sure the date is a sunday
   d = get_date(args.date)


   # fetch full speaker name from saupload.py.speakers in case --speaker nickname
   if not args.speaker:
      args.speaker = 'pastor' # default to nickname 'pastor'
   speaker = get_full_speaker(args.speaker)


   # make sure the passage does not abbreviate the book
   check_bibref(args.bibref)
   if not args.title:
      args.title = args.bibref


   # series is either None or a string if the --series option is used


   # print summary and verify
   print('\nDate:    ', d)
   print('AM/PM:   ', svc_str)
   print('Speaker: ', speaker)
   print('Passage: ', args.bibref)
   if args.title:
      print('Title:   ', args.title)
   if args.subtitle:
      print('Subtitle:', args.subtitle)

   confirm('Is this all correct?', 'OK, buhbye')



   try:
      print('\nCreating new sermon...')
      new_sermon = Broadcaster.create_or_update_sermon(
              accept_copyright=True,
              full_title=args.title,
              speaker_name=speaker,
              preach_date=d,
              publish_timestamp=datetime.now(),
              event_type=service,
              language_code="en",
              sermon_id=None,
              display_title=args.bibref,
              subtitle=args.subtitle,
              bible_text=args.bibref,
              more_info_text=None,
              keywords=None,
      )

      if new_sermon is None:
         die('Sermon creation failed!')
      # else
      url = 'https://www.sermonaudio.com/sermoninfo.asp?SID=' + str(new_sermon.sermon_id)
      print('New sermon created:', url)


      print('\nUploading mp3 file...')
      fullpath = os.path.abspath(args.mp3)
      Broadcaster.upload_audio(sermon_id=new_sermon.sermon_id,
                               path=fullpath)
      print('Success!')

   except:
      die('Exception caught :-(')
