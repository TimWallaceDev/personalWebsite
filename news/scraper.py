from sqlite3 import Date
from django.shortcuts import render
import requests
import re
import json
from bs4 import BeautifulSoup
import operator

from .models import *

orgs = ['https://abcnews.go.com', 'https://cbsnews.com', 'https://nbcnews.com', 'https://cbc.ca/news', 'https://ctvnews.ca', 'https://globalnews.ca/', 'https://news.sky.com', 'https://www.bbc.com/news', 'https://www.foxnews.com', 'https://www.rt.com']

def collectdata(request):
    OGrequest = request
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
    #get each front page
    rawtextlist = []

    for org in orgs:
        try:
            rawtext = requests.get(org).text
            rawtextlist.append({'org': org, 'text': rawtext})
            print('page recieved: ' + org)
        except:
            rawtextlist.append({'org': org, 'text' : 'no response from the org...'})
        
    print(len(rawtextlist))


    for rawtext in rawtextlist:

        #BS4

        HTML_DOC = rawtext['text']
        
        # Function to remove tags
        def remove_tags(html):
            # parse html content
            soup = BeautifulSoup(html, "html.parser")
            for data in soup(['style', 'script']):
                # Remove tags
                data.decompose()
            # return data by retrieving the tag content
            return soup.get_text()


        # Print the extracted data
        text = remove_tags(HTML_DOC)
        text = text.lower()
        splitext = text.split(' ')

        dictionary = {}
        results = {}

        #Sort and count ALL words
        for word in splitext:
            if word in dictionary:
                dictionary[word] += 1
            else: 
                dictionary[word] = 1

        #Filter out long words and blacklsit
        for word in dictionary:
            if len(word) < 15:
                if word not in blacklistwords:
                    results[word] = dictionary[word]
                
        dsc_results = sorted(results.items(), key=operator.itemgetter(1))

        for word in dsc_results:
            if word[1] > 3:
                newbs4 = Bs4(org=rawtext['org'], word=word[0], count=word[1])
                newbs4.save()
        print('bs4 done: ' + rawtext['org'])

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
                newbone = BoneBroth(org=rawtext['org'], word=word[0], count=word[1])
                newbone.save()
        print('bone broth: ' + rawtext['org'])

        #DEEP SEARCH
        text = rawtext['text']
        cleantext = re.sub('[<>+=\/":@$}{#-]', '', text)
        for word in whitelistwords:
            rawcount = re.findall(word, cleantext, re.IGNORECASE)
            count = len(rawcount)

            newentry = Entry(
            org = rawtext['org'], 
            word = word,
            count = count
            )

            newentry.save()
        print('done deepsearch' + rawtext['org'])
    print("done")
    return render(OGrequest, 'news/scrape.html')