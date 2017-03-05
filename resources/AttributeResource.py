from flask_restful import Resource

class AttributesResource(Resource):

    def get(self):
        from models.attribute import Attribute
        attributes = Attribute.query.all()
        return [ attribute.json for attribute in attributes ], 200