from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer


class UserMeView(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.is_active = False
        request.user.save()
        return Response(
            {'message': 'Аккаунт успешно удалён'},
            status=status.HTTP_200_OK
        )