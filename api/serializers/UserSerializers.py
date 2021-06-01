from django.db.models import fields
from django.utils import tree
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile, Interests, Qualification, WorkExperience


class OnlyUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", ]


class InterestSerializer(ModelSerializer):

    class Meta:
        model = Interests
        fields = "__all__"


class InterestDisplaySerializer(ModelSerializer):

    class Meta:
        model = Interests
        exclude = ["id", "description"]


class UserQualificationSerializer(ModelSerializer):

    class Meta:
        model = Qualification
        exclude = ["id", "user"]


class UserWorkExperienceSerializer(ModelSerializer):

    class Meta:
        model = WorkExperience
        exclude = ["id", "user"]


class UserProfileRetrieveAllSerializer(ModelSerializer):
    user_interests = serializers.SerializerMethodField()
    user_followers = serializers.SerializerMethodField()
    user_followings = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        exclude = ["interests", "followers", "following", "id", "user"]

    def get_user_interests(self, serializer):
        qs = serializer.interests.all()
        serialized = InterestDisplaySerializer(qs, many=True)
        return serialized.data

    def get_user_followers(self, serializer):
        qs = serializer.followers.all()
        serialized = UserLeastInfoSerializer(qs, many=True)
        return serialized.data

    def get_user_followings(self, serializer):
        qs = serializer.following.all()
        serialized = UserLeastInfoSerializer(qs, many=True)
        return serialized.data

class UserInterestSerializer(ModelSerializer):
    title = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()

    class Meta:
        model = Interests
        fields = "__all__"


class UserLeastInfoSerializer(ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["username", ]


class UserRetrieveSerializer(ModelSerializer):
    profile = UserProfileRetrieveAllSerializer(read_only=True)
    work_experiences = UserWorkExperienceSerializer(read_only=True, many=True)
    qualifications = UserQualificationSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", 
                  "profile", "work_experiences", "qualifications"]


class UserProfileSerializer(ModelSerializer):
    user = OnlyUserSerializer(read_only=True)

    class Meta:
        model = Profile
        exclude = ["interests", "followers", "following", "image"]


class UserProfileImageSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ["image", ]


class UserProfileDisplaySerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ["bio", "image", ]


class UserSerializer(ModelSerializer):
    profile = UserProfileDisplaySerializer(read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "profile"]

