from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
from utils.jwt_utils import decode_access_token


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != 'Bearer':
            raise AuthenticationFailed('Неверный формат токена')

        token = parts[1]

        try:
            payload = decode_access_token(token)
        except ValueError as e:
            raise AuthenticationFailed(str(e))

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('Пользователь не найден')

        if not user.is_active:
            raise AuthenticationFailed('Пользователь заблокирован')

        return (user, token)