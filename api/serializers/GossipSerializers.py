from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from gossips.models import GossipsModel, Comments, Tags, Reply
from .UserSerializers import UserSerializer, UserLeastInfoSerializer


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
    author = UserSerializer(read_only=True)
    image = serializers.ImageField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    shares = serializers.IntegerField(read_only=True)
    percentage_true = serializers.SerializerMethodField()
    percentage_false = serializers.SerializerMethodField()

    class Meta:
        model = GossipsModel
        exclude = ["q_tags", "true", "false"]

    def get_percentage_true(self, serializer):
        return percentage_true(serializer)

    def get_percentage_false(self, serializer):
        return percentage_false(serializer)


class GossipRetrieveSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    image = serializers.ImageField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    shares = serializers.IntegerField(read_only=True)
    percentage_true = serializers.SerializerMethodField()
    percentage_false = serializers.SerializerMethodField()
    voted_true = serializers.SerializerMethodField()
    voted_false = serializers.SerializerMethodField()

    class Meta:
        model = GossipsModel
        exclude = ["q_tags", "true", "false"]

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

