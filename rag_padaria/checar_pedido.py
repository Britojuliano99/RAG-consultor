import requests

# URL da API
url = 'http://localhost:5000/pedidos'

# Enviar a Requisição GET
response = requests.get(url)

# Verificar a Resposta
if response.status_code == 200:
    pedidos = response.json()
    print('Lista de pedidos:')
    for pedido in pedidos:
        print(pedido)
else:
    print(f'Erro ao obter pedidos: {response.status_code}')
