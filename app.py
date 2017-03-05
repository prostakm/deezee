from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
import os
import resources.ProductResource
import resources.CategoryResource
# import resources.UserResource
#from security import identity, authenticate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "EQK16Q3m37YZ00v6ij3K1pFhA16vT8Sp"
api = Api(app)
app.config['JSON_AS_ASCII'] = False

#jwt = JWT(app, authenticate, identity)

api.add_resource(resources.ProductResource.ProductRes, '/product/<int:_id>')
api.add_resource(resources.ProductResource.ProductList, '/products')
api.add_resource(resources.CategoryResource.CategoriesResource, '/categories')
# api.add_resource(resources.UserResource.UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    app.run(debug=True)