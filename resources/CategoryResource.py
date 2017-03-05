from flask_restful import Resource

class CategoriesResource(Resource):

    def get(self):
        from models.category import Category
        categories = Category.query.all()
        return {'categories': [category.json() for category in categories]}, 200