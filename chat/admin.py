from django.contrib import admin
from chat.models import Message, Conversation, DailyReport

# Register your models here.


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'role', 'created_at', 'content']

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_messages', 'active_users', 'avg_ai_response', 'report_data', 'generated_at']

    