from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

app = Flask(__name__)

# database creation part
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///items.db'
db = SQLAlchemy()
db.init_app(app)


class product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    img = db.Column(db.String(500), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    disc = db.Column(db.String(100), nullable=False)


class cart(db.Model):
    __tablename__ = "Cart section"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    img = db.Column(db.String(500), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    disc = db.Column(db.String(100), nullable=False)


class user(db.Model):
    __tablename__ = "user_authentication"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=True, nullable=False)


class image(db.Model):
    __tablename__ = "Ad image"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(500), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    query = db.session.execute(select([product])).scalars().all()
    img = db.session.execute(select([image])).scalars().all()

    return render_template("index.html", query=query, imgs=img)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        query = product(
            name=request.form['productName'],
            img=request.form['productImage'],
            desc=request.form['productDescription'],
            price=request.form['productPrice'],
            disc=request.form['productDiscount']
        )
        db.session.add(query)
        db.session.commit()
        return redirect('/')

    return render_template("add.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        query = user(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password']
        )
        db.session.add(query)
        db.session.commit()
        return redirect('/')
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)