from .models import *
import re

archives = BoneBrothArchive.objects.all()[:10000]

for archive in archives:
    #check if word needs editing
    if '(' in archive.word:
        #remove the unwanted characters
        newWord = re.sub(")(',", '',archive.word)
        newWord = re.sub('\d+', '', newWord)
        newWord = re.sub('\s+', '', newWord)
        print(newWord)