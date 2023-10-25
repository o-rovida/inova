from flask import Flask, request, render_template
import database as db
import library
from location import country_dict, federation_unity_list

db.create_database()

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template("home.jinja2")

@app.route("/portal", methods=['GET','POST'])
def portal():
    tabs = db.get_tabs()
    organizations = db.get_organizations("0")
    count_organizations = len(organizations)
    return render_template("portal.jinja2", tabs=tabs, organizations=organizations, count_organizations=count_organizations, tab_selected=0)

@app.route("/portal/<tab_id>", methods=['GET','POST'])
def portal_tab(tab_id):
    
    tabs = db.get_tabs()

    is_start_up = 0
    
    for tab in tabs:
        if str(tab['TabId']) == tab_id:
            is_start_up = tab['IsStartUp']
        else:
            continue

    organizations = db.get_organizations(tab_id)

    count_organizations = len(organizations)

    return render_template("portal.jinja2", tabs=tabs, organizations=organizations, count_organizations=count_organizations, tab_selected=tab_id, is_start_up=is_start_up)

@app.route("/portal/organization", methods=['GET','POST'])
def create_organization():
    tabs = db.get_tabs()
    return render_template("create_organization.jinja2", tabs=tabs, countries=country_dict.values(), federation_unities=federation_unity_list)

@app.route("/portal/organization/<organization_id>", methods=['GET','POST'])
def edit_organization(organization_id):
    #tabs = db.get_tabs()
    organization = db.get_a_single_organization(organization_id)
    return render_template("organization.jinja2", organization=organization, countries=country_dict.values(), federation_unities=federation_unity_list)

@app.route("/execute/generate_html", methods=['POST'])
def execute():
    return library.generate_html(request.form['tab_selected'])

@app.route("/execute/crate_organization", methods=['POST'])
def execute_create_organization():
    data = request.get_json()

    name = data['Name']
    website = data['WebSite']
    short_description = data['ShortDescription']
    country = data['Country']
    federation_unity = data['FederationUnity']
    types = data['Type']

    return db.create_organization_register(name, website, short_description, country, federation_unity, types)

@app.route("/execute/update_organization", methods=['POST'])
def execute_update_organization():
    data = request.get_json()

    name = data['Name']
    website = data['WebSite']
    short_description = data['ShortDescription']
    country = data['Country']
    federation_unity = data['FederationUnity']
    organization_id = data['OrganizationId']

    return db.update_organization_register(name, website, short_description, country, federation_unity, organization_id)

@app.route("/execute/delete_organization", methods=['POST'])
def execute_delete_organization():
    data = request.get_json()

    organization_id = data['OrganizationId']

    return db.delete_organization_register(organization_id)

@app.route("/execute/get_types", methods=['POST'])
def execute_get_types():
    data = request.get_json()
    tab_id = data['TabId']
    return db.get_types(tab_id)

if __name__ == "__main__":
    app.run(debug=True, port=5000)