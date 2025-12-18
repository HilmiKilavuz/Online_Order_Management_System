#  Online Order Management System

A production-ready microservices-based order management system built with Python, Docker, and deployed on AWS ECS. This project demonstrates modern cloud-native architecture, containerization, and DevOps practices.

![AWS](https://img.shields.io/badge/AWS-ECS-orange)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)

##  Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

---

##  Overview

This project is a microservices-based online order management system designed to handle user authentication, product management, order processing, payments, and notifications. Currently, the **Auth Service** is fully implemented and deployed on AWS.

### What's Implemented

- ✅ **Auth Service**: User registration, login, and JWT-based authentication
- ✅ **Web UI**: Modern, responsive interface for interacting with the Auth Service
- ✅ **AWS Deployment**: Fully deployed on AWS ECS with Application Load Balancer
- ✅ **Docker Containerization**: Production-ready Docker images
- ✅ **CI/CD Ready**: Infrastructure prepared for automated deployments

### Planned Services

- 🔄 **Product Service**: Product catalog management
- 🔄 **Order Service**: Order creation and management
- 🔄 **Payment Service**: Payment processing simulation
- 🔄 **Notification Service**: Email and event notifications

---

##  Architecture

### Current Architecture

```
Internet
   ↓
Application Load Balancer (ALB)
├── Public Subnet (AZ-1)
└── Public Subnet (AZ-2)
   ↓
ECS Service (Fargate)
├── Auth Service Task 1
└── Auth Service Task 2
   ↓
Database (SQLite/PostgreSQL)
```

### AWS Services Used

- **Amazon ECS (Fargate)**: Serverless container orchestration
- **Application Load Balancer**: Traffic distribution and health checks
- **Amazon ECR**: Private Docker registry
- **Amazon VPC**: Network isolation and security
- **AWS IAM**: Access control and permissions
- **CloudWatch**: Logging and monitoring
- **Amazon RDS**: (Planned) Managed PostgreSQL database

---

##  Features

### Auth Service

- **User Registration**: Secure user account creation with validation
- **JWT Authentication**: Token-based authentication with 24-hour expiration
- **Password Security**: Bcrypt hashing for password storage
- **Protected Routes**: Middleware for route protection
- **Health Monitoring**: Built-in health check endpoint

### Web UI

- **Modern Design**: Glassmorphism effects with gradient backgrounds
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Real-time Status**: API connection status indicator
- **User Dashboard**: Profile viewing and JWT token management
- **Smooth Animations**: Enhanced user experience with transitions

---

##  Technologies

### Backend

- **Python 3.11**: Core programming language
- **Flask 3.0**: Web framework
- **SQLAlchemy**: ORM for database operations
- **PyJWT**: JSON Web Token implementation
- **Bcrypt**: Password hashing
- **PostgreSQL**: Production database (planned)

### Frontend

- **HTML5/CSS3**: Structure and styling
- **JavaScript (ES6+)**: Application logic
- **Fetch API**: HTTP requests
- **CSS Grid/Flexbox**: Responsive layouts

### DevOps & Cloud

- **Docker**: Containerization
- **AWS ECS**: Container orchestration
- **AWS Fargate**: Serverless compute
- **AWS ECR**: Container registry
- **Application Load Balancer**: Load balancing
- **CloudWatch**: Monitoring and logging

### Development Tools

- **Git**: Version control
- **PowerShell**: Automation scripts
- **Python venv**: Virtual environments

---

##  Project Structure

```
online-order-management-system/
├── auth-service/              # Authentication microservice
│   ├── app.py                 # Main Flask application
│   ├── models.py              # Database models
│   ├── config.py              # Configuration management
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Docker image definition
│   ├── .dockerignore          # Docker build exclusions
│   ├── .env.example           # Environment template
│   └── README.md              # Service documentation
│
├── frontend/                  # Web user interface
│   ├── index.html             # Main HTML page
│   ├── styles.css             # Styling
│   ├── app.js                 # Application logic
│   ├── env.js                 # Environment loader
│   ├── .env.example           # Frontend config template
│   └── start-server.ps1       # Local dev server script
│
├── .gitignore                 # Git exclusions
└── README.md                  # This file
```

---

##  Getting Started

### Prerequisites

- Python 3.11+
- Docker Desktop
- AWS Account (for deployment)
- Git

### Local Development

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/online-order-management-system.git
cd online-order-management-system
```

#### 2. Set Up Auth Service

```bash
cd auth-service

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Run the service
python app.py
```

The Auth Service will be available at `http://localhost:5000`

#### 3. Set Up Frontend

```bash
cd frontend

# Create .env file
copy .env.example .env

# Update .env with your API URL
# For local development: API_URL=localhost:5000

# Start local server
python -m http.server 8000
```

Open `http://localhost:8000` in your browser

---

## 🌐 Deployment

### Docker Build

```bash
cd auth-service

# Build Docker image
docker build -t auth-service:latest .

# Run container locally
docker run -d -p 5001:5000 --name auth-service auth-service:latest

# Test
curl http://localhost:5001/health
```

### AWS Deployment

The project is configured for deployment on AWS ECS. Key components:

1. **VPC Setup**: Public and private subnets across multiple AZs
2. **Security Groups**: Configured for ALB and ECS communication
3. **ECR Repository**: Private Docker registry
4. **ECS Cluster**: Fargate-based container orchestration
5. **Application Load Balancer**: Traffic distribution
6. **IAM Roles**: Execution and task roles

For detailed deployment instructions, see the deployment guides in the `docs/` folder.

---

##  API Documentation

### Base URL

```
Production: http://your-alb-dns.region.elb.amazonaws.com
Local: http://localhost:5000
```

### Endpoints

#### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "auth-service",
  "timestamp": "2025-12-18T12:00:00"
}
```

#### Register User

```http
POST /register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

#### Login

```http
POST /login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

#### Get User Profile (Protected)

```http
GET /me
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "user": {
    "user_id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2025-12-18T12:00:00"
  }
}
```

---

##  Security

- **Password Hashing**: Bcrypt with salt rounds
- **JWT Tokens**: Secure token-based authentication
- **Environment Variables**: Sensitive data in .env files
- **HTTPS Ready**: SSL/TLS support (configure ALB)
- **CORS**: Configurable cross-origin policies
- **Input Validation**: Request data validation
- **SQL Injection Protection**: SQLAlchemy ORM

---

##  Testing

### Manual Testing

Use the included PowerShell test script:

```powershell
cd auth-service
powershell -ExecutionPolicy Bypass -File test-api.ps1
```

### API Testing

Use tools like:
- Postman
- cURL
- HTTPie
- The included web UI

---

##  Monitoring

- **CloudWatch Logs**: Container logs in `/ecs/auth-service-task`
- **Health Checks**: ALB performs regular health checks
- **Metrics**: ECS task metrics (CPU, memory, network)

---

##  Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---


##  Acknowledgments

- AWS Documentation
- Flask Community
- Docker Community
- Open Source Contributors

---



##  Roadmap

- [ ] Implement Product Service
- [ ] Implement Order Service
- [ ] Add Payment Service with SQS
- [ ] Add Notification Service with SNS
- [ ] Migrate to RDS PostgreSQL
- [ ] Implement CI/CD pipeline
- [ ] Add comprehensive test suite
- [ ] Add API Gateway
- [ ] Implement service mesh
- [ ] Add monitoring dashboards

---

**Built with  using Python, Docker, and AWS**
