import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-prod'
    DATABASE_URI = os.path.join(os.getcwd(), 'backend', 'data', 'superstore_enhanced.db')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    CORS_HEADERS = 'Content-Type'
