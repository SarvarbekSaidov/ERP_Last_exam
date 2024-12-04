from rest_framework.permissions import BasePermission

class IsAuthorOrAdminOrReadOnly(BasePermission):
    """
    Allow full access for admins and authors of the object, read-only for others.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'author') and obj.author == request.user:
            return True
        return request.method in ('GET', 'HEAD', 'OPTIONS')
