#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Cakes, Bakeries, CakeBakeries

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.get('/bakeries')
def get_all_bakeries():
    bakeries = Bakeries.query.all()
    data = [bakery.to_dict(rules=('-cakebakeries',)) for bakery in bakeries]
    return make_response(
        jsonify(data), 
        200
    )

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakeries.query.filter(Bakeries.id==id).first()

    if not bakery:
        return make_response(
            jsonify({"error": "Bakery not found"}),
            404
        )
        
    return make_response(
        jsonify(bakery.to_dict()),
        200
    )

@app.delete('/bakeries/<int:id>')
def delete_bakery(id):
    bakeries = Bakeries.query.filter(Bakeries.id==id).first()

    if not bakeries:
        return make_response(
            jsonify({"error": ["validation errors"]}),
            406
        )
    db.session.delete(bakeries)
    db.session.commit()

    return make_response(jsonify({}), 204)

@app.get('/cakes')
def get_all_cakes():
    cakes = Cakes.query.all()
    data = [cake.to_dict(rules=('-cakebakeries',)) for cake in cakes]
    return make_response(
        jsonify(data), 
        200
    )

@app.post('/cakebakeries')
def post_cakebakery():
    data = request.get_json()

    try:
        new_cakebakery = CakeBakeries(
            cake_id=data.get('camper_id'),
            bakery_id=data.get('bakery_id'),
            price=data.get('price'),
        )
        db.session.add(new_cakebakery)
        db.session.commit()

        return make_response(
            jsonify(new_cakebakery.to_dict(rules=('cakes', 'bakeries', '-cakes.cakebakeries', '-bakeries.cakebakeries'))),
            201
        )

    except ValueError:
        return make_response(
            jsonify({"errors": ["validation errors"]}),
            406
        )

if __name__ == '__main__':
    app.run(port=5555, debug=True)