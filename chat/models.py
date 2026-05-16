from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Conversation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    ROLE_CHOICES = [('user', 'User'),
                    ('assistant', 'Assistant')]
    role = models.CharField(choices=ROLE_CHOICES, max_length=20)
    content = models.TextField()
    response_time = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class DailyReport(models.Model):
    date = models.DateField(unique=True)
    total_messages = models.IntegerField()
    active_users = models.IntegerField()
    avg_ai_response = models.FloatField()
    report_data = models.JSONField()
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report - {self.date}"
    
    


