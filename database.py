import sqlite3
import os
import pandas as pd
import location

def create_database():

    if not os.path.exists("database/portal_db.db"):
        conn = sqlite3.connect('database/portal_db.db')
        with open('database/schema_portal_db.sql') as f:
            conn.executescript(f.read())
        conn.close()

    if not os.path.exists("database/descomplica_db.db"):
        conn = sqlite3.connect('database/descomplica_db.db')
        with open('database/schema_descomplica_db.sql') as f:
            conn.executescript(f.read())
        conn.close()

def get_tabs():
    tab_query = "SELECT TabId, Name FROM Tab"

    conn = sqlite3.connect('database/portal_db.db')
    tab_df = pd.read_sql_query(tab_query, conn)
    conn.close()

    tabs = tab_df.to_dict(orient='records')
    return tabs

def get_organizations(tab_id=None):
    
    if tab_id == None or tab_id == "0":
        where = " "
    else:
        where = f"WHERE tb.TabId = {tab_id}"

    organization_query = f"""
    SELECT
        o.OrganizationId,
        o.Name,
        o.WebSite,
        o.ShortDescription,
        o.Country,
        o.FederationUnity,
        GROUP_CONCAT(tp.Name, ', ') as Types
    FROM [OrganizationType] ot
        INNER JOIN [Organization] o ON ot.OrganizationId = o.OrganizationId
        INNER JOIN [Type] tp ON tp.TypeId = ot.TypeId
        INNER JOIN [Tab] tb ON tb.TabId = tp.TabId
    {where}
    GROUP BY
        o.Name,
        o.WebSite,
        o.ShortDescription,
        o.Country,
        o.FederationUnity
    ORDER BY o.Name ASC
    """
    conn = sqlite3.connect('database/portal_db.db')
    organization_df = pd.read_sql_query(organization_query, conn)
    conn.close()

    organization_df['Country'] = location.translate_country_codes(organization_df['Country'])
    organization_df['FederationUnity'] = location.translate_federation_unity_codes(organization_df['FederationUnity'])

    organizations = organization_df.to_dict(orient='records')

    return organizations

def get_a_single_organization(organization_id): #preciso identificar a melhor forma de pegar a lista de tipos de uma organização
    single_organization_query = f"""
    SELECT
        o.OrganizationId,
        o.Name,
        o.WebSite,
        o.ShortDescription,
        o.Country,
        o.FederationUnity
    FROM [Organization] o
    WHERE o.OrganizationId = {organization_id}
    """
    conn = sqlite3.connect('database/portal_db.db')
    single_organization_df = pd.read_sql_query(single_organization_query, conn)
    conn.close()

    single_organization_df['Country'] = location.translate_country_codes(single_organization_df['Country'])
    single_organization_df['FederationUnity'] = location.translate_federation_unity_codes(single_organization_df['FederationUnity'])

    single_organization = single_organization_df.to_dict(orient='records')
    single_organization = single_organization[0]

    return single_organization

def update_organization_register(name, website, short_description, country, federation_unity, organization_id):
        
    #country_values = list(location.country_dict.values())
    #country_keys = list(location.country_dict.keys())
    #country = country_keys[country_values.index(country)] 
        
    #federation_unity_values = list(location.federation_unity_dict.values())
    #federation_unity_keys = list(location.federation_unity_dict.keys())
    #federation_unity = federation_unity_keys[federation_unity_values.index(federation_unity)]

    query = f"""
    UPDATE [Organization]
    SET
        Name = '{name}',
        WebSite = '{website}',
        ShortDescription = '{short_description}',
        Country = '{country}',
        FederationUnity = '{federation_unity}'
    WHERE OrganizationId = {organization_id}
    """
        
    conn = sqlite3.connect('database/portal_db.db')
    conn.execute(query)
    conn.commit()
    conn.close()
    
    return "Organização editada com sucesso!"

if __name__ == "__main__":
    create_database()