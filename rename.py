#! /usr/bin/env python
import glob
import os
import re
import shutil


date_of = {}
ampm_of = {}
pasg_of = {}
book_of = {}
prch_of = {}
url__of = {}
with open('./eopc.wordpress.2019-10-16.xml') as xml:
   for line in xml:
      mch = re.search(r'<item>', line)
      if mch:
         ampm = 'xm'
         date = 'unknown'
         book = 'unknown'
         prch = 'unknown'
         pasg = 'unknown'

      mch = re.search(r'<wp:post_date.*(\d\d\d\d-\d\d-\d\d) ', line)
      if mch: date = mch.group(1)

      if re.search(r'orning', line): ampm = 'am'
      if re.search(r'vening', line): ampm = 'pm'

      mch = re.search(r'wpfc_bible_book.*CDATA\[(.*?)\]', line)
      if mch: book = mch.group(1)

      mch = re.search(r'wpfc_preacher.*CDATA\[(.*?)\]', line)
      if mch: prch = mch.group(1)
      if re.search(r'Keele', line): prch = 'Rev. Zach Keele'

      mch = re.search(r'meta_key.*CDATA\[(.*?)\]]', line)
      if mch:
         meta_key = mch.group(1)
      mch = re.search(r'meta_value.*CDATA\[(.*?)\]]', line)
      if mch:
         if meta_key == 'bible_passage':
            pasg = mch.group(1)
         elif meta_key == 'sermon_audio':
            url = mch.group(1)
            mp3 = os.path.basename(url)

            if re.search(r'isaac', mp3):
               stophere=1

            if pasg == 'unknown':
               mch = re.search(r'([A-Za-z]+)[-_.]?(\d+)[-_.v]+(\d+)[-_.v](\d+)[-_.v](\d+)', mp3)
               if mch:
                  pasg = '{} {}:{}-{}:{}'.format(mch.group(1), mch.group(2), mch.group(3), mch.group(4), mch.group(5))
               else:
                  mch = re.search(r'([A-Za-z]+)[-_.]?(\d+)[-_.v]+(\d+)[-_.v](\d+)', mp3)
                  if mch:
                     pasg = '{} {}:{}-{}'.format(mch.group(1), mch.group(2), mch.group(3), mch.group(4))
                  else:
                     mch = re.search(r'([A-Za-z]+)[-_.]?(\d+)', mp3)
                     if mch:
                        pasg = '{} {}'.format(mch.group(1), mch.group(2))
                     else:
                        stophere=1 # still unknown


            if re.search(r'Proverbs_Summary', mp3):
               pasg = 'Proverbs'
               book = 'Proverbs'

            if book == 'unknown':
               mch = re.search(r'([123]? ?\w+)', pasg)
               if mch: book = mch.group(1)

            if book == 'unknown':
               stophere=1

            #print("|".join((date, ampm, book, pasg, prch, url, mp3)))
            date_of[mp3] = date
            ampm_of[mp3] = ampm
            pasg_of[mp3] = pasg
            book_of[mp3] = book
            prch_of[mp3] = prch
            url__of[mp3] = url

csv_date_of = {}
csv_ampm_of = {}
with open('./dates_sermons.csv') as csv:
   for line in csv:
      words = line.split(',')
      for i in range(3,len(words)):
         if re.search(r'\.mp3$', words[i]):
            #print(words[i])
            date_of[words[i]] = words[0]
            if i==3 or i==4: ampm_of[words[i]] = 'AM'
            else:            ampm_of[words[i]] = 'PM'


for mp3, date in date_of.items():
   if date == '2000-01-02':
      stophere=1
      if mp3 in csv_date_of:
         date_of[mp3] = csv_date_of[mp3]
         #print('Date corrected to', date_of[mp3], ':', mp3)
      else:
         print('Date unknown for', mp3)



inndir = '/c/Users/reuben/eopc/mp3'
newdir = '/c/Users/reuben/eopc/new'
mp3s = glob.glob(inndir + '/*/*.mp3')

for path in mp3s:
   mp3 = os.path.basename(path)
   if mp3 in date_of and mp3 in ampm_of and mp3 in pasg_of and mp3 in book_of and mp3 in prch_of:
      pasg = re.sub(r':', 'v', pasg_of[mp3])
      pasg = re.sub(r'-', '_', pasg)
      pasg = re.sub(r'\s', '', pasg)
      pasg = re.sub(r'orintians', 'orinthians', pasg)
      pasg = re.sub('_', '-', pasg)
      if re.search(r'\d+\.\d+', pasg):
         stophere=1
      pasg = re.sub(r'(\d)\.(\d)', r'\1v\2', pasg)

      book = re.sub(r'\s', '', book_of[mp3])
      book = re.sub(r'orintians', 'orinthians', book)
      dir = os.path.join(newdir, book.lower())
      if not os.path.isdir(dir):
         os.mkdir(dir)

      url = url__of[mp3]

      prch = prch_of[mp3]
      mch = re.search(r'(van.*)', prch, re.IGNORECASE)
      if mch:
         prch = mch.group(1)
         prch = re.sub('\s', '', prch)
      else:
         mch = re.search('isaac', prch, re.IGNORECASE)
         if mch:
            prch = 'isaac-baugh'
         else:
            names = prch.split(' ')
            prch = names[-1]

      ampm = ampm_of[mp3]
      if ampm == '_m' and prch.lower() == 'keele':
         if      re.search('Matt',  book, re.IGNORECASE) or \
                 re.search('Sam',   book, re.IGNORECASE) or \
                 re.search('Act',   book, re.IGNORECASE) or \
                 re.search('Thess', book, re.IGNORECASE) or \
                 re.search('Cor',   book, re.IGNORECASE) or \
                 re.search('John',  book, re.IGNORECASE) or \
                 re.search('James', book, re.IGNORECASE) or \
                 re.search('Rev',   book, re.IGNORECASE):
            ampm = 'am'
         elif    re.search('Ezek', book, re.IGNORECASE) or \
                 re.search('Judg', book, re.IGNORECASE) or \
                 re.search('Ecc',  book, re.IGNORECASE) or \
                 re.search('Hos',  book, re.IGNORECASE) or \
                 re.search('Deut', book, re.IGNORECASE) or \
                 re.search('Jer',  book, re.IGNORECASE) or \
                 re.search('Ezr',  book, re.IGNORECASE) or \
                 re.search('Neh',  book, re.IGNORECASE) or \
                 re.search('Num',  book, re.IGNORECASE):
            ampm = 'pm'
         else:
            stophere=1

      newname = '{}_{}_{}_{}.mp3'.format(date_of[mp3], ampm.lower(), pasg.lower(), prch.lower())
      newpath = os.path.join(dir, newname)

      print("|".join((date, ampm, book, pasg, prch, prch_of[mp3], url, mp3, newname)))

      shutil.copyfile(path, newpath)
   else:
      print('Something missing for', mp3)
