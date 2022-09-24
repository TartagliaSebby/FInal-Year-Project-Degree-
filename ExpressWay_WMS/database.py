from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy

database = Blueprint("database", __name__)

db = SQLAlchemy()

class Seller(db.Model):
    _id = db.Column(db.Integer, primary_key =True)
    seller_id = db.Column(db.String(6), nullable=False, primary_key=True)
    seller_name =db.Column(db.String(50), nullable=False)

class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key =True)
    seller_id = db.Column(db.String(6), db.ForeignKey(Seller.seller_id))
    item_name = db.Column(db.String(50), nullable=False)
    item_desc = db.Column(db.String(150))
    weight = db.Column(db.Integer)


