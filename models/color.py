import db
database = db.db

class Color(database.Model):

    __tablename__ = 'colors'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80))
    hex = database.Column(database.String(6))

    def __init__(self, name, hex):
        self.name = name
        self.hex = hex

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'hex': self.hex
        }