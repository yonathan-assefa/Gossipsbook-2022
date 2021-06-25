from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from controls.models import FalseInformation, RFRModel, FeedbackModel
from .UserSerializers import UserSerializer, UserProfileDisplaySerializer
from .GossipSerializers import GossipListCreateSerializer


class FalseInformationListSerializer(ModelSerializer):
    gossip = GossipListCreateSerializer(read_only=True)

    class Meta:
        model = FalseInformation
        fields = "__all__"


class RFRModelSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    gossip = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = RFRModel
        fields = "__all__"


class FeedbackModelSerializer(ModelSerializer):

    class Meta:
        model = FeedbackModel
        fields = "__all__"

