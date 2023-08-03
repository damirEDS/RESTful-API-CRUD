import sqlite3
from flask import Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

app = Flask(__name__)

DATABASE = 'books.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                publisher TEXT NOT NULL,
                author TEXT NOT NULL,
                pages INTEGER NOT NULL,
                tags TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        db.commit()


@app.teardown_appcontext
def close_db(exception):
    db_connection = getattr(g, '_database', None)
    if db_connection is not None:
        db_connection.close()


app.config["SECRET_KEY"] = "KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)

jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

api = Api(app)


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if not username or not password:
            return {'message': 'Missing username or password'}, 400
        if User.query.filter_by(username=username).first():
            return {'message': 'Username not available'}, 400

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 200


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401


api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')


def get_book_by_title(title):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM books WHERE title LIKE ?', ('%' + title + '%',))
    book = cursor.fetchone()
    return dict(book) if book else None


# Show all books or filter by title
@app.route('/books', methods=['GET'])
def get_books():
    title_filter = request.args.get('title')

    if title_filter:
        book = get_book_by_title(title_filter)
        if book:
            return jsonify(book)
        else:
            return jsonify({"message": "Book not found"}), 404
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        return jsonify([dict(book) for book in books])


@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    try:
        new_book_data = request.get_json()
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO books (title, publisher, author, pages, tags, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            new_book_data['title'],
            new_book_data['publisher'],
            new_book_data['author'],
            new_book_data['pages'],
            ','.join(new_book_data['tags']),
            new_book_data['created_at'],
            new_book_data['updated_at'],
        ))
        db.commit()
        new_book_id = cursor.lastrowid
        cursor.execute('SELECT * FROM books WHERE id = ?', (new_book_id,))
        new_book = cursor.fetchone()
        return jsonify(dict(new_book)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    try:
        data = request.get_json()
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            UPDATE books
            SET title = ?, publisher = ?, author = ?, pages = ?, tags = ?, updated_at = ?
            WHERE id = ?
        ''', (
            data['title'],
            data['publisher'],
            data['author'],
            data['pages'],
            ','.join(data['tags']),
            data['updated_at'],
            book_id
        ))
        db.commit()
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        updated_book = cursor.fetchone()
        if updated_book:
            return jsonify(dict(updated_book))
        else:
            return jsonify({"message": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/books/<string:book_title>', methods=['DELETE'])
@jwt_required()
def delete_book(book_title):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM books WHERE title = ?', (book_title,))
        db.commit()
        return jsonify({"message": "Book successfully deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
