from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from meetings.models import Meeting
from members.models import Profile

# Create your models here.
class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent', blank=True, null=True)
    recipients = models.ManyToManyField(Profile, blank=True, related_name='notifications')
    title = models.CharField(max_length=200) 
    message = models.TextField(max_length=1000) 
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.message[:30]}..."
    

class EmailList(models.Model):
    title = models.CharField(max_length=300)
    members = models.ManyToManyField('members.Profile', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_mails_created')

    def __str__(self):
        return self.title
    
    @property
    def total_members(self):
        return self.members.count()


class EmailScheduled(models.Model):

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="scheduled_emails",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=255)
    message = models.TextField()
    attachments = models.ManyToManyField('EmailAttachment', blank=True)

    to_emails = models.TextField(blank=True, null=True)
    
    to_profiles = models.ManyToManyField(
        "members.Profile", 
        blank=True,
        related_name="emails_scheduled",
    )
    
    to_lists = models.ManyToManyField(
        EmailList, 
        blank=True,
        related_name="emails_scheduled",
    )

    send_now = models.BooleanField(default=False)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    send_time = models.TimeField(blank=True, null=True)

    FREQUENCY_CHOICES = [
        ("once", "Une seule fois"),
        ("daily", "Quotidien"),
        ("weekly", "Hebdomadaire"),
        ("biweekly", "Aux deux semaines"),
        ("monthly", "Mensuel"),
    ]
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default="once",
    )

    last_sent_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class EmailAttachment(models.Model):
    email = models.ForeignKey(EmailScheduled, on_delete=models.CASCADE, related_name='attachments_list')
    file = models.FileField(upload_to='emails/attachments/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100, blank=True)
    size = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.filename
    

class SystemEmail(models.Model):

    SYSTEM_EMAIL_CODES = (
        ('MEETING_REMINDER', 'RAPPEL REUNION'),
        ('ABSENCE_WARNING', 'ABSENCE ALERTE'),
        ('ROLE_REMINDER', 'RAPPEL ROLE'),
        ('ROLE_ATTRIBUTION', 'ATTRIBUTION ROLE'),
        ('CERTIFICAT_ATTRIBUTION', 'ATTRIBUTION CERTIFICAT'),
        ('MEETING_ALERT', 'NOUVELLE REUNION'),
    )

    SEND_AT_CHOICES = [
        # Minutes
        ('M5_BEFORE', '5 minutes avant'),
        ('M5_AFTER',  '5 minutes après'),

        ('M15_BEFORE', '15 minutes avant'),
        ('M15_AFTER',  '15 minutes après'),

        ('M30_BEFORE', '30 minutes avant'),
        ('M30_AFTER',  '30 minutes après'),

        # Hours
        ('H1_BEFORE',  '1 heure avant'),
        ('H1_AFTER',   '1 heure après'),

        ('H2_BEFORE',  '2 heures avant'),
        ('H2_AFTER',   '2 heures après'),

        ('H4_BEFORE',  '4 heures avant'),
        ('H4_AFTER',   '4 heures après'),

        ('H8_BEFORE',  '8 heures avant'),
        ('H8_AFTER',   '8 heures après'),

        ('H12_BEFORE', '12 heures avant'),
        ('H12_AFTER',  '12 heures après'),

        # Days
        ('D1_BEFORE',  '1 jour avant'),
        ('D1_AFTER',   '1 jour après'),

        ('D2_BEFORE',  '2 jours avant'),
        ('D2_AFTER',   '2 jours après'),

        ('D3_BEFORE',  '3 jours avant'),
        ('D3_AFTER',   '3 jours après'),

        ('D5_BEFORE',  '5 jours avant'),
        ('D5_AFTER',   '5 jours après'),

        ('D7_BEFORE',  '7 jours avant'),
        ('D7_AFTER',   '7 jours après'),
    ]

    code = models.CharField(
        max_length=50,
        choices=SYSTEM_EMAIL_CODES,
        unique=True
    )

    subject = models.CharField(max_length=255)
    body = models.TextField()
    footer = models.TextField(blank=True, null=True)

    send_offset = models.CharField(
        max_length=20,
        choices=SEND_AT_CHOICES,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return dict(self.SYSTEM_EMAIL_CODES).get(self.code, self.code)
    
    def get_send_delta(self):
        """Retourne un timedelta basé sur send_offset"""
        offset_map = {
            'M5_BEFORE': timedelta(minutes=-5),
            'M5_AFTER': timedelta(minutes=5),
            'M15_BEFORE': timedelta(minutes=-15),
            'M15_AFTER': timedelta(minutes=15),
            'M30_BEFORE': timedelta(minutes=-30),
            'M30_AFTER': timedelta(minutes=30),
            'H1_BEFORE': timedelta(hours=-1),
            'H1_AFTER': timedelta(hours=1),
            'H2_BEFORE': timedelta(hours=-2),
            'H2_AFTER': timedelta(hours=2),
            'H4_BEFORE': timedelta(hours=-4),
            'H4_AFTER': timedelta(hours=4),
            'H8_BEFORE': timedelta(hours=-8),
            'H8_AFTER': timedelta(hours=8),
            'H12_BEFORE': timedelta(hours=-12),
            'H12_AFTER': timedelta(hours=12),
            'D1_BEFORE': timedelta(days=-1),
            'D1_AFTER': timedelta(days=1),
            'D2_BEFORE': timedelta(days=-2),
            'D2_AFTER': timedelta(days=2),
            'D3_BEFORE': timedelta(days=-3),
            'D3_AFTER': timedelta(days=3),
            'D5_BEFORE': timedelta(days=-5),
            'D5_AFTER': timedelta(days=5),
            'D7_BEFORE': timedelta(days=-7),
            'D7_AFTER': timedelta(days=7),
        }
        return offset_map.get(self.send_offset, timedelta())


class SystemEmailAttachment(models.Model):
    email = models.ForeignKey(
        SystemEmail,
        on_delete=models.CASCADE,
        related_name="attachments"
    )
    file = models.FileField(upload_to="system_emails/")

    def __str__(self):
        return f"Pièce jointe - {self.email}"


class AbsenceEmailCondition(models.Model):

    ABSENCE_THRESHOLD_CHOICES = (
        (1, '1 absence'),
        (2, '2 absences'),
        (3, '3 absences'),
    )

    email = models.OneToOneField(
        SystemEmail,
        on_delete=models.CASCADE,
        related_name='absence_condition'
    )

    absence_count = models.PositiveIntegerField(
        choices=ABSENCE_THRESHOLD_CHOICES
    )

    last_triggered_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Dernière fois que cet email a été envoyé"
    )

    def __str__(self):
        return f"{self.absence_count} absences"


class SystemEmailLog(models.Model):
    email_config = models.ForeignKey(SystemEmail, on_delete=models.CASCADE, related_name='logs')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('email_config', 'recipient', 'meeting')