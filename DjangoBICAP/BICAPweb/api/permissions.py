from rest_framework import permissions

class IsMobileOrStaffUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.username  == 'mobile' or request.user and request.user.is_staff) 

class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsStaffUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)