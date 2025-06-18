#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
#    class Bakery(db.Model, SerializerMixin):
#     __tablename__ = 'bakeries'

#     serialize_rules = ('-baked_goods.bakery',)

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#     baked_goods = db.relationship('BakedGood', backref='bakery')

    
    bakeries = [bakery.to_dict()  for bakery in Bakery.query.all()]

    response = make_response(bakeries), 200
    return response
       

@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    if not bakery:
        return make_response({"error":"Bakery not found"}, 404)
    bakery_dict = bakery.to_dict()
    response = make_response(bakery_dict, 200)
    return response

@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return make_response([good.to_dict() for good in goods], 200)
    

    

@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(good.to_dict(), 200)
 
if __name__ == '__main__':
    app.run(port=5555, debug=True)
