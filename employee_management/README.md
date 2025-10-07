🧑‍💼 Employee Management System

A Django-based RESTful API for managing employees and departments.
The project includes features like employee CRUD operations, department management, filtering, search, pagination, CSV/JSON export, and API documentation with Swagger/Redoc.

🚀 Features

Manage Employees: Create, read, update, and soft delete employees.

Manage Departments: CRUD operations with employee count check before deletion.

Filtering, Searching, and Ordering for API endpoints.

Pagination support using custom pagination.

Export Employee Data in CSV or JSON formats.

API Documentation available via Swagger and Redoc.

Debug Toolbar and Query Count Middleware for development.

Pre-populated SQLite database included for testing.

🛠️ Tech Stack

Backend: Python 3.11+, Django 5.2

API: Django REST Framework (DRF)

Database: SQLite (default DB included)

Other Libraries

drf-spectacular (OpenAPI/Swagger/Redoc docs)

django-filter

django-debug-toolbar

querycount

📂 Project Structure
employee_management/
├── employee_management/ # Django project settings
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
├── employees/ # Django app
│ ├── api/v1/ # API endpoints
│ │ ├── serializers.py
│ │ ├── urls.py
│ │ └── views.py
│ ├── migrations/
│ ├── models.py
│ ├── pagination.py
│ ├── admin.py
│ └── apps.py
├── db.sqlite3 # Pre-populated database
├── manage.py
└── requirements.txt

⚙️ Getting Started

Follow these steps to run the project locally.

1️⃣ Clone the Repository
git clone <your-repo-url>
cd employee_management

2️⃣ Create a Virtual Environment
python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows

3️⃣ Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

4️⃣ Run the Project
python manage.py runserver

The project will be available at:
👉 http://127.0.0.1:8000/

🔗 Access API Endpoints
Endpoint Description
http://127.0.0.1:8000/api/v1/employees/
Employee API
http://127.0.0.1:8000/api/v1/employees/departments/
Department API
http://127.0.0.1:8000/api/docs/
Swagger UI
http://127.0.0.1:8000/api/redoc/
Redoc Docs
📝 Notes

The project uses SQLite as the database.
The file db.sqlite3 already contains sample data, so you can test the APIs immediately after cloning.

Employee deletion is a soft delete (data is not removed physically).

Department deletion is restricted if employees exist in that department.

🤝 Contributing

Fork the repository.

Create a new branch:

git checkout -b feature-name

Make your changes and commit:

git commit -m "Description of changes"

Push to your branch:

git push origin feature-name

Create a pull request.

🪪 License

This project is open-source and free to use.
