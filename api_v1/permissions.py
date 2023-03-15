from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('DELETE', 'PUT', 'POST', 'PATCH'):
            return request.user == obj.author
        return True

