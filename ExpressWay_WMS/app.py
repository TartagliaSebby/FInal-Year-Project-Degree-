from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template("login_page.html")



if(__name__) == "__main__":
    app.run(debug=True)
