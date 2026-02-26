# Sprint 2 - Authentication & Role Management

## Completed Tasks

### 1. JWT Authentication Implementation
- Created security module with password hashing (bcrypt)
- Implemented JWT token generation and validation
- Added token expiration handling
- Created OAuth2 password bearer scheme

### 2. User Registration & Login
- Built user registration endpoint with email validation
- Implemented login endpoint with JWT token generation
- Added OAuth2 compatible token endpoint for Swagger UI
- Password hashing for secure storage

### 3. Role-Based Access Control (RBAC)
- Implemented three user roles: Patient, Doctor, Admin
- Created role-specific dependency functions:
  - `get_current_user` - Any authenticated user
  - `get_current_patient` - Patient role only
  - `get_current_doctor` - Doctor role only
  - `get_current_admin` - Admin role only
- Protected endpoints with role-based dependencies

### 4. User Management
- User profile endpoints (view and update)
- Admin endpoint to view all users
- Email uniqueness validation
- User data update with conflict checking

### 5. Updated Appointment API
- Integrated JWT authentication with appointment endpoints
- Removed mock patient ID
- Added role-based access (patients only)
- Automatic patient ID extraction from JWT token

## API Endpoints

### Authentication Endpoints

#### Register User
```
POST /auth/register
Body: {
  "email": "patient@example.com",
  "password": "securepassword",
  "role": "patient",
  "first_name": "John",
  "last_name": "Doe"
}
Response: User object
```

#### Login
```
POST /auth/login
Body: {
  "email": "patient@example.com",
  "password": "securepassword"
}
Response: {
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### User Endpoints

#### Get Profile
```
GET /users/profile
Headers: Authorization: Bearer <token>
Response: User object
```

#### Update Profile
```
PUT /users/profile
Headers: Authorization: Bearer <token>
Body: {
  "first_name": "Jane",
  "last_name": "Smith"
}
Response: Updated user object
```

#### Get All Users (Admin Only)
```
GET /users/
Headers: Authorization: Bearer <admin_token>
Response: Array of user objects
```

### Appointment Endpoints (Updated)
All appointment endpoints now require JWT authentication:
- POST /appointments - Create appointment (Patient only)
- GET /appointments - Get user's appointments (Patient only)
- GET /appointments/{id} - Get specific appointment (Patient only)
- PUT /appointments/{id} - Update appointment (Patient only)
- DELETE /appointments/{id} - Cancel appointment (Patient only)

## Security Features

1. Password Hashing: Using bcrypt for secure password storage
2. JWT Tokens: Stateless authentication with expiration
3. Role-Based Access: Endpoint protection based on user roles
4. Email Validation: Pydantic email validation
5. Token Validation: Automatic token verification on protected routes

## Testing Authentication

### Using Swagger UI (http://localhost:8000/docs)

1. Register a new user via POST /auth/register
2. Click "Authorize" button at top right
3. Login using POST /auth/token with username (email) and password
4. Token will be automatically used for all subsequent requests

### Using cURL

```bash
# Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient@example.com",
    "password": "password123",
    "role": "patient",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient@example.com",
    "password": "password123"
  }'

# Use token for authenticated requests
curl -X GET "http://localhost:8000/users/profile" \
  -H "Authorization: Bearer <your_token_here>"
```

## Role Hierarchy

- Patient: Can book, view, update, and cancel their own appointments
- Doctor: Will be able to view appointments and create prescriptions (Sprint 3)
- Admin: Can view all users and access analytics (Sprint 3)

## Next Sprint

Sprint 3 will focus on:
- Prescription management (create, update, view)
- Doctor profile with specialization and availability
- Admin analytics and reporting
- Prescription download functionality
