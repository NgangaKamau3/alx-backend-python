"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]
# Using Django rest framework DefaultRouter to automatically create the conversations and messages for your viewsets

# Navigate to the main project’s urls.py i.e messaging_app/urls.py and include your created routes with path as api
from django.urls import path, include
from rest_framework import routers
from chats.views import UserViewSet, ConversationViewSet, MessageViewSet, AuthViewSet
from rest_framework_nested import routers
# Initialize main router
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'messages', MessageViewSet, basename='message')
# Create nested router for messages under conversations
# This allows URLs like: /conversations/1/messages/
conversations_router = routers.NestedDefaultRouter(
    router, r'conversations', lookup='conversation'
)
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')
# URL patterns
urlpatterns = [
    # Include main router URLs
    path('', include(router.urls)),
    # Include nested router URLs for conversation messages
    path('', include(conversations_router.urls)),
    # Optional: Add DRF's browsable API authentication
    path('api-auth/', include('rest_framework.urls')),
]
# Optional: Add API versioning
urlpatterns = [
    path('v1/', include((urlpatterns, 'v1'), namespace='v1')),
]
