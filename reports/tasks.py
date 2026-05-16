from chat.models import DailyReport
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from chat.models import Message, DailyReport
import logging
from django.contrib.auth import get_user_model
from django.db.models import Avg,Count

logger = logging.getLogger(__name__)
user = get_user_model()

@shared_task(name='reports.tasks.genrate_daily_report', bind=True, max_retries=3)
def genrate_daily_report(self):

    try:
        today = timezone.now().date()
        yesterday = today 

        logger.info(f"[genrate_daily_report] Generating daily report for {yesterday}" )

        # Day Before messages
        message_queue = Message.objects.filter(created_at__date=yesterday)

        # Count yesterdays all messages to generate the report of the day 
        total_messages = message_queue.count()

        #Active users 
        active_users = message_queue.filter(role='user').values('conversation__user').distinct()

        # Average of response time of Ai  of all yesterdays messages 
        avg_response = message_queue.filter(role='assistant', response_time__isnull=False).aggregate(avg_time=Avg('response_time'))
        ai_avg_response_time = round(avg_response['avg_time'] or 0.0, 2)

        per_user_state = message_queue.filter(role='user').values('conversation__user__username').annotate(msg_count=Count('id')).order_by('-msg_count')

        report_data = {
            "Date" : str(yesterday),
            "Top_users" : list(per_user_state),
            "AI_messages" : message_queue.filter(role='assistant').count(),
            "User_messages" : message_queue.filter(role='user').count(),
        }

        report, created = DailyReport.objects.update_or_create(
            date=yesterday,
            defaults={
                'total_messages': total_messages,
                'active_users': active_users,
                'avg_ai_response': ai_avg_response_time,
                'report_data': report_data,
            }
        )

        status = 'Created' if created else 'Updated'
        logger.info(f"[generate_daily_report] {status} report for {yesterday} ✓")
        logger.info(f"[generate_daily_report] {list(message_queue.values())}")
        return {
            "Status" : "Success",
            "date" : str(yesterday),
            'total_messages': total_messages,
            'active_users': active_users,
            'avg_ai_response_time': ai_avg_response_time
        }
    
    except Exception as exc:
        logger.error(f"[generate_daily_report] Failed : {exc}")
        raise self.retry(exc=exc, countdown=60)
        