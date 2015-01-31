# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

with open('pegida_korpus.txt') as f:
    content = [x.strip('\n') for x in f.readlines()]

# <codecell>

corpus = {}
comment = False
for line in content:
    if line.startswith('2014-') or line.startswith('2015-'):
        #print('Date: %s' % line)
        date = line
    elif line.startswith('#'):
        continue
    else:
        #print('Comment: %s' % line)
        comment = line

    if comment:
        corpus[date] = comment
        comment = False

# <codecell>

import csv

# <codecell>

writer = csv.writer(open('pegida_korpus.csv', 'wb'))
for key, value in corpus.items():
    writer.writerow([key, value])

# <codecell>


