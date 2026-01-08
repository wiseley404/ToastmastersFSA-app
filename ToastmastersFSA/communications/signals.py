from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, SystemEmail
from communications.tasks import send_system_email

@receiver(post_save, sender=Notification)
def on_notification_created(sender, instance, created, **kwargs):
    if instance.sender is not None and instance.recipients.exists():
        email_config = SystemEmail.objects.filter(code='MEETING_REMINDER').first()
        footer = email_config.footer if email_config else None
        
        for recipient in instance.recipients.all():
            send_system_email(
                recipient.user.email,
                "Nouvelle notification",
                "<p>Bonjour,</p><p>Vous avez une nouvelle notification sur votre compte.</p><p>Veuillez consulter pour en savoir plus !</p><p>L'équipe Toastmasters</p>",
                footer=footer
            )