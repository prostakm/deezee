from flask_restful import Resource, reqparse
from models.userModel import User

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='Username must be provideed'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='Password must be set'
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {tablename} VALUES (NULL, ?, ?)".format(tablename=self.TABLE_NAME)
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "user created"}, 200