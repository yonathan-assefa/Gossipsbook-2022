from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


SAFE_METHODS_WITH_PUT = ("GET", "OPTIONS", "HEAD", "PUT", "PATCH")
SAFE_METHODS_WITH_POST = ("GET", "OPTIONS", "HEAD", "POST")
SAFE_METHODS_WITH_DELETE = ("GET", "OPTIONS", "HEAD", "DELETE")


class IsGossipOfCurrentUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        try:
            circle = user.circle
            if obj.circle == circle:
                return True

        except ObjectDoesNotExist:
            pass
        
        return obj.author == user


class IsStatusOfCurrentUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        try:
            circle = user.circle
            if obj.circle == circle:
                return True

        except ObjectDoesNotExist:
            pass
        
        return obj.user == user


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


class DoesObjectToBelongCurrentUser(BasePermission):
    """
    This Permission is used for the permissions to update
                        Qualifications and Work-Experience...
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


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
        if request.method in SAFE_METHODS_WITH_PUT:
            return True

        return request.user == obj.user



class FriendRequestUpdatePermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user == obj.sent_by_user:
            return request.method in SAFE_METHODS_WITH_DELETE

        elif request.user == obj.to_user:
            return request.method in SAFE_METHODS_WITH_PUT

        return False

