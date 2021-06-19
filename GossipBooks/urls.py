from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import get_token
# from messaging.views import conntect_websocket

urlpatterns = [
    path('gossips/', include('gossips.urls', namespace='gossips')),
    path('questions/', include('questions.urls', namespace='questions')),
    path('cheaters/', include('cheaters.urls', namespace='cheaters')),
    path('answers', include('answers.urls', namespace='answers')),
    path('users/', include('users.urls', namespace='users')),
    path('accounts/', include('allauth.urls')),
    path('search/', include('searches.urls', namespace='searches')),
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path("api/authentication/token/", get_token.CustomAuthToken.as_view(), ),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('', include('controls.urls', namespace='controls')),
    # path("room/<username>/", conntect_websocket, name="Websocket_name"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
