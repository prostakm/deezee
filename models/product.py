import db
from models.category import Category
from models.attribute import Attribute
from models.color import Color

database = db.db

product_categories = database.Table('product_categories',
    database.Column('product_id', database.Integer, database.ForeignKey('products.id')),
    database.Column('category_id', database.Integer, database.ForeignKey('categories.id'))
)

class ProductStockSize(database.Model):

    __tablename__ = 'product_stock_size'

    id = database.Column(database.Integer, primary_key=True)
    product_id = database.Column(database.Integer, database.ForeignKey('products.id'))
    size = database.Column(database.String(4))
    stock = database.Column(database.Integer)

    def json(self):
        return {
            'size': self.size,
            'stock': self.stock
        }

class ProductImage(database.Model):

    __tablename__ = 'product_images'

    id = database.Column(database.Integer, primary_key=True)
    product_id = database.Column(database.Integer, database.ForeignKey('products.id'))
    image_url = database.Column(database.String(512))

    def json(self):
        return {
            "url" : self.image_url
        }

class ProductAttributes(database.Model):

    __tablename__ = 'product_attributes'

    product_id = database.Column(database.Integer, database.ForeignKey('products.id'), primary_key=True)
    product = database.relationship('Product', back_populates='attributes')
    attribute_id = database.Column(database.Integer, database.ForeignKey('attributes.id'), primary_key=True)
    attribute = database.relationship('Attribute')
    value = database.Column(database.String(128))

    def json(self):
        return {
            'attribute_id': self.attribute_id,
            'name': self.attribute.name,
            'value': self.value
        }

class Product(database.Model):

    __tablename__ = 'products'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255))
    current_price = database.Column(database.Float)
    standard_price = database.Column(database.Float)
    discount_type = database.Column(database.String(10))
    attributes_hash = database.Column(database.Integer)
    description = database.Column(database.String(256))
    average_rating = database.Column(database.Float)
    rating_count = database.Column(database.Integer)
    is_favourite = database.Column(database.Boolean)

    categories = database.relationship('Category', secondary=product_categories)
    attributes = database.relationship('ProductAttributes')
    images = database.relationship('ProductImage')
    stockSize = database.relationship('ProductStockSize')
    color_id = database.Column(database.Integer, database.ForeignKey('colors.id'))
    color = database.relationship('Color')

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def similar_products(self):
        return Product.query.filter_by(attributes_hash=self.attributes_hash).all()

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'current_price': self.current_price,
            'standard_price': self.standard_price,
            'discount_type': self.discount_type,
            'color': self.color.json(),
            'description': 'empty description',
            'average_rating': self.average_rating,
            'rating_count': self.rating_count,
            'is_favourite': self.is_favourite,

            'categories': [ category.json() for category in self.categories ],
            'attributes': [ productAttribute.json() for productAttribute in self.attributes ],
            'images': [ image.json() for image in self.images ],
            'sizes': [ stockSize.json() for stockSize in self.stockSize],
            'similar_products': [ {'id': similar.id, 'color': similar.color.json() } for similar in self.similar_products()]
        }