from rest_framework.response import Response
from rest_framework import status
from ..serializers import CircleSerializers, GossipSerializers
from django.contrib.auth.models import Permission, User
from rest_framework.permissions import IsAuthenticated
from users.models import Circle, CircleInfo, CirclePhoto, Status
from gossips.models import GossipsModel
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
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
        order_by = self.request.query_params.get("order_by", None)
        if order_by is not None:
            order_by = str(order_by).lower()
            if order_by == "most_followed":
                qs = sorted(qs, key=lambda x: x.followers.count(), reverse=True)
                return qs
                
            if order_by == "least_followed":
                qs = sorted(qs, key=lambda x: x.followers.count(), reverse=True)
                return qs
            
            msg = "Invalid Arguments for `order_by` only [`most_followed`, `least_followed`] are allowed..."
            raise ValidationError(msg)

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

    def update(self, *args, **kwargs):
        obj = self.get_object()
        curr_user = self.request.user
        if curr_user == obj.user:
            raise PermissionDenied("Invalid Request Provided...")
        
        prop = self.request.query_params.get("prop")
        data = {}
        if prop:
            prop = str(prop).lower()
            if prop == "follow":
                obj.followers.add(curr_user)
                data["detail"] = "Following " + str(obj.title)
            
            elif prop == "unfollow":
                obj.followers.remove(curr_user)
                data["detail"] = "Un-Following " + str(obj.title)

            elif prop == "check":
                qs = obj.followers.filter(username=curr_user.username)
                if qs.exists():
                    data["following"] = True
                    return Response(data, status=status.HTTP_200_OK)
                data["following"] = False
                return Response(data, status=status.HTTP_200_OK)
            
            else:
                raise ValidationError("Invalid Parameter for `prop` provided it can only accept [`follow`, `unfollow`, `check`]...")

            obj.save()
        
            return Response(data, status=status.HTTP_201_CREATED)

        raise PermissionDenied("no parameter `prop` provided...")


class GossipsForCircleListCreateAPIView(ListCreateAPIView):
    serializer_class = CircleSerializers.CircleGossipsSerializer
    permission_classes = [IsAuthenticated, permissions.TrueIfUserHaveACircle]

    def get_queryset(self):
        circle = self.get_circle()
        qs = circle.circle_gossips.all().order_by("-date_updated")
        return qs

    def get_circle(self):
        user = self.request.user
        circle = user.circle
        return circle

    def perform_create(self, serializer):
        circle = self.get_circle()
        serializer.save(circle=circle)


class GossipsForCircleListAPIView(ListAPIView):
    serializer_class = GossipSerializers.GossipListCreateSerializer
    permission_classes = [IsAuthenticated, ]    
    lookup_url_kwarg = "circle_slug"

    def get_circle(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_rest_404(Circle, slug=slug, msg="Circle With This slug donot exist...")
        return obj

    def get_queryset(self):
        circle = self.get_circle()
        qs = circle.circle_gossips.all().order_by("-date_updated")
        return qs
    

class StatusListCreateAPIView(ListCreateAPIView):
    serializer_class = CircleSerializers.StatusListCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        qs = Status.objects.none()
        created_by = self.request.query_params.get("created_by")
        if created_by:
            created_by = str(created_by).lower()
            if created_by == "circle":
                try:
                    circle = user.circle
                except ObjectDoesNotExist:
                    raise NotFound("User Do not have a Circle...")
                qs |= circle.circle_status.all()
                return qs

            elif created_by == "user":
                qs |= user.user_status.all()
            else:
                raise ValidationError("Invalid Argument to the Parameter `Created by` Provided...")
        if not qs.exists():
            qs = user.user_status.all()
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        created_by = self.request.query_params.get("created_by")
        if created_by:
            created_by = str(created_by).lower()
            if created_by == "circle":
                try:
                    circle = user.circle
                except ObjectDoesNotExist:
                    raise NotFound("User Do not have a Circle...")

                serializer.save(circle=circle)
                return

            elif created_by == "user":
                serializer.save(user=self.request.user)
                return

            raise ValidationError("Invalid Argument to the Parameter `Created by` Provided...")
        
        serializer.save(user=self.request.user)


class StatusUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CircleSerializers.StatusListCreateSerializer
    permission_classes = [IsAuthenticated, permissions.IsStatusOfCurrentUserOrReadOnly]
    lookup_url_kwarg = "status_slug"

    def get_object(self):
        self.modify_serializer()
        return self.get_status()

    def get_status(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        msg = "Status with this Slug do not Exist..."
        obj = get_object_or_rest_404(Status, slug=slug, msg=msg)
        return obj

    def modify_serializer(self):
        prop = self.request.query_params.get("props")
        if (prop is not None) and (prop == ""):
            prop = str(prop).lower()
            if prop == "image":
                self.serializer_class = CircleSerializers.StatusImageSerializer
                return

            raise ValidationError("Invalid Argument For `props` provided...")
