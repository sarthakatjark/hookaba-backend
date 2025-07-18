# hookaba-backend

A production-ready Flask backend for OTP authentication via phone number, using MongoDB and best practices.

## Features
- Flask application factory pattern
- Blueprints for modularity
- Service-layer architecture
- Environment-based configuration
- OTP authentication via phone number (MongoDB)
- Marshmallow for validation
- Logging for OTP events
- Docker-ready

## Project Structure

```
hookaba-backend/
├── app/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── common/
│   │   ├── sms.py
│   │   └── utils.py
│   ├── config.py
│   ├── extensions.py
│   ├── library/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── services.py
│   └── users/
│       ├── __init__.py
│       ├── routes.py
│       ├── schemas.py
│       └── services.py
├── instance/
│   └── config.py
├── tests/
│   └── test_auth.py
├── requirements.txt
├── Dockerfile
├── run.py
├── wsgi.py
├── README.md
└── .gitignore
```

## API Endpoints

### Auth Endpoints (`/auth`)

#### POST `/auth/request-otp`
Request an OTP for a phone number.

- **Request Body (JSON):**
  ```json
  {
    "phone": "string"
  }
  ```
- **Responses:**
  - 200 OK: `{ "message": "OTP sent" }`
  - 400 Bad Request: `{ "errors": { ... } }`

#### POST `/auth/verify-otp`
Verify an OTP for a phone number.

- **Request Body (JSON):**
  ```json
  {
    "phone": "string",
    "otp": "string"
  }
  ```
- **Responses:**
  - 200 OK (Success): `{ "success": true, "message": "OTP verified", "access_token": "jwt_token_here" }`
  - 200 OK (Failure): `{ "success": false, "message": "Invalid OTP" }`
  - 400 Bad Request: `{ "errors": { ... } }`

---

### User Endpoints

#### POST `/users`
Create a new user.

- **Request Body (JSON):**
  ```json
  {
    "username": "string",
    "number": "string"
  }
  ```
- **Responses:**
  - 201 Created: `{ "message": "User created", "user_id": "string" }`
  - 409 Conflict: `{ "error": "Phone number already in use" }` or `{ "error": "Username already in use" }`
  - 400 Bad Request: `{ "errors": { ... } }`
  - 500 Internal Server Error: `{ "error": "User creation failed" }`

#### GET `/users/<user_id>`
Get user details by user ID.

- **Response:**
  - 200 OK:
    ```json
    {
      "_id": "string",
      "username": "string",
      "number": "string",
      "created_on": "ISO8601 datetime string"
    }
    ```
  - 404 Not Found: `{ "error": "User not found" }`

---

### Library Endpoints (`/library`)

#### POST `/library/upload`
Upload an image or gif to S3 and store its URL, user ID, and upload time in MongoDB.

- **Request (multipart/form-data):**
  - `file`: The file to upload (required)
  - `user_id`: The user ID (required)
- **Responses:**
  - 201 Created: `{ "message": "File uploaded", "id": "string", "url": "string" }`
  - 400 Bad Request: `{ "error": "No file part" }`, `{ "error": "No selected file" }`, or `{ "error": "Missing user_id" }`
  - 500 Internal Server Error: `{ "error": "Failed to upload file to S3", "details": "string" }`, `{ "error": "Failed to save library item", "details": "string" }`, or `{ "error": "Internal server error", "details": "string" }`

#### GET `/library`
List all library items with pagination.

- **Query Parameters:**
  - `page` (integer, optional, default: 1)
  - `per_page` (integer, optional, default: 10)
- **Response:**
  - 200 OK:
    ```json
    {
      "items": [
        {
          "url": "string",
          "user_id": "string",
          "created_at": "ISO8601 datetime string"
        }
      ],
      "page": 1,
      "per_page": 10,
      "total": 100,
      "total_pages": 10
    }
    ```
  - 500 Internal Server Error: `{ "error": "Failed to fetch library items", "details": "string" }` or `{ "error": "Internal server error", "details": "string" }`