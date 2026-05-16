from django.shortcuts import render
from rest_framework.views import APIView
from chat.models import DailyReport
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.cache import cache

# Create your views here.


class DailyReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        cache_key = 'daily_report'
        cache_data = cache.get(cache_key)


        if cache_data:
            return Response(cache_data)
        else:
            report = DailyReport.objects.order_by('-date')[:30]
            data = [
                {
                    "date" : str(r.date),
                    "total_messages" : r.total_messages,
                    "active_users" : r.active_users,
                    "avg_ai_response" : r.avg_ai_response,
                    "report_data" : r.report_data,
                    "generated_at" : r.generated_at
                }
                for r in report
            ]

            cache.set(cache_key, data, timeout=60 * 5)

            return Response(data)
