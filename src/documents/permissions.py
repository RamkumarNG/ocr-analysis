from rest_framework import permissions

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'destroy':
            return False

        return True
    
