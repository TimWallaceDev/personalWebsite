import requests
import re

#get the page

page = requests.get('https://cbsnews.com').text

array = re.split(r'[><]', page)

millions = []

for chunk in array:
    if 'million' in chunk:
        if '=' not in chunk:
            if len(chunk) < 200:
                newchunk = chunk.strip()
                if newchunk not in millions:
                    millions.append(newchunk)

for chunk in array:
    if 'billion' in chunk:
        if '=' not in chunk:
            if len(chunk) < 200:
                newchunk = chunk.strip()
                if newchunk not in millions:
                    millions.append(newchunk)

for million in millions:
    print(million)
