#! py -3

import re

counts = {}
with open('rename.pipe') as file:
   for line in file:
      if re.search(r'Date unknown for', line):
         continue
      fields = line.split('|')
      p = fields[5]
      if p in counts:
         counts[p] = counts[p] + 1
      else:
         counts[p] = 1


for p,c in counts.items():
   print(c, p)