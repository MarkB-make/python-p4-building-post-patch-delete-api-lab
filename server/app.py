#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
        }
        bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    
    if request.method == 'GET':
        bakery_serialized = {
            'id': bakery.id,
            'name': bakery.name,
        }

        response = make_response(
            jsonify(bakery_serialized),
            200
        )
        response.headers["Content-Type"] = "application/json"

        return response
    
    elif request.method == 'PATCH':
        # Update the bakery name from form data
        if 'name' in request.form:
            bakery.name = request.form['name']
        
        # Commit the changes to the database
        db.session.commit()
        
        # Return the updated bakery as JSON
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
        }
        
        response = make_response(
            jsonify(bakery_dict),
            200
        )
        response.headers["Content-Type"] = "application/json"
        
        return response

@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'GET':
        baked_goods = []
        for baked_good in BakedGood.query.all():
            baked_good_dict = {
                'id': baked_good.id,
                'name': baked_good.name,
                'price': baked_good.price,
            }
            baked_goods.append(baked_good_dict)

        response = make_response(
            jsonify(baked_goods),
            201
        )
        response.headers["Content-Type"] = "application/json"

        return response
    
    elif request.method == 'POST':
        # Create a new baked good from form data
        new_baked_good = BakedGood(
            name=request.form['name'],
            price=request.form['price'],
            bakery_id=request.form.get('bakery_id')
        )
        
        # Add and commit to the database
        db.session.add(new_baked_good)
        db.session.commit()
        
        # Return the new baked good as JSON
        baked_good_dict = {
            'id': new_baked_good.id,
            'name': new_baked_good.name,
            'price': new_baked_good.price,
        }
        
        response = make_response(
            jsonify(baked_good_dict),
            201
        )
        response.headers["Content-Type"] = "application/json"
        
        return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def baked_good_by_id(id):
    baked_good = BakedGood.query.filter_by(id=id).first()
    
    # Delete the baked good from the database
    db.session.delete(baked_good)
    db.session.commit()
    
    # Return a confirmation message
    response_body = {
        'delete_successful': True,
        'message': 'Baked good successfully deleted.'
    }
    
    response = make_response(
        jsonify(response_body),
        200
    )
    response.headers["Content-Type"] = "application/json"
    
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)