from app import create_app
from models import db, Product, User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # sadece seedlenmemişse ekle
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password=generate_password_hash('admin123'))
        db.session.add(admin)

    if Product.query.count() == 0:
        products = [
            Product(name='Caffe Latte', description='Yumuşak sütlü latte', price=55, image_url='/static/img/latte.jpg'),
            Product(name='Espresso', description='Klasik sert espresso', price=40, image_url='/static/img/espresso.jpg'),
            Product(name='Cappuccino', description='Köpüklü cappuccino', price=60, image_url='/static/img/cappuccino.jpg'),
            Product(name='Mocha', description='Çikolatalı kahve', price=65, image_url='/static/img/mocha.jpg'),
        ]
        db.session.add_all(products)

    db.session.commit()
    print("Seed tamamlandı.")
