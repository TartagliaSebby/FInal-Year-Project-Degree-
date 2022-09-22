from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

""""
build login page then use this function
@app.route('/')
def login_page():
    return render_template("login_page.html")
"""""
@app.route("/")
def main():
    return render_template("employee_side/main_page.html")

# manager side pages
@app.route("/dashboard")
def dashboard():
    return render_template("manager_side/dashboard.html")

@app.route("/orders")
def orders_page():
    return render_template("manager_side/order_page.html")

@app.route("/inventory")
def inventory_page():
    return render_template("manager_side/inventory_page.html")

@app.route("/inbound_shipments")
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

if(__name__) == "__main__":
    app.run(debug=True)
