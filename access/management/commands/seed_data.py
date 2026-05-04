from django.core.management.base import BaseCommand
from access.models import Role, Permission, RolePermission, UserRole
from users.models import User


class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными'

    def handle(self, *args, **kwargs):
        admin_role, _ = Role.objects.get_or_create(name='admin')
        moderator_role, _ = Role.objects.get_or_create(name='moderator')
        viewer_role, _ = Role.objects.get_or_create(name='viewer')
        self.stdout.write('Роли созданы')

        permissions = [
            ('articles', 'read'),
            ('articles', 'write'),
            ('articles', 'delete'),
            ('users', 'read'),
            ('users', 'write'),
            ('users', 'delete'),
        ]
        perm_objects = {}
        for resource, action in permissions:
            perm, _ = Permission.objects.get_or_create(resource=resource, action=action)
            perm_objects[f'{resource}_{action}'] = perm
        self.stdout.write('Разрешения созданы')

        for perm in perm_objects.values():
            RolePermission.objects.get_or_create(role=admin_role, permission=perm)

        for key in ['articles_read', 'articles_write', 'articles_delete', 'users_read']:
            RolePermission.objects.get_or_create(role=moderator_role, permission=perm_objects[key])

        RolePermission.objects.get_or_create(role=viewer_role, permission=perm_objects['articles_read'])
        self.stdout.write('Разрешения назначены ролям')

        users_data = [
            ('admin@test.com', 'Admin', admin_role),
            ('moderator@test.com', 'Moderator', moderator_role),
            ('viewer@test.com', 'Viewer', viewer_role),
        ]
        for email, first_name, role in users_data:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'first_name': first_name, 'last_name': 'Test', 'patronymic': 'Test'}
            )
            if created:
                user.set_password('testpass123')
                user.save()
            UserRole.objects.get_or_create(user=user, role=role)

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены!'))