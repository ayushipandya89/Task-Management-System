# Task Management System

## Overview

The Task Management System (TMS) is a web application designed to facilitate the creation, management, and assignment of tasks. It allows users to create and manage task lists, assign tasks, and comment on tasks. The system differentiates between regular users and admin users, providing varying levels of access and control.

## Features

- **User Authentication**: Register, login, and manage user accounts.
- **Task Lists**: Create, update, and delete task lists.
- **Tasks**: Create, update, and delete tasks, with the ability to assign tasks to users.
- **Comments**: Add comments to tasks.
- **Admin Functionality**: Admin users have additional privileges such as assigning tasks to other users.

## Technology Stack

- **Backend**: Django, Django Rest Framework
- **Database**: PostgreSQL

## Installation

### Prerequisites

- Python 3.8 or higher

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ayushipandya89/Task-Management-System.git
    cd TMS
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply the database migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser (admin user):**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```
