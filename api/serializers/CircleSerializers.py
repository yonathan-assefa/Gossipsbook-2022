from users.models import Circle, CircleInfo, CirclePhoto, Status
from gossips.models import GossipsModel
from ..serializers.UserSerializers import OnlyUserSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
# from .GossipSerializers import get_reverse_url
from django.urls import reverse

def get_reverse_url(name, **kwargs):
    url = reverse(name, kwargs=kwargs)
    live = False
    
    if live:
        url = f"https://www.gossipsbook.com{url}"
        return url

    url = f"http://127.0.0.1:8000{url}"
    return url

class CircleSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Circle
        fields = "__all__"

    def get_followers(self, serializer):
        followers_qs = serializer.followers.all()[:3]
        ser = OnlyUserSerializer(followers_qs, many=True)
        return ser.data


class CircleInfoSerializer(ModelSerializer):
    circle = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CircleInfo
        fields = "__all__"


class CirclePhotoSerializer(ModelSerializer):
    circle = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CirclePhoto
        fields = "__all__"


class CircleForGossipSerializer(ModelSerializer):
    picture = CirclePhotoSerializer(read_only=True)
    circle_url = serializers.SerializerMethodField()

    class Meta:
        model = Circle
        fields = ["user", "title", "slug", "circle_url", "date_created", "picture"]

    def get_circle_url(self, serializer):
        return get_reverse_url("Circle-Retrieve", circle_slug=serializer.slug)


class CurrentUserCircleSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    info = CircleInfoSerializer(read_only=True)
    picture = CirclePhotoSerializer(read_only=True)

    class Meta:
        model = Circle
        fields = "__all__"


class CircleGossipsSerializer(ModelSerializer):
    circle = CurrentUserCircleSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)
    shares = serializers.ReadOnlyField()

    class Meta:
        model = GossipsModel
        exclude = ["author", "q_tags", "true", "false", "image", ]


class StatusListCreateSerializer(ModelSerializer):
    circle = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Status
        fields = "__all__"


class StatusImageSerializer(ModelSerializer):

    class Meta:
        model = Status
        fields = ["image", ]
