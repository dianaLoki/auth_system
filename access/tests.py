from rest_framework.test import APITestCase
from django.test import TestCase
from django.urls import reverse
from access.models import Role, Permission, UserRole, RolePermission
from users.models import User
from utils.jwt_utils import generate_access_token


class TestApiView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Test',
            patronymic='Test'
        )
        self.role = Role.objects.create(name='admin')

        self.articles_read = Permission.objects.create(resource='articles', action='read')
        self.articles_write = Permission.objects.create(resource='articles', action='write')
        self.users_read = Permission.objects.create(resource='users', action='read')
        self.articles_delete = Permission.objects.create(resource='articles', action='delete')

        RolePermission.objects.create(role=self.role, permission=self.articles_delete)
        UserRole.objects.create(user=self.user, role=self.role)
        RolePermission.objects.create(role=self.role, permission=self.articles_read)
        RolePermission.objects.create(role=self.role, permission=self.articles_write)
        RolePermission.objects.create(role=self.role, permission=self.users_read)

        token = generate_access_token(self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_article_list_view(self):
        url = reverse('article-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Список статей — доступно для viewer, moderator, admin')

    def test_article_no_token(self):
        self.client.credentials()
        url = reverse('article-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_article_create_view(self):
        url = reverse('article-create')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Статья создана — доступно для moderator, admin')

    def test_article_create_view_402(self):
        self.viewer = User.objects.create_user(
            email='viewer@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Test',
            patronymic='Test'
        )
        token = generate_access_token(self.viewer.id)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.role = Role.objects.create(name='viewer')
        UserRole.objects.create(user=self.viewer, role=self.role)
        url = reverse('article-create')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_article_delete_view(self):
        url = reverse('article-delete', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_user_list_view(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Список пользователей — доступно только для admin')

class TestModels(TestCase):

    def test_role_model(self):
        role = Role.objects.create(name = 'someone')
        self.assertEqual(str(role), role.name)

    def test_permission_model(self):
        permission = Permission.objects.create(resource='articles', action='read')
        self.assertEqual(str(permission), 'articles.read')
