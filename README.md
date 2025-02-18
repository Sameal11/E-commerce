E-Commerce DBMS Project - Login & Signup System

   Project Overview

 This project is a simple authentication system for an E-Commerce DBMS using MySQL as the database. It includes a login and signup system where users can register and log in securely.

Features

User Registration (Signup)

User Authentication (Login)

Secure Password Hashing (bcrypt)

REST API using Node.js & Express.js

MySQL Database Integration

Tech Stack

Backend: Node.js, Express.js

Database: MySQL

Frontend: HTML, CSS, JavaScript

Security: bcrypt for password hashing

Installation & Setup

Prerequisites

Ensure you have the following installed:

Node.js

MySQL

A REST Client (Postman or cURL) to test API endpoints

Steps to Setup

Clone the Repository:

git clone https://github.com/yourusername/e-commerce-login-signup.git
cd e-commerce-login-signup

Install Dependencies:

npm install

Setup MySQL Database:

Create a database named ecommerce_db.

Run the following SQL query to create the users table:

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

Configure Database Connection:

Open server.js and update the database credentials:

const db = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "yourpassword",
    database: "ecommerce_db"
});

Run the Server:

node server.js

Open Frontend (index.html) in Browser

The frontend consists of a simple form to register and login users.

API Endpoints

1. Signup (User Registration)

Endpoint: POST /signup

Request Body:

{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
}

Response:

{
    "message": "User registered successfully"
}

2. Login (User Authentication)

Endpoint: POST /login

Request Body:

{
    "email": "john@example.com",
    "password": "password123"
}

Response:

{
    "message": "Login successful",
    "token": "your_jwt_token"
}

Future Enhancements

Implement JWT-based authentication

Add role-based access control (Admin, Customer, Vendor)

Improve UI with a modern frontend framework (React/Vue)

License

This project is licensed under the MIT License.

Author

[Sameal11] - [github.com/sameal11]

