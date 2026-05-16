from chat.models import Message,Conversation
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(post_save,sender=Message)
def MessageCreatedSignal(sender, created, instance, **kwargs):
    if created:
        logger.info(f"Message created -> {instance.content}")
    else:
        logger.info(f"Message updated to -> {instance.content}")

@receiver(post_save, sender=Conversation)
def ConversationCreatedSignal(sender, created, instance, **kwargs):
    if created:
        logger.info(f"Conversation Created -> {instance.title}")
    else:
        logger.info(f"Conversation updated to -> {instance.title}")

@receiver(post_delete, sender=Conversation)
def ConversationDeletedSignal(sender, instance, **kwargs):
    logger.warning(f"Conversation deleted -> {instance.title}")

    
