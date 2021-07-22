from django.contrib.auth.models import User
from rest_framework.generics import (
    ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, 
    RetrieveAPIView, 
)
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from gossips.models import GossipObjection, GossipsModel, Comments, Tags, Reply
from ..serializers import GossipSerializers
from ..pagination import Results20SetPagination
from .. import permissions
from rest_framework import serializers, status
from rest_framework.response import Response


def get_object_or_rest_404(klass, msg="NotFound", **kwargs):
    qs = klass.objects.filter(**kwargs)
    if qs.exists():
        return qs.get()

    raise NotFound(msg)


class GossipsListCreateAPIView(ListCreateAPIView):
    serializer_class = GossipSerializers.GossipListCreateSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = Results20SetPagination

    def get_queryset(self):
        qs = GossipsModel.objects.all()
        qs = self.filter_qs_by_parameter(qs)
        return qs

    def filter_qs_by_parameter(self, qs):
        sort = self.request.query_params.get("sort_by")
        if sort is not None:
            sort = str(sort).lower()
            if sort == "latest" or sort == "late" or sort == "newest" or sort == "new":
                qs = qs.order_by("-date_published", "-date_updated")

            elif sort == "oldest" or sort == "old":
                qs = qs.order_by("date_published", "date_updated")
            
            else:
                raise PermissionDenied("Improper sort Parameter Provided [latest, newest are the parameters]...")

        filter_title = self.request.query_params.get("title_contains")
        if filter_title is not None:
            filter_title = str(filter_title)
            qs = qs.filter(title__icontains=filter_title)
            if not qs.exists():
                raise NotFound("No Gossips has been Found Containing this Title...")

        filter_act_title = self.request.query_params.get("title")
        if filter_act_title is not None:
            filter_act_title = str(filter_act_title)
            qs = qs.filter(title=filter_act_title)
            if not qs.exists():
                raise NotFound("No Gossips has been Found with this Title...")

        user_username = self.request.query_params.get("username")
        if user_username is not None:
            user_username = str(user_username)
            user = get_object_or_rest_404(User, username=user_username, msg="Invalid Name for User Provided")
            qs = qs.filter(author=user)
            if not qs.exists():
                raise NotFound("No Gossips for this User has been Found...")
        
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)


class GossipUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GossipSerializers.GossipRetrieveSerializer
    lookup_url_kwarg = "gossip_slug"
    permission_classes = [IsAuthenticated, permissions.IsGossipOfCurrentUserOrReadOnly]

    def get_queryset(self):
        pass

    def get_object(self):
        gossip_obj = self.get_gossip()
        return gossip_obj

    def get_gossip(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_rest_404(GossipsModel, slug=slug)
        self.modify_serializer_by_parameter() 
        return obj

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        serializer = self.get_serializer(instance)
        data = serializer.data
        qs = instance.true.filter(username=user.username)

        if qs.exists():
            data["current_user_vote"] = True
            
        elif instance.false.filter(username=user.username).exists():
            data["current_user_vote"] = False

        if instance.gossipobjection_set.filter(user=user).exists():
            data["has_objected"] = True

        gossip_author = instance.author
        if user.user1_frnds.filter(user2=gossip_author).exists():
            data["is_friend"] = True

        elif user.user2_frnds.filter(user1=gossip_author).exists():
            data["is_friend"] = True

        return Response(data)

    def modify_serializer_by_parameter(self):
        prop = self.request.query_params.get("property")
        if prop is not None:
            prop = str(prop).lower()
            if prop == "image":
                self.serializer_class = GossipSerializers.GossipUpdateImageSerializer
                return self.serializer_class

            if prop == "provider":
                self.serializer_class = GossipSerializers.GossipUpdateProviderSerializer
                return self.serializer_class

            raise ValidationError("Illegal Property Provided it takes only [image, provider]")

    def perform_update(self, serializer):
        serializer.save()
        

class GossipsVoteAPIView(ListCreateAPIView):
    serializer_class = GossipSerializers.UserLeastInfoSerializer
    lookup_url_kwarg = "gossip_slug"
    permission_classes = [IsAuthenticated, ]
    pagination_class = Results20SetPagination

    def get_queryset(self):
        voted_type = self.request.query_params.get("voted")
        if voted_type is not None:
            gossip = self.get_gossips()
            voted_type = str(voted_type).lower()
            if voted_type == "up" or voted_type == "true" or voted_type == "voted_true":
                qs = gossip.true.all()
                return qs
            if voted_type == "false" or voted_type == "voted_false" or voted_type == "down":
                qs = gossip.false.all()
                return qs

            raise ValidationError("Illegal Voted-Type Provided parameters are [true or false]...")

        raise PermissionDenied("No Parameter voted is provided")

    def get_gossips(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_rest_404(GossipsModel, slug=slug)
        return obj

    def perform_create(self, serializer):
        curr_user = self.request.user
        voted_type = self.request.query_params.get("voted")
        gossip = self.get_gossips()
        if curr_user == gossip.author:
            raise PermissionDenied("User Cannot Vote his/her own Gossip...")

        if voted_type is not None:
            voted_type = str(voted_type).lower()
            if voted_type == "true" or voted_type == "voted_true":
                gossip.true.add(curr_user)
                gossip.false.remove(curr_user)
                gossip.save()
                return self.serializer_class(curr_user)
            
            if voted_type == "false" or voted_type == "voted_false":
                gossip.false.add(curr_user)
                gossip.true.remove(curr_user)
                gossip.save()
                return self.serializer_class(curr_user)
            
            raise ValidationError("voted-type can either be true or false")

        raise PermissionDenied("No voted-type provided...")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer
        serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GossipAddTagAPIView(ListCreateAPIView):
    serializer_class = GossipSerializers.TagSerializer
    lookup_url_kwarg = "gossip_slug"
    permission_classes = [IsAuthenticated, ]

    def get_gossip(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_rest_404(GossipsModel, slug=slug)
        return obj

    def get_queryset(self):
        gossip = self.get_gossip()
        qs = gossip.q_tags.all()
        return qs

    def perform_create(self, serializer):
        obj = serializer.data.get("title")
        print(obj)
        obj = get_object_or_rest_404(Tags, msg="Tag with this title is not Found...", title=obj)
        gossip = self.get_gossip()
        if not self.request.user == gossip.author:
            raise PermissionDenied("Current-User is not the User of this Gossip...")
            
        gossip.q_tags.add(obj)
        gossip.save()
        print("Saved")
        serializer = self.serializer_class
        return serializer(obj)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        serializer = self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = GossipSerializers.CommentSerializer
    lookup_url_kwarg = "gossip_slug"
    permission_classes = [IsAuthenticated, ]
    pagination_class = Results20SetPagination

    def get_queryset(self):
        gossip = self.get_gossip()
        qs = gossip.comments_set.all()
        return qs

    def get_gossip(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_rest_404(GossipsModel, slug=slug)
        return obj

    def perform_create(self, serializer):
        gossip = self.get_gossip()
        serializer.save(author=self.request.user, gossip=gossip)


class CommentRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GossipSerializers.CommentRetrieveSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "gossip_slug"
    comment_id = "cmnt_id"

    def get_queryset(self):
        pass

    def get_object(self):
        obj = self.get_comment_by_id()
        return obj

    def get_comment_by_id(self):
        cmnt_id = self.kwargs.get(self.comment_id)
        gossip = self.get_gossip()
        qs = gossip.comments_set.filter(id=cmnt_id)
        if qs.exists():
            return qs.get()

        raise NotFound("Invalid Comment ID Provided..")

    def get_gossip(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_rest_404(GossipsModel, slug=slug)
        return obj

    def update(self, request, *args, **kwargs):
        cmnt = self.get_object()
        if self.request.user != cmnt.author:
            raise PermissionDenied("Invalid User to Update Comment...")

        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        cmnt = self.get_object()
        if self.request.user != cmnt.author:
            raise PermissionDenied("Invalid User to Delete Comment...")

        return super().delete(request, *args, **kwargs)


class ReplyToCommentListCreateAPIView(ListCreateAPIView):
    serializer_class = GossipSerializers.ReplyListSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "comment_id"

    def get_comment(self):
        cmnt_id = self.kwargs.get(self.lookup_url_kwarg)
        comment = get_object_or_rest_404(Comments, id=cmnt_id, msg="Comment With This Id do not Exist...")
        return comment

    def get_queryset(self):
        comment = self.get_comment()
        replies = comment.replies.all()
        return replies

    def perform_create(self, serializer):
        comment = self.get_comment()
        serializer.save(user=self.request.user, comment=comment)


class ReplyRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GossipSerializers.ReplyRetrieveSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "reply_id"

    def get_reply(self):
        id_reply = self.kwargs.get(self.lookup_url_kwarg)
        reply_obj = get_object_or_rest_404(Reply, id=id_reply, msg="Reply With this Id do not Exists...")
        return reply_obj

    def get_object(self):
        obj = self.get_reply()
        return obj

    def update(self, *args, **kwargs):
        reply = self.get_reply()
        if reply.user == self.request.user:
            return super().update(*args, **kwargs)

        raise PermissionDenied("Current User Do not Permission to Update Other's Reply")

    def patch(self, *args, **kwargs):
        reply = self.get_reply()
        if reply.user == self.request.user:
            return super().patch(*args, **kwargs)

        raise PermissionDenied("Current User Do not Permission to Update Other's Reply")

    def delete(self, *args, **kwargs):
        reply = self.get_reply()
        if reply.user == self.request.user:
            return super().delete(*args, **kwargs)

        raise PermissionDenied("Current User Do not Permission to Update Other's Reply")


class GossipObjectionListCreateAPIView(ListCreateAPIView):
    serializer_class = GossipSerializers.GossipObjectionSerializer
    lookup_url_kwarg = "gossip_slug"

    def get_queryset(self):
        gossip = self.get_gossip()
        return gossip.gossipobjection_set.all()

    def perform_create(self, serializer):
        gossip = self.get_gossip()
        serializer.save(user=self.request.user, gossipsmodel=gossip)

    def get_gossip(self):
        gossip_slug = self.kwargs.get(self.lookup_url_kwarg)
        qs = GossipsModel.objects.filter(slug=gossip_slug)
        if qs.exists():
            print(qs)
            return qs.get()

        raise NotFound("Gossip with this Slug is not Found...")


class GossipObjectionRetrieveAPIView(ListCreateAPIView):
    serializer_class = GossipSerializers.GossipObjectionSerializer
    lookup_url_kwarg = "gossip_slug"

    def get_objections(self):
        gossip = self.get_gossip()
        qs = gossip.gossipobjection_set.filter(user=self.request.user)
        if qs.exists():
            return qs.get()

        raise NotFound("User did not Object this Gossip...")

    def get_gossip(self):
        gossip_slug = self.kwargs.get(self.lookup_url_kwarg)
        qs = GossipsModel.objects.filter(slug=gossip_slug)
        if qs.exists():
            return qs.get()

        raise NotFound("Gossip with this Slug is not Found...")

    def get_object(self):
        return self.get_objections()
