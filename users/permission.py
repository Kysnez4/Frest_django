from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = 'You are moderator'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


class IsOwner(permissions.BasePermission):
    message = 'You are not the owner of this object'

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True

        return request.user == obj