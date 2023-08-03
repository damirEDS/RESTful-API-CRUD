# Flask Book Management API

## Introduction
Flask Book Management API is a web application built using Flask and SQLite, allowing users to manage books through a RESTful API. The application provides endpoints for user registration, login, and book management.

## Table of Contents
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [Database Setup](#database-setup)
- [User Authentication](#user-authentication)
- [Book Management](#book-management)
  - [Get All Books or Filter by Title](#get-all-books-or-filter-by-title)
  - [Add a New Book](#add-a-new-book)
  - [Update an Existing Book](#update-an-existing-book)
  - [Delete a Book](#delete-a-book)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## Requirements
- Python 3.x
- Flask
- Flask_SQLAlchemy
- Flask_Restful
- Flask_JWT_Extended
- SQLite3

## Setup and Installation
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the application with `python app.py`.
4. The server will be up and running on `http://127.0.0.1:5000/`.

## Database Setup
- The SQLite database file is located at `books.db`.
- The `init_db` function creates the necessary `books` table with the required schema.

## User Authentication
- User registration is handled via the `/register` endpoint. Users can register with a unique username and password.
- User login is handled via the `/login` endpoint. Valid credentials will receive an access token.

## Book Management
### Get All Books or Filter by Title
- The `/books` endpoint with a GET request provides a list of all books in the database. You can also filter books by title using the `title` query parameter.

### Add a New Book
- The `/books` endpoint with a POST request allows authenticated users to add a new book. Provide the required book details in the request body.

### Update an Existing Book
- The `/books/<int:book_id>` endpoint with a PUT request allows authenticated users to update an existing book. Provide the updated book details in the request body.

### Delete a Book
- The `/books/<string:book_title>` endpoint with a DELETE request allows authenticated users to delete a book by its title.

## Usage
1. Register a new user using the `/register` endpoint.
2. Obtain an access token by logging in with the registered user credentials using the `/login` endpoint.
3. Use the obtained access token to perform CRUD operations on books using the `/books` endpoints.
4. Remember to include the access token in the request headers for authenticated requests.

## Contributors
- [Damir](https://github.com/damirEDS)

