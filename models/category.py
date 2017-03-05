import db

database = db.db

class Category(database.Model):

    __tablename__ = 'categories'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80))
    parent_id = database.Column(database.Integer, database.ForeignKey('categories.id'))
    parent = database.relationship('Category')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'name': self.name.encode("utf8"),
            'parent_id': self.parent_id
        }
