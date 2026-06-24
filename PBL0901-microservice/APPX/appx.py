from flask import Flask, render_template, request, redirect, url_for
import json, requests

app = Flask(__name__)

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

@app.route('/')
def masukkeindeks():
    alamatserver_ms1_dba = "http://localhost:5051/cars"
    datas_dba = requests.get(alamatserver_ms1_dba)
    rows_dba = json.loads(datas_dba.text)

    alamatserver_ms3_dbb = "http://localhost:5053/cars"
    datas_dbb = requests.get(alamatserver_ms3_dbb)
    rows_dbb = json.loads(datas_dbb.text)

    return render_template('index.html', rows_dba=rows_dba,  rows_dbb=rows_dbb)

@app.route('/ms1')
def ms1():
    servermana='MS1'
    alamatserver = "http://localhost:5051/cars"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    return render_template('indexms.html', rows=rows,  servermana=servermana, DB='DB-A')

@app.route('/ms2')
def ms2():
    servermana='MS2'
    alamatserver = "http://localhost:5052/cars"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    return render_template('indexms.html', rows=rows,  servermana=servermana, DB='DB-A')
    

@app.route('/ms3')
def ms3():
    servermana='MS3'
    alamatserver = "http://localhost:5053/cars"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    return render_template('indexms.html',  rows=rows,servermana=servermana, DB='DB-B')

# ==================== CREATE ====================

@app.route('/createcar/<ms>')
def createcar(ms):
    try:
        return render_template('createcar.html', servermana=ms)
    except:
        ms = 'MS1'
        return render_template('createcar.html', servermana=ms)

@app.route('/createcarsave_ms1', methods=['GET','POST'])
def createcarsave_ms1():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']
    fdesc = "input from appx to MS1"

    datacar = {
        "carname" : fName,
        "carbrand" : fBrand, 
        "carmodel" : fModel,
        "carprice" : fPrice,
        "description":fdesc
    }
    
    datacar_json = json.dumps(datacar)

    alamatserver = "http://localhost:5051/cars/"
    
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}

    kirimdata = requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('ms1'))

@app.route('/createcarsave_ms2', methods=['GET','POST'])
def createcarsave_ms2():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']
    fdesc = "input from appx to MS2"

    datacar = {
        "carname" : fName,
        "carbrand" : fBrand, 
        "carmodel" : fModel,
        "carprice" : fPrice,
        "description":fdesc
    }
    
    datacar_json = json.dumps(datacar)

    alamatserver = "http://localhost:5052/cars/"
    
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}

    kirimdata = requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('ms2'))


@app.route('/createcarsave_ms3', methods=['GET','POST'])
def createcarsave_ms3():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']
    fdesc = "input from appx to MS3"

    datacar = {
        "carname" : fName,
        "carbrand" : fBrand, 
        "carmodel" : fModel,
        "carprice" : fPrice,
        "description":fdesc
    }
    
    datacar_json = json.dumps(datacar)

    alamatserver = "http://localhost:5053/cars/"
    
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}

    kirimdata = requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('ms3'))

# ==================== READ ====================

@app.route('/readcar/<ms>')
def readcar(ms):
    if ms in ['MS1','MS2']:
        alamatserver = "http://localhost:5051/cars"
        datas = requests.get(alamatserver)
        rows = json.loads(datas.text)

        return render_template('readcar.html', rows=rows, servermana=ms, DB='DB-A')

    elif ms in ['MS3']:
        alamatserver = "http://localhost:5053/cars"
        datas = requests.get(alamatserver)
        rows = json.loads(datas.text)
        return render_template('readcar.html', rows=rows, servermana=ms, DB='DB-B')

# ==================== UPDATE ====================

@app.route('/updatecar/<ms>')
def updatecar(ms):
    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    db_name = get_db_name(ms)
    return render_template('updatecar.html', rows=rows, servermana=ms, DB=db_name)

@app.route('/updatecarform/<ms>/<int:car_id>')
def updatecarform(ms, car_id):
    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/" + str(car_id)
    datas = requests.get(alamatserver)
    car = json.loads(datas.text)
    db_name = get_db_name(ms)
    return render_template('updatecarform.html', car=car, servermana=ms, DB=db_name)

@app.route('/updatecarsave/<ms>/<int:car_id>', methods=['POST'])
def updatecarsave(ms, car_id):
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']
    fdesc = "updated from appx via " + ms

    datacar = {
        "carname" : fName,
        "carbrand" : fBrand,
        "carmodel" : fModel,
        "carprice" : fPrice,
        "description": fdesc
    }

    datacar_json = json.dumps(datacar)

    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/" + str(car_id)

    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
    requests.put(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('updatecar', ms=ms))

# ==================== DELETE ====================

@app.route('/deletecar/<ms>')
def deletecar(ms):
    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    db_name = get_db_name(ms)
    return render_template('deletecar.html', rows=rows, servermana=ms, DB=db_name)

@app.route('/deletecarsave/<ms>/<int:car_id>', methods=['POST'])
def deletecarsave(ms, car_id):
    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/" + str(car_id)
    requests.delete(alamatserver)

    return redirect(url_for('deletecar', ms=ms))

# ==================== SEARCH ====================

@app.route('/searchcar/<ms>')
def searchcar(ms):
    db_name = get_db_name(ms)
    return render_template('searchcar.html', rows=[], servermana=ms, DB=db_name, query='')

@app.route('/searchcarsave/<ms>', methods=['GET', 'POST'])
def searchcarsave(ms):
    query = request.form.get('searchQuery', '') if request.method == 'POST' else request.args.get('q', '')

    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/search?q=" + query
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    db_name = get_db_name(ms)

    return render_template('searchcar.html', rows=rows, servermana=ms, DB=db_name, query=query)


if __name__ == '__main__':
    
    app.run(
        host = '0.0.0.0',
        debug = 'True',
        port = 5050
        )