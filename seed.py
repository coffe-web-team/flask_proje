from app import app
from models import db, Product

with app.app_context():
    db.session.add_all([
        Product(name="Latte", price=70, image="latte.jpg", description="Yumuşak içimli sütlü kahve"),
        Product(name="Mocha", price=75, image="mocha.jpg", description="Çikolatalı espresso"),
        Product(name="Americano", price=60, image="americano.jpg", description="Yoğun filtre kahve"),
        Product(name="Espresso", price=55, image="espresso.jpg", description="Saf espresso shot"),
        Product(name="Cappuccino", price=72, image="cappuccino.jpg", description="Köpüklü sütlü kahve")
    ])
    db.session.commit()
    print("Ürünler eklendi")










