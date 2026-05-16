from celery import shared_task
from django.core.mail import send_mail


@shared_task(name='accounts.tasks.send_welcome_email')
def send_welcome_email(user_email, username):
    send_mail(
        subject='Hey! Welcome to Areebs AiChatBot!',
        message=f'{username} your account is ready! If you have any Question Contact Us',
        from_email='igxareeb@gmail.com',
        recipient_list=[user_email]
    )





