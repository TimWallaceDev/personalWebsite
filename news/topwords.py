from .models import *

date = '2022' + '05' + '06' + '0900'

print(date)

#Top words for each org TODAY
cbc = BoneBrothArchive.objects.filter(org='cbc', date=date).order_by('-count')[:20]
ctv = BoneBrothArchive.objects.filter(org='ctv', date=date).order_by('-count')[:20]
glob = BoneBrothArchive.objects.filter(org='global', date=date).order_by('-count')[:20]

abc = BoneBrothArchive.objects.filter(org='abc', date=date).order_by('-count')[:20]
cbs = BoneBrothArchive.objects.filter(org='cbs', date=date).order_by('-count')[:20]
nbc = BoneBrothArchive.objects.filter(org='nbc', date=date).order_by('-count')[:20]

TopWordsByOrg.objects.all.delete()

for entry in cbc:
    newEntry = TopWordsByOrg(word=entry.word, org=entry.org)
    newEntry.save()

for entry in ctv:
    newEntry = TopWordsByOrg(word=entry.word, org=entry.org)
    newEntry.save()
    
for entry in glob:
    newEntry = TopWordsByOrg(word=entry.word, org=entry.org)
    newEntry.save()
    
for entry in abc:
    newEntry = TopWordsByOrg(word=entry.word, org=entry.org)
    newEntry.save()
    
for entry in cbs:
    newEntry = TopWordsByOrg(word=entry.word, org=entry.org)
    newEntry.save()
    
for entry in nbc:
    newEntry = TopWordsByOrg(word=entry.word, org=entry.org)
    newEntry.save()
