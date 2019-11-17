from datetime import date, datetime
import glob
import os
import re
import sys


dir = '/c/Users/reuben/eopc/new'
mp3s = glob.glob(os.path.join(dir, '*/*.mp3'))

mp32date = {}
with open('dates_sermons.csv') as file:
   for line in file