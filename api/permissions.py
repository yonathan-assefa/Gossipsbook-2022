from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsGossipOfCurrentUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsCommentOfCurrentUser(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        print("Object Permission")
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.author

