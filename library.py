def generate_html(tab_id):
    
    from bs4 import BeautifulSoup
    import requests
    import pyperclip as pc
    
    url = f'http://localhost:5000/portal/{tab_id}'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    html = soup.prettify()

    organization_table = soup.find('table', {'id': 'organization_table'})
    organization_table = str(organization_table)
    
    pc.copy(organization_table)

    return organization_table

if __name__ == "__main__":
    generate_html(1)