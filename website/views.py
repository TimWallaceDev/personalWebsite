import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import requests
from bs4 import BeautifulSoup
from .models import *
import random

#spotipy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .artists import *

# Create your views here.
            
#MAIN WEBSITE

def five(request):
    print("welcome home")
    return render(request, "website/5.html")

def fiveAbout(request):
    return render(request, "website/5-about.html")

def fiveProjects(request):
    return render(request, "website/5-projects.html")

def fiveGear(request):
    return render(request, "website/5-gear.html")

def moreprojects(request):
    return render(request, "website/moreprojects.html")

def archive(request):
    return render(request, "website/archive.html")

def mints(request):
    return render(request, "website/mints.html")

def popupdemo(request):
    return render(request, "website/popup.html")


#PAYS TO QUIT

def paystoquit(request):
    return render(request, "website/paystoquit.html")

#musicquiz
def musicquiz(request):
    return render(request, "website/musicquiz.html")

def musicquiz2(request):
    return render(request, "website/musicquiz2.html")

#lists

def lists(request):
    if request.method == "POST":
        print("posting")
        if "groceryItem" in request.POST:
            newItem = GroceryItem(name=request.POST["groceryItem"])
            newItem.save()
            print("addded grocery")

        if "funThing" in request.POST:
            newItem = FunThing(name=request.POST["funThing"])
            newItem.save()
            print("addded fun")

        if "chore" in request.POST:
            newItem = Chore(name=request.POST["chore"])
            newItem.save()
            print("addded chore", request.POST["chore"])

        if "thingToBuy" in request.POST:
            newItem = ThingToBuy(name=request.POST["thingToBuy"])
            newItem.save()
            print("addded thing to buy")

        return redirect("/lists")

    else:
        print("getting")
        groceries = GroceryItem.objects.all()
        funThings = FunThing.objects.all()
        chores = Chore.objects.all()
        thingsToBuy = ThingToBuy.objects.all()
        return render(request, "website/lists.html",{
            "groceries": groceries,
            "chores": chores,
            "funThings": funThings,
            "thingsToBuy": thingsToBuy,
        })

def listDelete(request):
    if request.method == "POST":
        if "groceryItem" in request.POST:
            toDelete = GroceryItem.objects.filter(name=request.POST["groceryItem"])
            toDelete.delete()
            print("deleted!", toDelete)

        if "funThing" in request.POST:
            toDelete = FunThing.objects.filter(name=request.POST["funThing"])
            toDelete.delete()
            print("deleted!", toDelete)

        if "chore" in request.POST:
            toDelete = Chore.objects.filter(name=request.POST["chore"])
            toDelete.delete()
            print("deleted!", toDelete)

        if "thingToBuy" in request.POST:
            toDelete = ThingToBuy.objects.filter(name=request.POST["thingToBuy"])
            toDelete.delete()
            print("deleted!", toDelete)

        return redirect("/lists")

#spotipy
def spotipy1(request):

    #grab 2 random artists
    artist1 = random.randint(0,22)
    artist2 = random.randint(0,22)
    while artist2 == artist1:
        artist2 = random.randint(0,22)

    dictkeys = dict.keys(artists)
    keys = []
    for key in dictkeys:
        keys.append(key)

    #get info for each artist
    artist1_uri = 'spotify:artist:' + artists[keys[artist1]]
    artist2_uri = 'spotify:artist:' + artists[keys[artist2]]

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    results1 = spotify.artist(artist1_uri)
    top = spotify.artist_top_tracks(artist1_uri)
    preview = top['tracks'][0]['preview_url']
    print(top['tracks'][0])
    print(preview)

    popularity1 = results1['popularity']
    img1 = results1['images'][2]['url']

    results2 = spotify.artist(artist2_uri)
    popularity2 = results2['popularity']
    img2 = results2['images'][2]["url"]

    #render the webpage
    return render(request, "website/spotipy.html", {
        "preview": preview,
        "artist1": results1,
        "img1": img1,
        "pop1": popularity1,
        "artist2": results2,
        "img2": img2,
        "pop2": popularity2,
    })


#IMAGE GENERATOR

def imageGenerator(request, keyword):
    if request.method == "GET":
        try:
            html_page = requests.get(f"https://images.google.com/search?q={keyword}&tbm=isch").text
            soup = BeautifulSoup(html_page)
            images = []
            for img in soup.findAll('img'):
                images.append(img.get('src'))


            return HttpResponse(f"{images[1]}", content_type="text/plain")
        except:
            return render(request, "website/generator.html")

#BLOG

def blog(request):
    posts = BlogPost.objects.filter(public=True)
    return render(request, "website/blog.html", {
            "posts":posts,
        })

def blogpost(request):
    if request.method == "POST":
        #TODO
        #authenticate
        #Save form data to database
        try:
            public = request.POST["public"]
            if public == "on":
                public = True
            else:
                public = False
        except:
            public = False
        title = request.POST["title"]
        content = request.POST["content"]
        img = request.POST["img"]
        entry = BlogPost(public=public, title=title, content=content, img=img)
        print(entry.public, entry.title, entry.content)
        entry.save()
        return render(request, "website/blogpost.html")
    

    if request.method == "GET":

        #TODO
        #authentication
        

        return render(request, "website/blogpost.html")

def blogSecret(request):
    secretPosts = BlogPost.objects.filter(public=False)
    return render(request, "website/blog.html", {
        "posts": secretPosts
    })


#TASKS

def tasks(request):
    return render(request, "website/localtasks.html")


#BIKES

def tbonesbikeshop(request):
    return render(request, "website/tbonesbikeshop.html")

#CALCULATOR

def calculator(request):
    return render(request, "website/calculator.html")

#EDUCATION

def education(request):
    return render(request, "website/education.html")

def coinsort(request):
    return render(request, "website/coinsort.html")

#ISITTOOHOTTOWORK

def isittoohottowork(request):
    return render(request, "website/toohot.html")

def answer(request):
    city = request.POST['city']
    sky = request.POST['sky']
    workload = request.POST['workload']

    answer = city + sky + workload

    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key=16728f405cfd4ffeac721605212906&q={city}&aqi=no")

    response = response.json()

    cleandata = response['current']

    temp = cleandata['temp_f']

    humidity = cleandata['humidity']

    clouds = cleandata['cloud']

    feelslike = cleandata['feelslike_f']

    #Extra Factors
    realtemp = 0

    if int(humidity) > 40:
        realtemp += 3
    elif int(humidity) > 50:
        realtemp += 6
    elif int(humidity) > 60:
        realtemp += 9

    if sky == "high":
        realtemp += 13
    if sky == "medium":
        realtemp += 7

    realtemp += temp

    answer = "NO"
    breaks = "NO, GET BACK TO WORK"

    #Workload
    if workload == "high":
        #High
        if realtemp > 105:
            answer = "YES"
            breaks = "Work should not continue. Find less sressful work or take the day off"
        elif realtemp > 104:
            answer = "YES"
            breaks = "Take a 45 minutes break every hour"
        elif realtemp > 102:
            answer = "YES"
            breaks = "Take a 40 minutes break every hour"
        elif realtemp > 101:
            answer = "YES"
            breaks = "Take a 35 minutes break every hour"
        elif realtemp > 99:
            answer = "YES"
            breaks = "Take a 30 minutes break every hour"
        elif realtemp > 97:
            answer = "YES"
            breaks = "Take a 25 minutes break every hour"
        elif realtemp > 96:
            answer = "YES"
            breaks = "Take a 20 minutes break every hour"
        elif realtemp > 94:
            answer = "YES"
            breaks = "Take a 15 minutes break every hour"
        
    #Medium
    if workload == "medium":
        if realtemp > 107:
            answer = "YES"
            breaks = "Work should not continue. Find less sressful work or take the day off"
        elif realtemp > 106:
            answer = "YES"
            breaks = "Take a 45 minutes break every hour"
        elif realtemp > 105:
            answer = "YES"
            breaks = "Take a 40 minutes break every hour"
        elif realtemp > 104:
            answer = "YES"
            breaks = "Take a 35 minutes break every hour"
        elif realtemp > 102:
            answer = "YES"
            breaks = "Take a 30 minutes break every hour"
        elif realtemp > 101:
            answer = "YES"
            breaks = "Take a 25 minutes break every hour"
        elif realtemp > 100:
            answer = "YES"
            breaks = "Take a 20 minutes break every hour"
        elif realtemp > 99:
            answer = "YES"
            breaks = "Take a 15 minutes break every hour"
        
    #Low
    if workload == "low":
        if realtemp > 110:
            answer = "YES"
            breaks = "Work should not continue. Find less sressful work or take the day off"
        elif realtemp > 109:
            answer = "YES"
            breaks = "Take a 45 minutes break every hour"
        elif realtemp > 108:
            answer = "YES"
            breaks = "Take a 30 minutes break every hour"
        elif realtemp > 107:
            answer = "YES"
            breaks = "Take a 25 minutes break every hour"
        elif realtemp > 106:
            answer = "YES"
            breaks = "Take a 20 minutes break every hour"
        elif realtemp > 105:
            answer = "YES"
            breaks = "Take a 15 minutes break every hour"

    return render(request, "website/answer.html", {
        "answer": answer,
        "breaks": breaks,
        "location": city.upper(),
        "realtemp": realtemp,
        "feelslike": feelslike,
        
    })
