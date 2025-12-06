from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models import db, Product, User, Order
import os

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_pyfile('config.py')

    db.init_app(app)

    # ensure instance folder exists
    os.makedirs('instance', exist_ok=True)

    @app.route('/')
    def index():
        # 3 öneri, ana sayfa slider'ı için
        products = Product.query.limit(3).all()
        return render_template('index.html', products=products)

    @app.route('/menu')
    def menu():
        products = Product.query.all()
        return render_template('menu.html', products=products)

    @app.route('/about')
    def about():
        # about content can be stored in DB in advanced version; kept static for simplicity
        return render_template('about.html')

    # ---------- Order route (public) ----------
    @app.route('/order/<int:product_id>', methods=['GET','POST'])
    def order_product(product_id):
        product = Product.query.get_or_404(product_id)
        if request.method == 'POST':
            customer_name = request.form.get('customer_name')
            customer_phone = request.form.get('customer_phone')
            order = Order(product_id=product.id, customer_name=customer_name, customer_phone=customer_phone)
            db.session.add(order)
            db.session.commit()
            flash('Siparişiniz alındı.', 'success')
            return redirect(url_for('menu'))
        return render_template('order.html', product=product)

    # ---------- ADMIN ----------
    @app.route('/admin/login', methods=['GET','POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['admin'] = True
                flash('Giriş başarılı', 'success')
                return redirect(url_for('admin_dashboard'))
            flash('Kullanıcı adı veya şifre yanlış', 'danger')
        return render_template('admin/login.html')

    @app.route('/admin/logout')
    def admin_logout():
        session.pop('admin', None)
        flash('Çıkış yapıldı', 'info')
        return redirect(url_for('admin_login'))

    @app.route('/admin/dashboard')
    def admin_dashboard():
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        # basit dashboard: ürün sayısı ve sipariş sayısı
        total_products = Product.query.count()
        total_orders = Order.query.count()
        return render_template('admin/dashboard.html', total_products=total_products, total_orders=total_orders)

    # Admin - products list
    @app.route('/admin/products')
    def admin_products():
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        products = Product.query.all()
        return render_template('admin/products.html', products=products)

    # Admin - add product
    @app.route('/admin/products/add', methods=['GET','POST'])
    def admin_add_product():
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        if request.method == 'POST':
            p = Product(
                name=request.form.get('name'),
                description=request.form.get('description'),
                price=float(request.form.get('price') or 0),
                image_url=request.form.get('image_url') or '/static/img/default-coffee.jpg'
            )
            db.session.add(p)
            db.session.commit()
            flash('Ürün eklendi', 'success')
            return redirect(url_for('admin_products'))
        return render_template('admin/add_product.html')

    # Admin - edit
    @app.route('/admin/products/edit/<int:id>', methods=['GET','POST'])
    def admin_edit_product(id):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        p = Product.query.get_or_404(id)
        if request.method == 'POST':
            p.name = request.form.get('name')
            p.description = request.form.get('description')
            p.price = float(request.form.get('price') or 0)
            p.image_url = request.form.get('image_url') or p.image_url
            db.session.commit()
            flash('Ürün güncellendi', 'success')
            return redirect(url_for('admin_products'))
        return render_template('admin/edit_product.html', product=p)

    # Admin - delete
    @app.route('/admin/products/delete/<int:id>', methods=['POST'])
    def admin_delete_product(id):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        p = Product.query.get_or_404(id)
        db.session.delete(p)
        db.session.commit()
        flash('Ürün silindi', 'success')
        return redirect(url_for('admin_products'))

    # Admin - orders
    @app.route('/admin/orders')
    def admin_orders():
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        orders = Order.query.all()
        return render_template('admin/orders.html', orders=orders)

    @app.route('/admin/orders/delete/<int:id>', methods=['POST'])
    def admin_delete_order(id):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        o = Order.query.get_or_404(id)
        db.session.delete(o)
        db.session.commit()
        flash('Sipariş silindi', 'success')
        return redirect(url_for('admin_orders'))

    return app

# run
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
