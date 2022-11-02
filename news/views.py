from sqlite3 import Date
from django.shortcuts import render, redirect
from datetime import *
import re
import requests
import pytz

#from .scraper import *
from .models import *

def topwords(request):
    date = '2022' + '05' + '07' + '0900'

    print(date)

    #Top words for each org TODAY
    cbc = BoneBrothArchive.objects.filter(org='cbc', date=date).order_by('-count')[:20]
    ctv = BoneBrothArchive.objects.filter(org='ctv', date=date).order_by('-count')[:20]
    glob = BoneBrothArchive.objects.filter(org='global', date=date).order_by('-count')[:20]

    abc = BoneBrothArchive.objects.filter(org='abc', date=date).order_by('-count')[:20]
    cbs = BoneBrothArchive.objects.filter(org='cbs', date=date).order_by('-count')[:20]
    nbc = BoneBrothArchive.objects.filter(org='nbc', date=date).order_by('-count')[:20]


    
    #Top words COMBINED

    topcombined = []

    for entry in abc[:4]:
        if entry.word not in topcombined:
            topcombined.append(entry.word)

    for entry in cbs[:4]:
        if entry.word not in topcombined:
            topcombined.append(entry.word)

    for entry in nbc[:4]:
        if entry.word not in topcombined:
            topcombined.append(entry.word)

    for entry in cbc[:4]:
        if entry.word not in topcombined:
            topcombined.append(entry.word)

    for entry in ctv[:4]:
        if entry.word not in topcombined:
            topcombined.append(entry.word)

    for entry in glob[:4]:
        if entry.word not in topcombined:
            topcombined.append(entry.word)

    #save top words for today

    for word in topcombined:
        newTopWord = TopWords(word=word, date=date)
        newTopWord.save()

    print("done")
        
    return render(request, 'news/about.html')

def about(request):
    return render(request, 'news/about.html')

def thirtythree(request):
    #33

    thirtythrees = []

    thirtythreees = ThirtyThrees.objects.all()

    for thirty in thirtythreees:
        thirtythrees.append(thirty.headline)
        
    return render(request, 'news/thitythree.html', {
        'thirtythrees': thirtythrees,
        })

def index(request):

    #Get Todays Date
    todaysdate = datetime.now()
    todaysdate = todaysdate - timedelta(hours=4)
    todaysdate = todaysdate.date()
    print(todaysdate)

    #Top words for each org TODAY
    cbc = TopWordsByOrg.objects.filter(org='cbc', date=todaysdate).order_by('id')[:20]
    ctv = TopWordsByOrg.objects.filter(org='ctv', date=todaysdate).order_by('id')[:20]
    glob = TopWordsByOrg.objects.filter(org='global', date=todaysdate).order_by('id')[:20]
    
    abc = TopWordsByOrg.objects.filter(org='abc', date=todaysdate).order_by('id')[:20]
    cbs = TopWordsByOrg.objects.filter(org='cbs', date=todaysdate).order_by('id')[:20]
    nbc = TopWordsByOrg.objects.filter(org='nbc', date=todaysdate).order_by('id')[:20]
    
    #bbc
    bbc = TopWordsByOrg.objects.filter(org='bbc', date=todaysdate).order_by('id')[:20]
    
    #sky
    sky = TopWordsByOrg.objects.filter(org='sky', date=todaysdate).order_by('id')[:20]

    #Top words COMBINED

    topcombinedquery = TopWords.objects.filter(date=todaysdate)

    topcombined = []

    for word in topcombinedquery:
        topcombined.append(word.word)


    #Top NEW words
    
    today = todaysdate - timedelta(hours=4)
        
    yesterdaysDate = today - timedelta(days = 1)

    topYesterday = TopWords.objects.filter(date=yesterdaysDate)
    topNew = []
    yesterdaystop = []

    for word in topYesterday:
        yesterdaystop.append(word.word)

    for word in topcombined:
        if word not in yesterdaystop:
            topNew.append(word)

    #Remove New From Top Words

    for word in topNew:
        if word in topcombined:
            topcombined.remove(word)
    

    #Millions

    todaysmillions = []

    millions = Millions.objects.filter(date=datetime.now()).order_by('-id')

    for million in millions:
        todaysmillions.append(million.headline)


    return render(request, "news/indexvar.html", {
        'cbc1': cbc[:10],
        'cbc2': cbc[10:],
        'ctv1': ctv[:10],
        'ctv2': ctv[10:],
        'global1': glob[:10],
        'global2': glob[10:],
        'abc1': abc[:10],
        'abc2': abc[10:],
        'cbs1': cbs[:10],
        'cbs2': cbs[10:],
        'nbc1': nbc[:10],
        'nbc2': nbc[10:],
        'topcombined1': topcombined[:7],
        'topcombined2': topcombined[7:14],
        'topnew': topNew[:10],
        'millions': todaysmillions[:3],
        'date': todaysdate,
    })

def admin(request):

    if request.user.is_authenticated:
        #GET request
        keywords = Whitelist.objects.all()
        blacklist = Blacklist.objects.all()
        topwords = BoneBrothArchive.objects.filter(count__gt=5).order_by('-count')

        #Top words for each org TODAY

        current = datetime.now()

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

        cbc = BoneBrothArchive.objects.filter(org='cbc', date=date).order_by('-count')[:20]
        ctv = BoneBrothArchive.objects.filter(org='ctv', date=date).order_by('-count')[:20]
        glob = BoneBrothArchive.objects.filter(org='global', date=date).order_by('-count')[:20]
        
        abc = BoneBrothArchive.objects.filter(org='abc', date=date).order_by('-count')[:20]
        cbs = BoneBrothArchive.objects.filter(org='cbs', date=date).order_by('-count')[:20]
        nbc = BoneBrothArchive.objects.filter(org='nbc', date=date).order_by('-count')[:20]

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
                BoneBrothArchive.objects.filter(word=word).delete()
                DeepArchive.objects.filter(word=word).delete()
            if whichlist == "whitelist":
                newwhitelist = Whitelist(word=word)
                newwhitelist.save()

            #return confirmation
            return redirect('/news/keywordadmin')
    else:
        return redirect('/news')

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
            if keyword != "":
                keywordList.append({'word': keyword.lower(), 'org': orgs[counter]})
            counter+=1

        #From keyword list, make list of entries
        entryList = []


        #looping over KeywordList, each time adding a list to the list of dictionaries
        for word in keywordList:
            print(word)
            tmpentry = []
            singleentry = BoneBrothArchive.objects.filter(word=word['word'], org=word['org']).order_by('date')
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
