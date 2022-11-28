from flask import Flask, redirect, url_for, render_template, request,jsonify, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text,select,delete, update
from ExpressWay_WMS.database import orders, customer, item_location,item, seller,asn, asn_items, receive_discrepancies, order_item, delivery, employee,instruction ,pick_list, shift,picking_parameters
from ExpressWay_WMS.database import db
from sqlalchemy.engine.row import LegacyRow
from datetime import timedelta
import random
import json




app = Flask(__name__)
app.secret_key = "FYP"
app.config['JSON_SORT_KEYS'] = False
app.permanent_session_lifetime = timedelta(hours=3)

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


engine = db.create_engine(SQLALCHEMY_DATABASE_URI, {})


db.init_app(app)
with app.app_context():
    db.create_all()

def manager_login(x):
    @wraps(x)
    def decorated_function(*args, **kwargs):
        if session.get("logged_in") is None or session.get("authorisation") != "manager":
            flash("Please Log in!")
            return render_template("login_page.html")
        return x(*args, **kwargs)
    return decorated_function
def emp_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("logged_in") is None or session.get("authorisation") != "worker":
            flash("Please Log in!")
            return render_template("login_page.html")
        return f(*args, **kwargs)
    return decorated_function

#build login page then use this function
@app.route('/', methods=['POST', 'GET'])
def login_page():
    if request.method =="GET":
        return render_template("login_page.html")
    elif request.method =="POST":
        emp_id = request.form.get("emp_id")
        password = request.form.get("password")
        #authenticate and authorise user
        employee_info = db.session.execute(select(employee.password, employee.position).where(employee.emp_id ==emp_id)).all()
        if len(employee_info) ==0 or compareTo(str(employee_info[0].password), password) != 0:
            flash("Invalid credentials!")
            return redirect(url_for("login_page"))
        else:
            session["emp_id"] = emp_id
            session["logged_in"] = "logged_in"
            session ["authorisation"] = employee_info[0].position
            session.permanent =True
            
            if session.get("authorisation") == "worker":
                return redirect(url_for('mainMenu'))
            elif session.get("authorisation") == "manager":
                return redirect(url_for('dashboard'))


# manager side pages
@app.route("/dashboard",methods = ['POST', 'GET'])
@manager_login
def dashboard():
    with engine.connect() as connection:
        ord= connection.execute(text('select count(order_id) from orders where order_status="pending";'))
        inBShip = connection.execute(text('SELECT COUNT(asn_id) FROM asn WHERE asn_status="pending" AND arrival_date= CURDATE();'))
        empPresent = connection.execute(text('SELECT COUNT(emp_id) FROM employee WHERE present = True;'))
    return render_template("manager_side/dashboard.html", numOrdTBF=ord.scalar() ,numInboundShipment =inBShip.scalar(), numEmpPresent =empPresent.scalar())


@app.route("/orders",methods = ['POST', 'GET'])
@manager_login
def orders_page():
    if request.method == 'GET':
        with engine.connect() as connection:
            query = connection.execute(text('SELECT o.order_id, c.name as "Customer Name", SUM(oi.quantity) as "num of items", order_status, placed_date FROM orders o, customer c, order_item oi where o.order_id = oi.order_id AND o.customer_id = c.customer_id  Group BY placed_date;')).all()
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
@manager_login
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
@manager_login
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
@manager_login
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
            tableL = db.session.execute(select(receive_discrepancies.item_id, item.item_name, receive_discrepancies.expected, receive_discrepancies.received, receive_discrepancies.damaged).where(receive_discrepancies.item_id == item.item_id).where(receive_discrepancies.asn_id == asnid)).all()
        overlayRow = overlayL[0]
        #preparing table data in the form of a list
        disc_item_list = []
        for itemdata in tableL:
            row = [itemdata.item_id, itemdata.item_name, itemdata.expected, itemdata.received, itemdata.damaged]
            disc_item_list.append(row)
        overlayData = {"shipment_no":overlayRow.asn_id, "seller_name":overlayRow.seller_name, "shipment_type":overlayRow.shipment_type, "date":str(overlayRow.arrival_date), "time":str(overlayRow.arrival_time),"note":overlayRow.note}
        return jsonify({"overlay":overlayData, "table":disc_item_list})

@app.route("/deliveries", methods = ['POST', 'GET'])
@manager_login
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
@manager_login
def job_assigment_page():
    if request.method == "GET":
        return render_template("manager_side/job_assignment_page.html")

    if request.method =="POST":
        #allows job table to update data periodically
        if "jobTab" in request.form:
            #shows employees with and without instructions (employees without instructions have "-" in their tasks and )
            with engine.connect() as connection:
                query = connection.execute(text("SELECT e.emp_id, e.name, i.task, i.station FROM employee e LEFT OUTER JOIN instruction i ON e.emp_id = i.emp_id WHERE e.position= 'worker' ORDER BY e.emp_id;")).all()
            strResults= []
            if len(stringify(query)) != 0:
                for row in stringify(query):
                    for i in range (2,4,1):
                        if(row[i]=="None"):
                            row[i] = "-"
                    strResults.append(row)
            return (jsonify({"data":strResults}))

        elif "update" in request.form:
            #adds a new instruction row to the database if there isnt one
            with engine.connect() as connection:
                instructionRows = db.session.query(instruction).filter(instruction.emp_id == request.form["data[emp_id]"]).all()
            if len(instructionRows)!=0:
                db.session.execute(delete(instruction).where(instruction.emp_id ==request.form["data[emp_id]"] ))
            instructions = instruction(emp_id = request.form["data[emp_id]"], task=request.form["data[task]"],station =request.form["data[station]"],instructions =request.form["data[instruction]"])
            db.session.add(instructions)
            db.session.commit()
            return ("s")
        elif "delete" in request.form:
            db.session.execute(delete(instruction).where(instruction.emp_id ==request.form["emp_id"] ))
            db.session.commit()
            return(str(request.form))


@app.route("/employees", methods =["GET"])
@manager_login
def employee_page():
        with engine.connect() as connection:
            query = connection.execute(text('SELECT emp_id, name, email, phone_no FROM employee')).all()
        strResults = stringify(query) if len(query) !=  0  else []
        return render_template("manager_side/employee_page.html", employeeData =strResults)

@app.route("/pick_pack_assignment", methods = ["GET","POST"])
@manager_login
def pick_pack_assignment_page():
    if request.method =="GET":
        return render_template("manager_side/pick_pack_assignment_page.html")

    elif request.method =="POST":
        #requests for table data
        if "table_data_req" in request.form:
            if request.form["table_data_req"] =="pending_orders":
                with engine.connect() as connection:
                    query = connection.execute(text("SELECT o.order_id, SUM(oi.quantity) as items, placed_date FROM orders o, order_item oi WHERE o.order_id = oi.order_id AND o.order_status = 'pending' Group BY o.order_id;")).all()
                strResults= query
                if len(strResults) == 0:
                    strResults = []
                return (jsonify({"data":stringify(strResults)}))

            elif request.form["table_data_req"] == "available_emp":
                with engine.connect() as connection:
                    query = connection.execute(text("SELECT e.emp_id, e.name, i.task, i.station FROM employee e LEFT OUTER JOIN instruction i ON e.emp_id = i.emp_id WHERE position ='worker'")).all()
                strResults= []
                if len(stringify(query)) != 0:
                    for row in stringify(query):
                        for i in range (2,4,1):
                            if(row[i]=="None"):
                                row[i] = "-"
                        strResults.append(row)
                return(jsonify({"data":strResults}))
        #request for generating pick list
        if "pick_pack_para" in request.form:

            #check if inventory has enough items to fulfil order
            selectedOrders = request.form["ord_id"]
            with engine.connect() as connection:
                ord_inv_list = connection.execute(text("""
                    SELECT ord.item_id,  ord_quantity, inv_quantity
                    FROM (
                        SELECT il.item_id, SUM(il.quantity) AS inv_quantity
                        FROM item_location il
                        WHERE item_id IN(
                            SELECT item_id
                            FROM order_item
                            WHERE order_id IN ({})
                        )
                        GROUP BY il.item_id
                        ORDER BY il.item_id
                    ) inv RIGHT OUTER JOIN (
                        SELECT oi.item_id, SUM(oi.quantity) AS ord_quantity
                        FROM order_item oi, orders o
                        WHERE oi.order_id = o.order_id
                        AND oi.order_id IN({})
                        GROUP BY oi.item_id
                        ORDER BY oi.item_id
                    ) ord
                    ON ord.item_id = inv.item_id;
                """.format(selectedOrders[1:-1],selectedOrders[1:-1]))). all()
            insufItems =[]
            fulfilable =True
            for ord_inv in ord_inv_list:
                item_id =  ord_inv.item_id
                if str(ord_inv.inv_quantity) == "None":
                    insufItems.append(item_id)
                    fulfilable = False
                else:
                    if ord_inv.ord_quantity > ord_inv.inv_quantity:
                        insufItems.append(item_id)
                        fulfilable = False
            if not fulfilable:
                return {"insufficient_items": str(insufItems)}
            #if inventory has sufficient stock add parameters to database to allow script to generate pick list at specified time
            with engine.connect() as conn:
                conn.execute(text("DELETE FROM picking_parameters where 1=1 "))
            selectedEmployees = request.form["emp_id"]
            pick_para = picking_parameters(id = 1, order_ids ={'order_id':selectedOrders[1:-1]}, employee_ids ={'employee_id':selectedEmployees[1:-1]})
            db.session.add(pick_para)
            db.session.commit()
            return ({"success":"success"})

#employee side pages
@app.route("/main_menu", methods = ["GET","POST"])
@emp_login
def mainMenu():
    return render_template("employee_side/main_page.html")

@app.route("/instructions", methods = ["GET","POST"])
@emp_login
def instructions():
    if request.method == "GET":
        return render_template("employee_side/instructions_page.html")

    elif request.method =="POST":
        tasks = db.session.execute(select(instruction.task, instruction.station, instruction.instructions).where(instruction.emp_id == session.get("emp_id"))).all()
        if len(tasks) ==0:
            return{"no_inst":stringify([])}
        else:
            return ({"data":[stringify([tasks[0].task, tasks[0].station])], "inst":tasks[0].instructions})

@app.route("/receive", methods = ["GET","POST"])
@emp_login
def receive():
    if request.method == "GET":
        return render_template("employee_side/receiving_page.html")
    elif request.method == "POST":
        if "ship_tdy" in request.form:    
            with engine.connect() as connection:
                data = connection.execute(text("SELECT asn_id, arrival_time, vehicle_no, asn_status FROM asn  where DATE(arrival_date) = curdate() and asn_status = 'pending'")).all()
            asn_list =[]
            for asn in data:
                row = [str(asn.asn_id),str(asn.arrival_time), asn.vehicle_no, asn.asn_status]
                asn_list.append(row)
            return (jsonify({"asn":asn_list}))
        elif "asn_items" in request.form:
            asnid = request.form.get("asn_id")
            with engine.connect() as connection:
                data = connection.execute(text("SELECT ai.item_id, i.item_name, i.item_desc, ai.quantity FROM asn_items ai, item i WHERE ai.item_id = i.item_id AND asn_id = {}".format(asnid))).all()
            asn_item_list =[]
            for asn_item in data:
                row = [asn_item.item_id, asn_item.item_name, asn_item.item_desc, asn_item.quantity]
                asn_item_list.append(row)
            return(jsonify({"asn_items":asn_item_list}))
        elif "asn_info" in request.form:
            asnid = request.form.get("asn_id")
            with engine.connect() as connection:
                data = connection.execute(text("SELECT ai.item_id, i.item_name, ai.quantity FROM asn_items ai, item i WHERE ai.item_id = i.item_id AND asn_id = {}".format(asnid))).all()
            asn_item_list = []
            for asn_item in data:
                row = [asn_item.item_id, asn_item.item_name, asn_item.quantity, "-", "-"]
                asn_item_list.append(row)
            return (jsonify({"data": asn_item_list}))
        elif "receive" in request.form:
            asn_id = request.form.get("asn_id")
            with engine.connect() as connection:
                #query for items that are already in the warehouse and items that are not
                nonDupItems =  connection.execute(text("select item_id, quantity from asn_items WHERE item_id Not IN ( select ai.item_id from asn_items ai, item_location il where ai.item_id = il.item_id AND asn_id = {})AND asn_id = {}".format(asn_id, asn_id))).all()
                dupItems = connection.execute(text("select distinct ai.item_id, ai.quantity from asn_items ai, item_location il WHERE ai.item_id = il.item_id AND ai.asn_id = {}".format(asn_id))).all()
            for item in dupItems:
                with engine.connect() as connection:
                    disc = connection.execute(text("select received from receive_discrepancies where item_id ={} and asn_id ={}".format(item.item_id, asn_id))).all()
                    if len(disc) == 0:
                        item_quantity = item.quantity
                    else:
                        item_quantity = disc[0].received
                    loc = connection.execute(text("select location, quantity from item_location where item_id = {} order by quantity".format(item.item_id))).all()[0]
                    connection.execute(text("insert into received_items values({},0, {}, \'{}\')".format(item.item_id, item_quantity, loc.location)))
            for item in nonDupItems:
                with engine.connect() as connection:
                    disc = connection.execute(text("select received from receive_discrepancies where item_id ={} and asn_id ={}".format(item.item_id, asn_id))).all()
                    if len(disc) == 0:
                        item_quantity = item.quantity
                    else:
                        item_quantity = disc[0].received
                    connection.execute(text("insert into received_items values({},0, {}, \'{}\'))".format(item.item_id,  item_quantity,genRandLoc())))
            with engine.connect() as connection:
               connection.execute(text("update asn set asn_status = 'received' where asn_id = {}".format(asn_id)))
            return ({"success":"success"})
        elif "disc_report" in request.form:
            db.session.add(receive_discrepancies(asn_id = request.form.get("asn_id"),item_id = request.form.get("item_id"),note = request.form.get("note"),expected = request.form.get("expected"),received = request.form.get("received"),damaged = request.form.get("damaged")))
            db.session.commit()
            return ({"success":"success"})



@app.route("/putAway", methods = ["GET","POST"])
@emp_login
def putAway():
    if request.method == "GET":
        return render_template("employee_side/put_away_page.html")
    elif request.method == "POST":
        if "put_away_items" in request.form:
            with engine.connect() as connection:
                query =connection.execute(text("select ri.item_id, i.item_name, ri.location from received_items ri, item i where ri.item_id = i.item_id and putaway = false;")).all()
            item_list =[]
            for item in query:
                row =[item.item_id, item.item_name, item.location ]
                item_list.append(row)
            return ({"data":item_list})
        elif "confirmPA" in request.form:
            item_id = request.form.get("item_id")
            with engine.connect() as connection:
                item = connection.execute(text("select item_id from item_location  where item_id = {}".format(item_id))).all()
                item_info = connection.execute(text("select location, quantity from received_items where item_id ={}".format(item_id))).all()[0]
                connection.execute("update received_items set putaway = 1 where item_id = {}".format(item_id))

            if len(item_id) == 0:
                db.session.add(item_location(location = item_info.location, item_id=item_id, quantity = item_info.quantity))
                db.session.commit()
            else:
                with engine.connect() as connection:
                    connection.execute(text("update item_location set quantity = quantity + {} where location = \'{}\'".format(item_info.quantity, item_info.location)))
            return({"success":"success"})
        

@app.route("/picking", methods = ["GET","POST"])
@emp_login
def picking():
    if request.method == "GET":
        return render_template("employee_side/picking_page.html")

    elif request.method == "POST":
        if "pick_orders" in request.form:
            with engine.connect() as connection:
                query = connection.execute(text("select oi.order_id, count(oi.item_id) as noOfItems from assigned_orders ao, order_item oi where ao.order_id = oi.order_id and emp_id ={} group by order_id".format(session["emp_id"]))).all()
            order_list = []
            x=1
            for item in query:
                row = [x, item.order_id,item.noOfItems]
                order_list.append(row)
                x+=1
            return({"data": order_list})
        elif "order_items" in request.form:
            order_id = request.form["order_id"]
            with engine.connect() as connection:
                query = connection.execute(text("select i.item_id, i.item_name, o.quantity from item i, order_item o where i.item_id = o.item_id and o.order_id =  {}".format(order_id))).all()
            item_list = []
            x=1
            for item in query:
                row =[x, item.item_id, item.item_name,item.quantity]
                x+=1
                item_list.append(row)
            return({"data":item_list})
        elif "picklist" in request.form:
            with engine.connect() as connection:
                query = connection.execute(text("select pick_list from pick_list where emp_id = {}".format(session["emp_id"]))).all()
            item_list =[]
            x=1
            if len(query) != 0:
                pickListJson = json.loads(query[0].pick_list)
                items = list(pickListJson.values())
                
                for item in items:                    
                    with engine.connect() as connection:
                        item_name = connection.execute(text("select item_name from item where item_id ={}".format(item.get("item_id")))).all()[0].item_name
                    row = [x, item.get("item_id"), item_name, item.get("quantity"),item.get("location")]
                    item_list.append(row)
                    x+=1
            return ({"data":item_list })
        elif "complete_pick" in request.form:
            with engine.connect() as connection:
                query = connection.execute(text("select pick_list from pick_list where emp_id = {}".format(session["emp_id"]))).all()
            if len(query) != 0:
                pickListJson = json.loads(query[0].pick_list)
                items = list(pickListJson.values())
            for item in items:
                with engine.connect() as connection:
                    query = connection.execute(text("update item_location set quantity = quantity - {} where location = \"{}\" ".format(item.get("quantity"), item.get("location"))))     
                    #free up empty locations in database
                    connection.execute(text("delete from item_location where quantity<1"))
            return ({"success":"success"})

@app.route("/packing", methods = ["GET","POST"])
@emp_login
def packing():
    if request.method == "GET":
        return render_template("employee_side/packing_page.html")
    elif request.method =="POST":
        if "pack_orders" in request.form:
            with engine.connect() as connection:
                packitem = connection.execute(text("select o.order_id, count(oi.item_id) as noOfItems, sum(i.weight) as weight from orders o, order_item oi, item i where o.order_id = oi.order_id and oi.item_id = i.item_id and o.order_status = 'picking' group by o.order_id;")).all()
            item_list =[]
            x=1
            if len(packitem) != 0:
                for item in packitem:
                    row =[x, item.order_id, item.noOfItems,(str(item.weight) +"g")]
                    item_list.append(row)
                    x+=1
            return({"data":item_list})
        elif "order_items" in request.form:
            order_id =request.form.get("order_id")
            with engine.connect() as connection:
                ordItem = connection.execute(text("select oi.item_id, oi.quantity, i.weight from order_item oi, item i where oi.item_id = i.item_id and oi.order_id = {}".format(order_id))).all()
            row_list =[]
            x=1
            for item in ordItem:
                row =[x, item.item_id, item.quantity, item.weight]
                row_list.append(row)
                x+=1
            return({"data":row_list})
        elif "completePack" in request.form:
            order_id = request.form.get("order_id")
            with engine.connect() as connection:
                connection.execute(text("update orders set order_status ='packed' where order_id ={} ".format(order_id)))
            return({"success":"s"})
            


@app.route("/inventoryCount", methods = ["GET","POST"])
@emp_login
def inventoryCount():
    if request.method == "GET":
        return render_template("employee_side/inventory_count_page.html")
    elif request.method == "POST":
        if "chkInv" in request.form:
            location = request.form.get("location")
            with engine.connect() as connection:
                query = connection.execute(text("select item_id, location, quantity from item_location where location =\"{}\"".format(location))).all()
            if len(query) == 0:
                return({"no item":"no item"})
            else:
                return({"success":"success","item_id":query[0].item_id, "location":query[0].location, "quantity":query[0].quantity})
        elif "update_inv":
            location = request.form.get("location")
            quantity = request.form.get("quantity")
            with engine.connect() as connection:
                connection.execute(text("update item_location set quantity = {} where location = \"{}\"".format(quantity, location)))
            return({"success":"success"})


@app.route("/loading", methods = ["GET","POST"])
@emp_login
def loading():
    return render_template("employee_side/loading_page.html")

#logout 
@app.route("/logout", methods = ["GET","POST"])
def logout():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for('login_page'))


#general methods
def stringify(List):
    result =[]
    for item in List:
        if isinstance(item, LegacyRow):
            result.append(stringify(item))
        else:
           result.append(str(item))
    return result
#used to sanitise user input (returns zero when string matches exactly)
def compareTo(a,b):
    return ((a > b) - (a < b))

def genRandLoc ():
    while True:
        aisle = ["01","02","03","04"]
        rack = ['A','B','C','D']
        bay =["1","2","3","4","5","6","7","8"]
        level = ["L1","L2","L3"]
        bin =["1","2","3"]
        ordaisle = str(random.choice(aisle)) 
        if ordaisle == "01":
            orderrack = 'A'
        else:
            aisles= int(ordaisle) 
            orderrack = str(random.choice(rack[aisles-2: aisles]))
        ordbay = str(random.choice(bay))  
        ordlevel = str(random.choice(level)) 
        ordbin = str(random.choice(bin))
        ordloc = ordaisle+ "-" + orderrack + "-"+ordbay +"-"+ordlevel +"-" +ordbin
        with engine.connect() as connection:
            chk = connection.execute(text("select location from item_location where location = {}".format(ordloc))).all()
        if len(chk)==0:
            return ordloc



if(__name__) == "__main__":
    app.run(debug=True)
