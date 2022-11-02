from django_cron import CronJobBase, Schedule
from .models import *
import re
import operator
from bs4 import BeautifulSoup
import requests
import datetime


orgs = [
    #india
    {'url' : 'https://indiatoday.in/india', 'code': 'indiatoday'},{'url' : 'https://ndtv.com/india', 'code': 'ndtv'},{'url' : 'https://timesofindia.indiatimes.com/india', 'code': 'indiatimes'},
    
    #USA
    {'url' : 'https://abcnews.go.com', 'code':'abc'}, {'url':'https://cbsnews.com', 'code':'cbs'}, {'url' : 'https://nbcnews.com',  'code':'nbc'}, {'url' : 'https://www.foxnews.com', 'code': 'fox'},
    
    #CANADA
    {'url' : 'https://cbc.ca/news', 'code': 'cbc'}, {'url' : 'https://ctvnews.ca', 'code': 'ctv'}, {'url' : 'https://globalnews.ca/',  'code':'global'},
    
    #AUSTRALIA
    {'url' : 'https://news.sky.com',  'code':'sky'},
    
    #UK
    {'url' : 'https://www.bbc.com/news',  'code':'bbc'}, {'url' : 'https://theguardian.com/uk-news', 'code': 'ukg'}, {'url' : 'https://independent.co.uk/news/uk', 'code': 'uki'},
    
    #RUSSIA
    {'url' : 'https://www.rt.com',  'code':'rt'},
    ]

class DailyArchiver(CronJobBase):
    #RUN_AT_TIMES = ['09:00'] # every day
    
    #schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'news.cron.dailyarchiver'    # a unique code

    #Get keywords from Database

    whitelist = Whitelist.objects.all()
    blacklist = Blacklist.objects.all()

    whitelistwords = []

    blacklistwords = []

    for word in whitelist:
        whitelistwords.append(word.word)

    for word in blacklist:
        blacklistwords.append(word.word)

    print(whitelistwords)
    print(blacklistwords)

    #Get todays date

    dateCheck = datetime.datetime.now()
    year = str(dateCheck.year)
    
    month = str(dateCheck.month)
    if len(month) < 2:
        month = '0' + month
        
    day = str(dateCheck.day)
    if len(day) < 2:
        day = '0' + day
    hour = '0900'
    todaysDate = year + month + day + hour
    print(todaysDate)

    #get each front page
    rawtextlist = []

    for org in orgs:
        try:
            rawtext = requests.get(org['url']).text
            rawtextlist.append({'org': org['code'], 'text': rawtext})
            print('page recieved: ' + org['code'])
        except:
            rawtextlist.append({'org': org['code'], 'text' : 'no response from the org...'})
        
    print(len(rawtextlist))


    for rawtext in rawtextlist:

        #Get Those Millions!

        array = re.split(r'[><]', rawtext['text'])

        millions = []

        for chunk in array:
            if 'million' in chunk:
                if '=' not in chunk:
                    if len(chunk) < 200:
                        newchunk = chunk.strip()
                        if newchunk not in millions:
                            millions.append(newchunk)


        for million in millions:
            newmillion = Millions(headline=million)
            newmillion.save()

        print('millions done')
        
        #33!

        array = re.split(r'[><]', rawtext['text'])

        thirtythrees = []

        for chunk in array:
            if '33' in chunk:
                if '=' not in chunk:
                    if len(chunk) < 200:
                        newchunk = chunk.strip()
                        if newchunk not in thirtythrees:
                            millions.append(newchunk)


        for thirty in thirtythrees:
            newthirtythree = ThirtyThrees(headline=thirty)
            newthirtythree.save()

        print('millions done')

        #BONEBROTH
        request = rawtext['text']

        def remove_tags(html):
            # parse html content
            soup = BeautifulSoup(html, "html.parser")
            for data in soup(['style', 'script']):
                # Remove tags
                data.decompose()
            # return data by retrieving the tag content
            return soup

        text = remove_tags(request)
        text = request.lower()

        cleanText = ''
        open = False

        for letter in text:
            #check if tag is open
            if letter == "<":
                open = True
            elif letter == ">":
                open = False

            #if closed, add to cleanText
            if open == False:
                cleanText += letter

        #get rid of unwanted characters

        text = re.sub('[>+=\-).,(/":&@$}|%;{#]', '--------------------', cleanText)
        text = re.sub('[0-9]', '', text)
        text = re.sub('>', ' ', text)
        text = re.sub('\n', ' ', text)
        text = re.sub('\t', ' ', text)

        splitText = text.split(' ')

        dictionary = {}

        results = {}
        #sort ALL words
        for word in splitText:
            if word in dictionary:
                dictionary[word] += 1
            else: 
                dictionary[word] = 1
        #filter words
        for word in dictionary:
            if len(word) < 15:
                if word not in blacklistwords:
                    results[word] = dictionary[word]
                
        dsc_results = sorted(results.items(), key=operator.itemgetter(1))

        for word in dsc_results:
            if word[1] > 3:
                newbone = BoneBrothArchive(org=rawtext['org'], word=word[0], count=word[1], date=todaysDate)
                newbone.save()
        print('bone broth: ' + rawtext['org'])

        #DEEP SEARCH
        text = rawtext['text']
        cleantext = re.sub('[<>+=\/":@$}{#-]', '', text)
        for word in whitelistwords:
            rawcount = re.findall(word, cleantext, re.IGNORECASE)
            count = len(rawcount)

            newentry = DeepArchive(
            org = rawtext['org'], 
            word = word,
            count = count,
            date = todaysDate,
            )

            newentry.save()
        print('done deepsearch' + rawtext['org'])

    #Top words for each org TODAY

    current = datetime.datetime.now()

    year = str(current.year)
    month = str(current.month)
    if len(month) < 2:
        month = '0' + month
    day = str(current.day)
    if len(day) < 2:
        day = '0' + day
    hour = '0900'

    date = year + month + day + hour

    print(date)

    #Top words for each org TODAY
    #CANADA
    cbc = BoneBrothArchive.objects.filter(org='cbc', date=date).order_by('-count')[:20]
    ctv = BoneBrothArchive.objects.filter(org='ctv', date=date).order_by('-count')[:20]
    glob = BoneBrothArchive.objects.filter(org='global', date=date).order_by('-count')[:20]
    
    #USA
    abc = BoneBrothArchive.objects.filter(org='abc', date=date).order_by('-count')[:20]
    cbs = BoneBrothArchive.objects.filter(org='cbs', date=date).order_by('-count')[:20]
    nbc = BoneBrothArchive.objects.filter(org='nbc', date=date).order_by('-count')[:20]
    
    #Australia
    sky = BoneBrothArchive.objects.filter(org='sky', date=date).order_by('-count')[:20]
    
    #England
    bbc = BoneBrothArchive.objects.filter(org='bbc', date=date).order_by('-count')[:20]
    
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
        
    for entry in sky:
        newEntry = TopWordsByOrg(word=entry.word, org=entry.org)
        newEntry.save()
        
    for entry in bbc:
        newEntry = TopWordsByOrg(word=entry.word, org=entry.org)
        newEntry.save()

    #Top words COMBINED

    topcombined = []

    for entry in abc[:5]:
        if entry.word not in topcombined:
            topcombined.append(entry.word)

    for entry in cbs[:5]:
        if entry.word not in topcombined:
            topcombined.append(entry.word)

    for entry in nbc[:5]:
        if entry.word not in topcombined:
            topcombined.append(entry.word)

    for entry in cbc[:5]:
        if entry.word not in topcombined:
            topcombined.append(entry.word)

    for entry in ctv[:5]:
        if entry.word not in topcombined:
            topcombined.append(entry.word)

    for entry in glob[:5]:
        if entry.word not in topcombined:
            topcombined.append(entry.word)

    #save top words for today

    for word in topcombined:
        newTopWord = TopWords(word=word, date=date)
        newTopWord.save()

    print("done")
