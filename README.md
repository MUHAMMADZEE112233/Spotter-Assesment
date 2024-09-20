# Spotter-Assesment / Django Library Management System

This is a Django-based API for managing books, user favorites, and book recommendations. The app allows users to add books to their favorites, retrieve book recommendations, and manage their favorite books.

## Table of Contents

- [Setting Up the Project](#setting-up-the-project)
- [Creating a Virtual Environment](#creating-a-virtual-environment)
- [Requirements](#requirements)
- [Running Migrations](#running-migrations)
- [Running the Django Server](#running-the-django-server)
- [API Endpoints](#api-endpoints)

## Settign Up the Project
### 1. Clone the Repository

```bash
git clone https://github.com/your-username/library-management.git
cd library-management
```
### 2. Create Virtual Environment
you can use the [resource](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/) to create virtual environment.

### 3. Requirements
The requirements are listed in requirements.txt file, you can us below command to install
```
pip install -r requirements.txt
```
### 4. Running Migrations
- You need to specify the database credentials in `setting.py` file
- Run the below command to migrate the models into database.
```
python manage.py migrate
```
### 5. Running Django Server
- Use the command to run the django server
```
python manage.py runserver
```
### 6. API Endpoints
- Navigate to the api documentation using link below, where you will find the api schema. The API schema is generated with Swagger.
```
http://127.0.0.1:8000/api/docs/
```
### 7. Loom Video
- The explanation using loom video can be find by using the [link](https://www.loom.com/share/c8251d7bb8444f8b93e0258afe1cda5e?sid=2e504a35-a1fd-4569-9f44-5c860eb25688)
