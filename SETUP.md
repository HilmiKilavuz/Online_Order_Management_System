# Quick Setup Guide

## For New Contributors

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/online-order-management-system.git
cd online-order-management-system
```

### 2. Set Up Auth Service
```bash
cd auth-service
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your settings
python app.py
```

### 3. Set Up Frontend
```bash
cd frontend
copy .env.example .env
# Edit .env with your API URL
python -m http.server 8000
```

### 4. Access the Application
- Auth Service API: http://localhost:5000
- Web UI: http://localhost:8000

## Environment Variables

### Auth Service (.env)
```
DATABASE_URL=sqlite:///auth.db
JWT_SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Frontend (.env)
```
API_URL=localhost:5000
```

For AWS deployment, update API_URL with your load balancer DNS.

## Testing

Run the test script:
```powershell
cd auth-service
powershell -ExecutionPolicy Bypass -File test-api.ps1
```

## Need Help?

See the main [README.md](README.md) for detailed documentation.
