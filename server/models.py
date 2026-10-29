from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_marshmallow import Marshmallow
from marshmallow import fields

db = SQLAlchemy()
ma = Marshmallow()

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    items = db.relationship('Item', secondary='reviews', back_populates='customers', overlaps="reviews,customer")

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan', overlaps="customers,items")
    customers = db.relationship('Customer', secondary='reviews', back_populates='items', overlaps="reviews,item")

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews', overlaps="items,customers")
    item = db.relationship('Item', back_populates='reviews', overlaps="items,customers")

# Marshmallow Schemas
class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = True

    customer = fields.Nested(lambda: CustomerSchema(exclude=('reviews', 'items')))
    item = fields.Nested(lambda: ItemSchema(exclude=('reviews',)))

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True

    reviews = fields.Nested(ReviewSchema, exclude=('item',), many=True)
    customers = fields.Nested(lambda: CustomerSchema(exclude=('items', 'reviews')), many=True)

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True

    reviews = fields.Nested(ReviewSchema, exclude=('customer',), many=True)
    items = fields.Nested(ItemSchema, exclude=('reviews', 'customers'), many=True)