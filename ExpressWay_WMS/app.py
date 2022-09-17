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
    return render_template("manager_side/dashboard.html")

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

if(__name__) == "__main__":
    app.run(debug=True)
