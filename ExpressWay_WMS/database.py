from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
database = Blueprint("database", __name__)

db = SQLAlchemy()

class seller(db.Model):
    seller_id = db.Column(db.String(6), nullable=False, primary_key=True)
    seller_name =db.Column(db.String(50), nullable=False)


class item(db.Model):
    item_id = db.Column(mysql.INTEGER(6), primary_key =True)
    seller_id = db.Column(db.String(6), db.ForeignKey(seller.seller_id))
    item_name = db.Column(db.String(50), nullable=False)
    item_desc = db.Column(db.String(150))
    weight = db.Column(db.Integer)
    seller = relationship("seller", back_populates="seller")

class item_location(db.Model):
    location = db.Column(db.String(13), primary_key =True)
    item_id = db.Column(mysql.INTEGER(6), db.ForeignKey(item.item_id))
    quantity = db.Column(mysql.INTEGER(6))
    item =relationship("item", back_populates="item")

class ASN(db.Model):
        asn_id = db.Column(mysql.INTEGER(6), primary_key =True)
        seller_id = db.Column(db.String(6), db.ForeignKey(seller.seller_id))
        arrival_date = db.Column()
        arrival_time = db.Column()
        shipment_type = db.Column()
        asn_status = db.Column()
        vehicle_no = db.Column()