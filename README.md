## 📄 Overview

This project is a FastAPI 🚀 todo application, designed to manage users' todo lists.

## Project Backlog

The backlog includes detailed documentation about the process of this project.

I've used GitHub Projects to manage the requirements of this project. The URL can be
found [here](https://github.com/users/misraX/projects/1).

- [Add Authentication to FastAPI so that we can allow access to external users](https://github.com/misraX/fastapi-todo/issues/1)
    - ** Linked Pull Requests**: [PR #3](https://github.com/misraX/fastapi-todo/pull/3), [PR #4](https://github.com/misraX/fastapi-todo/pull/4), [PR #5](https://github.com/misraX/fastapi-todo/pull/5), [PR #6](https://github.com/misraX/fastapi-todo/pull/6), [PR #7](https://github.com/misraX/fastapi-todo/pull/7)
- [Adding login by username and password](https://github.com/misraX/fastapi-todo/pull/6)
- [Creating the user model and adding pytest support](https://github.com/misraX/fastapi-todo/pull/4)
- [Create a todo list so that a user can create/update/delete their lists](https://github.com/misraX/fastapi-todo/issues/2)
    - **Linked Pull Requests**: [PR #9](https://github.com/misraX/fastapi-todo/pull/9), [PR #12]
- [Add sharing to allow users to share their todos with others](https://github.com/misraX/fastapi-todo/issues/12)
    - **Linked Pull Requests**: [PR #13](https://github.com/misraX/fastapi-todo/pull/13)

## 🌐 APIs

### 🔐 Authentication

- **POST** `/user/login` - [JWT Login](http://localhost:8000/user/login)
- **POST** `/user/logout` - [JWT Logout](http://localhost:8000/user/logout)
- **POST** `/user/register` - [Register](http://localhost:8000/user/register)

### ✅ Todo

- **POST** `/todo/` - [Create Todo](http://localhost:8000/todo/)
- **GET** `/todo/` - [Get Todos](http://localhost:8000/todo/)
- **GET** `/todo/{todo_id}` - [Get Todo](http://localhost:8000/todo/{todo_id})
- **PATCH** `/todo/{todo_id}` - [Partial Update](http://localhost:8000/todo/{todo_id})
- **DELETE** `/todo/{todo_id}` - [Delete Todo](http://localhost:8000/todo/{todo_id})
- **POST** `/todo/{todo_id}/share/` - [Share Todo](http://localhost:8000/todo/{todo_id}/share/)
- **DELETE** `/todo/{todo_id}/unshare/` - [Unshare Todo](http://localhost:8000/todo/{todo_id}/unshare/)

### 📋 Task

- **POST** `/task/` - [Create Task](http://localhost:8000/task/)
- **GET** `/task/` - [Get Tasks](http://localhost:8000/task/)
- **GET** `/task/{task_id}` - [Get Task](http://localhost:8000/task/{task_id})
- **PATCH** `/task/{task_id}` - [Partial Update](http://localhost:8000/task/{task_id})
- **DELETE** `/task/{task_id}` - [Delete Task](http://localhost:8000/task/{task_id})

### 🔄 Shared Todo

- **GET** `/shared-todo/` - [Shared Todo](http://localhost:8000/shared-todo/)
- **GET** `/shared-todo/{todo_id}/tasks` - [Shared Tasks](http://localhost:8000/shared-todo/{todo_id}/tasks)

### 🩺 Health Check

- **GET** `/health` - [Read Root](http://localhost:8000/health)

# Installation

`docker-compose up -d`

`docker-compose exec fastapi python -m alembic upgrade head` # Database migration

`python e2e.py` make sure faker, requests is installed in your machine

## Main Libraries Used

- `fastapi-user`
- `pytest`
- `pytest-asyncio`
- `pytest-dotenv`

## Main Features

1. **User Authentication:**
    - Users can log in and log out.
    - Users can register.

2. **Authenticated User Actions:**
    - Creating todo lists.
    - Creating tasks.
    - Sharing todo lists with others.
    - Canceling sharing of todo lists with others.

3. **Architecture:**
    - The project embraces the service-repository pattern.
    - The project packaging is designed for scalability.
    - The project includes a unit of work.

## Potential Improvements

1. Adding a unified API schema base structure.
2. Adding more test cases.
3. Adding Celery for background tasks, such as creating todo lists in PDF format.
