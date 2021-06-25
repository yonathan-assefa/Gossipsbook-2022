from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ChatingRoom
from api.views.GossipViews import get_object_or_rest_404
from api.serializers.UserSerializers import UserWithProfileSerializer
from .serializers import ChatingRoomMessageListSerializer


@login_required
def conntect_websocket(request, username):
    print(request.user)
    user_obj = get_object_or_404(User, username=username)
    context = {
        "user_chating_with": user_obj,
    }
    return render(request, "chating.html", context)


class RoomMessagesListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChatingRoomMessageListSerializer
    lookup_url_kwarg = "username"

    def get_user_by_username(self):
        username = self.kwargs.get(self.lookup_url_kwarg)
        user = get_object_or_rest_404(User, username=username, msg="User with this Username is not Found...")
        if self.request.user == user:
            raise PermissionDenied("Room with own-self is defined...")

        return user

    def get_queryset(self):
        get_user = self.get_user_by_username()
        obj = ChatingRoom.objects.filter_room(get_user.username, self.request.user.username)
        if obj is None:
            raise NotFound("No Room Exists with this User...")

        qs = obj.ch_messages.all()
        return qs


class RoomListAPIView(ListAPIView):
    serializer_class = UserWithProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get_chating_room_qs(self):
        user = self.request.user
        qs = ChatingRoom.objects.none()
        qs |= user.user1_chating_room.all()
        qs |= user.user2_chating_room.all()
        return qs

    def get_user_values(self):
        qs = self.get_chating_room_qs()
        lst = []
        for i in range(1, 2):
            new_qs = qs.values_list(f"user{i}", flat=True).distinct()
            if new_qs.exists():
                lst.append(new_qs[0])
        try:
            lst.remove(self.request.user.id)
        except ValueError:
            pass

        return lst

    def get_queryset(self):
        user_values = self.get_user_values()
        qs = User.objects.none()
        for i in user_values:
            qs |= User.objects.filter(id=i)

        return qs