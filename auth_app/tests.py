from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User
from access.models import Role, RolePermission, UserRole
from django.urls import reverse

class ViewAuthAppTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test_email@gmail.com',
            password='12345',
            first_name='test',
            last_name='test',
            patronymic='test'
        )

    def test_register_view(self):
        url = reverse('register')
        response = self.client.post(url, data={
            'email': 'new_user@gmail.com',
            'password': '12345',
            'password_confirm': '12345',
            'first_name': 'test',
            'last_name': 'test',
            'patronymic': 'test'
        })
        self.assertEqual(response.status_code, 201)

    def test_register_400(self):
        url = reverse('register')
        response = self.client.post(url, data={
            'email': 'test_email@gmail.com',
            'password': '12345',
            'password_confirm': '12345',
            'first_name': 'test',
            'last_name': 'test',
            'patronymic': 'test'
        })
        self.assertEqual(response.status_code, 400)


    def test_login_view(self):
        url = reverse('login')
        response = self.client.post(url, data={
            'email': 'test_email@gmail.com',
            'password': '12345',
        })
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_login_view_401(self):
        url = reverse('login')
        response = self.client.post(url, data={
            'email': 'test_email@gmail.com',
            'password': '111111',
        })
        self.assertEqual(response.status_code, 401)

    def test_logout_view(self):
        login_response = self.client.post(reverse('login'), data={
            'email': 'test_email@gmail.com',
            'password': '12345',
        })
        access_token = login_response.data['access_token']
        refresh_token = login_response.data['refresh_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('logout')
        response = self.client.post(url, data={'refresh_token': refresh_token})
        self.assertEqual(response.status_code, 200)

    def test_logout_view_403(self):
        url = reverse('logout')
        self.client.credentials()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)