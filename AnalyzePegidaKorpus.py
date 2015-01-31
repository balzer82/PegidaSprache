# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Analyse des Pegida Korpus

# <headingcell level=3>

# Kommentare von der deutschen Pegida-Facebook-Seite

# <markdowncell>

# Quelle: http://0x0a.li/de/die-sprache-pegidas/

# <markdowncell>

# Anfangs nur zu Dokumentationszwecken ließ 0x0a (Gregor Weichbrodt und Hannes Bajohr) diese Kommentare durch ein Scraping-Script regelmäßig sammeln. Seit Dezember letzten Jahres ist bis heute ein 282.596 Kommentare und 7.751.654 Wortformen umfassendes Textkorpus der Pegida-Sprache entstanden.

# <markdowncell>

# First, import stuff we need.

# <codecell>

import pandas as pd
from pandas.tseries.resample import TimeGrouper
from pandas.tseries.offsets import DateOffset

%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context("poster")
sns.set_style("white")

from datetime import datetime
print('Pandas Version: %s' % pd.__version__)

# <codecell>

corpus = pd.read_csv('pegida_korpus.csv', delimiter=',', names=['Datum','Comment'], index_col='Datum', parse_dates=True)

# <headingcell level=3>

# Show something

# <codecell>

corpus.tail(10)

# <markdowncell>

# You see some links: Nice! [Here is a short overview](http://theblog.de/280k-pegida-kommentare-meistverlinkte-urls-und-domains/).

# <headingcell level=2>

# Comments per Minute

# <codecell>

commentsperday = corpus['Comment'].resample('24H', how='count')

# <markdowncell>

# Spaziergänge waren immer montags gegen 18:30Uhr seit dem 20.10.2014, außer am [19.01.2015 wegen Morddrohungen gegen Bachmann](http://www.zeit.de/gesellschaft/zeitgeschehen/2015-01/dresden-pegida-demonstration-montag-abgesagt)

# <codecell>

spaz = pd.date_range('10/20/2014 18:30', periods=15, freq='7D')
spaz

# <codecell>

plt.figure(figsize=(12,4))
commentsperday.plot(kind='area', alpha=0.5)

#for i, s in enumerate(spaz):
#    plt.axvline(x=s, label='Spaziergang' if i==0 else '', alpha=0.3, c='k')

#plt.ylabel('Comments per Day')
#leg = plt.legend(loc='upper left')

plt.title('Kommentare pro Tag auf der Deutschen Pegida facebook Seite')

plt.annotate('Pegida facebook Seite, Korpus von 0x0a (http://0x0a.li/de/die-sprache-pegidas)', \
             xy=(1,1), xytext=(0.95,0.2), xycoords='figure fraction', ha='right')

plt.savefig('Comments-per-Day.png', dpi=150, bbox_inches='tight')

# <codecell>

def countperdayplot(wordlist):
    plt.figure(figsize=(12,4))
    for word in wordlist:
        corpus['Comment'][corpus.Comment.str.contains(word)].resample('1D', how='count').plot(kind='area', label=word, alpha=0.3)

    plt.legend(loc='best')
    plt.ylabel('am Tag')

    plt.annotate('Pegida facebook Seite, Korpus von 0x0a (http://0x0a.li/de/die-sprache-pegidas)', \
                 xy=(1,1), xytext=(0.95,0.2), xycoords='figure fraction', ha='right')

    plt.title('So oft wurde das Wort ... in den Kommentaren gebraucht')
    return plt

# <headingcell level=3>

# Wie haben die Leute die Presse genannt

# <codecell>

plot = countperdayplot(['Medien', 'Lügenpresse', 'Systemmedien'])
plot.savefig('Comments-per-Day-Presse.png', dpi=150, bbox_inches='tight')

# <headingcell level=3>

# Was gab es zu den Linken zu sagen

# <codecell>

plot = countperdayplot(['Antifa', 'Gutmenschen', 'Linke'])
plot.savefig('Comments-per-Day-Linke.png', dpi=150, bbox_inches='tight')

# <headingcell level=2>

# Wie sieht es mit Lutz Bachmann aus

# <codecell>

plot = countperdayplot(['Bachmann', 'Führer'])
plot.savefig('Comments-per-Day-Bachmann.png', dpi=150, bbox_inches='tight')

# <headingcell level=3>

# Wie sieht es so politisch aus?

# <codecell>

plot = countperdayplot(['CDU', 'AfD', 'SPD', 'NPD'])
plot.savefig('Comments-per-Day-Parteien.png', dpi=150, bbox_inches='tight')

# <headingcell level=1>

# Text Processing with the Natural Language Toolkit

# <markdowncell>

# ![](http://covers.oreilly.com/images/9780596516499/cat.gif)
# That great Book covers almost everything shown here:
# 
# [Natural Language Processing with Python](http://www.nltk.org/book/)
# by Steven Bird, Ewan Klein, and Edward Loper
# O'Reilly Media, 2009

# <codecell>

import nltk
from nltk.corpus import stopwords
from nltk import FreqDist

# <markdowncell>

# Common Words of a Language to filter out

# <codecell>

stop_eng = stopwords.words('english')
stop_ger = stopwords.words('german')
customstopwords = ['mal', 'mehr', 'dass', 'schon', 'wer', 'viele', 'bitte', \
                   'wohl', 'für', 'gibt', 'macht', 'einfach', 'über', 'ganz', \
                   'unsere', 'können']

# <markdowncell>

# Clean the Comments from a bunch of stuff we are not interested in

# <codecell>

def cleancomments(comments):
    try:
        txt = comments['Comment']
    except:
        txt = str(comments)
    
    tokens = []
    sentences = []
    
    sentences.append(txt.lower())
    tokens.extend([t.lower().strip("\"<>()*^:,.!?") for t in txt.split()])

    hashtags = [w for w in tokens if w.startswith('#')]
    mentions = [w for w in tokens if w.startswith('@')]
    links = [w for w in tokens if w.startswith('http') or w.startswith('www')]
    filtered_tokens = [w.decode('utf-8') for w in tokens \
                       if not w in stop_eng \
                       and not w in stop_ger \
                       and not w in customstopwords \
                       and not len(w)<3 \
                       and not w in hashtags \
                       and not w in links \
                       and not w in mentions]

    return ' '.join(filtered_tokens)

# <codecell>

corpus['tokens'] = corpus.apply(cleancomments, axis=1)

# <codecell>

corpus.head(20)

# <headingcell level=2>

# Top 10 Words

# <codecell>

filtered_tokens=[]
for idx, row in corpus.tokens.iteritems():
    filtered_tokens.extend(row.split())

# <codecell>

freq_dist = nltk.FreqDist(filtered_tokens)

# <codecell>

freq_dist.plot(11)

# <codecell>

from collections import OrderedDict

# <codecell>

words = ['Islamisierung', 'Systemmedien', 'Gutmenschen', 'Führer', 'Lügenpresse','Bachmann','Wirtschaftsflüchtlinge', \
         'Hass', 'Liebe', 'Geld', 'Abschieben', 'Helfen', 'Pack', 'Deutschland', 'Menschen', 'Land', 'Volk', 'Islam']

freq={}
for w in words:
    freq[w] = freq_dist.freq(w.lower().decode('utf-8'))

#Sort it
freq = OrderedDict(sorted(freq.items(), key=lambda t: t[1]))

# <codecell>

plt.figure(figsize=(11,5))

plt.bar(range(len(freq)), [v for v in freq.values()])
plt.xticks([x+0.5 for x in range(len(freq))], [lab.decode('utf-8') for lab in freq.keys()], rotation=40, ha='right')

plt.ylabel('Wortanteil in Kommentaren')
plt.title(u'Darüber spricht Pegida auf facebook')
plt.annotate('Kommentare von Pegida facebook Seite, Korpus von 0x0a (http://0x0a.li/de/die-sprache-pegidas)', \
             xy=(1,1), xytext=(0.94,0.05), xycoords='figure fraction', ha='right')
plt.savefig('WordFreq.png', dpi=150, bbox_inches='tight')

# <headingcell level=2>

# Länge der Kommentare

# <codecell>

def length(comment):
    wortlist = comment.Comment.split()
    return len(wortlist)

# <codecell>

corpus['Worte'] = corpus.apply(length, axis=1)

# <headingcell level=4>

# Top10 Längste Kommentare

# <codecell>

top10length = corpus.sort(columns='Worte', ascending=False).head(10)

# <markdowncell>

# Diese sind folgende:

# <codecell>

top10length

# <markdowncell>

# Längster Kommentar ist 1108 Wörter lang!

# <codecell>

top10length.Comment.to_csv('Top10LangeKommentare.csv', header='Die 10 längsten Kommentare')

# <markdowncell>

# An sonsten wird sich eher kurz gehalten.

# <codecell>

corpus.Worte.plot(kind='hist', bins=200)
plt.ylabel(u'Anzahl der Kommentare')
plt.xlabel(u'Länge des Kommentars (Worte)')
plt.xlim(0, 200)
plt.savefig('Commentlength.png', dpi=150, bbox_inches='tight')

# <headingcell level=2>

# Concordance

# <markdowncell>

# Use of the same word in context

# <codecell>

corpustokens = nltk.wordpunct_tokenize(unicode(corpus.Comment.tolist()))
rawcommenttext = nltk.Text(corpustokens)

# <codecell>

rawcommenttext.concordance("Systemmedien")

# <codecell>

rawcommenttext.concordance("Asylanten")

# <codecell>

rawcommenttext.concordance("Gutmensch")

# <codecell>

rawcommenttext.concordance("Gutmenschen")

# <codecell>

rawcommenttext.concordance("Islamisierung")

# <headingcell level=5>

# Thanks

# <markdowncell>

# By [@Balzer82](https://twitter.com/Balzer82), Data Analyst bei [MechLab Engineering](http://mechlab-engineering.de/geschaeftsfelder/mechlab-datalab/)

# <codecell>


