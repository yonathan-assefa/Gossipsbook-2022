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
from django.contrib.auth import authenticate


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


class PasswordChangeAPIView(CreateAPIView):
    serializer_class = UserSerializers.PasswordChangeSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        data = serializer.data
        print(data)
        password = data["prev_password"]
        username = self.request.user
        user = authenticate(username=username, password=password)
        if user:
            passcode_new = data["password_confirm"]
            user.set_password(passcode_new)
            user.save()
            return user
        
        raise PermissionDenied("Your Previous Password did not match...")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {
            "status": "ok",
            "changed": True
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)



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

            if param == "core":
                self.serializer_class = UserSerializers.OnlyUserSerializer
                return True

            raise ValidationError("only [image, ] can be found in fields...")

        return False

    def get_object(self):
        user = self.request.user
        if self.modify_serializer_by_parameter():
            return user
            
        return user.profile

    def update(self, request, *args, **kwargs):
        self.modify_serializer_by_parameter()

        return super().update(request, *args, **kwargs)


class CurrentUserProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializers.UserRetrieveSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        pass

    def get_object(self):
        return self.request.user


class CurrentUserFeedListAPIView(ListAPIView):
    serializer_class = GossipSerializers.GossipListCreateSerializer
    # pagination_class = pagination.Results20SetPagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        qs = self.get_user_feeds_orderly_arranged()
        return qs

    def get_user_feeds_orderly_arranged(self):
        qs = GossipsModel.objects.none()
        curr_user = self.request.user
        
        frnd_qs = Friend.objects.none()
        frnd_qs |= curr_user.user1_frnds.all()
        frnd_qs |= curr_user.user2_frnds.all()

        users_list = []
        for i in frnd_qs:
            user1 = i.user1
            user2 = i.user2
            if user1 == curr_user:
                users_list.append(user2)
            else:
                users_list.append(user1)

        for i in users_list:
            qs |= i.gossip_author.all()

        # circle_qs = curr_user.user_circle_followers.all()
        # for i in circle_qs:
        #     qs |= i.circle_gossips.all()

        return qs.order_by("-date_published", "-date_updated")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            print(page)
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            count = 0
            curr_user = self.request.user.username
            for i in data:
                gossip = page[count]
                print(gossip)
                qs = gossip.true.filter(username=curr_user)
                if qs.exists():
                    print(True)
                    i["user_vote"] = True
                elif gossip.false.filter(username=curr_user).exists():
                    print(False)
                    i["user_vote"] = False
                else:
                    print(None)
                    i["user_vote"] = None
                print()
                count += 1
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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

    def is_friend(self, user_obj):
        curr_user = self.request.user
        if user_obj == curr_user:
            return None

        qs = curr_user.user1_frnds.filter(user2=user_obj)
        if qs.exists():
            return True

        qs = curr_user.user2_frnds.filter(user1=user_obj)
        if qs.exists():
            return True

        return False

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data["is_friend"] = self.is_friend(instance)
        return Response(data)

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
        qs = FriendRequest.objects.filter_friend_request(user.username, other_user.username)
        if qs is not None:
            return qs

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