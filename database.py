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
    tab_query = "SELECT TabId, Name, IsStartUp FROM Tab ORDER by IsStartUp, Name"

    conn = sqlite3.connect('database/portal_db.db')
    tab_df = pd.read_sql_query(tab_query, conn)
    conn.close()

    tabs = tab_df.to_dict(orient='records')
    return tabs

def get_types(tab_id):
    type_query = f"SELECT TypeId, Name as TypeName FROM Type WHERE TabId = {tab_id} ORDER by Name"

    conn = sqlite3.connect('database/portal_db.db')
    type_df = pd.read_sql_query(type_query, conn)
    conn.close()
    types = type_df.to_dict(orient='records')

    return types

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
        o.City,
        GROUP_CONCAT(tp.Name, ' , ') as Types
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
        o.FederationUnity,
        o.City
    FROM [Organization] o
    WHERE o.OrganizationId = {organization_id}
    """
    conn = sqlite3.connect('database/portal_db.db')
    single_organization_df = pd.read_sql_query(single_organization_query, conn)
    conn.close()

    single_organization_df['Country'] = location.translate_country_codes(single_organization_df['Country'])

    single_organization = single_organization_df.to_dict(orient='records')
    single_organization = single_organization[0]

    return single_organization

def create_organization_register(name, website, short_description, country, federation_unity, types, city):
        country_values = list(location.country_dict.values())
        country_keys = list(location.country_dict.keys())
        country = country_keys[country_values.index(country)] 
               
        query = f"""
        INSERT INTO [Organization]
            (Name, WebSite, ShortDescription, Country, FederationUnity, City)
        VALUES
            ("{name}", "{website}", "{short_description}", '{country}', '{federation_unity}', '{city}')
        """
            
        conn = sqlite3.connect('database/portal_db.db')
        conn.execute(query)
        conn.commit()
        
        last_id = "SELECT last_insert_rowid() as last_id"

        last_id_df = pd.read_sql_query(last_id, conn)
        organization_id = last_id_df['last_id'][0]
        
        for type_id in types:
            query = f"""
            INSERT INTO [OrganizationType]
                (OrganizationId, TypeId)
            VALUES
                ({organization_id}, {type_id})
            """
            conn.execute(query)
            conn.commit()
            
        conn.close()
        
        return "Organização criada com sucesso!"

def update_organization_register(name, website, short_description, country, federation_unity, organization_id, city):
        
    country_values = list(location.country_dict.values())
    country_keys = list(location.country_dict.keys())
    country = country_keys[country_values.index(country)] 
        
    query = f"""
    UPDATE [Organization]
    SET
        Name = "{name}",
        WebSite = "{website}",
        ShortDescription = "{short_description}",
        Country = '{country}',
        FederationUnity = '{federation_unity}',
        City = '{city}'
    WHERE OrganizationId = {organization_id}
    """
        
    conn = sqlite3.connect('database/portal_db.db')
    conn.execute(query)
    conn.commit()
    conn.close()
    
    return "Organização editada com sucesso!"

def delete_organization_register(organization_id):
    query = f"""
    DELETE FROM [Organization]
    WHERE OrganizationId = {organization_id}
    """
        
    conn = sqlite3.connect('database/portal_db.db')
    conn.execute(query)
    conn.commit()
    conn.close()
    
    return "Organização deletada com sucesso!"

if __name__ == "__main__":
    create_database()