from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Product, User, Order
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# ---------- ADMIN KULLANICI OLUŞTURMA ----------
def create_admin_user():
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            phone="1234567890",
            password="admin123",
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin kullanıcı oluşturuldu: admin / admin123")

# ---------- DB INIT ----------
with app.app_context():
    db.create_all()
    create_admin_user()

# ---------- GENEL SAYFALAR ----------
@app.route("/")
def index():
    products = Product.query.limit(3).all()
    return render_template("index.html", products=products)

@app.route("/menu")
def menu():
    products = Product.query.all()
    return render_template("menu.html", products=products)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---------- AUTH ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.password == request.form["password"]:
            session["user"] = user.username
            session["admin"] = user.is_admin
            flash("Giriş başarılı!", "success")
            return redirect(url_for("admin_dashboard" if user.is_admin else "index"))
        flash("Geçersiz kullanıcı adı veya şifre.", "danger")
    return render_template("auth/login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            phone=request.form["phone"],
            password=request.form["password"],
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()
        flash("Kayıt başarılı! Giriş yapabilirsiniz.", "success")
        return redirect(url_for("login"))
    return render_template("auth/register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for("index"))

# ---------- SİPARİŞ ----------
@app.route("/order/<int:product_id>", methods=["GET", "POST"])
def order(product_id):
    if "user" not in session:
        flash("Sipariş vermek için giriş yapmalısınız.", "warning")
        return redirect(url_for("login"))

    product = Product.query.get(product_id)

    if request.method == "POST":
        new_order = Order(
            customer_name=session["user"],
            product_name=product.name,
            status="Beklemede"
        )
        db.session.add(new_order)
        db.session.commit()
        flash("Siparişiniz alındı!", "success")
        return redirect(url_for("menu"))

    return render_template("order.html", product=product)

# ---------- ADMIN ----------
@app.route("/admin")
def admin_dashboard():
    if not session.get("admin"):
        flash("Bu sayfaya erişim yetkiniz yok.", "danger")
        return redirect(url_for("login"))

    orders = Order.query.all()
    products = Product.query.all()
    return render_template("admin/dashboard.html", orders=orders, products=products)

@app.route("/admin/order/<int:id>/accept", methods=["POST"])
def accept_order(id):
    if not session.get("admin"):
        flash("Yetkiniz yok.", "danger")
        return redirect(url_for("login"))

    order = Order.query.get(id)
    order.status = "Onaylandı"
    db.session.commit()
    flash("Sipariş onaylandı.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/product/add", methods=["POST"])
def add_product():
    if not session.get("admin"):
        flash("Yetkiniz yok.", "danger")
        return redirect(url_for("login"))

    product = Product(
        name=request.form["name"],
        price=request.form["price"],
        image=request.form["image"],
        description=request.form["description"]
    )
    db.session.add(product)
    db.session.commit()
    flash("Ürün eklendi.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/product/delete/<int:id>", methods=["POST"])
def delete_product(id):
    if not session.get("admin"):
        flash("Yetkiniz yok.", "danger")
        return redirect(url_for("login"))

    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    flash("Ürün silindi.", "success")
    return redirect(url_for("admin_dashboard"))












