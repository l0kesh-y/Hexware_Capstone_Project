# Sprint 1 - Project Setup & Basic Appointment API

## Completed Tasks

### 1. Project Structure Setup
- Created modular project structure with separation of concerns
- Organized code into layers: models, schemas, repositories, services, API routes
- Set up core infrastructure (config, database, constants)

### 2. Database Configuration
- Configured SQLAlchemy with PostgreSQL
- Created base model with UUID primary keys and timestamps
- Implemented User and Appointment models
- Set up Alembic for database migrations

### 3. Appointment API Implementation
- Created Appointment model with patient_id, doctor_id, appointment_time, status
- Implemented CRUD operations for appointments
- Built repository layer for data access
- Built service layer for business logic
- Created REST API endpoints:
  - POST /appointments - Book new appointment
  - GET /appointments - Get all patient appointments
  - GET /appointments/{id} - Get specific appointment
  - PUT /appointments/{id} - Update/reschedule appointment
  - DELETE /appointments/{id} - Cancel appointment

### 4. Docker Setup
- Created Dockerfile for API service
- Created docker-compose.yml with PostgreSQL and API services
- Configured health checks and volume persistence

### 5. Testing Setup
- Added pytest configuration
- Created basic health check tests
- Set up test structure for future integration tests

## API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy"}
```

### Create Appointment
```
POST /appointments
Body: {
  "doctor_id": "uuid",
  "appointment_time": "2026-03-10T10:00:00",
  "notes": "Optional notes"
}
Response: {
  "id": "uuid",
  "patient_id": "uuid",
  "doctor_id": "uuid",
  "appointment_time": "2026-03-10T10:00:00",
  "status": "booked",
  "notes": "Optional notes",
  "created_at": "2026-02-26T..."
}
```

### Get All Appointments
```
GET /appointments
Response: [array of appointments]
```

## Running the Application

### Using Docker (Recommended)
```bash
docker-compose up --build
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## Access Points
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- PostgreSQL: localhost:5432

## Notes
- Currently using mock patient ID for testing
- JWT authentication will be added in Sprint 2
- Role-based access control will be implemented in Sprint 2

## Next Sprint
Sprint 2 will focus on:
- JWT authentication implementation
- User registration and login
- Role-based access control (Patient, Doctor, Admin)
- Password hashing and security
