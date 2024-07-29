import requests


def get_itens():
    url = 'http://127.0.0.1:5000/itens'  # URL da sua API Flask
    response = requests.get(url)

    if response.status_code == 200:
        itens = response.json()
        return itens
    else:
        print(f"Erro ao obter itens: {response.status_code}")
        return []


if __name__ == '__main__':
    itens = get_itens()
    for item in itens:
        print(item)
