from rest_framework.serializers import Serializer
from messaging import serializers
from rest_framework.generics import (
    ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, 
    RetrieveAPIView, 
)
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.models import Interests, Profile, Qualification, WorkExperience, FriendRequest, Friend
from gossips.models import GossipsModel
from django.contrib.auth.models import User
from ..serializers import UserSerializers, GossipSerializers
from rest_framework import status
from rest_framework.response import Response
from .. import pagination
from .. import permissions
from ..models import RestToken
from smtplib import SMTPAuthenticationError


def get_object_or_rest_404(klass, msg="NotFound", **kwargs):
    qs = klass.objects.filter(**kwargs)
    if qs.exists():
        return qs.get()

    raise NotFound(msg)


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializers.UserRegistrationSerializer
    permission_classes = [permissions.IsCurrentUserNotAuthenticated, ]

    def get_queryset(self):
        pass

    def perform_create(self, serializer):
        try:
            valid_data = serializer.validated_data
        except:
            raise ValidationError("Illegal Data Provided...")

        username = valid_data.get("username")
        email = valid_data.get("email")
        password1 = valid_data.get("password1")
        password2 = valid_data.get("password2")

        if str(password1) != str(password2):
            raise ValidationError("The Two Password Field did not Match...")

        user_obj = User(username=username, email=email)
        user_obj.set_password(password2)
        user_obj.save()
        serializer = UserSerializers.OnlyUserSerializer(user_obj)
        return serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class CurrentUserProfileUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializers.UserProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        pass

    def modify_serializer_by_parameter(self):
        param = self.request.query_params.get("fields")
        if param is not None:
            param = str(param).lower()
            if param == "image":
                self.serializer_class = UserSerializers.UserProfileImageSerializer
                return True

            raise ValidationError("only [image, ] can be found in fields...")

        return False

    def get_object(self):
        user = self.request.user
        self.modify_serializer_by_parameter()
        return user.profile


class CurrentUserProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializers.UserRetrieveSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        pass

    def get_object(self):
        return self.request.user


class CurrentUserFeedListAPIView(ListAPIView):
    serializer_class = GossipSerializers.GossipListCreateSerializer
    pagination_class = pagination.Results20SetPagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        qs = self.get_followers_feed_ordered()
        return qs

    def get_followers_feed_ordered(self):
        user_profile = self.request.user.profile
        following_qs = user_profile.following.all()
        qs = GossipsModel.objects.none()
        for following_user in following_qs:
            qs |= following_user.gossip_author.all()
        
        return qs.order_by("-date_published", "-date_updated")


class UserProfileWorkExperienceListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializers.UserWorkExperienceSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = pagination.Results10SetPagination

    def get_queryset(self):
        user = self.request.user
        qs = user.work_experiences.order_by("-date_created")
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileQualificationListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializers.UserQualificationSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = pagination.Results10SetPagination

    def get_queryset(self):
        user = self.request.user
        qs = user.qualifications.order_by("-date_created")
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserRetrieveAndUpdatePropertyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializers.UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    lookup_url_kwarg = "username"

    def get_queryset(self):
        pass

    def get_object(self):
        return self.get_user_profile().user

    def get_user_profile(self):
        username = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_rest_404(User, username=username)
        return obj.profile

    def perform_update(self, serializer, flw_type=None):
        if flw_type is not None:
            user = self.get_user_profile()
            if user.user == self.request.user:
                raise PermissionDenied("User Cannot Follow or Unfollow Itself...")
            if flw_type == "unfollow":
                user.followers.remove(self.request.user)
            elif flw_type == "follow":
                user.followers.add(self.request.user)

            user.save()
            return serializer(user.user)

        serializer.save()

    def now_update(self, flw_type):
        serializer = self.get_serializer
        serializer = self.perform_update(serializer, flw_type)
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        prop = self.request.query_params.get("prop")
        if prop is not None:
            prop = str(prop).lower()
            if prop == "follow":
                return self.now_update(flw_type="follow")
            elif prop == "unfollow":
                return self.now_update(flw_type="unfollow")
            else:
                raise ValidationError("Prop can be only Follow or Unfollow...")
        
        raise PermissionDenied("Current User is not able to update it...")


class InterestListAPIView(ListAPIView):
    serializer_class = UserSerializers.InterestSerializer
    pagination_class = pagination.Results20SetPagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        qs = Interests.objects.all()
        return qs


class CurrentUserProfileAddInterestAPIView(ListCreateAPIView):
    serializer_class = UserSerializers.UserInterestSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = pagination.Results10SetPagination

    def get_current_profile(self):
        return self.request.user.profile

    def get_queryset(self):
        profile = self.get_current_profile()
        qs = profile.interests.all()
        return qs

    def perform_create(self, serializer):
        interest = self.request.query_params.get("interest")
        if interest is not None:
            interest = str(interest)
            obj = get_object_or_rest_404(Interests, msg="Bad Interest Provided...", title=interest)
            profile = self.get_current_profile()
            rmv = str(self.request.query_params.get("remove")).lower()
            
            if rmv == "true":
                profile.interests.remove(obj)
            else:
                profile.interests.add(obj)
            profile.save()
            return serializer(obj)

        raise PermissionDenied("No interest Provided...")
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer
        serializer = self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserSendMailGeneratorAPIView(CreateAPIView):
    serializer_class = UserSerializers.UserEmailPasswordResetSerializer

    def get_queryset(self):
        pass

    def perform_create(self, serializer):
        data = serializer.validated_data
        email = data.get("email")
        try:
            user_obj = User.objects.get(email=email)
            token = RestToken.objects.create(user=user_obj) 
        except SMTPAuthenticationError:
            raise ValidationError("The Authentication Credentials for sending email is not Valid...")
        except:
            raise ValidationError("Something Went Wrong While Sending mail...")

        return token

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'An Email Has been sent',
        }
        return Response(response)


class UserTokenConfirmAPIView(CreateAPIView):
    serializer_class = UserSerializers.RestTokenSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data
        token = data.get("token")
        password = data.get("password")
        token_obj = RestToken.objects.get(token=token)
        user = token_obj.user
        user.set_password(password)
        print(user)
        user.save()
        token_obj.expired = True
        token_obj.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'The Password Has been Set...',
        }
        return Response(response)


class FriendListAPIView(ListAPIView):
    serializer_class = UserSerializers.FriendsListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        u1 = self.request.user
        qs = Friend.objects.none()
        qs |= u1.user1_frnds.all()
        qs |= u1.user2_frnds.all()

        return qs


class FriendRequestListAPIView(ListAPIView):
    serializer_class = UserSerializers.FriendRequestListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        u1 = self.request.user
        qs = u1.friend_requested.all() 

        return qs


class FriendRequestCreateAPIView(CreateAPIView):
    serializer_class = UserSerializers.FriendRequestCreateSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "username"

    def get_other_user(self):
        username = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_rest_404(User, username=username, msg="User with this Name is not Found...")
        return obj

    def perform_create(self, serializer):
        username1 = self.kwargs.get(self.lookup_url_kwarg)
        username2 = self.request.user.username
        filt_qs = FriendRequest.objects.filter_friend_request(user1_username=username1, user2_username=username2)
        if filt_qs is None:
            user2 = User.objects.get(username=username1)
            serializer.save(sent_by_user=self.request.user, to_user=user2)
            return serializer

        if filt_qs.to_user == self.request.user:
            raise PermissionDenied("The User has already sent a Friend Request to you...")

        raise PermissionDenied("You already sent a Friend Request to him/her...")
        

    def create(self, request, *args, **kwargs):
        self.get_other_user()
        return super().create(request, *args, **kwargs)


class FriendRequestUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializers.FriendRequestListSerializer
    permission_classes = [IsAuthenticated, permissions.FriendRequestUpdatePermission]
    lookup_url_kwarg = "username"

    def get_user(self):
        username = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_rest_404(User, username=username, msg="User with this Username is not Found")
        return obj

    def get_object(self):
        other_user = self.get_user()
        user = self.request.user
        qs = user.friend_requested.filter(sent_by_user=other_user).filter(accepted=False)
        if qs.exists():
            return qs.get()

        raise NotFound("This User did not send a friend request")

    def perform_update(self, serializer):
        serializer.save(accepted=True)

    def update(self, request, *args, **kwargs):
        request_prop = self.request.query_params.get("request")
        if request_prop is not None:
            request_prop = str(request_prop).lower()
            if request_prop == "accepted":
                return super().update(request, *args, **kwargs)

            elif request_prop == "rejected":
                return super().delete(request, *args, **kwargs)

            raise PermissionDenied("request can have arguments of [`accepted`, `rejected`]...")
        raise PermissionDenied("No query parameter of request is provided...")