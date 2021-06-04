"""GossipBooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import get_token

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)