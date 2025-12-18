"""
Configuration file for Auth Service

This file loads environment variables and provides configuration
settings for the Flask application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Application configuration class
    
    Loads configuration from environment variables with sensible defaults
    """
    
    # Database Configuration
    # SQLAlchemy will use this URL to connect to the database
    # It works with both SQLite (local) and PostgreSQL (AWS RDS)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'sqlite:///auth.db'  # Default to SQLite for local development
    )
    
    # Disable SQLAlchemy modification tracking (saves memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Secret Key
    # This is used to sign and verify JWT tokens
    # IMPORTANT: Change this in production to a random, secure string
    JWT_SECRET_KEY = os.getenv(
        'JWT_SECRET_KEY', 
        'dev-secret-key-change-in-production'
    )
    
    # JWT Token Expiration (in seconds)
    # 24 hours = 86400 seconds
    JWT_EXPIRATION_SECONDS = 86400
    
    # Flask Configuration
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # CORS Configuration (allows frontend to call this API)
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')  # Allow all origins in development


# Create a config instance
config = Config()
