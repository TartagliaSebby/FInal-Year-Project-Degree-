from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text,select
from ExpressWay_WMS.database import orders
from ExpressWay_WMS.database import db
from sqlalchemy.engine.row import LegacyRow
import json



app = Flask(__name__)

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
    if request.method == 'GET':
        with engine.connect() as connection:
            query = connection.execute(text('SELECT o.order_id, c.name as "Customer Name", SUM(oi.quantity) as "num of items", order_status, placed_date FROM orders o, customer c, order_item oi where o.order_id = oi.order_id AND o.customer_id = c.customer_id AND o.order_status != "delivered" Group BY placed_date;'))
        results = query.all()
        strResults = json.dumps(stringify(results))
    elif request.method == 'POST':
        #access formdata selectedOrd
        with engine.connect() as connection:
            query = db.session.execute( select(orders.order_id, customer.name,orders.order_status, orders.placed_date).where(order.customer_id == customer.customer_id).where(order.order_id == selectedOrd))
    return render_template("manager_side/order_page.html" , orderTable_data= strResults, orderItemsTable_data =strResults)

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
    with engine.connect() as connection:
        query = connection.execute(text('SELECT o.order_id, c.name as "Customer Name", SUM(oi.quantity) as "num of items", order_status, placed_date FROM orders o, customer c, order_item oi where o.order_id = oi.order_id AND o.customer_id = c.customer_id AND o.order_status != "delivered" Group BY placed_date;'))
    results = query.all()
    #strResults = [[for str(s) in sublist] for sublist in results]
    strResults = json.dumps(stringify(results))
    #strResults = type(results[0])
    return render_template("manager_side/order_page.html", orderTable_data= strResults, testjson =strResults)

@app.route("/inventory", methods = ['POST', 'GET'])
def inventory_page():
    return render_template("manager_side/inventory_page.html")

@app.route("/inbound_shipments", methods = ['POST', 'GET'])
def inbound_shipment_page():
    return render_template("manager_side/inbound_shipments_page.html")

@app.route("/receive_discrepancies")
def receive_discrepancy_page():
    return render_template("manager_side/receive_discrepancy_page.html")

@app.route("/deliveries")
def delivery_page():
    return render_template("manager_side/deliveries_page.html")

@app.route("/job_assignment")
def job_assigment_page():
    return render_template("manager_side/job_assignment_page.html")

@app.route("/employees")
def employee_page():
    return render_template("manager_side/employee_page.html")

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
@app.route('/postSimple', methods=['POST'])
def get_simple_js():
    simpleJsData = request.form['simpleJsData']
    return simpleJsData


if(__name__) == "__main__":
    app.run(debug=True)
