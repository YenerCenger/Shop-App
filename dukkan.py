from flask import Flask,render_template,flash,redirect,url_for,session,logging,request,g
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/Yener/Desktop/dukkan/dukkan.db"
app.secret_key= "Dukkan"
db = SQLAlchemy(app)

# Kullanıcı Giriş Decorator'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın.","danger")
            return redirect(url_for("login"))
    return decorated_function

# Ürün Class'ı

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    isim = db.Column(db.String, nullable=False)
    alis_fiyat = db.Column(db.Integer, nullable=False)
    satis_fiyat = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    ekleyen = db.Column(db.String, nullable=False)

# Kullanıcı Class'ı

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

# Ürünler
@app.route("/products")
@login_required
def products():
    products = Product.query.all()
    return render_template("products.html",products = products)

# Konrol Paneli
@app.route("/dashboard")
@login_required
def dashboard():
    current_user_username = session["username"]
    user_products = Product.query.filter_by(ekleyen=current_user_username).all()
    return render_template("dashboard.html", products=user_products)

# Hesap
@app.route("/account")
@login_required
def account():
    return render_template("account.html")

# Kullanıcı Çıkış
@app.route("/logout")
@login_required
def logout():
    session["logged_in"] = False
    return redirect(url_for("index"))

#Kullanıcı Giriş
@app.route("/login", methods = ["GET","POST"])
def login():
    if (request.method == "POST"):
        check_username = request.form.get("username")
        check_password = request.form.get("password")

        user = User.query.filter_by(username = check_username).first()
        real_password = user.password

        if check_password_hash(real_password, check_password):
            flash("Başarıyla giriş yaptınız.", "success")
            session["logged_in"] = True
            session["username"] = check_username
            return redirect(url_for("index"))
        else:
            flash("Geçersiz kullanıcı adı veya parola.", "danger")
            return render_template("login.html")
    else:
        return render_template("login.html")

# Kullanıcı Kayıt
@app.route("/register", methods = ["GET","POST"])
def register():
    name = request.form.get("name")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm = request.form.get("confirm")

    if (request.method == "POST"):

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash("Bu kullanıcı adı zaten kullanımda.", "danger")
            return redirect(url_for("register"))
        existing_email = User.query.filter_by(email=email).first()
        
        if existing_email:
            flash("Bu e-posta adresi zaten kullanımda.", "danger")
            return redirect(url_for("register"))
        
        if (password != confirm):
            flash("Girdiğiniz parolalar birbiri ile uyuşmuyor...","warning")
            return redirect(url_for("register"))
        
        else:
            hashed_password = generate_password_hash(password)
            newUser = User(name=name,username=username,email=email,password=hashed_password)
            db.session.add(newUser)
            db.session.commit()
            flash("Başarıyla Kayıt Oldunuz.","success")
            return redirect(url_for("login"))
    else:
        return render_template("register.html")

# Ürün Ekle
@app.route("/addproduct",methods = ["GET","POST"])
@login_required
def addproduct():
    isim = request.form.get("isim")
    alis_fiyat = request.form.get("alis_fiyat")
    satis_fiyat = request.form.get("satis_fiyat")
    ekleyen = session["username"]

    if (request.method == "POST"):
        newProduct = Product(isim=isim,alis_fiyat=alis_fiyat,satis_fiyat=satis_fiyat,ekleyen=ekleyen)
        db.session.add(newProduct)
        db.session.commit()
        flash("Ürün başarıyla eklendi.","success")
        return redirect(url_for("addproduct"))
    else:
        return render_template("addproduct.html")
    
# Ürün Güncelleme
@app.route("/edit/<string:id>",methods = ["GET","POST"])
@login_required
def edit(id):
    product = Product.query.get(id)
    if (request.method == "POST"):
        yeni_isim = request.form.get("isim")
        yeni_alis_fiyat = request.form.get("alis_fiyat")
        yeni_satis_fiyat = request.form.get("satis_fiyat")

        product.isim =  yeni_isim
        product.alis_fiyat = yeni_alis_fiyat
        product.satis_fiyat = yeni_satis_fiyat

        db.session.commit()
        flash("Ürün başarıyla güncellendi.", "success")
        return redirect(url_for("products"))
    else:
        return render_template("edit.html",product=product)

# Ürün Sil
@app.route("/delete/<int:id>")
@login_required
def delete(id):
    product = Product.query.get(id)

    if product:
        db.session.delete(product)
        db.session.commit()
        flash("Ürün başarıyla silindi.", "success")
    else:
        flash("Ürün bulunamadı.", "danger")

    return redirect(url_for("products"))

# Products Arama URL
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")

        products = Product.query.filter(Product.isim.ilike(f'%{keyword}%')).all()

        if not products:
            flash('Aranan kelimeye uygun ürün bulunamadı...', 'warning')
            return redirect(url_for('products'))
        else:
            return render_template('products.html', products=products)

# Dashboard Arama URL
@app.route("/search_dashboard", methods=["GET", "POST"])
@login_required
def search_dashboard():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")

        products = Product.query.filter(Product.isim.ilike(f'%{keyword}%')).all()

        if not products:
            flash('Aranan kelimeye uygun ürün bulunamadı...', 'warning')
            return redirect(url_for('dashboard'))
        else:
            return render_template('dashboard.html', products=products)


# Ürün Ekranı
@app.route("/product/<string:id>")
@login_required
def product(id):
    product = Product.query.filter_by(id=id).first()
    return render_template("product.html",product=product)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)