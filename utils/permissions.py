from rest_framework.permissions import BasePermission
from access.models import UserRole, RolePermission


class RBACPermission(BasePermission):

    def __init__(self, resource, action):
        self.resource = resource
        self.action = action

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        user_roles = UserRole.objects.filter(user=user).values_list('role', flat=True)

        has_access = RolePermission.objects.filter(
            role__in=user_roles,
            permission__resource=self.resource,
            permission__action=self.action
        ).exists()

        return has_access