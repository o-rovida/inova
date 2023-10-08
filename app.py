from flask import Flask, request, render_template
import database as db
import library

db.create_database()

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template("home.jinja2")

@app.route("/portal/<tab>", methods=['GET','POST'])
def portal_tab(tab):
    
        tabs = db.get_tabs()
        organizations = db.get_organizations(tab)
        count_organizations = len(organizations)
    
        return render_template("portal.jinja2", tabs=tabs, organizations=organizations, count_organizations=count_organizations, tab_selected=tab)

@app.route("/execute/generate_html", methods=['POST'])
def execute():
    return library.generate_html(request.form['tab_selected'])

if __name__ == "__main__":
    app.run(debug=True, port=5000)