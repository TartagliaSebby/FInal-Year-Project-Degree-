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

class asn(db.Model):
    asn_id = db.Column(mysql.INTEGER(6), primary_key =True)
    seller_id = db.Column(db.String(6), db.ForeignKey(seller.seller_id))
    arrival_date = db.Column(db.Date())
    arrival_time = db.Column(mysql.TIME)
    shipment_type = db.Column(db.String(10))
    asn_status = db.Column(db.String(10))
    vehicle_no = db.Column(db.String(7))
    seller = relationship("seller", back_populates="seller")

class asn_items(db.Model):
    asn_id = db.Column(mysql.INTEGER(6), db.ForeignKey(asn.asn_id), primary_key =True)
    item_id = db.Column(mysql.INTEGER(6),db.ForeignKey(item.item_id), primary_key =True)
    quantity =db.Column(mysql.INTEGER(4))
    item =relationship("item", back_populates="item")
    asn = relationship("asn", back_populates="asn")

class receive_discrepancies(db.Model):
    asn_id = db.Column(mysql.INTEGER(6), db.ForeignKey(asn.asn_id), primary_key =True)
    item_id = db.Column(mysql.INTEGER(6),db.ForeignKey(item.item_id), primary_key =True)
    note = db.Column(db.String(200))
    expected = db.column(mysql.INTEGER(4))
    received = db.column(mysql.INTEGER(4))
    damaged = db.column(mysql.INTEGER(4))
    item =relationship("item", back_populates="item")
    asn = relationship("asn", back_populates="asn")

class customer(db.Model):
    customer_id = db.Column(mysql.INTEGER(6), primary_key = True)
    name = db.Column(db.String(10))
    city = db.Column(db.String(30))
    street = db.Column(db.String(30))
    zip_code = db.Column(db.String(10))

class order(db.Model):
    order_id = db.Column(mysql.INTEGER(7), primary_key = True)
    customer_id = db.Column(mysql.INTEGER(7), db.ForeignKey(customer.customer_id))
    order_status = db.Column(db.String(20))
    placed_date = db.Column(db.Date())
    customer = relationship("customer", back_populates="customer")

class order_item(db.Model):
    order_id = db.Column(mysql.INTEGER(7), db.ForeignKey(order.order_id), primary_key = True)
    item_id = db.Column(mysql.INTEGER(6), db.ForeignKey(item.item_id), primary_key =True)
    quantity =db.Column(mysql.INTEGER(6))
    order = relationship("order", back_populates="order")
    item =relationship("item", back_populates="item")

class delivery(db.Model):
    delivery_id = db.Column(mysql.INTEGER(7), primary_key = True)
    order_id = db.Column(mysql.INTEGER(7), db.ForeignKey(order.order_id), primary_key = True)
    date = db.Column(db.Date())
    time = db.Column(mysql.TIME)
    vehicle_num = db.Column(db.String(7))
    order = relationship("order", back_populates="order")

class employee(db.Model):
    emp_id = db.Column(mysql.INTEGER(4), primary_key = True)
    name = db.Column(db.String(40))
    email = db.Column(db.String(50))
    phone_no = db.Column(mysql.INTEGER(10))

class Instructions(db.Model):
    emp_id = db.Column(mysql.INTEGER(4), db.ForeignKey(employee.emp_id), primary_key = True)
    instructions = db.Column(db.String(200))
    task =  db.Column(db.String(20))
    station = db.Column(db.String(30))
    employee = relationship("employee", back_populates = "employee")

class pick_list(db.Model):
    emp_id = db.Column(mysql.INTEGER(4), db.ForeignKey(employee.emp_id), primary_key = True)
    pick_list = db.Column(mysql.JSON())
    employee = relationship("employee", back_populates = "employee")

class shift(db.Model):
    emp_id = db.Column(mysql.INTEGER(4), db.ForeignKey(employee.emp_id), primary_key = True)
    date = db.Column(db.Date())
    start_time = db.Column(mysql.TIME())
    end_time = db.Column(mysql.TIME())
    employee = relationship("employee", back_populates = "employee")

class assigned_orders(db.Model):
    order_id = db.Column(mysql.INTEGER(7), db.ForeignKey(order.order_id), primary_key = True)
    emp_id = db.Column(mysql.INTEGER(4), db.ForeignKey(employee.emp_id), primary_key = True)
    packing_station = db.Column(mysql.INTEGER(2))
    employee = relationship("employee", back_populates = "employee")
    order = relationship("order", back_populates="order")

class received_items(db.Model):
    item_id = db.Column(mysql.INTEGER(6), db.ForeignKey(item.item_id), primary_key =True)
    putaway = db.Column(mysql.BOOLEAN)
    quantity = db.Column(mysql.INTEGER(6))
    location = db.Column(mysql.INTEGER(10))
