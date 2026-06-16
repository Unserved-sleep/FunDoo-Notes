# Fundoo Notes Backend API

A secure and scalable backend application inspired by Google Keep, built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy ORM**. The application provides user authentication, note management, label management, and JWT-based authorization.

---

## Features

### User Management

* User Registration
* User Login with JWT Authentication
* Password Hashing using bcrypt
* Secure Authorization using OAuth2 and JWT Tokens

### Notes Management

* Create Notes
* Retrieve Notes
* Update Notes
* Delete Notes
* Archive Notes
* Move Notes to Trash
* Access only authenticated user's notes

### Labels Management

* Create Labels
* Delete Labels
* Assign Labels to Notes
* Remove Labels from Notes

### Security

* JWT Authentication
* OAuth2 Password Flow
* Password Hashing using Passlib and bcrypt
* Protected Endpoints with Bearer Token Authentication

---

## Tech Stack

| Technology       | Purpose                       |
| ---------------- | ----------------------------- |
| FastAPI          | Backend Framework             |
| PostgreSQL       | Relational Database           |
| SQLAlchemy       | ORM                           |
| Pydantic         | Data Validation               |
| Passlib + bcrypt | Password Hashing              |
| Python-JOSE      | JWT Authentication            |
| Uvicorn          | ASGI Server                   |
| Swagger UI       | Interactive API Documentation |
| ReDoc            | API Documentation             |

---

## Project Structure

```bash
Fundoo-Notes/
│
├── app/
│   ├── config/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── note.py
│   │   ├── label.py
│   │   └── note_label.py
│   │
│   ├── routers/
│   │   ├── user_router.py
│   │   ├── note_router.py
│   │   └── label_router.py
│   │
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── note_schema.py
│   │   └── label_schema.py
│   │
│   ├── utils/
│   │   ├── auth.py
│   │   └── security.py
│   │
│   └── main.py
│
├── requirements.txt
├── .env
└── README.md
```

---

## Database Design

### Users Table

| Column     | Type            |
| ---------- | --------------- |
| id         | Integer         |
| first_name | String          |
| last_name  | String          |
| email      | String (Unique) |
| password   | Hashed String   |

---

### Notes Table

| Column      | Type        |
| ----------- | ----------- |
| id          | Integer     |
| title       | String      |
| description | Text        |
| is_archived | Boolean     |
| is_trashed  | Boolean     |
| user_id     | Foreign Key |

---

### Labels Table

| Column | Type            |
| ------ | --------------- |
| id     | Integer         |
| name   | String (Unique) |

---

### Note Labels Table

Used for the many-to-many relationship between Notes and Labels.

| note_id | label_id |
| ------- | -------- |

---

## Relationships

* **One User** can have **Many Notes**
* **One Note** can have **Many Labels**
* **One Label** can belong to **Many Notes**

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

### Swagger UI

Interactive API documentation and testing:

```text
http://127.0.0.1:8000/docs
```

Features:

* Interactive endpoint testing
* JWT Authorization support
* Request and response validation

---

### ReDoc

Alternative API documentation interface:

```text
http://127.0.0.1:8000/redoc
```

---

## Authentication Workflow

1. Register a new user.
2. Login using email and password.
3. Receive JWT access token.
4. Authorize using Swagger UI.
5. Access protected Notes and Labels endpoints.

---

## API Endpoints

### Authentication

| Method | Endpoint       | Description   |
| ------ | -------------- | ------------- |
| POST   | `/users/`      | Register User |
| POST   | `/users/login` | Login User    |

---

### Users

| Method | Endpoint      | Description    |
| ------ | ------------- | -------------- |
| GET    | `/users/`     | Get All Users  |
| GET    | `/users/{id}` | Get User by ID |
| PUT    | `/users/{id}` | Update User    |
| DELETE | `/users/{id}` | Delete User    |

---

### Notes

| Method | Endpoint              | Description        |
| ------ | --------------------- | ------------------ |
| POST   | `/notes/`             | Create Note        |
| GET    | `/notes/`             | Get User Notes     |
| GET    | `/notes/{id}`         | Get Note by ID     |
| PUT    | `/notes/{id}`         | Update Note        |
| DELETE | `/notes/{id}`         | Delete Note        |
| PATCH  | `/notes/{id}/archive` | Archive Note       |
| PATCH  | `/notes/{id}/trash`   | Move Note to Trash |

---

### Labels

| Method | Endpoint                             | Description            |
| ------ | ------------------------------------ | ---------------------- |
| POST   | `/labels/`                           | Create Label           |
| GET    | `/labels/`                           | Get All Labels         |
| DELETE | `/labels/{id}`                       | Delete Label           |
| POST   | `/labels/{label_id}/notes/{note_id}` | Assign Label to Note   |
| DELETE | `/labels/{label_id}/notes/{note_id}` | Remove Label from Note |

---

## Security Implementation

* Passwords are securely hashed using **bcrypt** before storing in the database.
* JWT tokens are generated after successful authentication.
* Protected routes require a valid Bearer token.
* Users can only access and modify their own notes.
