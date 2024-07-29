from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///padaria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date)
    endereco = db.Column(db.String(200))
    pedidos = db.relationship('Pedido', backref='cliente', lazy=True)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data_pedido = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    data_entrega = db.Column(db.Date)
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    embalagem = db.Column(db.String(50))
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    data_fabricacao = db.Column(db.Date)
    data_validade = db.Column(db.Date)
    ingredientes = db.Column(db.Text)
    informacoes_nutricionais = db.Column(db.Text)
    pedidos = db.relationship('ItemPedido', backref='item', lazy=True)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Função para criar as tabelas
def create_tables():
    with app.app_context():
        db.create_all()

# Chama a função para criar as tabelas
create_tables()

# Rotas para Clientes
@app.route('/clientes', methods=['POST'])
def add_cliente():
    data = request.json
    cliente = Cliente(**data)
    db.session.add(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente adicionado'}), 201

@app.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.as_dict() for cliente in clientes])

@app.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.as_dict())

@app.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.json
    cliente = Cliente.query.get_or_404(id)
    for key, value in data.items():
        setattr(cliente, key, value)
    db.session.commit()
    return jsonify({'message': 'Cliente atualizado'})

@app.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente removido'})

# Rotas para Pedidos
@app.route('/pedidos', methods=['POST'])
def add_pedido():
    data = request.json
    cliente_id = data.get('cliente_id')
    data_pedido = data.get('data_pedido')
    valor = data.get('valor')
    data_entrega = data.get('data_entrega')
    itens = data.get('itens')

    if not cliente_id or not data_pedido or not valor or not itens:
        return jsonify({'message': 'Dados insuficientes para criar pedido'}), 400

    # Criar o pedido
    pedido = Pedido(
        cliente_id=cliente_id,
        data_pedido=datetime.strptime(data_pedido, '%Y-%m-%d'),
        valor=valor,
        data_entrega=datetime.strptime(data_entrega, '%Y-%m-%d') if data_entrega else None
    )
    db.session.add(pedido)
    db.session.commit()

    # Adicionar itens ao pedido
    for item_data in itens:
        item_id = item_data.get('item_id')
        quantidade = item_data.get('quantidade')
        if not item_id or not quantidade:
            return jsonify({'message': 'Dados insuficientes para adicionar item ao pedido'}), 400

        item_pedido = ItemPedido(
            pedido_id=pedido.id,
            item_id=item_id,
            quantidade=quantidade
        )
        db.session.add(item_pedido)

    db.session.commit()

    return jsonify({'message': 'Pedido adicionado', 'pedido_id': pedido.id}), 201


@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([pedido.as_dict() for pedido in pedidos])

@app.route('/pedidos/<int:id>', methods=['GET'])
def get_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    return jsonify(pedido.as_dict())

@app.route('/pedidos/<int:id>', methods=['PUT'])
def update_pedido(id):
    data = request.json
    pedido = Pedido.query.get_or_404(id)
    for key, value in data.items():
        setattr(pedido, key, value)
    db.session.commit()
    return jsonify({'message': 'Pedido atualizado'})

@app.route('/pedidos/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()
    return jsonify({'message': 'Pedido removido'})

# Rotas para Itens
@app.route('/itens', methods=['POST'])
def add_item():
    data = request.json
    item = Item(**data)
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Item adicionado'}), 201

@app.route('/itens', methods=['GET'])
def get_itens():
    itens = Item.query.all()
    return jsonify([item.as_dict() for item in itens])

@app.route('/itens/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.as_dict())

@app.route('/itens/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.json
    item = Item.query.get_or_404(id)
    for key, value in data.items():
        setattr(item, key, value)
    db.session.commit()
    return jsonify({'message': 'Item atualizado'})

@app.route('/itens/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item removido'})

if __name__ == '__main__':
    app.run(debug=True)
