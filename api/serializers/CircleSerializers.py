from users.models import Circle, CircleInfo, CirclePhoto
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class CircleSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Circle
        fields = "__all__"


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


class CurrentUserCircleSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    info = CircleInfoSerializer(read_only=True)
    picture = CirclePhotoSerializer(read_only=True)

    class Meta:
        model = Circle
        fields = "__all__"
