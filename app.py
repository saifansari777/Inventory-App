from flask import Flask, render_template, request, redirect, url_for,session, g, flash
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'devlopment'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    
    _tablename = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Product(db.Model):

    _tablename = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.name

@app.route("/hello")
def hello():
    return render_template("base.html")

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        print(request.form)
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        error = None

        if not username:
            error = "username cannot be none"
        elif not password:
            error = "password cannot be empty"
        elif User.query.filter_by(username=username).first() != None:
            error = "username already exist"
        
        if error is None:

            user = User(username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login'))

        flash(error)
        print(error)
    
    g.products = Product.query.all()

    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":

        print(request.form)
        username = request.form.get("username")
        password = request.form.get("password")

        error = None
        try:
            user = User.query.filter_by(username=username).first()
            print(user)
            if user.password != password:
                error = "Wrong Password!"
            else:
                session["username"] = username
                return redirect(url_for('product_list'))
        except Exception as e:
            error = f"Username not Found! {e}"

        flash(error)
    return render_template('login.html')



@app.before_request
def load_logged_in_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = User.query.filter_by(username=username).first()

@app.route('/logout')
def logout():
    

    session.clear()

    return redirect(url_for('index'))



@app.route("/product", methods=["GET", "POST"])
def product_list():

    if request.method == "POST":

        print(request.form)
        name = request.form.get("name")
        quantity = request.form.get("quantity")
        price = request.form.get("price")

        error = None

        if not name:
            error = "Product name Is required!"
        elif not quantity:
            error = "Product Quantity is Required"
        elif not price:
            error = "Product Price Is Required!"
        elif Product.query.filter_by(name=name).first() != None:
            error = "Product name already exist"
        
        if error is None:

            product = Product(name=name, price=price, quantity=quantity)
            print(product)
            db.session.add(product)
            db.session.commit()
            flash('product added successfully!')


        flash(error)
        print(error)

    products = Product.query.all()

    return render_template("product-list.html", products=products)





if '__main__' == __name__ :

    app.run()