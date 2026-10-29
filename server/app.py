from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from marshmallow import fields
from models import db, Customer, Item, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True

    reviews = fields.Nested('ReviewSchema', exclude=('customer',), many=True)
    items = fields.Nested('ItemSchema', exclude=('reviews', 'customers'), many=True)

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True

    reviews = fields.Nested('ReviewSchema', exclude=('item',), many=True)

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = True

    customer = fields.Nested('CustomerSchema', exclude=('reviews', 'items'))
    item = fields.Nested('ItemSchema', exclude=('reviews',))

@app.route('/')
def home():
    return "Welcome to the e-commerce backend!"

if __name__ == '__main__':
    app.run(port=5555, debug=True)