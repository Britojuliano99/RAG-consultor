import requests

# URL da API
url = 'http://localhost:5000/pedidos'

# Dados do Pedido
pedido_data = {
    "cliente_id": 1,
    "data_pedido": "2024-07-29",
    "valor": 2000.00,
    "data_entrega": "2024-08-05",
    "itens": [
        {"item_id": 1, "quantidade": 100},
        {"item_id": 2, "quantidade": 5},
        {"item_id": 3, "quantidade": 9}
    ]
}

# Enviar a Requisição POST
response = requests.post(url, json=pedido_data)

# Verificar a Resposta
if response.status_code == 201:
    print('Pedido criado com sucesso!')
else:
    try:
        error_message = response.json()
    except requests.exceptions.JSONDecodeError:
        error_message = response.text
    print(f'Erro ao criar pedido: {error_message}')
