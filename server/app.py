#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def restaurants():
    restaurants = Restaurant.query.all()
    return [restaurant.to_dict() for restaurant in restaurants]
@app.route('/restaurants/<int:id>')
def restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return restaurant.to_dict()
    else:
        return {'error': 'Restaurant not found'}, 404
    
@app.route('/pizzas')
def pizzas():
    pizzas = Pizza.query.all()
    return [pizza.to_dict() for pizza in pizzas]
@app.route('/pizzas/<int:id>')
def pizza(id):
    pizza = Pizza.query.get(id)
    if pizza:
        return pizza.to_dict()
    else:
        return {'error': 'Pizza not found'}, 404
    
@app.route('/restaurant_pizzas')
def restaurant_pizzas():
    restaurant_pizzas = RestaurantPizza.query.all()
    return [restaurant_pizza.to_dict() for restaurant_pizza in restaurant_pizzas]
@app.route('/restaurant_pizzas/<int:id>')
def restaurant_pizza(id):
    restaurant_pizza = RestaurantPizza.query.get(id)
    if restaurant_pizza:
        return restaurant_pizza.to_dict()
    else:
        return {'error': 'Restaurant Pizza not found'}, 404
    
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    restaurant_id = data.get('restaurant_id')
    pizza_id = data.get('pizza_id')
    price = data.get('price')

    if not restaurant_id or not pizza_id or not price:
        return {'error': 'Missing required fields'}, 400

    restaurant = Restaurant.query.get(restaurant_id)
    pizza = Pizza.query.get(pizza_id)

    if not restaurant or not pizza:
        return {'error': 'Restaurant or Pizza not found'}, 404

    restaurant_pizza = RestaurantPizza(restaurant=restaurant, pizza=pizza, price=price)
    db.session.add(restaurant_pizza)
    db.session.commit()

    return restaurant_pizza.to_dict(), 201
@app.route('/restaurant_pizzas/<int:id>', methods=['DELETE'])
def delete_restaurant_pizza(id):
    restaurant_pizza = RestaurantPizza.query.get(id)
    if restaurant_pizza:
        db.session.delete(restaurant_pizza)
        db.session.commit()
        return {'message': 'Restaurant Pizza deleted successfully'}
    else:
        return {'error': 'Restaurant Pizza not found'}, 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
