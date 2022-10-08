from turtle import position
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
    seller_id = db.Column(db.String(6))
    item_name = db.Column(db.String(50), nullable=False)
    item_desc = db.Column(db.String(150))
    weight = db.Column(db.Integer)


class item_location(db.Model):
    location = db.Column(db.String(13), primary_key =True)
    item_id = db.Column(mysql.INTEGER(6))
    quantity = db.Column(mysql.INTEGER(6))


class asn(db.Model):
    asn_id = db.Column(mysql.INTEGER(6), primary_key =True)
    seller_id = db.Column(db.String(6))
    arrival_date = db.Column(db.Date())
    arrival_time = db.Column(mysql.TIME)
    shipment_type = db.Column(db.String(10))
    asn_status = db.Column(db.String(10))
    vehicle_no = db.Column(db.String(7))


class asn_items(db.Model):
    asn_id = db.Column(mysql.INTEGER(6),  primary_key =True)
    item_id = db.Column(mysql.INTEGER(6), primary_key =True)
    quantity =db.Column(mysql.INTEGER(4))



class receive_discrepancies(db.Model):
    asn_id = db.Column(mysql.INTEGER(6), primary_key =True)
    item_id = db.Column(mysql.INTEGER(6), primary_key =True)
    note = db.Column(db.String(200))
    expected = db.Column(mysql.INTEGER(4))
    received = db.Column(mysql.INTEGER(4))
    damaged = db.Column(mysql.INTEGER(4))

class customer(db.Model):
    customer_id = db.Column(mysql.INTEGER(6), primary_key = True)
    name = db.Column(db.String(10))
    city = db.Column(db.String(30))
    street = db.Column(db.String(30))
    zip_code = db.Column(db.String(10))

class orders(db.Model):
    order_id = db.Column(mysql.INTEGER(7), primary_key = True)
    customer_id = db.Column(mysql.INTEGER(7))
    order_status = db.Column(db.String(20))
    placed_date = db.Column(db.Date())

class order_item(db.Model):
    order_id = db.Column(mysql.INTEGER(7), primary_key = True)
    item_id = db.Column(mysql.INTEGER(6),  primary_key =True)
    quantity =db.Column(mysql.INTEGER(6))



class delivery(db.Model):
    delivery_id = db.Column(mysql.INTEGER(7), primary_key = True)
    order_id = db.Column(mysql.INTEGER(7),  primary_key = True)
    date = db.Column(db.Date())
    time = db.Column(mysql.TIME)
    vehicle_num = db.Column(db.String(7))


class employee(db.Model):
    emp_id = db.Column(mysql.INTEGER(4), primary_key = True)
    name = db.Column(db.String(40))
    email = db.Column(db.String(50))
    phone_no = db.Column(mysql.INTEGER(10))
    position = db.Column(db.String(10))
    password = db.Column(db.String(16), nullable=False)
    present = db.Column(mysql.BOOLEAN)

class Instructions(db.Model):
    emp_id = db.Column(mysql.INTEGER(4),  primary_key = True)
    instructions = db.Column(db.String(200))
    task =  db.Column(db.String(20))
    station = db.Column(db.String(30))


class pick_list(db.Model):
    emp_id = db.Column(mysql.INTEGER(4),  primary_key = True)
    pick_list = db.Column(mysql.JSON())
    

class shift(db.Model):
    emp_id = db.Column(mysql.INTEGER(4),  primary_key = True)
    date = db.Column(db.Date())
    start_time = db.Column(mysql.TIME())
    end_time = db.Column(mysql.TIME())
    

class assigned_orders(db.Model):
    order_id = db.Column(mysql.INTEGER(7), primary_key = True)
    emp_id = db.Column(mysql.INTEGER(4),  primary_key = True)
    packing_station = db.Column(mysql.INTEGER(2))
    

class received_items(db.Model):
    item_id = db.Column(mysql.INTEGER(6), primary_key =True)
    putaway = db.Column(mysql.BOOLEAN)
    quantity = db.Column(mysql.INTEGER(6))
    location = db.Column(mysql.INTEGER(10))


