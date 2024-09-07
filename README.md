# Library Management System v2.0

The Library Management System is a robust multi-user application designed to manage e-books efficiently. This system caters to both librarians and general users, providing an intuitive interface for requesting, reading, returning, and managing e-books. Version 2.0 builds upon the foundational features of v1.0 with significant enhancements to improve user experience and system performance.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [ER Diagram](#er-diagram)
- [Wireframe](#wireframe)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Technologies Used

### Frontend
- HTML
- CSS
- Bootstrap
- Vue.js

### Backend
- Flask

### Templating Engine
- Jinja

### Data Storage
- SQLite
- Redis

### Task Scheduling
- Celery

### PDF Generation
- Pdfkit

### Email Handling
- Smtplib

### Libraries
- **Flask**: A micro web framework for Python.
- **SQLAlchemy**: A Python SQL toolkit and Object-Relational Mapping (ORM) library.
- **Flask-SQLAlchemy**: An extension for Flask that adds support for SQLAlchemy.
- **Flask-RESTful**: An extension for Flask that adds support for quickly building REST APIs.
- **Matplotlib**: A comprehensive library for creating static, animated, and interactive visualizations in Python.
- **Seaborn**: A data visualization library based on Matplotlib that provides a high-level interface for drawing attractive and informative statistical graphics.
- **Pdfkit**: Helps to create PDF reports from HTML content, which can be sent to users.
- **Smtplib**: Enables sending emails with attachments and custom content.

### IDE
- Visual Studio Code (VS Code)

## Features

### Core Features (from v1.0)
1. **User Authentication**: Users and librarians can log in to access the system.
2. **Section Management**: Librarians can add new sections with details like name, date created, and description.
3. **Book Management**: Librarians can add new books with attributes such as title, content, author(s), etc.
4. **Book Issuing**: Users can request books, and librarians can approve or reject these requests.
5. **Book Return**: Users can return books after reading.
6. **Data Visualization**: Graphical representation of data such as user roles distribution, book request status, and section-wise book count.
7. **File Handling**: Functionality for uploading and downloading e-books.
8. **Search Options**: Users can search for books.

### New Features in v2.0
1. **Advanced User Authentication**: Enhanced with RBAC (Role-Based Access Control).
2. **Redis Caching**: Implemented for the stats page to reduce unnecessary database queries and improve performance.
3. **Task Scheduling**: Automated tasks like sending monthly reports and daily reminders using Celery.
4. **Book Rating**: Users can now rate books once they have been returned.
5. **CSV Download**: Users can download a CSV file of their issued, requested, and completed books.
6. **One-Click Book Download**: Users can download books directly with a single click after access has been granted.
7. **5-Book Request Limit**: Users are now limited to requesting up to 5 books at a time.

## Installation

### Prerequisites
- Python 3.x
- Redis (for caching and Celery task queue)
- wkhtmltopdf (for Pdfkit)

### Steps
1. **Clone the repository:**
    ```sh
    git clone https://github.com/Akashkunwar/Library_Management_System.git
    ```

2. **Navigate to the project directory:**
    ```sh
    cd Library_Management_System
    ```

3. **Create a virtual environment:**
    ```sh
    python3 -m venv venv
    ```

4. **Activate the virtual environment:**
    - On Windows:
      ```sh
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      source venv/bin/activate
      ```

5. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

6. **Set up the database:**
    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

7. **Run Redis server:**
    ```sh
    redis-server
    ```

8. **Start Celery worker:**
    ```sh
    celery -A celery_schedule.celery worker --loglevel=info
    ```

9. **Run the application:**
    ```sh
    flask run
    ```

## Usage

1. **Access the application** in your web browser at `http://127.0.0.1:5000`.
2. **Log in with provided credentials:**
    - Admin: `admin` / `admin`
    - Super User: `super` / `user`
    - User: `user` / `user`
    - Demo User: `demo` / `user`
    - Dummy User: `dummy` / `dummy`
3. **Explore** the new and existing features such as section management, book management, issuing and returning books, and advanced functionalities like Redis caching, task scheduling, and book rating.

## ER Diagram
![ER Diagram](https://raw.githubusercontent.com/Akashkunwar/Library_Management_System_v2/main/ERD.png)

## Wireframe
![Wireframe](https://raw.githubusercontent.com/Akashkunwar/Library_Management_System/main/LMS.jpeg)

## Future Enhancements

For future versions, we aim to introduce:
- **Enhanced Search Functionality**: Implementing fuzzy search and filters.
- **Recommendation System**: Suggesting books based on user history and ratings.
- **API Integration**: Expanding REST APIs for third-party integrations.
- **Multi-Language Support**: Adding support for multiple languages.
- **Mobile Application**: Developing a mobile app version of the system.

## Contributing

We welcome contributions! Feel free to fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

---

Feel free to reach out if you have any questions or suggestions. Thank you for your interest in my project!

---
