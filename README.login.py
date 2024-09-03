User Management and Todo API:
Description:
This project is a FastAPI-based web application that provides a comprehensive user management system along with a todo list feature. It includes endpoints for user registration, login, profile management, and CRUD operations for todo tasks. The application uses JWT authentication to secure endpoints and ensure only authorized users can access or modify their data.

Key Features:
User Registration: New users can register with their details, including name, office, hire date, address, email, and password. Passwords are securely hashed using Argon2.
User Login: Registered users can log in using their email and password. A JWT token is generated for authenticated sessions.
JWT Authentication: Secure routes are protected using JWT tokens to ensure that only authorized users can access or modify their information.
Profile Management: Users can view and update their profile information, including name, office, address, and hire date.
Todo Management: Users can create, update, delete, and view their todo tasks.
Database Integration: The application is connected to a MySQL database using SQLAlchemy for ORM and direct SQL queries.
Technologies Used:
FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
SQLAlchemy: An SQL toolkit and Object-Relational Mapping (ORM) library for Python.
Argon2: A cryptographic hashing algorithm used for secure password storage.
JWT (JSON Web Tokens): Used for securely transmitting information between the client and server as a JSON object.
MySQL: A widely used relational database management system.
