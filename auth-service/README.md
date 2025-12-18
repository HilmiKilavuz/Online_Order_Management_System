# Auth Service - README

## 🎯 What This Service Does

The Auth Service handles user authentication for the entire system:
- User registration
- User login with JWT tokens
- Token validation for other services

## 📁 Project Structure

```
auth-service/
├── app.py              # Main Flask application
├── models.py           # Database models (User table)
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── .gitignore         # Git ignore rules
```

## 🚀 Running Locally

### Step 1: Install Dependencies

```bash
cd auth-service
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# For local development (SQLite)
DATABASE_URL=sqlite:///auth.db
JWT_SECRET_KEY=your-secret-key
FLASK_ENV=development
FLASK_DEBUG=True
```

### Step 3: Run the Service

```bash
python app.py
```

The service will start on `http://localhost:5000`

## 📡 API Endpoints

### 1. Health Check
```
GET /health
```

### 2. Register User
```
POST /register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePassword123"
}
```

### 3. Login
```
POST /login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePassword123"
}
```

Returns JWT token.

### 4. Validate Token
```
POST /validate
Content-Type: application/json

{
  "token": "your-jwt-token"
}
```

### 5. Get Current User (Protected)
```
GET /me
Authorization: Bearer <your-jwt-token>
```

## 🔐 Security Features

- ✅ Passwords hashed with bcrypt
- ✅ JWT tokens with expiration
- ✅ Protected endpoints with token validation
- ✅ CORS enabled for frontend access

## 🗄️ Database

**Local Development**: SQLite (file-based)
**Production**: PostgreSQL on AWS RDS

The service automatically creates tables on first run.

## 🐳 Docker (Coming Next)

We'll containerize this service in the next step!
