from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(50), nullable=False)

first_request = True

@app.before_request
def create_tables():
    global first_request
    if first_request:
        db.create_all()
        # Добавляем данные в базу данных, если они еще не существуют
        if Product.query.count() == 0:
            products = [
                Product(name="Toaster", company="BORK"),
                Product(name="Blender", company="BORK"),
                Product(name="Coffee Maker", company="BORK"),
                Product(name="Vacuum Cleaner", company="BORK"),
                Product(name="Blender", company="PHILIPS"),
                Product(name="Electric Toothbrush", company="PHILIPS"),
                Product(name="Vacuum Cleaner", company="PHILIPS"),
                Product(name="Hair Dryer", company="PHILIPS")
            ]
            db.session.bulk_save_objects(products)
            db.session.commit()
        first_request = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_common_products', methods=['POST'])
def get_common_products():
    bork_products = {product.name for product in Product.query.filter_by(company='BORK').all()}
    philips_products = {product.name for product in Product.query.filter_by(company='PHILIPS').all()}

    common_products = list(bork_products & philips_products)

    return render_template('index.html', common_products=common_products)

if __name__ == '__main__':
    app.run(debug=True)