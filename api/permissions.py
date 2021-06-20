from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

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


class IsCurrentUserNotAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_authenticated


# Circle Permissions


class TrueIfUserHaveACircle(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        try:
            request.user.circle
        except ObjectDoesNotExist:
            raise PermissionDenied("User Do not have a Circle [].")

        return True


class TrueIfUserNotHaveACircle(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        try:
            request.user.circle
        except ObjectDoesNotExist:
            return True

        raise PermissionDenied("User Do not have a Circle [].")


class DoCircleBelongToCurrentUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.user
