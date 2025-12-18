"""
Database models for Auth Service

This file defines the database schema using SQLAlchemy ORM.
ORM = Object-Relational Mapping (we write Python classes, SQLAlchemy creates SQL tables)
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

# Create SQLAlchemy instance
# This will be initialized with the Flask app in app.py
db = SQLAlchemy()


class User(db.Model):
    """
    User model - represents the 'users' table in the database
    
    Each instance of this class represents one row in the users table.
    SQLAlchemy automatically creates the table based on this class definition.
    """
    
    # Table name in the database
    __tablename__ = 'users'
    
    # Columns
    # Primary key: unique identifier for each user
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Username: must be unique and cannot be null
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    
    # Email: must be unique and cannot be null
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    
    # Password hash: we NEVER store plain text passwords!
    # We store the bcrypt hash of the password
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Timestamps: automatically track when user was created/updated
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        """String representation of User object (for debugging)"""
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """
        Hash the password and store it
        
        Args:
            password (str): Plain text password
            
        Security Note:
            - We use bcrypt with salt (automatic in bcrypt)
            - Salt ensures same password creates different hashes
            - This protects against rainbow table attacks
        """
        # Convert password to bytes
        password_bytes = password.encode('utf-8')
        
        # Generate salt and hash password
        # bcrypt.gensalt() creates a random salt
        # bcrypt.hashpw() combines password + salt and hashes it
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Store the hash as a string
        self.password_hash = hashed.decode('utf-8')
    
    def check_password(self, password):
        """
        Verify if the provided password matches the stored hash
        
        Args:
            password (str): Plain text password to check
            
        Returns:
            bool: True if password matches, False otherwise
        """
        # Convert inputs to bytes
        password_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        
        # bcrypt.checkpw() compares password with hash
        # It extracts the salt from the hash and re-hashes the password
        # Then compares the result with the stored hash
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    def to_dict(self):
        """
        Convert User object to dictionary (for JSON responses)
        
        Returns:
            dict: User data without sensitive information
            
        Security Note:
            We NEVER include password_hash in API responses!
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
