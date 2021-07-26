from users.models import Circle
from django.contrib.auth.models import User
from django.urls import path, include
from django.conf.urls import url
from .views import GossipViews, ControlsViews, UserViews, CircleViews
from messaging.views import (RoomMessagesListAPIView, RoomListAPIView, NotificationsListAPIView,
                            NotificationRetrieveAPIView, UserRoomListAPIView, UserChattingRoomAPIView)

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
    path("gossips/objections/<gossip_slug>/", GossipViews.GossipObjectionListCreateAPIView.as_view(), ),
    path("gossips/objections/<gossip_slug>/user/retrieve/", GossipViews.GossipObjectionRetrieveAPIView.as_view(), ),

    path("false-info/gossip/", ControlsViews.FalseInformationListAPIView.as_view()),
    path("false-info/gossip/<gossip_slug>/", ControlsViews.FalseInformationCreateAPIView.as_view(), ),
    path("false-info/<false_id>/retrieve/", ControlsViews.FalseInformationRetrieveAPIView.as_view()),
    path("request-to-remove/user/", ControlsViews.RFRModelListAPIView.as_view(), ),
    path("request-to-remove/user/gossip/<gossip_slug>/", ControlsViews.RFRModelCreateAPIView.as_view(), ),
    path("request-to-remove/user/retrieve/<rfr_model_id>/", ControlsViews.RFRModelRetrieveAPIView.as_view(), ),
    path("feedback/list-create/", ControlsViews.FeedbackListCreateAPIView.as_view(), ),
    path("feedback/retrieve/<feedback_id>/", ControlsViews.FeedbackRetrieveAPIView.as_view(), ),

    path("user/auth/registration/", UserViews.UserRegistrationView.as_view(), ),
    path("user/auth/password-change/", UserViews.PasswordChangeAPIView.as_view(), ),
    path("user/auth/password-reset/", UserViews.UserSendMailGeneratorAPIView.as_view(), ),
    path("user/auth/password-reset/confirm-token/", UserViews.UserTokenConfirmAPIView.as_view(), ),

    path("current-user/profile/retrieve/", UserViews.CurrentUserProfileRetrieveAPIView.as_view(), ),
    path("current-user/profile/update/", UserViews.CurrentUserProfileUpdateAPIView.as_view(), ),
    path("user/retrieve/<username>/", UserViews.UserRetrieveAndUpdatePropertyAPIView.as_view(), name="User-Retrieve"),
    path("current-user/feed/", UserViews.CurrentUserFeedListAPIView.as_view(), ),
    path("current-user/Interests/list-create/", UserViews.CurrentUserProfileAddInterestAPIView.as_view(), ),

    path("current-user/profile/experiences/", UserViews.UserProfileWorkExperienceListCreateAPIView.as_view(), ),
    path("current-user/profile/experiences/<experience_id>/", UserViews.handle_user_work_experience_object, ),
    path("current-user/profile/qualifications/", UserViews.UserProfileQualificationListCreateAPIView.as_view(), ),
    path("current-user/profile/qualifications/<qualification_id>/", UserViews.handle_qualification_object, ),

    path("current-user/circle/update/", CircleViews.CurrentUserCircleRetrieveAPIView.as_view(), ),

    path("current-user/friends/list/", UserViews.FriendListAPIView.as_view(), ),
    path("current-user/friend-request/list/", UserViews.FriendRequestListAPIView.as_view(), ),
    path("current-user/friend-request/create/<username>/", UserViews.FriendRequestCreateAPIView.as_view(), ),
    path("current-user/friend-request/list/update/<username>/", UserViews.FriendRequestUpdateAPIView.as_view(), ),
    path("user/friend-suggestion/", UserViews.FriendSuggestionListAPIView.as_view(), ),
    path("interest/list/", UserViews.InterestListAPIView.as_view(), ),

    path("circle/list-create/", CircleViews.CircleListCreateAPIView.as_view(), name="Circle-List"),
    path("circle/retrieve/<circle_slug>/", CircleViews.CircleRetrieveAPIView.as_view(), name="Circle-Retrieve"),
    path("circle/<circle_slug>/gossips/list/", CircleViews.GossipsForCircleListAPIView.as_view(), name="Circle-Gossips-List"),
    path("current-user/circle/gossips/list-create/", CircleViews.GossipsForCircleListCreateAPIView.as_view(), ),

    path("status/list-create/", CircleViews.StatusListCreateAPIView.as_view()),
    path("current-user/status/feed/", CircleViews.CurrentUserStatusFeed.as_view(), ),
    path("status/update/<status_slug>/", CircleViews.StatusUpdateAPIView.as_view(), ),

    path("room/<username>/", RoomMessagesListAPIView.as_view(), ),
    path("room/", RoomListAPIView.as_view(), ),
    path("user/room/", UserChattingRoomAPIView.as_view(), ),
    path("notifications/", NotificationsListAPIView.as_view(), ),
    path("notifications/<not_id>/", NotificationRetrieveAPIView.as_view(), )
]
