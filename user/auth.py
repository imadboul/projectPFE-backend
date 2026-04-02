import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .models import Client

SECRET_KEY = settings.SECRET_KEY

def create_jwt(user: Client):
    access_payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=2),
        "type": "access"
    }
    
    access_token = jwt.encode( access_payload , SECRET_KEY, algorithm="HS256")
    
    refresh_payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(days=10),
        "type": "refresh"
        
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")
    
    return access_token , refresh_token
    
    

def decode_jwt(token):
    
    print("decode hit")
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return "expired"
    except jwt.InvalidTokenError:
        return None
    
    

        
    
    