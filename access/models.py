from django.db import models


class Role(models.Model):
    name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    resource = models.CharField(max_length=50)
    action = models.CharField(max_length = 50)

    def __str__(self):
        return f"{self.resource}.{self.action}"

    class Meta:
        unique_together = ('resource', 'action')

class UserRole(models.Model):
    user = models.ForeignKey(to = 'users.User', on_delete = models.CASCADE)
    role = models.ForeignKey(to = 'Role', on_delete = models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.email} : {self.role.name}"


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')