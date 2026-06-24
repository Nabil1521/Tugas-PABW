import sqlite3
from peewee import *
from flask import Flask, render_template, request, url_for, redirect

# Initialize Flask app and config
app = Flask(__name__)
appType = 'Monolith'

# Initialize database for cars
database = SqliteDatabase('carsweb.db')

# Initialize users database
def init_users_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL)''')
    
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    c.close()
    conn.close()

# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()

        c.close()
        conn.close()

        if user:
            return redirect(url_for('indeks'))
        else:
            return "Login Gagal"
    return render_template('login.html', appType=appType)

class BaseModel(Model):
    class Meta:
        database = database

class TBCars(BaseModel):
    id = AutoField()
    carname = TextField()
    carbrand = TextField()
    carmodel = TextField()
    carprice = TextField()

def create_tables():
    with database:
        database.create_tables([TBCars])

@app.route('/')
def indeks():
    return render_template('index.html', appType=appType)

# ================= CREATE =================
@app.route('/createcar')
def createcar():
    return render_template('createcar.html', appType=appType)

@app.route('/createcarsave', methods=['POST'])
def createcarsave():
    TBCars.create(
        carname=request.form['carName'],
        carbrand=request.form['carBrand'],
        carmodel=request.form['carModel'],
        carprice=request.form['carPrice'] 
    )
    return redirect(url_for('readcar'))

# ================= READ =================
@app.route('/readcar')
def readcar():
    rows = TBCars.select()
    return render_template('readcar.html', rows=rows, appType=appType)

# ================= UPDATE =================
@app.route('/updatecar/<int:id>', methods=['GET', 'POST'])
def updatecar(id):
    car = TBCars.get_by_id(id)

    if request.method == 'POST':
        car.carname = request.form['carName']
        car.carbrand = request.form['carBrand']
        car.carmodel = request.form['carModel']
        car.carprice = request.form['carPrice']
        car.save()

        return redirect(url_for('readcar'))

    return render_template('updatecar.html', car=car, appType=appType)

# ================= DELETE =================
@app.route('/deletecar/<int:id>')
def deletecar(id):
    car = TBCars.get_by_id(id)
    car.delete_instance()
    return redirect(url_for('readcar'))

# ================= SEARCH =================
@app.route('/searchcar', methods=['GET', 'POST'])
def searchcar():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = TBCars.select().where(TBCars.carname.contains(keyword))
    
    return render_template('searchcar.html', results=results, appType=appType)

@app.route('/help')
def help():
    return "ini halaman Helps"

if __name__ == '__main__':
    init_users_db()
    create_tables()
    app.run(port=5010, host='0.0.0.0', debug=True)