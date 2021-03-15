from rest_framework import permissions


class ReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
