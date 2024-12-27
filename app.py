from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'minha chave 123'  # Necessário para Flask-Login

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Inicializa o LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Define a rota de login

# Habilita o CORS para o aplicativo
CORS(app)

# Modelo de usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    # Método para verificar a senha
    def check_password(self, password):
        return self.password == password

# Modelo de produto
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

# Função auxiliar para obter um produto pelo ID
def get_product_or_404(product_id):
    return Product.query.get(product_id)

# Modelo de item de carrinho
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

# Rota para login
@app.route('/login', methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    if user and user.check_password(data.get("password")):
        login_user(user)  # Loga o usuário
        return jsonify({"message": "Logged in successfully"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Função para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rota para logout
@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

# Rota para adicionar um produto
@app.route('/api/products/add', methods=['POST'])
@login_required
def add_product():
    try:
        data = request.get_json()
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para deletar um produto
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    product = get_product_or_404(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully!"}), 200
    return jsonify({"message": "Product not found!"}), 404

# Rota para obter os detalhes de um produto
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = get_product_or_404(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }), 200
    return jsonify({"message": "Product not found!"}), 404

# Rota para atualizar um produto
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = get_product_or_404(product_id)
    if product:
        data = request.get_json()
        for key, value in data.items():
            setattr(product, key, value)
        db.session.commit()
        return jsonify({"message": "Product updated successfully!"}), 200
    return jsonify({"message": "Product not found!"}), 404

# Rota para obter todos os produtos
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    if not products:
        return jsonify({"message": "No products found!"}), 404
    return jsonify([{"id": p.id, "name": p.name, "price": p.price, "description": p.description} for p in products]), 200

# Rota para adicionar um produto ao carrinho
@app.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    user = User.query.get(int(current_user.id))  # Corrigido o erro de digitação: Usuer -> User
    product = Product.query.get(product_id)

    if user and product:
        # Verificar se o produto já está no carrinho do usuário
        existing_item = CartItem.query.filter_by(user_id=user.id, product_id=product.id).first()
        if existing_item:
            return jsonify({"message": "Product already in cart"}), 400
        
        # Adicionar o produto ao carrinho
        cart_item = CartItem(user_id=user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item added to the cart successfully'}), 200
    
    return jsonify({'message': 'Failed to add item to the cart'}), 400

# Rota para remover um produto do carrinho
@app.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    # Obter o item de carrinho do usuário
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item removed from the cart successfully'}), 200
    
    return jsonify({'message': 'Failed to remove item from the cart'}), 400

# Rota para visualizar o carrinho de compras
@app.route('/api/cart', methods=['GET'])
@login_required
def view_cart():
    user = User.query.get(int(current_user.id))
    cart_items = user.cart_items  # Corrigido para acessar o relacionamento correto

    cart_content = []
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)  # Buscar os detalhes do produto
        cart_content.append({
            "id": cart_item.id,
            "user_id": cart_item.user_id,
            "product_id": cart_item.product_id,
            "product_name": product.name,
            "product_price": product.price
        })   

    return jsonify(cart_content)

# Rota para checkout
@app.route('/api/cart/checkout', methods=["POST"])
@login_required
def checkout():
    user = User.query.get(int(current_user.id))
    cart_items = user.cart_items  # Corrigido para acessar o relacionamento correto

    # Limpar o carrinho
    for cart_item in cart_items:
        db.session.delete(cart_item)
    
    db.session.commit()
    
    return jsonify({'message': 'Checkout successful, cart has been cleared!'}), 200


 
# Rodando o aplicativo Flask
if __name__ == "__main__":
    with app.app_context():  # Garantir que o contexto do app esteja ativo antes de acessar o banco
        db.create_all()  # Cria as tabelas se elas não existirem
    app.run(debug=True)
