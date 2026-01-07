import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from celery import shared_task
from communications.models import EmailScheduled, SystemEmail
from meetings.models import Meeting, MeetingAttendance
from speechs.models import Speech, Certificat
from members.models import Profile
from django.db.models import Q, Count
from django.core.files.storage import default_storage
from dateutil.relativedelta import relativedelta
import os
from django.template import Template, Context


logger = logging.getLogger(__name__)

@shared_task(bind=True)
def send_scheduled_email(self, email_id):
    """
    Tâche Celery pour envoyer un EmailScheduled spécifique
    """
    logger.warning(
    f"TASK START send_scheduled_email id={email_id}"
)
    now = timezone.now()
    today = now.date()
    try:
        email_scheduled = EmailScheduled.objects.get(id=email_id, is_active=True)
    except EmailScheduled.DoesNotExist:
        logger.error(f"EmailScheduled {email_id} non trouvé")
        return "FAILED"

    # Récupère les destinataires
    recipients = get_recipients(email_scheduled)
    if not recipients:
        logger.error(f"Aucun destinataire pour {email_scheduled.title}")
        return "NO_RECIPIENTS"

    # Crée l'email
    msg = EmailMultiAlternatives(
        email_scheduled.title.capitalize(),
        email_scheduled.message.capitalize(),
        os.getenv('DEFAULT_FROM_EMAIL'),
        recipients,
    )
    msg.attach_alternative(email_scheduled.message, "text/html")

    # Pièces jointes
    for att in email_scheduled.attachments_list.all():
        with default_storage.open(att.file.name, 'rb') as f:
            msg.attach(att.filename, f.read(), att.mime_type)

    # Envoi
    msg.send()
    email_scheduled.last_sent_at = now
    
    if email_scheduled.send_now:
        email_scheduled.is_active = False
    if email_scheduled.frequency == "Une seule fois":
        email_scheduled.is_active = False
    if email_scheduled.end_date and email_scheduled.end_date < today:
        email_scheduled.is_active = False

    email_scheduled.save()
    
    logger.info(f"Email '{email_scheduled.title}' envoyé à {len(recipients)} destinataires")
    return f"SUCCESS: {len(recipients)} recipients"


def get_recipients(email_scheduled):
    """Logique destinataires: email + profile + liste"""
    recipients = []
    
    if email_scheduled.to_email:
        recipients.append(email_scheduled.to_email)
    
    if email_scheduled.to_profile and email_scheduled.to_profile.user.email:
        recipients.append(email_scheduled.to_profile.user.email)
    
    if email_scheduled.to_list:
        recipients.extend([m.user.email for m in email_scheduled.to_list.members.all() if m.user.email])
    
    return recipients


@shared_task
def check_and_send_scheduled_emails():
    now = timezone.now()
    today = now.date()

    emails = EmailScheduled.objects.filter(
        is_active=True,
        send_now=False,
        start_date__lte=today,
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=today)
    )

    for email in emails:
        if should_send(email, now):
            send_scheduled_email.delay(email.id)



def should_send(email, now):
    if not email.start_date or not email.send_time:
        return False

    send_at = timezone.make_aware(
        datetime.combine(email.start_date, email.send_time),
        timezone.get_current_timezone()
    )

    if now < send_at:
        return False

    if email.frequency == "Une seule fois":
        return email.last_sent_at is None

    if email.frequency == "Quotidien":
        return not email.last_sent_at or email.last_sent_at.date() < now.date()

    if email.frequency == "Hebdomadaire":
        return not email.last_sent_at or email.last_sent_at < now - timedelta(days=7)
    
    if email.frequency == "Aux deux semaines":
        return not email.last_sent_at or email.last_sent_at + relativedelta(weeks=2) <= now
    
    if email.frequency == "Mensuel":
        return not email.last_sent_at or email.last_sent_at + relativedelta(months=1) <= now

    return False




def send_system_email(user_email, subject, body, footer=None):
    """Envoie un email avec subject et body"""
    full_body = body
    if footer:
        full_body += f"\n\n{footer}"
    
    msg = EmailMultiAlternatives(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )
    msg.attach_alternative(full_body, "text/html")
    msg.send()
    logger.info(f"Email envoyé à {user_email}: {subject}")


def render_template(template_str, context_data):
    """Rend un template avec les variables"""
    template = Template(template_str)
    return template.render(Context(context_data))


@shared_task
def check_and_send_meeting_reminders():
    """Envoie les rappels de réunion selon send_offset"""
    now = timezone.now()
    email_config = SystemEmail.objects.filter(code='MEETING_REMINDER', is_active=True).first()
    
    if not email_config:
        return "No MEETING_REMINDER config"
    
    delta = email_config.get_send_delta()
    send_time = now - delta
    
    meetings = Meeting.objects.filter(
        date__gte=send_time.date(),
        date__lte=(send_time + timedelta(days=1)).date()
    )
    
    for meeting in meetings:
        attendances = MeetingAttendance.objects.filter(meeting=meeting)
        
        for attendance in attendances:
            member = attendance.member
            context = {
                'first_name': member.user.first_name,
                'meeting_date': meeting.date.strftime('%d/%m/%Y'),
                'meeting_time': meeting.start_time.strftime('%H:%M'),
                'meeting_location': meeting.location or 'Non spécifié',
            }
            
            subject = render_template(email_config.subject, context)
            body = render_template(email_config.body, context)
            
            send_system_email(member.user.email, subject, body, email_config.footer)


@shared_task
def check_and_send_absence_warnings():
    """Envoie les alertes d'absence selon send_offset et condition"""
    now = timezone.now()
    email_config = SystemEmail.objects.filter(code='ABSENCE_WARNING', is_active=True).first()
    
    if not email_config:
        return "No ABSENCE_WARNING config"
    
    try:
        condition = email_config.absence_condition
    except:
        return "No absence condition"
    
    delta = email_config.get_send_delta()
    send_time = now - delta
    
    # Récupère les membres absents récemment
    absent_members = MeetingAttendance.objects.filter(
        meeting__date__gte=(send_time - timedelta(days=7)).date(),
        meeting__date__lte=send_time.date(),
        is_present=False,
        confirmed_at__isnull=True
    ).values('member').annotate(
        absence_count=Count('id')
    ).filter(absence_count__gte=condition.absence_count)
    
    for absence_record in absent_members:
        member = Profile.objects.get(id=absence_record['member'])
        context = {
            'first_name': member.user.first_name,
        }
        
        subject = render_template(email_config.subject, context)
        body = render_template(email_config.body, context)
        
        send_system_email(member.user.email, subject, body, email_config.footer)
    
    condition.last_triggered_at = now
    condition.save()


@shared_task
def check_and_send_role_attribution():
    """Envoie les attributions de rôle selon send_offset"""
    now = timezone.now()
    email_config = SystemEmail.objects.filter(code='ROLE_ATTRIBUTION', is_active=True).first()
    
    if not email_config:
        return "No ROLE_ATTRIBUTION config"
    
    delta = email_config.get_send_delta()
    send_time = now - delta
    
    speeches = Speech.objects.filter(
        meeting__date__gte=send_time.date(),
        meeting__date__lte=(send_time + timedelta(days=1)).date()
    )
    
    for speech in speeches:
        member = speech.orator
        context = {
            'first_name': member.first_name,
            'role_title': speech.role.title,
            'meeting_date': speech.meeting.date.strftime('%d/%m/%Y'),
            'meeting_time': speech.meeting.start_time.strftime('%H:%M'),
            'meeting_location': speech.meeting.location or 'Non spécifié',
        }
        
        subject = render_template(email_config.subject, context)
        body = render_template(email_config.body, context)
        
        send_system_email(member.email, subject, body, email_config.footer)


@shared_task
def check_and_send_role_reminder():
    """Envoie les rappels de rôle selon send_offset"""
    now = timezone.now()
    email_config = SystemEmail.objects.filter(code='ROLE_REMINDER', is_active=True).first()
    
    if not email_config:
        return "No ROLE_REMINDER config"
    
    delta = email_config.get_send_delta()
    send_time = now - delta
    
    speeches = Speech.objects.filter(
        meeting__date__gte=send_time.date(),
        meeting__date__lte=(send_time + timedelta(days=1)).date()
    )
    
    for speech in speeches:
        member = speech.orator
        context = {
            'first_name': member.first_name,
            'role_title': speech.role.title,
            'meeting_date': speech.meeting.date.strftime('%d/%m/%Y'),
            'meeting_time': speech.meeting.start_time.strftime('%H:%M'),
            'meeting_location': speech.meeting.location or 'Non spécifié',
        }
        
        subject = render_template(email_config.subject, context)
        body = render_template(email_config.body, context)
        
        send_system_email(member.email, subject, body, email_config.footer)


@shared_task
def check_and_send_certificate_attribution():
    """Envoie les attributions de certificat selon send_offset"""
    now = timezone.now()
    email_config = SystemEmail.objects.filter(code='CERTIFICAT_ATTRIBUTION', is_active=True).first()
    
    if not email_config:
        return "No CERTIFICAT_ATTRIBUTION config"
    
    delta = email_config.get_send_delta()
    send_time = now - delta
    
    certificates = Certificat.objects.filter(
        issue_date=send_time.date(),
        is_won=True
    )
    
    for cert in certificates:
        member = cert.speech.orator
        context = {
            'first_name': member.first_name,
            'certificate_type': cert.title,
        }
        
        subject = render_template(email_config.subject, context)
        body = render_template(email_config.body, context)
        
        send_system_email(member.email, subject, body, email_config.footer)


@shared_task
def mark_absences():
    """Marque les absences après la réunion"""
    now = timezone.now()
    
    meetings = Meeting.objects.filter(
        date__lt=now.date()
    )
    
    for meeting in meetings:
        MeetingAttendance.objects.filter(
            meeting=meeting,
            is_present=False,
            confirmed_at__isnull=True
        ).update(is_present=False)
