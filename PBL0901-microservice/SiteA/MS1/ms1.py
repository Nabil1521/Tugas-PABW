from flask import Flask, jsonify
from peewee import *
from flask_restful import Resource, Api, reqparse 


app = Flask(__name__)
api = Api(app)

db = SqliteDatabase('../DB-A.db')

class BaseModel(Model):
    class Meta:
        database = db

class TBCarsWeb(BaseModel):
    carname = TextField()
    carbrand = TextField() 
    carmodel = TextField()
    carprice = TextField()
    description = TextField()

def create_tables():
    with db:
        db.create_tables([TBCarsWeb])

@app.route('/')
def masukkeindeks():
    return "MS1 Server Ready"

class CAR(Resource):
    def get(self):
        rows = TBCarsWeb.select()    
        datas=[]

        for row in rows:
            datas.append({
            'id':row.id,
            'carname':row.carname,
            'carbrand':row.carbrand,
            'carmodel':row.carmodel,
            'carprice':row.carprice,
            'description':row.description
        })
        return jsonify(datas)

    def post(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carname')
        parserData.add_argument('carbrand')
        parserData.add_argument('carmodel')
        parserData.add_argument('carprice')
        parserData.add_argument('description')

        parserAmbilData = parserData.parse_args()

        fName = parserAmbilData.get('carname')
        fBrand = parserAmbilData.get('carbrand')
        fModel = parserAmbilData.get('carmodel')
        fPrice = parserAmbilData.get('carprice')
        fDescription = parserAmbilData.get('description')

        car_simpan = TBCarsWeb.create(
            carname = fName,
            carbrand = fBrand, 
            carmodel = fModel,
            carprice = fPrice,
            description = fDescription
            )

        rows = TBCarsWeb.select()    
        datas=[]
        for row in rows:
            datas.append({
                'id':row.id,
                'carname':row.carname,
                'carbrand':row.carbrand,
                'carmodel':row.carmodel,
                'carprice':row.carprice,
                'description':row.description
            })
        return jsonify(datas)

class CARDetail(Resource):
    def get(self, car_id):
        try:
            car = TBCarsWeb.get_by_id(car_id)
            return jsonify({
                'id': car.id,
                'carname': car.carname,
                'carbrand': car.carbrand,
                'carmodel': car.carmodel,
                'carprice': car.carprice,
                'description': car.description
            })
        except TBCarsWeb.DoesNotExist:
            return {'message': 'Car not found'}, 404

    def put(self, car_id):
        try:
            car = TBCarsWeb.get_by_id(car_id)
        except TBCarsWeb.DoesNotExist:
            return {'message': 'Car not found'}, 404

        parserData = reqparse.RequestParser()
        parserData.add_argument('carname')
        parserData.add_argument('carbrand')
        parserData.add_argument('carmodel')
        parserData.add_argument('carprice')
        parserData.add_argument('description')

        parserAmbilData = parserData.parse_args()

        car.carname = parserAmbilData.get('carname', car.carname)
        car.carbrand = parserAmbilData.get('carbrand', car.carbrand)
        car.carmodel = parserAmbilData.get('carmodel', car.carmodel)
        car.carprice = parserAmbilData.get('carprice', car.carprice)
        car.description = parserAmbilData.get('description', car.description)
        car.save()

        return jsonify({
            'id': car.id,
            'carname': car.carname,
            'carbrand': car.carbrand,
            'carmodel': car.carmodel,
            'carprice': car.carprice,
            'description': car.description
        })

    def delete(self, car_id):
        try:
            car = TBCarsWeb.get_by_id(car_id)
            car.delete_instance()
            return {'message': 'Car deleted successfully'}, 200
        except TBCarsWeb.DoesNotExist:
            return {'message': 'Car not found'}, 404

class CARSearch(Resource):
    def get(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('q', location='args')
        args = parserData.parse_args()
        query = args.get('q', '')

        rows = TBCarsWeb.select().where(
            (TBCarsWeb.carname.contains(query)) |
            (TBCarsWeb.carbrand.contains(query)) |
            (TBCarsWeb.carmodel.contains(query))
        )
        datas = []
        for row in rows:
            datas.append({
                'id': row.id,
                'carname': row.carname,
                'carbrand': row.carbrand,
                'carmodel': row.carmodel,
                'carprice': row.carprice,
                'description': row.description
            })
        return jsonify(datas)

api.add_resource(CAR, '/cars/', endpoint="cars/")
api.add_resource(CARDetail, '/cars/<int:car_id>', endpoint="car_detail")
api.add_resource(CARSearch, '/cars/search', endpoint="cars_search")


if __name__ == '__main__':
    create_tables()
    app.run(
        host = '0.0.0.0',
        debug = 'True',
        port=5051
        )