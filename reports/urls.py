from django.urls import path, include
from reports.views import DailyReportView

urlpatterns = [
    path('daily/', DailyReportView.as_view(), name='Daily-report'),



]

