from django.db.models.signals import post_save
from django.dispatch import receiver
from communications.models import Notification
from speechs.models import Speech
from communications.tasks import send_role_attribution_email_task

@receiver(post_save, sender=Speech)
def send_role_on_creation(sender, instance, created, **kwargs):
    if created:
        send_role_attribution_email_task.delay(instance.id)
        notif = Notification.objects.create(
            sender=None,
            title='Vous avez un nouveau role',
            message=f'Vous avez le role de {instance.role.title} pour la réunion du {instance.meeting.date}'
        )
        notif.recipients.add(instance.orator.profile)