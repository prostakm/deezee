import db
database = db.db

class User(database.Model):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80))
    password = database.Column(database.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()