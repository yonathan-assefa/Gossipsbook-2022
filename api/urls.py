from django.contrib.auth.models import User
from django.urls import path, include
from django.conf.urls import url
from .views import GossipViews, ControlsViews, UserViews

urlpatterns = [
    path("authentication/", include("rest_framework.urls")),
    path("gossips/list-create/", GossipViews.GossipsListCreateAPIView.as_view(), name="Gossip-List-Create"),
    path("gossips/update/<gossip_slug>/", GossipViews.GossipUpdateAPIView.as_view(), name="Gossip-Update"),
    path("gossips/<gossip_slug>/user/vote/", GossipViews.GossipsVoteAPIView.as_view(), name="Gossips-Vote"),
    path("gossips/<gossip_slug>/comment/list-create/", GossipViews.CommentListCreateAPIView.as_view(), name="Comment-Gossip"),
    path("gossips/<gossip_slug>/comment/retrieve/<cmnt_id>/", GossipViews.CommentRetrieveAPIView.as_view(), name="Comment-Retrieve"),
    path("gossips/<gossip_slug>/tags/list-create/", GossipViews.GossipAddTagAPIView.as_view(), ),
    path("gossips/comments/<comment_id>/replies/list-create/", GossipViews.ReplyToCommentListCreateAPIView.as_view(), ),
    path("gossips/replies/<reply_id>/update-retrieve/", GossipViews.ReplyRetrieveAPIView.as_view(), ),

    path("false-info/gossip/<gossip_slug>/", ControlsViews.FalseInformationListCreateAPIView.as_view()),
    path("false-info/<false_id>/retrieve/", ControlsViews.FalseInformationRetrieveAPIView.as_view()),
    path("request-to-remove/user/", ControlsViews.RFRModelListCreateAPIView.as_view(), ),
    path("request-to-remove/user/retrieve/<rfr_model_id>/", ControlsViews.RFRModelRetrieveAPIView.as_view(), ),
    path("feedback/list-create/", ControlsViews.FeedbackListCreateAPIView.as_view(), ),
    path("feedback/retrieve/<feedback_id>/", ControlsViews.FeedbackRetrieveAPIView.as_view(), ),

    path("user/auth/registration/", UserViews.UserRegistrationView.as_view(), ),
    path("user/auth/password-reset/", UserViews.UserSendMailGeneratorAPIView.as_view(), ),
    path("user/auth/password-reset/confirm-token/", UserViews.UserTokenConfirmAPIView.as_view(), ),

    path("current-user/profile/retrieve/", UserViews.CurrentUserProfileRetrieveAPIView.as_view(), ),
    path("current-user/profile/update/", UserViews.CurrentUserProfileUpdateAPIView.as_view(), ),
    path("user/retrieve/<username>/", UserViews.UserRetrieveAndUpdatePropertyAPIView.as_view(), ),
    path("current-user/feed/", UserViews.CurrentUserFeedListAPIView.as_view(), ),
    path("current-user/Interests/list-create/", UserViews.CurrentUserProfileAddInterestAPIView.as_view(), ),
    path("current-user/profile/experiences/", UserViews.UserProfileWorkExperienceListCreateAPIView.as_view(), ),
    path("current-user/profile/qualifications/", UserViews.UserProfileQualificationListCreateAPIView.as_view(), ),
    
    path("interest/list/", UserViews.InterestListAPIView.as_view(), ),

]
