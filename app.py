import json

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animals.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

# model


class Animals(db.Model):
    id = db.Column('animal_id', db.Integer, primary_key=True)
    typename = db.Column(db.String(100))
    specie = db.Column(db.String(50))
    amount= db.Column(db.Integer)

    def __init__(self, typename, specie, amount):
        self.typename = typename
        self.specie = specie
        self.amount = amount
# model


@app.route('/animals', methods=['GET', 'POST'])
@app.route('/animals/<id>',methods=['DELETE','PUT'])
def crud_animals(id=0):
    if request.method == 'POST':
        request_data = request.get_json()
        print(request_data)
        print(request_data['typename'])

        typename = request_data['typename']
        specie = request_data["specie"]
        amount = request_data["amount"]

        newAnimal = Animals(typename, specie,amount )
        db.session.add(newAnimal)
        db.session.commit()
        return "a new rcord was create"
    if request.method == 'GET':
        res = []
        for animal in Animals.query.all():
            res.append(
                { "id": animal.id,"typename": animal.typename, "specie": animal.specie,"amount": animal.amount})
        return (json.dumps(res))

    if request.method == 'DELETE': #not implemented yet
        del_animal = Animals.query.filter_by(id=id).first()
        db.session.delete(del_animal)
        db.session.commit()
        return "an animal was deleted"
    
    if request.method == 'PUT': #not implemented yet
        request_data = request.get_json()
        upd_animal= Animals.query.filter_by(id=id).first()
        upd_animal.typename = request_data['typename']
        upd_animal.specie = request_data["specie"]
        upd_animal.amount = request_data["amount"]
        db.session.commit()
        return "an animal was updated"
@app.route('/')
def hello():
    return 'Hello animal World!'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
