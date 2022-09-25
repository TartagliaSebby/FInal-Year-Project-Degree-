from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy

database = Blueprint("database", __name__)

db = SQLAlchemy()

class seller(db.Model):
    seller_id = db.Column(db.String(6), nullable=False, primary_key=True)
    seller_name =db.Column(db.String(50), nullable=False)

class item(db.Model):
    item_id = db.Column(db.Integer, primary_key =True)
    seller_id = db.Column(db.String(6), db.ForeignKey(seller.seller_id))
    item_name = db.Column(db.String(50), nullable=False)
    item_desc = db.Column(db.String(150))
    weight = db.Column(db.Integer)


