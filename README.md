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

| Technology       | Purpose             |
| ---------------- | ------------------- |
| FastAPI          | Backend Framework   |
| PostgreSQL       | Relational Database |
| SQLAlchemy       | ORM                 |
| Pydantic         | Data Validation     |
| Passlib + bcrypt | Password Hashing    |
| Python-JOSE      | JWT Authentication  |
| Uvicorn          | ASGI Server         |
| Swagger UI       | API Documentation   |
| Postman          | API Testing         |

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

### User Table

| Column     | Type          |
| ---------- | ------------- |
| id         | Integer       |
| first_name | String        |
| last_name  | String        |
| email      | String        |
| password   | Hashed String |

### Notes Table

| Column      | Type        |
| ----------- | ----------- |
| id          | Integer     |
| title       | String      |
| description | Text        |
| is_archived | Boolean     |
| is_trashed  | Boolean     |
| user_id     | Foreign Key |

### Labels Table

| Column | Type    |
| ------ | ------- |
| id     | Integer |
| name   | String  |

### Note Labels Table

Used for many-to-many relationship between Notes and Labels.

| note_id | label_id |
| ------- | -------- |

---

## Relationships

* One User can have Many Notes.
* One Note can have Many Labels.
* One Label can belong to Many Notes.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/Fundoo-Notes.git

cd Fundoo-Notes
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/fundoo_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

Application will run on:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## Authentication Workflow

1. Register a new user.
2. Login using email and password.
3. Receive JWT access token.
4. Authorize using Swagger or Postman.
5. Access protected Notes and Labels APIs.

---

## API Endpoints

### Authentication

| Method | Endpoint       | Description   |
| ------ | -------------- | ------------- |
| POST   | `/users/`      | Register User |
| POST   | `/users/login` | Login User    |

### Users

| Method | Endpoint      |
| ------ | ------------- |
| GET    | `/users/`     |
| GET    | `/users/{id}` |
| PUT    | `/users/{id}` |
| DELETE | `/users/{id}` |

### Notes

| Method | Endpoint              |
| ------ | --------------------- |
| POST   | `/notes/`             |
| GET    | `/notes/`             |
| GET    | `/notes/{id}`         |
| PUT    | `/notes/{id}`         |
| DELETE | `/notes/{id}`         |
| PATCH  | `/notes/{id}/archive` |
| PATCH  | `/notes/{id}/trash`   |

### Labels

| Method | Endpoint                             |
| ------ | ------------------------------------ |
| POST   | `/labels/`                           |
| GET    | `/labels/`                           |
| DELETE | `/labels/{id}`                       |
| POST   | `/labels/{label_id}/notes/{note_id}` |
| DELETE | `/labels/{label_id}/notes/{note_id}` |

---

## API Testing

The APIs can be tested using:

* Swagger UI (`/docs`)
* ReDoc (`/redoc`)
* Postman Collections

---

## Future Improvements

* Alembic Database Migrations
* Docker Support
* Unit Testing with Pytest
* Redis Caching
* Email Verification
* Password Reset Functionality
* CI/CD Pipeline Integration

---

## Author

**Your Name**

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile

---

## License

This project is licensed under the MIT License.
