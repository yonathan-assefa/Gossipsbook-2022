from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from gossips.models import GossipsModel, Comments, Tags, Reply
from .UserSerializers import UserSerializer, UserLeastInfoSerializer, UserForGossipsSerializer
from .CircleSerializers import CircleForGossipSerializer
from django.urls import reverse
import random


def get_reverse_url(name, **kwargs):
    url = reverse(name, kwargs=kwargs)
    live = True
    
    if live:
        url = f"https://www.gossipsbook.com{url}"
        return url

    url = f"http://127.0.0.1:8000{url}"
    return url


def percentage_true(serializer):
    true_voted = serializer.true.count()
    false_voted = serializer.false.count()
    total = true_voted + false_voted
    try:
        data = (true_voted / total) * 100
    except ZeroDivisionError:
        data = None

    return data

def percentage_false(serializer):
    true_voted = serializer.true.count()
    false_voted = serializer.false.count()
    total = true_voted + false_voted
    try:
        data = (false_voted / total) * 100
    except ZeroDivisionError:
        data = None

    return data


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tags
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    gossip = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = "__all__"


class GossipListCreateSerializer(ModelSerializer):
    """ 
    Serializer For ListView and CreateView of the API...
    """
    author = UserForGossipsSerializer(read_only=True)
    circle = CircleForGossipSerializer(read_only=True)
    image = serializers.ImageField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    gossip_url = serializers.SerializerMethodField()
    gossip_comments_list_url = serializers.SerializerMethodField()
    shares = serializers.IntegerField(read_only=True)
    percentage_true = serializers.SerializerMethodField()
    percentage_false = serializers.SerializerMethodField()
    footer_comments = serializers.SerializerMethodField()
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = GossipsModel
        exclude = ["q_tags", "true", "false",]

    def get_percentage_true(self, serializer):
        return percentage_true(serializer)

    def get_total_votes(self, serializer):
        return int(serializer.true.count()) + int(serializer.false.count())

    def get_percentage_false(self, serializer):
        return percentage_false(serializer)

    def get_gossip_url(self, serializer):
        return get_reverse_url("Gossip-Update", gossip_slug=serializer.slug)

    def get_gossip_comments_list_url(self, serializer):

        return get_reverse_url("Comment-Gossip", gossip_slug=serializer.slug)

    def get_footer_comments(self, serializer):
        qs = serializer.comments_set.all()
        try:
            user = random.choice(qs).author
        except IndexError:
            return None

        statement = f"{user.username} and {qs.count()-1} has commented on it"
        return statement



class GossipRetrieveSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    circle = serializers.StringRelatedField(read_only=True)
    image = serializers.ImageField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    shares = serializers.IntegerField(read_only=True)
    percentage_true = serializers.SerializerMethodField()
    percentage_false = serializers.SerializerMethodField()
    voted_true = serializers.SerializerMethodField()
    voted_false = serializers.SerializerMethodField()
    comments_url = serializers.SerializerMethodField()

    class Meta:
        model = GossipsModel
        exclude = ["q_tags", "true", "false", ]

    def get_comments_url(self, serializer):

        return get_reverse_url("Comment-Gossip", gossip_slug=serializer.slug)

    def get_percentage_true(self, serializer):
        return percentage_true(serializer)

    def get_percentage_false(self, serializer):
        return percentage_false(serializer)

    def get_voted_true(self, serializer):
        qs = serializer.true.all()
        ser = UserLeastInfoSerializer(qs, many=True)
        return ser.data

    def get_voted_false(self, serializer):
        qs = serializer.false.all()
        ser = UserLeastInfoSerializer(qs, many=True)
        return ser.data
        

class GossipUpdateProviderSerializer(ModelSerializer):

    class Meta:
        model = GossipsModel
        fields = ["from_question_user", "from_question_answer_provider"]


class GossipUpdateImageSerializer(ModelSerializer):

    class Meta:
        model = GossipsModel
        fields = ["image", ]


class CommentRetrieveSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    gossip = GossipListCreateSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = "__all__"


class ReplyListSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reply
        exclude = ["comment", ]


class ReplyRetrieveSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = "__all__"

