import jwt
import secrets
from datetime import datetime, timedelta, timezone
from django.conf import settings

def generate_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=60),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
    return token

def generate_refresh_token():
    return secrets.token_hex(64)


def decode_access_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Токен истёк')
    except jwt.InvalidTokenError:
        raise ValueError('Токен недействителен')