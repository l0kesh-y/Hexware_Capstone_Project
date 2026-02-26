# Sprint 5 - Microservice Architecture

## Completed Tasks

### 1. Service Decomposition
Successfully decomposed the monolithic application into three independent microservices:

#### Auth Service (Port 8001)
- User registration and authentication
- JWT token generation and validation
- User profile management
- Independent deployment
- Shared by all other services

#### Appointment Service (Port 8002)
- Appointment booking and management
- Doctor profile management
- Patient appointment tracking
- Depends on Auth Service for authentication

#### Prescription Service (Port 8003)
- Prescription creation and management
- Medicine tracking
- Doctor prescription history
- Depends on Auth Service for authentication

### 2. Service Communication
- REST-based synchronous communication
- HTTP requests between services
- Token validation via Auth Service
- Service discovery using Docker networking

### 3. Independent Deployment
Each service has:
- Own Dockerfile
- Own requirements.txt
- Own database models
- Independent scaling capability
- Isolated failure domain

### 4. Docker Orchestration
- docker-compose.microservices.yml for all services
- Shared PostgreSQL database
- Service networking
- Health checks for each service
- Dependency management

## Microservice Architecture

```
Client → Auth Service (8001)
      ↓
      → Appointment Service (8002) → Auth Service
      ↓
      → Prescription Service (8003) → Auth Service
      ↓
      → Shared PostgreSQL Database
```

## Service Details

### Auth Service
**Responsibilities:**
- User registration
- User login
- JWT token generation
- Token validation endpoint
- User profile management

**Endpoints:**
- POST /auth/register
- POST /auth/login
- POST /auth/validate-token
- GET /health

**Database Tables:**
- users

### Appointment Service
**Responsibilities:**
- Create appointments
- List appointments
- Update appointments
- Cancel appointments

**Endpoints:**
- POST /appointments
- GET /appointments
- GET /health

**Database Tables:**
- appointments

**Dependencies:**
- Auth Service (for token validation)

### Prescription Service
**Responsibilities:**
- Create prescriptions
- List prescriptions
- Update prescriptions

**Endpoints:**
- POST /prescriptions
- GET /prescriptions
- GET /health

**Database Tables:**
- prescriptions

**Dependencies:**
- Auth Service (for token validation)

## Running Microservices

### Start All Services
```bash
docker-compose -f docker-compose.microservices.yml up --build
```

### Start Specific Service
```bash
docker-compose -f docker-compose.microservices.yml up auth-service
```

### View Logs
```bash
# All services
docker-compose -f docker-compose.microservices.yml logs -f

# Specific service
docker-compose -f docker-compose.microservices.yml logs -f appointment-service
```

### Stop Services
```bash
docker-compose -f docker-compose.microservices.yml down
```

### Rebuild Service
```bash
docker-compose -f docker-compose.microservices.yml up --build auth-service
```

## Service URLs

When running with Docker Compose:
- Auth Service: http://localhost:8001
- Appointment Service: http://localhost:8002
- Prescription Service: http://localhost:8003
- PostgreSQL: localhost:5432

## API Documentation

Each service has its own Swagger documentation:
- Auth Service: http://localhost:8001/docs
- Appointment Service: http://localhost:8002/docs
- Prescription Service: http://localhost:8003/docs

## Testing Microservices

### 1. Register User (Auth Service)
```bash
curl -X POST "http://localhost:8001/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient@example.com",
    "password": "TestPass123",
    "role": "patient",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 2. Login (Auth Service)
```bash
curl -X POST "http://localhost:8001/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient@example.com",
    "password": "TestPass123"
  }'
```

### 3. Create Appointment (Appointment Service)
```bash
curl -X POST "http://localhost:8002/appointments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "doctor_id": "uuid-here",
    "appointment_time": "2026-03-10T10:00:00",
    "notes": "Regular checkup"
  }'
```

### 4. Create Prescription (Prescription Service)
```bash
curl -X POST "http://localhost:8003/prescriptions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <doctor_token>" \
  -d '{
    "appointment_id": "uuid-here",
    "notes": "Patient has mild fever",
    "medicines": [
      {
        "name": "Paracetamol",
        "dosage": "500mg",
        "duration": "3 days",
        "instructions": "Take after meals"
      }
    ]
  }'
```

## Benefits Achieved

### 1. Independent Deployment
- Deploy services independently
- No downtime for other services
- Faster deployment cycles

### 2. Technology Flexibility
- Each service can use different tech stack
- Upgrade dependencies independently
- Experiment with new technologies safely

### 3. Scalability
- Scale services independently based on load
- Auth Service: 1 instance
- Appointment Service: 3 instances (high traffic)
- Prescription Service: 2 instances

### 4. Fault Isolation
- Failure in one service doesn't affect others
- Graceful degradation
- Better system resilience

### 5. Team Autonomy
- Different teams can own different services
- Independent development cycles
- Reduced coordination overhead

## Challenges & Solutions

### Challenge 1: Service Communication
**Problem:** Services need to communicate
**Solution:** REST APIs with proper error handling

### Challenge 2: Data Consistency
**Problem:** Shared database can cause conflicts
**Solution:** Each service owns its tables, use transactions

### Challenge 3: Authentication
**Problem:** All services need authentication
**Solution:** Centralized Auth Service with token validation

### Challenge 4: Service Discovery
**Problem:** Services need to find each other
**Solution:** Docker Compose service names, DNS resolution

### Challenge 5: Monitoring
**Problem:** Multiple services to monitor
**Solution:** Centralized logging, health check endpoints

## Comparison: Monolith vs Microservices

### Monolithic Architecture (Sprint 1-4)
**Pros:**
- Simple deployment
- Easy to develop initially
- Single codebase
- No network latency

**Cons:**
- Tight coupling
- Difficult to scale
- Long deployment times
- Technology lock-in

### Microservice Architecture (Sprint 5)
**Pros:**
- Independent deployment
- Technology flexibility
- Better scalability
- Fault isolation
- Team autonomy

**Cons:**
- Complex deployment
- Network latency
- Distributed system challenges
- More infrastructure needed

## Future Enhancements

### 1. API Gateway
Add Nginx or Kong as API Gateway:
- Single entry point
- Rate limiting
- Load balancing
- SSL termination

### 2. Service Mesh
Implement Istio or Linkerd:
- Service-to-service encryption
- Traffic management
- Observability
- Circuit breaking

### 3. Message Queue
Add RabbitMQ or Kafka:
- Asynchronous communication
- Event-driven architecture
- Better decoupling
- Improved reliability

### 4. Caching Layer
Add Redis:
- Cache frequently accessed data
- Session management
- Rate limiting
- Improved performance

### 5. Monitoring & Observability
Implement:
- Prometheus for metrics
- Grafana for visualization
- Jaeger for distributed tracing
- ELK Stack for logging

### 6. CI/CD Pipeline
Set up:
- Automated testing
- Automated deployment
- Blue-green deployment
- Canary releases

## Production Considerations

### 1. Security
- HTTPS for all services
- Service-to-service authentication
- API key management
- Secrets management (Vault)

### 2. Reliability
- Circuit breakers
- Retry logic
- Timeout configuration
- Graceful shutdown

### 3. Performance
- Connection pooling
- Caching strategy
- Database optimization
- Load balancing

### 4. Monitoring
- Health checks
- Metrics collection
- Log aggregation
- Alerting

### 5. Deployment
- Container orchestration (Kubernetes)
- Auto-scaling
- Rolling updates
- Rollback strategy

## Conclusion

Sprint 5 successfully transformed the monolithic Healthcare API into a microservice architecture. The system is now more scalable, maintainable, and resilient. Each service can be developed, deployed, and scaled independently, providing better flexibility for future growth.

The microservice architecture provides a solid foundation for:
- Handling increased load
- Adding new features
- Improving system reliability
- Supporting multiple teams
- Adopting new technologies

This completes the Healthcare Appointment & E-Prescription API project with a production-ready microservice architecture.
