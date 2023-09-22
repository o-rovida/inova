import sqlite3
import os
import pandas as pd

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
    
    if tab_id == None:
        where = " "
    else:
        where = f"WHERE tb.TabId = {tab_id}"

    organization_query = f"""
    SELECT
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

    organizations = organization_df.to_dict(orient='records')

    return organizations

if __name__ == "__main__":
    create_database()