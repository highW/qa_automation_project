import jwt
import os
import datetime
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "qa_automation_super_secret_key_32chars!")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "qa_secure_pass_2024!")

def generate_token(username):
    """Generates a signed JWT token that expires in 30 minutes."""
    payload = {
        'sub': username,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30),
        'iat': datetime.datetime.now(datetime.timezone.utc)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def token_required(f):
    """Decorator that protects a route — rejects requests without a valid JWT."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify(error='Authentication token is missing'), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.current_user = payload['sub']
        except jwt.ExpiredSignatureError:
            return jsonify(error='Token has expired, please log in again'), 401
        except jwt.InvalidTokenError:
            return jsonify(error='Invalid token'), 401

        return f(*args, **kwargs)

    return decorated
