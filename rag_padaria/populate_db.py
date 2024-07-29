from app import db, Item  # Certifique-se de que a configuração de importação está correta
from datetime import datetime

def populate_items():
    itens = [
        {
            'nome': 'Pão Francês',
            'descricao': 'Pão francês fresco e crocante.',
            'embalagem': 'Saco de papel',
            'valor': 0.50,
            'data_fabricacao': datetime.strptime('2024-07-01', '%Y-%m-%d').date(),
            'data_validade': datetime.strptime('2024-07-07', '%Y-%m-%d').date(),
            'ingredientes': 'Farinha, água, sal, fermento',
            'informacoes_nutricionais': '250 calorias por 100g'
        },
        {
            'nome': 'Bolo de Chocolate',
            'descricao': 'Bolo de chocolate recheado com creme.',
            'embalagem': 'Caixa de papelão',
            'valor': 15.00,
            'data_fabricacao': datetime.strptime('2024-07-02', '%Y-%m-%d').date(),
            'data_validade': datetime.strptime('2024-07-10', '%Y-%m-%d').date(),
            'ingredientes': 'Farinha, açúcar, cacau, ovos, manteiga',
            'informacoes_nutricionais': '400 calorias por 100g'
        },
        {
            'nome': 'Croissant',
            'descricao': 'Croissant amanteigado e folhado.',
            'embalagem': 'Saco plástico',
            'valor': 3.00,
            'data_fabricacao': datetime.strptime('2024-07-03', '%Y-%m-%d').date(),
            'data_validade': datetime.strptime('2024-07-08', '%Y-%m-%d').date(),
            'ingredientes': 'Farinha, manteiga, açúcar, fermento',
            'informacoes_nutricionais': '300 calorias por 100g'
        }
    ]

    for item_data in itens:
        item = Item(**item_data)
        db.session.add(item)

    db.session.commit()
    print("Banco de dados populado com os itens.")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        populate_items()
