from flask import Flask, request, render_template
import database as db

db.create_database()

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template("home.html")

@app.route("/portal", methods=['GET','POST'])
def portal():

    tabs = db.get_tabs()
    organizations = db.get_organizations()
    
    return render_template("portal.html", tabs=tabs, organizations=organizations)

@app.route("/portal/<tab>", methods=['GET','POST'])
def portal_tab(tab):
    
        tabs = db.get_tabs()
        organizations = db.get_organizations(tab)
    
        return render_template("portal.html", tabs=tabs, organizations=organizations, tab_selected=tab)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)