from flask import Flask, redirect, url_for, render_template, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text,select
from ExpressWay_WMS.database import orders, customer, item_location,item, seller,asn, asn_items, receive_discrepancies, order_item, delivery, employee,instruction ,pick_list, shift
from ExpressWay_WMS.database import db
from sqlalchemy.engine.row import LegacyRow
import json

from symbol import parameters



app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#database connection
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Sebas",
    password="FypDatabase",
    hostname="Sebas.mysql.pythonanywhere-services.com",
    databasename="Sebas$FYP",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


engine = db.create_engine(SQLALCHEMY_DATABASE_URI,{})

"""
from sqlalchemy.orm import Session, sessionmaker
Session = sessionmaker()
session = Session.configure(bind=engine)
"""
db.init_app(app)
with app.app_context():
    db.create_all()

"""
build login page then use this function
@app.route('/')
def login_page():
    return render_template("login_page.html")
"""""
@app.route("/", methods = ['POST', 'GET'])
def main():
    if request.method == "GET":
        return render_template("manager_side/job_assignment_page.html")

    if request.method =="POST":
        if "jobTab" in request.form:
            with engine.connect() as connection:
                query = connection.execute(text("SELECT e.emp_id, e.name, i.task, i.station FROM employee e LEFT OUTER JOIN instruction i ON e.emp_id = i.emp_id ORDER BY e.emp_id;")).all()
            strResults= []
            if len(stringify(query)) != 0:
                for row in stringify(query):
                    for i in range (2,4,1):
                        if(row[i]=="None"):
                            row[i] = "-"
                    strResults.append(row)
            return (jsonify({"data":strResults}))
        elif "update" in request.form:

            with engine.connect() as connection:
                emp_id = db.session.execute(select(employee.emp_id).where(employee.emp_id == instruction.emp_id).where(employee.emp_id == request.form["data[emp_id]"])).all()

            if len(emp_id)==0:
                instructions = instruction(emp_id = request.form["data[emp_id]"], task=request.form["data[task]"],station =request.form["data[station]"],instructions =request.form["data[instruction]"])
                db.session.add(instructions)
                db.session.commit()

            return ("s")
            #else:
             #   with engine.connect as connection:






# manager side pages
@app.route("/dashboard",methods = ['POST', 'GET'])
def dashboard():
    with engine.connect() as connection:
        ord= connection.execute(text('select count(order_id) from orders where order_status="pending";'))
        inBShip = connection.execute(text('SELECT COUNT(asn_id) FROM asn WHERE asn_status="pending" AND arrival_date= CURDATE();'))
        empPresent = connection.execute(text('SELECT COUNT(emp_id) FROM employee WHERE present = True;'))
    return render_template("manager_side/dashboard.html", numOrdTBF=ord.scalar() ,numInboundShipment =inBShip.scalar(), numEmpPresent =empPresent.scalar())


@app.route("/orders",methods = ['POST', 'GET'])
def orders_page():
    if request.method == 'GET':
        with engine.connect() as connection:
            query = connection.execute(text('SELECT o.order_id, c.name as "Customer Name", SUM(oi.quantity) as "num of items", order_status, placed_date FROM orders o, customer c, order_item oi where o.order_id = oi.order_id AND o.customer_id = c.customer_id AND o.order_status != "delivered" Group BY placed_date;')).all()
        #if the query is empty return an empty list to prevent the data table from  crashing
        strResults = stringify(query) if len(query) !=  0  else []
        return render_template("manager_side/order_page.html" , orderTable_data= strResults)
    #if client side sends post to receive order items data
    elif request.method == 'POST':
        #get order id from post
        ord_id = request.form['order_id']
        with engine.connect() as connection:
            overlayDataR = db.session.execute( select(orders.order_id, customer.name,orders.order_status, orders.placed_date).where(orders.customer_id == customer.customer_id).where(orders.order_id == ord_id)).all()
            order_itemR = db.session.execute( select(item.item_id, item.item_name, seller.seller_id, order_item.quantity).where(item.item_id == order_item.item_id).where(item.seller_id == seller.seller_id).where(order_item.order_id == ord_id)).all()
        if overlayDataR is not None and order_itemR is not None:
            #convert overlay data into dictionary/json
            overlayData = {"order_id":str(overlayDataR[0][0]), "customer_name":str(overlayDataR[0][1]), "order_status": str(overlayDataR[0][2]), "placed_date": str(overlayDataR[0][3])}
            # convert order_item into list
            order_items_list=[]
            count=1
            for itemdata in order_itemR:
                row = [str(count),str(itemdata.item_id),str(itemdata.item_name),str(itemdata.seller_id),str(itemdata.quantity)]
                order_items_list.append(row)
                count+=1
        #return in the form of json
        return jsonify({'overlay':overlayData, 'table':order_items_list})

@app.route("/inventory", methods = ['POST', 'GET'])
def inventory_page():
    if request.method =="GET":
        with engine.connect() as connection:
          query = connection.execute(text("SELECT i.item_id, i.item_name, s.seller_id, sum(il.quantity) FROM item i, seller s, item_location il WHERE i.item_id = il.item_id AND i.seller_id = s.seller_id GROUP BY i.item_id")).all()
          strResults = stringify(query) if len(query) !=  0  else []
        return render_template("manager_side/inventory_page.html", invTable_data=strResults)
    elif request.method=="POST":
        itemid = request.form["item_id"]
        with engine.connect() as connection:
            overlayL = db.session.execute(select(item.item_id,seller.seller_id,item.weight,item.item_desc,item.item_name).where(seller.seller_id == item.seller_id).where(item.item_id == itemid)).all()
            item_locR = db.session.execute(select(item_location.location, item_location.quantity).where(item_location.item_id == itemid)).all()
        if len(overlayL) != 0 and len(item_locR) != 0:
            overlayRow = overlayL[0]
            overlayData = {"item_id": overlayRow.item_id, "seller_id":overlayRow.seller_id,"weight": str(overlayRow.weight) +"g", "item_desc":overlayRow.item_desc,"item_name":overlayRow.item_name}
            item_locList = []
            for itemdata in item_locR:
                row = {"location": itemdata.location, "quantity":itemdata.quantity}
                item_locList.append(row)
        return jsonify({"overlay":overlayData, "table":item_locList })

@app.route("/inbound_shipments", methods = ['POST', 'GET'])
def inbound_shipment_page():
    if request.method =="GET":
        with engine.connect() as connection:
          query = connection.execute(text("SELECT a.asn_id,  s.seller_name, a.shipment_type, a.arrival_date, a.arrival_time, a.asn_status FROM asn a,seller s WHERE a.seller_id = s.seller_id;")).all()
          strResults = stringify(query) if len(query) !=  0  else []
        return render_template("manager_side/inbound_shipments_page.html",inShipmentData=strResults)
    elif request.method=="POST":
        asnid =request.form["asn_id"]
        with engine.connect() as connection:
            overlayL = db.session.execute(select(asn.asn_id, asn.seller_id,seller.seller_name,asn.shipment_type,asn.arrival_date,asn.arrival_time).where(asn.seller_id == seller.seller_id).where(asn.asn_id == asnid)).all()
            tableL =db.session.execute(select(asn_items.item_id, item.item_name, item.item_desc, asn_items.quantity).where(asn_items.item_id == item.item_id).where(asn_items.asn_id == asnid)).all()
        if len(overlayL)!= 0 or len(tableL) != 0:
            overlayRow =overlayL[0]
            #convert overlay query to Json
            overlayData = {"shipment_no": overlayRow.asn_id, "seller_id":overlayRow.seller_id, "seller_name":overlayRow.seller_name, "shipment_type":overlayRow.shipment_type, "date":str(overlayRow.arrival_date),"time":str(overlayRow.arrival_time)}
            #convert asn data to list
            tableDataList = []
            for itemdata in tableL:
                row = [itemdata.item_id, itemdata.item_name, itemdata.item_desc, itemdata.quantity]
                tableDataList.append(row)
            return jsonify({'overlay':overlayData, "table": tableDataList})
        return jsonify({'overlay':"", "table": []})

@app.route("/receive_discrepancies", methods = ['POST', 'GET'])
def receive_discrepancy_page():
    if request.method == 'GET':
        with engine.connect() as connection:
            query = connection.execute(text("SELECT rd.asn_id, s.seller_id, s.seller_name, a.shipment_type, a.arrival_date,a.arrival_time FROM asn a, seller s, receive_discrepancies rd WHERE a.seller_id = s.seller_id AND rd.asn_id =a.asn_id")).all()
            strResults = stringify(query) if len(query) !=  0  else []
        return render_template("manager_side/receive_discrepancy_page.html", discrepancy=strResults)
    elif request.method == 'POST':
        asnid = request.form["asn_id"]
        with engine.connect() as connection:
            overlayL = db.session.execute(select(receive_discrepancies.asn_id, seller.seller_name, asn.shipment_type, asn.arrival_date,asn.arrival_time,receive_discrepancies.note).where(asn.seller_id == seller.seller_id).where(receive_discrepancies.asn_id == asn.asn_id).where(receive_discrepancies.asn_id == asnid)).all()
            tableL = db.session.execute(select(receive_discrepancies.item_id, item.item_name, receive_discrepancies.expected, receive_discrepancies.received, receive_discrepancies.damaged).where(receive_discrepancies.item_id == item.item_id).where(receive_discrepancies.asn_id == asnid))
        overlayRow = overlayL[0]
        #preparing table data in the form of a list
        disc_item_list = []
        for itemdata in tableL:
            row = [itemdata.item_id, itemdata.item_name, itemdata.expected, itemdata.received, itemdata.damaged]
            disc_item_list.append(row)
        overlayData = {"shipment_no":overlayRow.asn_id, "seller_name":overlayRow.seller_name, "shipment_type":overlayRow.shipment_type, "date":str(overlayRow.arrival_date), "time":str(overlayRow.arrival_time),"note":overlayRow.note}
        return jsonify({"overlay":overlayData, "table":disc_item_list})

@app.route("/deliveries", methods = ['POST', 'GET'])
def delivery_page():
    if request.method =="GET":
        with engine.connect() as connection:
            query = connection.execute(text('SELECT d.delivery_id, d.vehicle_num FROM orders o, delivery d WHERE o.order_id = d.order_id')).all()
        strResults = stringify(query) if len(query) !=  0  else []
        return render_template("manager_side/deliveries_page.html", deliveryData =strResults)
    elif request.method == "POST":
        if request.form["table"] == "del_orders":
            delid = request.form["del_id"]
            with engine.connect() as connection:
                overlayL = db.session.execute( select(delivery.delivery_id,delivery.vehicle_num,delivery.time).where(delivery.delivery_id == delid)).all()
                tableL = db.session.execute(select(delivery.order_id, customer.name, delivery.vehicle_num).where(delivery.order_id == orders.order_id).where(customer.customer_id == orders.customer_id).where(delivery.delivery_id==delid)).all()
            overlayRow = overlayL[0]
            overlayData = {"del_id":overlayRow.delivery_id, "vehicle_num":overlayRow.vehicle_num, "time":str(overlayRow.time)}
            del_list = []
            for itemdata in tableL:
                row = [itemdata.order_id,itemdata.name, itemdata.vehicle_num]
                del_list.append(row)
            return jsonify({"overlay":overlayData, "table":del_list})
        elif request.form["table"] == "del_ord_items":
            delordid = request.form["del_ord_id"]
            with engine.connect() as connection:
                overlayL = db.session.execute(select(orders.order_id, customer.name, delivery.date).where(orders.customer_id == customer.customer_id).where(delivery.order_id == orders.order_id).where(orders.order_id == delordid)).all()
                tableL = db.session.execute(select(item.item_id, item.item_name, seller.seller_name, order_item.quantity).where(item.item_id == order_item.item_id).where(item.seller_id == seller.seller_id).where(order_item.order_id == delordid)).all()
            overlayRow = overlayL[0]
            overlayData = {"ord_id":overlayRow.order_id, "cust_name":overlayRow.name, "date":str(overlayRow.date)}
            del_ord_item_list = []
            count = 1
            for itemdata in tableL:
                row = [str(count),itemdata.item_id, itemdata.item_name, itemdata.seller_name, itemdata.quantity]
                del_ord_item_list.append(row)
                count+=1
            return jsonify({"overlay":overlayData,"table":del_ord_item_list})

@app.route("/job_assignment", methods = ['POST', 'GET'])
def job_assigment_page():
    return render_template("manager_side/job_assignment_page.html")

@app.route("/employees", methods =["GET"])
def employee_page():
        with engine.connect() as connection:
            query = connection.execute(text('SELECT emp_id, name, email, phone_no FROM employee')).all()
        strResults = stringify(query) if len(query) !=  0  else []
        return render_template("manager_side/employee_page.html", employeeData =strResults)

@app.route("/pick_pack_assignment")
def pick_pack_assignment_page():
    return render_template("manager_side/pick_pack_assignment_page.html")

#employee side pages
@app.route("/main_menu")
def mainMenu():
    return render_template("employee_side/main_page.html")

@app.route("/instructions")
def instructions():
    return render_template("employee_side/instructions_page.html")

@app.route("/receive")
def receive():
    return render_template("employee_side/receiving_page.html")

@app.route("/putAway")
def putAway():
    return render_template("employee_side/put_away_page.html")

@app.route("/picking")
def picking():
    return render_template("employee_side/picking_page.html")

@app.route("/packing")
def packing():
    return render_template("employee_side/packing_page.html")

@app.route("/inventoryCount")
def inventoryCount():
    return render_template("employee_side/inventory_count_page.html")

@app.route("/loading")
def loading():
    return render_template("employee_side/loading_page.html")

#general methods
def stringify(List):
    result =[]
    for item in List:
        if isinstance(item, LegacyRow):
            result.append(stringify(item))
        else:
           result.append(str(item))
    return result




if(__name__) == "__main__":
    app.run(debug=True)
