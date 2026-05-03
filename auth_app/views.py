from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from auth_app.serializers import RegisterSerializer, LoginSerializer
from auth_app.models import RefreshToken
from utils.jwt_utils import generate_access_token, generate_refresh_token
from datetime import datetime, timedelta, timezone


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Пользователь успешно зарегистрирован'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {'error': 'Неверный email или пароль'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh_token = generate_refresh_token()
        access_token = generate_access_token(user.id)

        RefreshToken.objects.create(
            user=user,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=30)
        )

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
        }, status=status.HTTP_200_OK)