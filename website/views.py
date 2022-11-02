import requests
from django.shortcuts import render
import smtplib


# Create your views here.
def test():
	print('this is not a test')
	with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login('timwallace959@gmail.com', 'password')

            subject = 'IN STOCK NOW'
            body = 'TIRES IN STOCK NOW: https://radpowerbikes.ca/collections/replacement-parts/products/kenda-kraze-20-x-4-25-tire'

            msg = f'Subject: {subject}/n/n{body}'

            smtp.sendmail('timwallace959@gmail.com', 'timwallace959@gmail.com', msg)
            
#MAIN WEBSITE

def five(request):
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
#PAYS TO QUIT

def paystoquit(request):
	return render(request, "website/paystoquit.html")

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