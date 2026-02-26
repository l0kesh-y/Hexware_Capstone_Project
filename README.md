# Healthcare Appointment & E-Prescription API

A RESTful API for managing healthcare appointments and e-prescriptions built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- Patient registration and appointment booking
- Doctor availability management and prescription issuance
- Admin user management and analytics
- JWT-based authentication
- Role-based access control

## Technology Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Docker
- Alembic (Database Migrations)

## Project Structure

### Monolithic Architecture (Sprint 1-4)
```
healthcare-api/
├── app/
│   ├── main.py
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── api/
│   ├── middleware/
│   ├── exceptions/
│   └── utils/
├── alembic/
├── tests/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

### Microservice Architecture (Sprint 5)
```
healthcare-api/
├── microservices/
│   ├── auth-service/
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── appointment-service/
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── prescription-service/
│       ├── main.py
│       ├── Dockerfile
│       └── requirements.txt
└── docker-compose.microservices.yml
```

## Setup Instructions

### Local Development

1. Clone the repository
```bash
git clone https://github.com/l0kesh-y/Hexware_Capstone_Project.git
cd Hexware_Capstone_Project
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations
```bash
alembic upgrade head
```

6. Start the server
```bash
uvicorn app.main:app --reload
```

### Docker Setup

#### Monolithic Application
```bash
docker-compose up --build
```

#### Microservices
```bash
docker-compose -f docker-compose.microservices.yml up --build
```

## API Documentation

Once the server is running, visit:

### Monolithic Application
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Microservices
- Auth Service: http://localhost:8001/docs
- Appointment Service: http://localhost:8002/docs
- Prescription Service: http://localhost:8003/docs

## Development Sprints

- [x] Sprint 1: Project Setup & Basic Appointment API
- [x] Sprint 2: Authentication & Role Management
- [x] Sprint 3: Prescription & Admin Reporting
- [x] Sprint 4: Security & Deployment
- [x] Sprint 5: Microservice Architecture

## License

MIT
