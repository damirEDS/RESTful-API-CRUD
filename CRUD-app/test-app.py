import json
import pytest
from app import app, init_db


# Update your_app_name to the actual name of your application file

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test_database.db'
    with app.app_context():
        init_db()  # Initialize the test database
    with app.test_client() as client:
        yield client


def test_register_user(client):
    # Test user registration
    data = {"username": "test_user", "password": "test_password"}
    response = client.post('/register', data=json.dumps(data), content_type='application/json')

    # Modify the assertion to check for a successful registration (status code 201)
    assert response.status_code == 200
    assert b'User created successfully' in response.data


def test_login_user(client):
    # Test user login
    data = {"username": "test_user", "password": "test_password"}
    client.post('/register', data=json.dumps(data), content_type='application/json')
    response = client.post('/login', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b'access_token' in response.data


def test_add_book(client):
    # Test adding a new book
    data = {
        "title": "Test Book",
        "publisher": "Test Publisher",
        "author": "Test Author",
        "pages": 200,
        "tags": ["test", "book"],
        "created_at": "2023-08-03",
        "updated_at": "2023-08-03"
    }
    access_token = get_access_token(client)  # Helper method to get a valid access token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('/books', data=json.dumps(data), headers=headers, content_type='application/json')
    assert response.status_code == 201
    assert b'Test Book' in response.data


def test_get_books(client):
    # Test fetching all books
    response = client.get('/books')
    assert response.status_code == 200
    assert b'Test Book' in response.data  # Assuming Test Book is added in the previous test


def test_get_books_by_title(client):
    # Test fetching books by title
    response = client.get('/books?title=Test Book')
    assert response.status_code == 200
    assert b'Test Book' in response.data


def test_update_book(client):
    # Test updating a book
    data = {"title": "Updated Book", "publisher": "Updated Publisher", "author": "Updated Author", "pages": 1648,
            "created_at": "2017-01-12T00:00:00+03:00", "tags": ["Python", "Development", "Learning"],
            "updated_at": "2017-01-12T00:00:00+03:00"}
    access_token = get_access_token(client)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.put('/books/1', data=json.dumps(data), headers=headers, content_type='application/json')
    assert response.status_code == 200
    assert b'Updated Book' in response.data


def test_delete_book(client):
    # Test deleting a book
    access_token = get_access_token(client)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.delete('/books/Test%20Book', headers=headers)
    assert response.status_code == 200
    assert b'Book successfully deleted' in response.data


def get_access_token(client):
    # Helper method to get a valid access token (you may need to update this based on your application logic)
    data = {"username": "test_user", "password": "test_password"}
    response = client.post('/login', data=json.dumps(data), content_type='application/json')
    return json.loads(response.data)['access_token']
