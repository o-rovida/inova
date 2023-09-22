from flask import Flask, render_template
import database as db

db.create_database()
tabs = db.get_tabs()
organizations = db.get_organizations()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/portal")
def portal():
    return render_template("portal.html", tabs=tabs, organizations=organizations)

@app.route("/descomplica")
def descomplica():
    return render_template("descomplica.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)