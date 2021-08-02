from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

from datetime import datetime
import stripe
import os

from forms import TaskForm, RegisterForm, LoginForm

DOMAIN = os.environ.get('DOMAIN')
stripe.api_key = os.environ.get('SECRET_API_KEY')

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL?sslmode=require", "sqlite:///shop.db")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(250), nullable=False)
    number_of_img = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=True)
    category = db.Column(db.String(250), nullable=True)
    price_id = db.Column(db.String(250), nullable=True)

    # Relationship with CartItem
    cart_items = relationship("CartItem", back_populates='product')


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    # Relationship with Product
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = relationship('Product', back_populates='cart_items')

    # Relationship to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship('User', back_populates='cart_items')

    # Order ID
    order_id = db.Column(db.Integer, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    # Relationship with CartItem
    cart_items = relationship("CartItem", back_populates='user')

    # Relationship with Order
    orders = relationship("Order", back_populates='user')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    total_price = db.Column(db.String(100), nullable=False)
    order_id = db.Column(db.Integer, nullable=False)

    # Relationship to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')

# LOGIN
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

@app.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('index.html', items=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if email has already been used
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("You've already signed up with this email. Please log in.")
            return redirect(url_for('login'))
        else:
            hash_and_salted_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
            new_user = User(
                email=form.email.data,
                password=hash_and_salted_password,
                name=form.name.data
            )
        db.session.add(new_user)
        db.session.commit()
        # Login User
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        # Email is not exist
        if not user:
            flash("This email hasn't been registered.")
            return redirect(url_for('login'))
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
            # Password Incorrect
            else:
                flash("Incorrect password. Please try again.")
                return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def detail(item_id):
    if request.method == 'POST':
        # Check if user is login
        if current_user.is_active:
            # Check if the item is in the cart
            cart_item = db.session.query(CartItem).filter_by(user=current_user, product_id=item_id, order_id=0).first()
            if cart_item:
                new_quantity = str(int(cart_item.quantity) + int(request.form['quantity']))
                # Maximum Quantity = 10
                if int(new_quantity) > 10:
                    cart_item.quantity = str(10)
                else:
                    cart_item.quantity = new_quantity
                db.session.commit()
            else:
                new_cart_item = CartItem(
                    product=db.session.query(Product).get(item_id),
                    quantity=request.form['quantity'],
                    user=current_user,
                    order_id=0
                )
                db.session.add(new_cart_item)
                db.session.commit()
            return redirect(url_for('cart'))
        else:
            flash("Please login before you shop.")
            return redirect(url_for('login'))
    return render_template('detail.html', item=db.session.query(Product).get(item_id))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        new_quantity = request.form['quantity']
        cart_item_id = request.form['cart_item_id']
        cart_item = db.session.query(CartItem).get(cart_item_id)
        cart_item.quantity = new_quantity
        if int(new_quantity) == 0:
            cart_item_to_delete = CartItem.query.get(cart_item_id)
            db.session.delete(cart_item_to_delete)
        db.session.commit()
        return redirect(url_for('cart'))
    cart_items = db.session.query(CartItem).filter_by(user=current_user, order_id=0).all()
    total_price = 0
    for item in cart_items:
        total_price += item.product.price * int(item.quantity)
    return render_template('cart.html', cart_items=cart_items, total_price=str(total_price))


# CHECK OUT
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    cart_items = db.session.query(CartItem).filter_by(user=current_user, order_id=0).all()
    line_items = [
        {'price': item.product.price_id,
         'quantity': int(item.quantity)} for item in cart_items
    ]
    # Check if there's item in the cart
    if not line_items:
        return redirect(url_for('cancel'))
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=[
              'card',
            ],
            line_items=line_items,
            mode='payment',
            success_url=DOMAIN + '/success',
            cancel_url=DOMAIN + '/cancel',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@app.route('/success')
def success():
    # GET THE LATEST ORDER NUMBER
    all_order_items = db.session.query(CartItem).filter_by(user=current_user).all()
    all_order_id = []
    for item in all_order_items:
        if item.order_id not in all_order_id:
            all_order_id.append(int(item.order_id))
    new_order_id = max(all_order_id) + 1
    # CHANGE ORDER ID OF ALL CART ITEM TO NEW ORDER ID
    cart_items = db.session.query(CartItem).filter_by(user=current_user, order_id=0).all()
    total_price = 0
    for item in cart_items:
        item.order_id = new_order_id
        total_price += item.product.price * int(item.quantity)
    db.session.commit()
    # CREATE ORDER
    today = datetime.now().strftime("%Y/%m/%d")
    new_order = Order(
        date=today,
        total_price=str(total_price),
        order_id=new_order_id,
        user=current_user,
    )
    db.session.add(new_order)
    db.session.commit()
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

@app.route('/order')
def order():
    # GET THE LATEST ORDER NUMBER
    all_order_items = db.session.query(CartItem).filter_by(user=current_user).all()
    all_order_id = []
    for item in all_order_items:
        if item.order_id not in all_order_id:
            all_order_id.append(int(item.order_id))
    max_order_id = max(all_order_id)
    orders = []
    for order_id in range(1, max_order_id + 1):
        new_order = {
            "order_items": db.session.query(CartItem).filter_by(user=current_user, order_id=order_id).all(),
            "order_db": db.session.query(Order).filter_by(user=current_user, order_id=order_id).first()
        }
        orders.append(new_order)
    return render_template('order.html', orders=orders)


if __name__ == '__main__':
    app.run(debug=True)

