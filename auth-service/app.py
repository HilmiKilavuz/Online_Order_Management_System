"""
Auth Service - Main Application

This is the entry point for the Auth Service microservice.
It provides endpoints for user registration, login, and token validation.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User
from config import config
import jwt
from datetime import datetime, timedelta
from functools import wraps

# Create Flask application
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(config)

# Initialize database with Flask app
db.init_app(app)

# Enable CORS (Cross-Origin Resource Sharing)
# This allows other services and frontends to call our API
CORS(app, origins=config.CORS_ORIGINS)


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_database():
    """
    Initialize the database
    
    This creates all tables defined in models.py if they don't exist.
    In production, you'd use migrations (Alembic), but for learning this is fine.
    """
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_jwt_token(user_id, username, email):
    """
    Generate a JWT token for authenticated user
    
    Args:
        user_id (int): User's ID
        username (str): User's username
        email (str): User's email
        
    Returns:
        str: JWT token
        
    JWT Structure:
        - Header: Algorithm and token type
        - Payload: User data and expiration
        - Signature: Ensures token hasn't been tampered with
    """
    # Calculate expiration time
    expiration = datetime.utcnow() + timedelta(seconds=config.JWT_EXPIRATION_SECONDS)
    
    # Create payload (data to encode in token)
    payload = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'exp': expiration,  # Expiration time
        'iat': datetime.utcnow()  # Issued at time
    }
    
    # Encode payload with secret key
    token = jwt.encode(
        payload,
        config.JWT_SECRET_KEY,
        algorithm='HS256'  # HMAC with SHA-256
    )
    
    return token


def decode_jwt_token(token):
    """
    Decode and validate a JWT token
    
    Args:
        token (str): JWT token to decode
        
    Returns:
        dict: Decoded payload if valid
        None: If token is invalid or expired
    """
    try:
        # Decode token with secret key
        payload = jwt.decode(
            token,
            config.JWT_SECRET_KEY,
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid (tampered with or malformed)
        return None


def token_required(f):
    """
    Decorator to protect endpoints that require authentication
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route(current_user):
            return jsonify({'message': f'Hello {current_user["username"]}'})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get token from Authorization header
        # Expected format: "Bearer <token>"
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Authorization header is missing'}), 401
        
        # Extract token from "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Invalid authorization header format. Use: Bearer <token>'}), 401
        
        token = parts[1]
        
        # Decode and validate token
        payload = decode_jwt_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Pass user info to the route function
        return f(current_user=payload, *args, **kwargs)
    
    return decorated


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Used by AWS load balancers to check if service is running.
    Returns 200 if service is healthy.
    """
    return jsonify({
        'status': 'healthy',
        'service': 'auth-service',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/register', methods=['POST'])
def register():
    """
    User registration endpoint
    
    Request Body (JSON):
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "SecurePassword123"
        }
        
    Response (Success - 201):
        {
            "message": "User registered successfully",
            "user": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com"
            }
        }
        
    Response (Error - 400):
        {
            "error": "Error message"
        }
    """
    # Get JSON data from request
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Check all fields are present
    if not all([username, email, password]):
        return jsonify({'error': 'Missing required fields: username, email, password'}), 400
    
    # Validate username length
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    # Validate password length
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Check if user already exists
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        if existing_user.username == username:
            return jsonify({'error': 'Username already exists'}), 400
        else:
            return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    try:
        new_user = User(
            username=username,
            email=email
        )
        new_user.set_password(password)  # Hash the password
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@app.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    
    Request Body (JSON):
        {
            "email": "john@example.com",
            "password": "SecurePassword123"
        }
        
    Response (Success - 200):
        {
            "message": "Login successful",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "user": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com"
            }
        }
        
    Response (Error - 401):
        {
            "error": "Invalid credentials"
        }
    """
    # Get JSON data from request
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Missing required fields: email, password'}), 400
    
    # Find user by email
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Check if account is active
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 401
    
    # Verify password
    if not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate JWT token
    token = generate_jwt_token(user.id, user.username, user.email)
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    }), 200


@app.route('/validate', methods=['POST'])
def validate_token():
    """
    Token validation endpoint
    
    Other services can call this to validate JWT tokens.
    
    Request Body (JSON):
        {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
        
    Response (Success - 200):
        {
            "valid": true,
            "user": {
                "user_id": 1,
                "username": "john_doe",
                "email": "john@example.com"
            }
        }
        
    Response (Error - 401):
        {
            "valid": false,
            "error": "Invalid or expired token"
        }
    """
    data = request.get_json()
    
    if not data or 'token' not in data:
        return jsonify({'valid': False, 'error': 'No token provided'}), 400
    
    token = data['token']
    
    # Decode and validate token
    payload = decode_jwt_token(token)
    
    if not payload:
        return jsonify({'valid': False, 'error': 'Invalid or expired token'}), 401
    
    return jsonify({
        'valid': True,
        'user': {
            'user_id': payload['user_id'],
            'username': payload['username'],
            'email': payload['email']
        }
    }), 200


@app.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """
    Get current user information
    
    Protected endpoint - requires valid JWT token in Authorization header.
    
    Request Headers:
        Authorization: Bearer <token>
        
    Response (Success - 200):
        {
            "user": {
                "user_id": 1,
                "username": "john_doe",
                "email": "john@example.com"
            }
        }
    """
    return jsonify({'user': current_user}), 200


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    # Initialize database tables
    init_database()
    
    # Run Flask development server
    # host='0.0.0.0' makes it accessible from other containers/machines
    # port=5000 is the standard Flask port
    print("\n" + "="*60)
    print("🚀 Auth Service Starting...")
    print("="*60)
    print(f"📍 Running on: http://localhost:5000")
    print(f"🗄️  Database: {config.SQLALCHEMY_DATABASE_URI}")
    print(f"🔐 JWT Secret: {config.JWT_SECRET_KEY[:10]}...")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=config.DEBUG
    )
