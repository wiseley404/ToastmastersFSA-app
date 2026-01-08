from django.db.models.signals import post_save
from django.dispatch import receiver
from meetings.models import Meeting
from communications.tasks import send_meeting_creation_email_task
from communications.models import Notification
from members.models import Profile

@receiver(post_save, sender=Meeting)
def send_meeting_creation_notification(sender, instance, created, **kwargs):
    if created:
        send_meeting_creation_email_task.delay(instance.id)
        notif = Notification.objects.create(
            sender=None,
            title='Nouvelle réunion programmée',
            message=f'Une réunion est prévue le {instance.date}'
        )
        notif.recipients.set(Profile.objects.all())
