from django.db.models import fields
from django.utils import tree
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile, Interests, Qualification, WorkExperience, Friend, FriendRequest
from ..models import RestToken
from django.urls import reverse


def get_reverse_url(name, **kwargs):
    url = reverse(name, kwargs=kwargs)
    live = False
    
    if live:
        url = f"https://www.gossipsbook.com{url}"
        return url

    url = f"http://127.0.0.1:8000{url}"
    return url


class UserRegistrationSerializer(ModelSerializer):
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def validate_value(self, value):
        value = str(value)
        if "@" not in value:
            raise serializers.ValidationError("Please Provide a Correct Email...")

        return value

    def validate(self, data):
        if str(data["password1"]) != str(data["password2"]):
            print("Here..")
            raise serializers.ValidationError("The Two Password Field Did not Match...")
        
        email = data["email"]
        qs = User.objects.filter(email=email)
        if qs.exists():
            print("Ea Here...")
            raise serializers.ValidationError("Email Already exists...")

        return data


class OnlyUserSerializer(ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", ]


class PasswordChangeSerializer(ModelSerializer):
    prev_password = serializers.CharField()
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    class Meta:
        model = User
        fields = ["prev_password", "password", "password_confirm"]

    def validate(self, values):
        p1 = values["password"]
        p2 = values["password_confirm"]
        if not p1 == p2:
            raise serializers.ValidationError("Both the Passwords did not match")

        return values


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
    truth_speaking = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", 
                  "profile", "work_experiences", "qualifications", "truth_speaking"]

    def get_truth_speaking(self, serializer):
        qs = serializer.gossip_author.all()
        total = 0
        for i in qs:
            total += i.percent_true

        if total == 0:
            return None

        try:
            a = total / qs.count()
            return a
        except ZeroDivisionError:
            return None

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
    author_url = serializers.SerializerMethodField()
    gossips_list_url = serializers.SerializerMethodField(method_name="get_user_gossips")
    truth_speaking = serializers.SerializerMethodField()
    is_friend = serializers.CharField(default=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "profile", 
                        "gossips_list_url", "author_url", "truth_speaking", "is_friend"]


    def get_truth_speaking(self, serializer):
        qs = serializer.gossip_author.all()
        total = 0
        for i in qs:
            total += i.percent_true

        if total == 0:
            return None

        try:
            a = total / qs.count()
            return a
        except ZeroDivisionError:
            return None

    def get_user_gossips(self, serializer):
        url = f"https://www.gossipsbook.com/api/gossips/list-create/?username={serializer.username}"
        return url

    def get_author_url(self, serializer):
        return get_reverse_url("User-Retrieve", username=serializer.username)



class UserForGossipsSerializer(ModelSerializer):
    profile = UserProfileDisplaySerializer(read_only=True)
    author_url = serializers.SerializerMethodField()
    designation = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "profile", "author_url", "designation"]

    def get_author_url(self, serializer):
        return get_reverse_url("User-Retrieve", username=serializer.username)

    def get_designation(self, serializer):
        try:
            designation = serializer.profile.designation
            if (designation == "") or (designation == None):
                return None
            return designation
        except:
            return None

class RestTokenSerializer(ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = RestToken
        fields = ["token", "password"]

    def validate_token(self, value):
        qs = RestToken.objects.filter(token=value)
        if qs.exists():
            if not qs.filter(expired=False).exists():
                raise serializers.ValidationError("The Token has been Expired...")
                
            return value

        raise serializers.ValidationError("This is not a Valid Token...")


class UserEmailPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        print(value)
        qs = User.objects.filter(email=value)
        if qs.exists():
            return value

        raise serializers.ValidationError("No User is registered with this User...")


class UserWithProfileSerializer(ModelSerializer):
    profile = UserProfileImageSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "profile"]



class FriendsListSerializer(ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Friend
        fields = "__all__"


class FriendRequestListSerializer(ModelSerializer):
    sent_by_user = UserSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)
    accepted = serializers.BooleanField(read_only=True)

    class Meta:
        model = FriendRequest
        exclude = ["to_user", ]


class FriendRequestCreateSerializer(ModelSerializer):
    to_user = UserSerializer(read_only=True)
    sent_by_user = UserSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)
    accepted = serializers.BooleanField(read_only=True)

    class Meta:
        model = FriendRequest
        fields = "__all__"

