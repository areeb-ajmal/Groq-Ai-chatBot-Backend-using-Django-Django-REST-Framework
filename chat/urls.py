from django.urls import path, include
from chat.views import ChatCreate, ChatDetailView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"conversations", ChatDetailView, basename="conversations")

urlpatterns = [
    path('send/', ChatCreate.as_view(), name='chat-api'),

]+router.urls


