from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'patronymic', 'created_at']
        read_only_fields = ['id', 'email', 'created_at']
