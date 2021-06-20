from django.core import exceptions
from ..serializers import CircleSerializers
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from users.models import Circle, CircleInfo, CirclePhoto
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from django.core.exceptions import ObjectDoesNotExist
from .ControlsViews import get_object_or_rest_404
from .. import permissions


class CircleListCreateAPIView(ListCreateAPIView):
    """
    API-VIEW TO CREATE AND SHOW LIST OF CIRCLES OF USERS 
        AND 403 IF USER ALREADY HAS ONE...
    """

    permission_classes = [IsAuthenticated, permissions.TrueIfUserNotHaveACircle]
    serializer_class = CircleSerializers.CircleSerializer

    def get_queryset(self):
        qs = Circle.objects.all()
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        try:
            obj = user.circle
        except ObjectDoesNotExist:
            serializer.save(user=user)
            return serializer

        raise PermissionDenied(f"User already have a Circle named as {obj.title}")


class CurrentUserCircleRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.TrueIfUserHaveACircle]
    serializer_class = CircleSerializers.CurrentUserCircleSerializer

    def get_queryset(self):
        return 

    def get_object(self):
        try:
            obj = self.request.user.circle
        except ObjectDoesNotExist:
            raise NotFound("User do not have any Circle...")

        return obj


class CircleRetrieveAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, permissions.DoCircleBelongToCurrentUser]
    serializer_class = CircleSerializers.CurrentUserCircleSerializer
    lookup_url_kwarg = "circle_slug"

    def get_queryset(self):
        pass

    def get_object(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_rest_404(Circle, slug=slug, msg="Circle With this slug do not exists...")
        return obj
