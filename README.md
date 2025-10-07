# Blogging Website

[![Python](https://img.shields.io/badge/python-%3E%3D3.8-blue)]()

A Django-based web application for blogging. It allows users to create, edit, and manage blog posts, organize content by categories and tags, comment on posts, and search for content. The admin interface provides tools for user management, post moderation, and content organization. The project uses Django templates for frontend rendering, static assets for styling and interactivity, and a modular Python backend to handle business logic. The full stack involves Python, Django, HTML, CSS, and JavaScript.

---

## Overview

Blogging Website enables users to:

* Manage **blog posts** with full CRUD functionality
* Handle **user authentication and roles**
* Post and manage **comments**
* Organize content with **categories and tags**
* Search for **posts** efficiently
* View content on **mobile and desktop** through responsive design
* Navigate posts easily using **pagination**

---

## Features

* **CRUD Functionality**: Create, read, update, and delete blog posts.
* **User Authentication & Authorization**: Secure login, registration, and role-based access control.
* **Commenting System**: Users can comment on blog posts.
* **Categories & Tags**: Organize posts for easy navigation.
* **Search Functionality**: Search posts by keywords.
* **Responsive Design**: Works across mobile and desktop screens.
* **Pagination**: Split posts across pages for better readability.

---

## Tech Stack

* **Backend:** Django 4.x+
* **Frontend:** HTML, CSS, JavaScript (Django templates)
* **Database:** SQLite / PostgreSQL
* **Other Libraries:** As listed in `requirements.txt`

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Lachi1921/Blogging.git
cd Blogging
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

* **Windows:**

```bash
venv\Scripts\activate
```

* **macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set up environment variables

Create a `.env` file in the project root with values like:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
```

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## Usage

* Access the **Admin Dashboard** at `/admin` to manage:

  * Blog posts
  * Users and roles
  * Comments
  * Categories and tags

* Users can register, log in, create and comment on posts, search for content, and browse paginated posts.
