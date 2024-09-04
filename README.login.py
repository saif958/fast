<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Management and Todo API</title>
</head>
<body>
    <h1>User Management and Todo API</h1>
    <p><strong>Description:</strong></p>
    <p>This project is a FastAPI-based web application that provides a comprehensive user management system along with a todo list feature. It includes endpoints for user registration, login, profile management, and CRUD operations for todo tasks. The application uses JWT authentication to secure endpoints and ensure only authorized users can access or modify their data.</p>
    
    <h2>Key Features:</h2>
    <ul>
        <li><strong>User Registration:</strong> New users can register with their details, including name, office, hire date, address, email, and password. Passwords are securely hashed using Argon2.</li>
        <li><strong>User Login:</strong> Registered users can log in using their email and password. A JWT token is generated for authenticated sessions.</li>
        <li><strong>JWT Authentication:</strong> Secure routes are protected using JWT tokens to ensure that only authorized users can access or modify their information.</li>
        <li><strong>Profile Management:</strong> Users can view and update their profile information, including name, office, address, and hire date.</li>
        <li><strong>Todo Management:</strong> Users can create, update, delete, and view their todo tasks.</li>
        <li><strong>Database Integration:</strong> The application is connected to a MySQL database using SQLAlchemy for ORM and direct SQL queries.</li>
    </ul>
    
    <h2>Technologies Used:</h2>
    <ul>
        <li><strong>FastAPI:</strong> A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.</li>
        <li><strong>SQLAlchemy:</strong> An SQL toolkit and Object-Relational Mapping (ORM) library for Python.</li>
        <li><strong>Argon2:</strong> A cryptographic hashing algorithm used for secure password storage.</li>
        <li><strong>JWT (JSON Web Tokens):</strong> Used for securely transmitting information between the client and server as a JSON object.</li>
        <li><strong>MySQL:</strong> A widely used relational database management system.</li>
    </ul>
</body>
</html>
