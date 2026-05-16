from django.urls import path, include
from accounts.views import Signup_view, LoginView, TokenRefreshView

urlpatterns = [
    path('register/', Signup_view.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),

    
]
