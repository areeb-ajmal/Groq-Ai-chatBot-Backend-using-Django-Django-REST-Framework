from django.urls import path, include
from analytics.views import MessageSummary, MostActiveUsers

urlpatterns = [
    path('summary/', MessageSummary.as_view(), name='Message-analytics'),
    path('top-users/',MostActiveUsers.as_view(), name='top-users-api' ),
    
    


]
