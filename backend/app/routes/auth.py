from flask import Blueprint, request, jsonify
import jwt
import datetime
from ..config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Mock authentication - in prod check DB
    if data.get('username') == 'admin' and data.get('password') == 'admin':
        token = jwt.encode({
            'user': 'admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, Config.JWT_SECRET_KEY, algorithm="HS256")
        
        return jsonify({'token': token, 'role': 'CEO'}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401
