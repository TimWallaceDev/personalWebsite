from sqlite3 import Date
from django.shortcuts import render, redirect
import requests
import re
import json
from datetime import date
from bs4 import BeautifulSoup
import operator

#from .scraper import *
from .models import *

# Create your views here.
orgs = ['https://abcnews.go.com', 'https://cbsnews.com', 'https://nbcnews.com', 'https://cbc.ca/news', 'https://ctvnews.ca', 'https://globalnews.ca/', 'https://news.sky.com', 'https://www.bbc.com/news', 'https://www.foxnews.com', 'https://www.rt.com']


#admin

def archive(request):
    archiver()
    return render(request, 'news/archive.html')

def archiver():
    whitelist = Whitelist.objects.all()
    blacklist = Blacklist.objects.all()

    whitelistwords = []

    blacklistwords = []

    for word in whitelist:
        whitelistwords.append(word.word)

    for word in blacklist:
        blacklistwords.append(word.word)

    startyear = '2022'
    startmonth = '04'
    startday = '12'
    starthour = '0900'


    todaysyear = '2022'
    todaysmonth = '04'
    todaysday = '12'
    todayshour = '0900'

    for date in range(2000):
        #get starting day
        
        #Subtrack todaysday
        todaysday = int(todaysday) - 1
        todaysday = str(todaysday)


        #make sure day has two integers
        if (len(todaysday) < 2):
            #add Zero spacer
            todaysday = '0' + todaysday

        #check if month needs to change    
        if todaysday == '00':
            #subtract the month
            print('month change')
            todaysmonth = int(todaysmonth) - 1
            todaysmonth = str(todaysmonth)
            if len(todaysmonth) < 2:
                todaysmonth = '0' + todaysmonth
            #add correct amount of days for the month
            if todaysmonth == '00': 
                todaysday = '31'
            if todaysmonth == '01':
                todaysday = '28'
            if todaysmonth == '02':
                todaysday = '31'
            if todaysmonth == '03':
                todaysday = '30'
            if todaysmonth == '04':
                todaysday = '31'
            if todaysmonth == '05':
                todaysday = '30'
            if todaysmonth == '06':
                todaysday = '31'
            if todaysmonth == '07':
                todaysday = '31'
            if todaysmonth == '08':
                todaysday = '30'
            if todaysmonth == '09':
                todaysday = '31'
            if todaysmonth == '10':
                todaysday = '30'
            if todaysmonth == '11':
                todaysday = '31'

        #Check if month is 0 and change year
        if todaysmonth == '00':
            print('year change')
            todaysmonth = '12'
            todaysyear = int(todaysyear) - 1
            todaysyear = str(todaysyear)
            
        todaysdate = todaysyear + todaysmonth + todaysday + todayshour
        
        request = requests.get(f'https://web.archive.org/web/{todaysdate}/http://www.cbc.ca/news').text
        
        #do the scrape
        text = request.lower()
        cleantext = re.sub('[<>+=\/":@$}{#-]', '', text)
        todaysdate = int(todaysdate)
        for word in whitelistwords:
            rawcount = re.findall(word, cleantext, re.IGNORECASE)
            count = len(rawcount)

            newentry = DeepArchive(
            org = 'cbc', 
            word = word,
            count = count,
            date = todaysdate
            )

            newentry.save()

        #BONEBROTH
        request = text

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
                date = int(todaysdate)
                newbone = BoneBrothArchive(org='cbc', word=word, count=count, date=todaysdate)
                newbone.save()
        print(str(todaysdate) + ' Done.')
    print('All Done.')

def admin(request):
    if request.user.is_authenticated:
        #GET request
        keywords = Whitelist.objects.all()
        blacklist = Blacklist.objects.all()
        topwords = Bs4.objects.filter(count__gt=5).order_by('-count')
        abc = BoneBroth.objects.filter(org='https://abcnews.go.com', count__gt=5, date='2022-04-11').order_by('-count')
        cbs = BoneBroth.objects.filter(org='https://cbsnews.com', count__gt=5).order_by('-count')
        nbc = BoneBroth.objects.filter(org='https://nbcnews.com', count__gt=5).order_by('-count')
        cbc = BoneBroth.objects.filter(org='https://cbc.ca/news', count__gt=5).order_by('-count')
        ctv = BoneBroth.objects.filter(org='https://ctvnews.ca', count__gt=5).order_by('-count')
        glob = BoneBroth.objects.filter(org='https://globalnews.ca/').order_by('-count')

        if request.method == "GET":
            return render(request, 'news/admin.html', {
                "keywords": keywords,
                "blacklist": blacklist,
                "topwords": topwords,
                "abc": abc,
                "cbs": cbs,
                "nbc": nbc,
                "cbc": cbc,
                "ctv": ctv,
                "global": glob,
            })
        #POST request
        if request.method == "POST":
            #get keyword from admin. get blacklist or whitelist
            word = request.POST['word']
            whichlist = request.POST['list']

            #Do database stuff

            if whichlist == "blacklist":
                newblacklist = Blacklist(word=word)
                newblacklist.save()
                BoneBroth.objects.filter(word=word).delete()
                Bs4.objects.filter(word=word).delete()
            if whichlist == "whitelist":
                newwhitelist = Whitelist(word=word)
                newwhitelist.save()

            #return confirmation
            return redirect('/keywordadmin')

#search results
def oneOrgOneKey(request):
    entries = DeepArchive.objects.filter(word="russia", org='https://cbc.ca/news')

    chartdata = []

    for entry in entries:
        chartdata.append({'x': entry.org, 'y': entry.count, 'date': entry.date})
        

    return render(request, 'news/oneOrgOneKey.html', {
        "chartdata": chartdata,
        "keyword": "Russia"
    })

def oneOrgManyKeys(request):
    return render(request, 'news/oneOrgManyKeys.html')

def sampleDouble(request):

    #Double Keyword Search (1 org)
    if request.method == "POST":
        keywords = request.POST.getlist('keyword')
        org = request.POST['org']
        entries = Entry.objects.filter(word=keywords[0], org=org)
        entries2 = Entry.objects.filter(word=keywords[1], org=org)
        chartdata = []

        chartdata2 = []

        for entry in entries:
            chartdata.append({'x': entry.org, 'y': entry.count, 'date': entry.date})
        
        for entry in entries2:
            chartdata2.append({'x': entry.org, 'y': entry.count, 'date': entry.date})

        return render(request, 'news/twolines.html', {
            "keyword": keywords[0],
            "keyword2": keywords[1],
            "chartdata": chartdata,
            "chartdata2": chartdata2,
        })

    #default result
    entries = Entry.objects.filter(word="russia", org='https://cbc.ca/news')

    entries2 = Entry.objects.filter(word="ukraine", org='https://cbc.ca/news')

    chartdata = []

    chartdata2 = []

    for entry in entries:
        chartdata.append({'x': entry.org, 'y': entry.count, 'date': entry.date})
    
    for entry in entries2:
        chartdata2.append({'x': entry.org, 'y': entry.count, 'date': entry.date})

    return render(request, 'news/twolines.html', {
        "keyword": "Russia",
        "keyword2": "ukraine",
        "chartdata": chartdata,
        "chartdata2": chartdata2,
    })

def sampleMany(request):
    
    #TRIPLE Keyword Search (1 org)
    if request.method == "POST":
        keywords = request.POST.getlist('keyword')
        org = request.POST['org']
        entries = Entry.objects.filter(word=keywords[0], org=org)
        entries2 = Entry.objects.filter(word=keywords[1], org=org)
        entries3 = Entry.objects.filter(word=keywords[2], org=org)
        chartdata = []
        chartdata2 = []
        chartdata3 = []

        for entry in entries:
            chartdata.append({'x': entry.org, 'y': entry.count, 'date': entry.date})
        
        for entry in entries2:
            chartdata2.append({'x': entry.org, 'y': entry.count, 'date': entry.date})
        
        for entry in entries3:
            chartdata3.append({'x': entry.org, 'y': entry.count, 'date': entry.date})

        return render(request, 'news/threelines.html', {
            "keyword": keywords[0],
            "keyword2": keywords[1],
            "keyword3": keywords[2],
            "org": org,
            "chartdata": chartdata,
            "chartdata2": chartdata2,
            "chartdata3": chartdata3,
        })

    #default result
    entries = Entry.objects.filter(word="russia", org='https://cbc.ca/news')
    entries2 = Entry.objects.filter(word="ukraine", org='https://cbc.ca/news')
    entries3 = Entry.objects.filter(word="covid", org='https://cbc.ca/news')

    chartdata = []
    chartdata2 = []
    chartdata3 = []

    for entry in entries:
        chartdata.append({'x': entry.org, 'y': entry.count, 'date': entry.date})
    
    for entry in entries2:
        chartdata2.append({'x': entry.org, 'y': entry.count, 'date': entry.date})

    for entry in entries3:
        chartdata3.append({'x': entry.org, 'y': entry.count, 'date': entry.date})
    
    


    return render(request, 'news/threelines.html', {
        "keyword": "Russia",
        "keyword2": "ukraine",
        "chartdata": chartdata,
        "chartdata2": chartdata2,
        "chartdata3": chartdata3,
    })


def samplelist(request):
    #default
    if request.method == 'GET':
        return render(request, 'news/many.html')

    #TRIPLE Keyword Search (1 org)
    if request.method == "POST":

        #collect search terms and data
        keywords = request.POST.getlist('keyword')
        orgs = request.POST.getlist('org')
         
        #Get keywords and orgs into a list of dictionaries. 
        keywordList = []

        counter = 0

        for keyword in keywords:
            print(keyword)
            keywordList.append({'word': keyword, 'org': orgs[counter]})
            counter+=1

        #From keyword list, make list of entries
        entryList = []


        #looping over KeywordList, each time adding a list to the list of dictionaries
        for word in keywordList:
            print(word)
            tmpentry = []
            singleentry = DeepArchive.objects.filter(word=word['word'], org=word['org'])
            tmpentry.append(singleentry)
            entryList.append(tmpentry)

        #now that we have entries, we can make chartdata 
        
        
        chartdatalist = []


        for  entries in entryList:
            for entry in entries:
                chartdatatmp = []
                for piece in entry:
                    chartdatatmp.append({'x': piece.org, 'y': piece.count, 'date': piece.date})
                
            chartdatalist.append(chartdatatmp)

        return render(request, 'news/many.html', {
            "keyword": keywordList,
            "chartdata": chartdatalist,
            "entryList": entryList,
        })

def index(request):

    #Top words for each org TODAY
    cbc = BoneBroth.objects.filter(org='https://cbc.ca/news', date='2022-04-13').order_by('-count')[:20]
    ctv = BoneBroth.objects.filter(org='https://ctvnews.ca', date='2022-04-13').order_by('-count')[:20]
    glob = BoneBroth.objects.filter(org='https://globalnews.ca/', date='2022-04-13').order_by('-count')[:20]
    
    abc = BoneBroth.objects.filter(org='https://abcnews.go.com', date='2022-04-13').order_by('-count')[:20]
    cbs = BoneBroth.objects.filter(org='https://cbsnews.com', date='2022-04-13').order_by('-count')[:20]
    nbc = BoneBroth.objects.filter(org='https://nbcnews.com', date='2022-04-13').order_by('-count')[:20]

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
   
   
   
            

    #Top NEW words


    return render(request, "news/index.html", {
        'cbc': cbc,
        'ctv': ctv,
        'global': glob,
        'abc': abc,
        'cbs': cbs,
        'nbc': nbc,
        'topcombined': topcombined
    })