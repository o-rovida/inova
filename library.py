def generate_html(tab_id):
    
    from bs4 import BeautifulSoup
    import requests
    import pyperclip as pc
    
    url = f'http://localhost:5000/portal/{tab_id}'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    html_basic = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    """

    head = soup.find('head')
    head = str(head)

    search_bar = soup.find('input', {'id': 'search'})
    search_bar = str(search_bar)

    organization_table = soup.find('table', {'id': 'organization_table'})
    organization_table = str(organization_table)

    soup.find('head').extract()
    
    script_list = []

    for script in soup.find_all('script'):
        script_list.append(str(script))

    html = [html_basic, head, '<body>', '<div>',search_bar, '</div> <div>',organization_table, '</div>'] + script_list + ['</body>','</html>']
    html = '\n'.join(html)
    
    pc.copy(html)

    return organization_table

if __name__ == "__main__":
    generate_html(1)