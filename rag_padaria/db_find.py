from app import db, Item
from datetime import datetime

def get_itens():
    itens = Item.query.all()
    return [item.as_dict() for item in itens]

if __name__ == '__main__':
    from app import app
    with app.app_context():
        itens = get_itens()
        for item in itens:
            print(item)
