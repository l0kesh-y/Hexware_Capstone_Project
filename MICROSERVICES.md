# Microservice Architecture Guide

## Overview

This document describes the microservice architecture for the Healthcare API system. The monolithic application has been decomposed into three independent microservices:

1. Auth Service - User authentication and authorization
2. Appointment Service - Appointment management
3. Prescription Service - Prescription management

## Architecture Diagram

```
┌─────────────┐
│   Client    │
│ (Web/Mobile)│
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   API Gateway   │ (Optional - Nginx/Kong)
│   Port: 80/443  │
└────────┬────────┘
         │
    ┌────┴────┬────────────┬────────────┐
    │         │            │            │
    ▼         ▼            ▼            ▼
┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│  Auth  │ │Appointment│ │Prescription│ │  Admin  │
│Service │ │ Service  │ │  Service  │ │ Service │
│:8001   │ │  :8002   │ │   :8003   │ │  :8004  │
└───┬────┘ └────┬─────┘ └─────┬────┘ └────┬─────┘
    │           │              │            │
    └───────────┴──────────────┴────────────┘
                      │
                      ▼
              ┌──────────────┐
              │  PostgreSQL  │
              │   Database   │
              └──────────────┘
```

## Service Breakdown

### 1. Auth Service (Port 8001)

Responsibilities:
- User registration
- User login
- JWT token generation
- Token validation
- User profile management

Database Tables:
- users

Endpoints:
- POST /auth/register
- POST /auth/login
- POST /auth/token
- GET /auth/validate-token
- GET /users/profile
- PUT /users/profile

### 2. Appointment Service (Port 8002)

Responsibilities:
- Appointment booking
- Appointment management
- Doctor profile management
- Schedule management

Database Tables:
- appointments
- doctor_profiles

Endpoints:
- POST /appointments
- GET /appointments
- GET /appointments/{id}
- PUT /appointments/{id}
- DELETE /appointments/{id}
- POST /doctors/profile
- GET /doctors/profile
- PUT /doctors/profile
- GET /doctors

Dependencies:
- Auth Service (for token validation)

### 3. Prescription Service (Port 8003)

Responsibilities:
- Prescription creation
- Prescription management
- Medicine tracking

Database Tables:
- prescriptions

Endpoints:
- POST /prescriptions
- GET /prescriptions
- GET /prescriptions/{id}
- PUT /prescriptions/{id}

Dependencies:
- Auth Service (for token validation)
- Appointment Service (to verify appointment exists)

### 4. Admin Service (Port 8004)

Responsibilities:
- System analytics
- User management
- Reporting

Endpoints:
- GET /admin/analytics
- GET /admin/users

Dependencies:
- Auth Service (for admin role validation)

## Communication Patterns

### 1. Synchronous Communication (REST)
Services communicate via HTTP REST APIs:
```python
# Appointment Service validates token with Auth Service
response = requests.post(
    "http://auth-service:8001/auth/validate-token",
    headers={"Authorization": f"Bearer {token}"}
)
```

### 2. Service Discovery
- Docker Compose: Services discover each other by service name
- Kubernetes: Use service DNS names
- Production: Use service mesh (Istio) or API Gateway

## Deployment

### Docker Compose Setup

Each service has its own:
- Dockerfile
- docker-compose.yml entry
- Environment variables
- Health checks

### Running Microservices

```bash
# Start all services
docker-compose -f docker-compose.microservices.yml up --build

# Start specific service
docker-compose -f docker-compose.microservices.yml up auth-service

# View logs
docker-compose -f docker-compose.microservices.yml logs -f appointment-service

# Stop all services
docker-compose -f docker-compose.microservices.yml down
```

## Service Configuration

### Auth Service
```env
DATABASE_URL=postgresql://user:password@db:5432/healthcare
SECRET_KEY=your-secret-key
PORT=8001
```

### Appointment Service
```env
DATABASE_URL=postgresql://user:password@db:5432/healthcare
AUTH_SERVICE_URL=http://auth-service:8001
PORT=8002
```

### Prescription Service
```env
DATABASE_URL=postgresql://user:password@db:5432/healthcare
AUTH_SERVICE_URL=http://auth-service:8001
APPOINTMENT_SERVICE_URL=http://appointment-service:8002
PORT=8003
```

## Benefits of Microservices

1. Independent Deployment: Deploy services independently
2. Technology Flexibility: Use different tech stacks per service
3. Scalability: Scale services independently based on load
4. Fault Isolation: Failure in one service doesn't affect others
5. Team Autonomy: Different teams can own different services
6. Easier Maintenance: Smaller codebases are easier to understand

## Challenges & Solutions

### Challenge 1: Service Communication
Solution: Use REST APIs with proper error handling and timeouts

### Challenge 2: Data Consistency
Solution: Use distributed transactions or eventual consistency patterns

### Challenge 3: Service Discovery
Solution: Use Docker Compose service names or Kubernetes DNS

### Challenge 4: Monitoring
Solution: Centralized logging (ELK) and distributed tracing (Jaeger)

### Challenge 5: Authentication
Solution: JWT tokens validated by Auth Service

## Migration Path

### Phase 1: Monolith (Current)
All functionality in single application

### Phase 2: Modular Monolith
Separate modules with clear boundaries (Already done in Sprint 1-4)

### Phase 3: Microservices
Extract modules into independent services (Sprint 5)

### Phase 4: Production Ready
Add API Gateway, service mesh, monitoring

## Testing Microservices

### Unit Tests
Test each service independently

### Integration Tests
Test service-to-service communication

### End-to-End Tests
Test complete user workflows across services

## Monitoring & Observability

### Metrics
- Request rate per service
- Response time per endpoint
- Error rate
- Resource usage (CPU, memory)

### Logging
- Centralized logging with correlation IDs
- Structured logging format
- Log aggregation (ELK Stack)

### Tracing
- Distributed tracing (Jaeger/Zipkin)
- Request flow visualization
- Performance bottleneck identification

## Security Considerations

1. Service-to-Service Authentication
2. API Gateway for external access
3. Network isolation
4. Secrets management
5. Rate limiting per service
6. Input validation at service boundaries

## Next Steps

1. Implement API Gateway (Nginx/Kong)
2. Add service mesh (Istio)
3. Implement circuit breakers
4. Add distributed tracing
5. Set up centralized logging
6. Implement service monitoring
7. Add automated testing pipeline
8. Set up CI/CD for each service
