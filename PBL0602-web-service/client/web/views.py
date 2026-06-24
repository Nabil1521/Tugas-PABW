from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
import json
import requests

APP_TYPE = 'Web Service'
API_SERVER_URL = settings.API_SERVER_URL


def index(request):
    """Home page"""
    return render(request, 'index.html', {'appType': APP_TYPE})


def createcar(request):
    """Show create car form"""
    return render(request, 'createcar.html', {'appType': APP_TYPE})


@require_http_methods(["GET", "POST"])
@csrf_protect
def createcarsave(request):
    """Handle car creation"""
    if request.method == 'POST':
        fname = request.POST.get('carName')
        fbrand = request.POST.get('carBrand')
        fmodel = request.POST.get('carModel')
        fprice = request.POST.get('carPrice')

        datacar = {
            "carname": fname,
            "carbrand": fbrand,
            "carmodel": fmodel,
            "carprice": fprice
        }

        datacar_json = json.dumps(datacar)
        alamatserver = f"{API_SERVER_URL}/cars/"
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        try:
            requests.post(alamatserver, data=datacar_json, headers=headers)
        except requests.RequestException:
            pass

        return redirect('web:readcar')

    return redirect('web:index')


def readcar(request):
    """Display all cars"""
    try:
        alamatserver = f"{API_SERVER_URL}/cars"
        datas = requests.get(alamatserver)
        rows = json.loads(datas.text) if datas.text else []
    except (requests.RequestException, json.JSONDecodeError):
        rows = []

    return render(request, 'readcar.html', {'rows': rows, 'appType': APP_TYPE})


def updatecar(request):
    """Show update car form"""
    return render(request, 'updatecar.html', {'appType': APP_TYPE})


@require_http_methods(["GET", "POST"])
@csrf_protect
def updatecarsave(request):
    """Handle car update"""
    if request.method == 'POST':
        fname = request.POST.get('carName')
        fbrand = request.POST.get('carBrand')
        fmodel = request.POST.get('carModel')
        fprice = request.POST.get('carPrice')

        datacar = {
            "carname": fname,
            "carbrand": fbrand,
            "carmodel": fmodel,
            "carprice": fprice
        }

        datacar_json = json.dumps(datacar)
        alamatserver = f"{API_SERVER_URL}/cars/"
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        try:
            requests.put(alamatserver, data=datacar_json, headers=headers)
        except requests.RequestException:
            pass

        return redirect('web:readcar')

    return redirect('web:index')


def deletecar(request):
    """Show delete car form"""
    return render(request, 'deletecar.html', {'appType': APP_TYPE})


@require_http_methods(["GET", "POST"])
@csrf_protect
def deletecarsave(request):
    """Handle car deletion"""
    if request.method == 'POST':
        fname = request.POST.get('carName')

        datacar = {
            "carname": fname
        }

        datacar_json = json.dumps(datacar)
        alamatserver = f"{API_SERVER_URL}/cars/"
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        try:
            requests.delete(alamatserver, data=datacar_json, headers=headers)
        except requests.RequestException:
            pass

        return redirect('web:readcar')

    return redirect('web:index')
