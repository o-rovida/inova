def generate_html(tab_id):
    
    from bs4 import BeautifulSoup
    import requests
    import pyperclip as pc
    
    url = f'http://localhost:5000/portal/{tab_id}'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    head = """
<head>
<style>
/* Estilização da tooltip */
.tooltip-inner {
  max-width: 200px; /* Ajuste o valor conforme necessário */
  background-color: #f0f0f0; /* Cor de fundo cinza claro */
  color: #333; /* Cor do texto */
  padding: 10px; /* Espaçamento interno */
  border-radius: 5px; /* Borda arredondada */
  white-space: pre-wrap; /* Quebra de linha automática */
}

</style>
</head>
"""
    search_bar = soup.find('input', {'id': 'search'})
    search_bar = str(search_bar)

    organization_table = soup.find('table', {'id': 'organization_table'})
    organization_table = str(organization_table)
   
    script_list = []

    for script in soup.find_all('script'):
        script_list.append(str(script))

    # o head tem que ser um estilização que combine no WordPress, não necessariamente o head do sistema, depois testar estilos.
    # remover js nao utilizado
    html = [head,'<body>', '<div>',search_bar, '</div> <div>',organization_table, '</div>'] + script_list[0:-1] + ['</body>']
    html = '\n'.join(html)
    
    pc.copy(html)

    return organization_table

if __name__ == "__main__":
    generate_html(1)