from flask_restful import Resource

class ProductRes(Resource):
    def get(self, _id):
        import models.product
        product = models.product.Product.find_by_id(_id)
        if product:
            return product.json()
        return {"message": "Product not found"}, 404


class ProductList(Resource):
    def get(self):
        import models.product
        products = models.product.Product.query.all()
        return { 'products' : [ product.json() for product in products ] }, 200