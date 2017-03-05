import db
database = db.db

class Attribute(database.Model):

    __tablename__ = 'attributes'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80))

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': unicode(self.name, 'utf-8')
        }