from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse


from .models import Host
import os
import requests
from requests.exceptions import HTTPError


def index(request):
    template = loader.get_template('nanny/index.html')
    context = {}
    print(get_tomtom_report())
    return HttpResponse(template.render(context, request))

def parentSignUp(request):
    template = loader.get_template('nanny/parentSignUp.html')
    context = {}
    return HttpResponse(template.render(context, request))

def parentProcess(request):
    info = {
    "username" : request.POST["user_name"],
    "first_name" :  request.POST["first"],
    "last_name" : request.POST["last"],
    "phone" : request.POST["phone"],
    "password" : request.POST["password"],
    "location" : ""+request.POST["street"]+" "+request.POST["street2"]+", "+request.POST["city"]+", "+request.POST["state"]
    }

    id = Host.objects.create(**info);
    return HttpResponseRedirect("nanny/done")

def nannySignUp(request):
    template = loader.get_template('nanny/nannySignUp.html')
    context = {}
    return HttpResponse(template.render(context, request))

def nannyProcess(request):
    info = {
    "username" : request.POST["user_name"],
    "first_name" :  request.POST["first"],
    "last_name" : request.POST["last"],
    "phone" : request.POST["phone"],
    "password" : request.POST["password"],
    "location" : ""+request.POST["street"]+" "+request.POST["street2"]+", "+request.POST["city"]+", "+request.POST["state"]
    }

    id = Host.objects.create(**info);
    return HttpResponseRedirect("nanny/done")

def done(request):
    return render(request, 'nanny/done.html', {})

def locator(request):
    template = loader.get_template('nanny/locator.html')
    # reportID = get_tomtom_report().summary.project
    report = get_tomtom_report()
    print(type(report))
    submission = False
    if request.method == 'POST' and request.POST["projname"]:
        try:
            add_tomtom_project(projname)
            submission = True
        except Exception as err:
            print(f'Other error occurred: {err}')

    context = {
    "report": report,
    "submission": submission
    }
    return HttpResponse(template.render(context, request))

def get_tomtom_report(latitude='37.787600', longitude='-122.396630'):
    # default latitude and longtitude at hackathon site, 44 Tehama, San Francisco, CA.
    url = 'https://api.tomtom.com/geofencing/1/report/projectId'
    key = os.getenv('TOM_APIKEY')
    projectId = os.getenv('TOM_PROJID')

    try:
        response = requests.get(f'https://api.tomtom.com/geofencing/1/report/{projectId}?key={key}&point={longitude},{latitude}')
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        return response.text

def add_tomtom_project(projname):
    key = os.getenv('TOM_APIKEY')
    projectId = os.getenv('TOM_PROJID')

    try:
        response = requests.get(f'https://api.tomtom.com/geofencing/1/report/{projectId}?key={key}&point={longitude},{latitude}')
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        return response.text