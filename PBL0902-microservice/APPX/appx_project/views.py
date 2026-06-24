from django.shortcuts import render, redirect
from django.urls import reverse
import requests
import json

def get_server_url(ms):
    """Return the base URL for the given microservice."""
    servers = {
        'MS1': 'http://localhost:5051',
        'MS2': 'http://localhost:5052',
        'MS3': 'http://localhost:5053'
    }
    return servers.get(ms, 'http://localhost:5051')

def get_db_name(ms):
    """Return the database name for the given microservice."""
    if ms in ['MS1', 'MS2']:
        return 'DB-A'
    return 'DB-B'

def masukkeindeks(request):
    alamatserver_ms1_dba = "http://localhost:5051/cars/"
    datas_dba = requests.get(alamatserver_ms1_dba)
    rows_dba = json.loads(datas_dba.text)

    alamatserver_ms3_dbb = "http://localhost:5053/cars/"
    datas_dbb = requests.get(alamatserver_ms3_dbb)
    rows_dbb = json.loads(datas_dbb.text)

    return render(request, 'index.html', {'rows_dba': rows_dba, 'rows_dbb': rows_dbb})

def ms1(request):
    servermana = 'MS1'
    alamatserver = "http://localhost:5051/cars/"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    return render(request, 'indexms.html', {'rows': rows, 'servermana': servermana, 'DB': 'DB-A'})

def ms2(request):
    servermana = 'MS2'
    alamatserver = "http://localhost:5052/cars/"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    return render(request, 'indexms.html', {'rows': rows, 'servermana': servermana, 'DB': 'DB-A'})

def ms3(request):
    servermana = 'MS3'
    alamatserver = "http://localhost:5053/cars/"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    return render(request, 'indexms.html', {'rows': rows, 'servermana': servermana, 'DB': 'DB-B'})

def createcar(request, ms):
    try:
        return render(request, 'createcar.html', {'servermana': ms})
    except:
        ms = 'MS1'
        return render(request, 'createcar.html', {'servermana': ms})

def createcarsave_ms1(request):
    if request.method == 'POST':
        fName = request.POST.get('carName', '')
        fBrand = request.POST.get('carBrand', '')
        fModel = request.POST.get('carModel', '')
        fPrice = request.POST.get('carPrice', '')
        fdesc = "input from appx to MS1"

        datacar = {
            "carname": fName,
            "carbrand": fBrand, 
            "carmodel": fModel,
            "carprice": fPrice,
            "description": fdesc
        }
        
        datacar_json = json.dumps(datacar)
        alamatserver = "http://localhost:5051/cars/"
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect('ms1')

def createcarsave_ms2(request):
    if request.method == 'POST':
        fName = request.POST.get('carName', '')
        fBrand = request.POST.get('carBrand', '')
        fModel = request.POST.get('carModel', '')
        fPrice = request.POST.get('carPrice', '')
        fdesc = "input from appx to MS2"

        datacar = {
            "carname": fName,
            "carbrand": fBrand, 
            "carmodel": fModel,
            "carprice": fPrice,
            "description": fdesc
        }
        
        datacar_json = json.dumps(datacar)
        alamatserver = "http://localhost:5052/cars/"
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect('ms2')

def createcarsave_ms3(request):
    if request.method == 'POST':
        fName = request.POST.get('carName', '')
        fBrand = request.POST.get('carBrand', '')
        fModel = request.POST.get('carModel', '')
        fPrice = request.POST.get('carPrice', '')
        fdesc = "input from appx to MS3"

        datacar = {
            "carname": fName,
            "carbrand": fBrand, 
            "carmodel": fModel,
            "carprice": fPrice,
            "description": fdesc
        }
        
        datacar_json = json.dumps(datacar)
        alamatserver = "http://localhost:5053/cars/"
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect('ms3')

def readcar(request, ms):
    if ms in ['MS1', 'MS2']:
        alamatserver = "http://localhost:5051/cars/"
        datas = requests.get(alamatserver)
        rows = json.loads(datas.text)
        return render(request, 'readcar.html', {'rows': rows, 'servermana': ms, 'DB': 'DB-A'})

    elif ms in ['MS3']:
        alamatserver = "http://localhost:5053/cars/"
        datas = requests.get(alamatserver)
        rows = json.loads(datas.text)
        return render(request, 'readcar.html', {'rows': rows, 'servermana': ms, 'DB': 'DB-B'})
    
    return redirect('masukkeindeks')

def updatecar(request, ms):
    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    db_name = get_db_name(ms)
    return render(request, 'updatecar.html', {'rows': rows, 'servermana': ms, 'DB': db_name})

def updatecarform(request, ms, car_id):
    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/" + str(car_id)
    datas = requests.get(alamatserver)
    car = json.loads(datas.text)
    db_name = get_db_name(ms)
    return render(request, 'updatecarform.html', {'car': car, 'servermana': ms, 'DB': db_name})

def updatecarsave(request, ms, car_id):
    if request.method == 'POST':
        fName = request.POST.get('carName', '')
        fBrand = request.POST.get('carBrand', '')
        fModel = request.POST.get('carModel', '')
        fPrice = request.POST.get('carPrice', '')
        fdesc = "updated from appx via " + ms

        datacar = {
            "carname": fName,
            "carbrand": fBrand,
            "carmodel": fModel,
            "carprice": fPrice,
            "description": fdesc
        }

        datacar_json = json.dumps(datacar)
        server_url = get_server_url(ms)
        alamatserver = server_url + "/cars/" + str(car_id)

        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        requests.put(alamatserver, data=datacar_json, headers=headers)

    return redirect('updatecar', ms=ms)

def deletecar(request, ms):
    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    db_name = get_db_name(ms)
    return render(request, 'deletecar.html', {'rows': rows, 'servermana': ms, 'DB': db_name})

def deletecarsave(request, ms, car_id):
    if request.method == 'POST':
        server_url = get_server_url(ms)
        alamatserver = server_url + "/cars/" + str(car_id)
        requests.delete(alamatserver)

    return redirect('deletecar', ms=ms)

def searchcar(request, ms):
    db_name = get_db_name(ms)
    return render(request, 'searchcar.html', {'rows': [], 'servermana': ms, 'DB': db_name, 'query': ''})

def searchcarsave(request, ms):
    query = request.POST.get('searchQuery', '') if request.method == 'POST' else request.GET.get('q', '')

    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/search?q=" + query
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    db_name = get_db_name(ms)

    return render(request, 'searchcar.html', {'rows': rows, 'servermana': ms, 'DB': db_name, 'query': query})
