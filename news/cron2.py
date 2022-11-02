from django_cron import CronJobBase, Schedule
from .models import *
import re
import operator
from bs4 import BeautifulSoup
import requests

class Archiver(CronJobBase):
    RUN_EVERY_MINS = 12000 # every 2 hours

    code = 'news.cron.archiver'    # a unique code

    def do(self):
        whitelist = Whitelist.objects.all()
        blacklist = Blacklist.objects.all()

        whitelistwords = []

        blacklistwords = []

        for word in whitelist:
            whitelistwords.append(word.word)

        for word in blacklist:
            blacklistwords.append(word.word)

        todaysyear = '2022'
        todaysmonth = '04'
        todaysday = '23'
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

            if todaysdate == '202204110900':
                exit()

            try:
                request = requests.get(f'https://web.archive.org/web/{todaysdate}/https://nbcnews.com/').text
            except:
                request = 'no entry for this date'
            
            #do the scrape
            text = request.lower()
            cleantext = re.sub('[<>+=\/":@$}{#-]', '', text)
            todaysdate = int(todaysdate)
            for word in whitelistwords:
                rawcount = re.findall(word, cleantext, re.IGNORECASE)
                count = len(rawcount)

                newentry = DeepArchive(
                org = 'nbc', 
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
                    newbone = BoneBrothArchive(org='nbc', word=word, count=count, date=todaysdate)
                    newbone.save()
            print(str(todaysdate) + ' Done.')
        print('All Done.')