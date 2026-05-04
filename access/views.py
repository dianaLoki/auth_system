from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.permissions import RBACPermission


class ArticleListView(APIView):
    def get_permissions(self):
        return [RBACPermission(resource='articles', action='read')]

    def get(self, request):
        return Response(
            {'message': 'Список статей — доступно для viewer, moderator, admin'},
            status=status.HTTP_200_OK
        )


class ArticleCreateView(APIView):
    def get_permissions(self):
        return [RBACPermission(resource='articles', action='write')]

    def post(self, request):
        return Response(
            {'message': 'Статья создана — доступно для moderator, admin'},
            status=status.HTTP_201_CREATED
        )


class ArticleDeleteView(APIView):
    def get_permissions(self):
        return [RBACPermission(resource='articles', action='delete')]

    def delete(self, request, pk):
        return Response(
            {'message': f'Статья {pk} удалена — доступно только для admin'},
            status=status.HTTP_200_OK
        )


class UserListView(APIView):
    def get_permissions(self):
        return [RBACPermission(resource='users', action='read')]

    def get(self, request):
        return Response(
            {'message': 'Список пользователей — доступно только для admin'},
            status=status.HTTP_200_OK
        )