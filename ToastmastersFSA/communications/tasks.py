import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from celery import shared_task
from communications.models import EmailScheduled, Notification, SystemEmail, SystemEmailLog
from meetings.models import Meeting, MeetingAttendance
from speechs.models import Speech, Certificat
from members.models import Profile
from forms.utils import generate_certificat
from django.db.models import Q, Count
from django.core.files.storage import default_storage
from dateutil.relativedelta import relativedelta
import os
from django.template import Template, Context
from django.test import RequestFactory
from django.template.loader import render_to_string
from weasyprint import HTML


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

    email_scheduled.save()
    
    logger.info(f"Email '{email_scheduled.title}' envoyé à {len(recipients)} destinataires")
    return f"SUCCESS: {len(recipients)} recipients"


def get_recipients(email_scheduled):
    """Retourne tous les emails destinataires"""
    emails = set()
    
    if email_scheduled.to_emails:
        for email in email_scheduled.to_emails.split('\n'):
            email = email.strip()
            if email:
                emails.add(email)
    
    for profile in email_scheduled.to_profiles.all():
        if profile.user.email:
            emails.add(profile.user.email)

    for email_list in email_scheduled.to_lists.all():
        for member in email_list.members.all():
            if member.user.email:
                emails.add(member.user.email)
    
    return list(emails)


@shared_task
def check_and_send_scheduled_emails():
    now = timezone.now()
    today = now.date()

    EmailScheduled.objects.filter(
        is_active=True,
        end_date__lt=today
    ).update(is_active=False)

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

    send_at = datetime.combine(email.start_date, email.send_time)

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


def generate_meeting_pdf_content(meeting):
    """Génère le contenu PDF de la réunion"""
    factory = RequestFactory()
    fake_request = factory.get('/')
    logo_path = os.path.join(settings.STATIC_ROOT, 'images/logo-toastmasters.svg')
    html_string = render_to_string('meetings/meeting_pdf.html', {
        'meeting': meeting,
        'logo_url': f'file:///{logo_path}'
        })
    pdf_content = HTML(string=html_string, base_url=fake_request.build_absolute_uri()).write_pdf()
    return pdf_content


def send_system_email(user_email, subject, body, footer=None, attachments=None):
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
    if attachments: 
        for filename, content, mimetype in attachments:
            msg.attach(filename, content, mimetype)
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
    
    # Cherche les futures réunions
    meetings = Meeting.objects.filter(date__gte=now.date()).order_by('date')
    
    for meeting in meetings:
        reference_time = meeting.start_time if delta.total_seconds() < 0 else meeting.end_time
        
        meeting_datetime = datetime.combine(meeting.date, reference_time)
        send_datetime = meeting_datetime + delta
        
        if now >= send_datetime and now < send_datetime + timedelta(minutes=1):
            programmation_pdf = generate_meeting_pdf_content(meeting)
            
            attachments = None
            if programmation_pdf:
                attachments = [('programmation.pdf', programmation_pdf, 'application/pdf')]
            
            members = Profile.objects.all()
            
            for member in members:
                already_sent = SystemEmailLog.objects.filter(
                    email_config=email_config,
                    recipient=member,
                    meeting=meeting
                ).exists()
                
                if not already_sent:
                    context = {
                        'first_name': member.user.first_name,
                        'meeting_date': meeting.date.strftime('%d/%m/%Y'),
                        'meeting_time': meeting.start_time.strftime('%H:%M'),
                        'meeting_location': meeting.location or 'Non spécifié',
                    }
                    
                    subject = render_template(email_config.subject, context)
                    body = render_template(email_config.body, context)
                    send_system_email(member.user.email, subject, body, email_config.footer, attachments)
                    
                    SystemEmailLog.objects.create(
                        email_config=email_config,
                        recipient=member,
                        meeting=meeting
                    )
    
    return "Done"


@shared_task
def check_and_send_absence_warnings():
    now = timezone.now()
    email_config = SystemEmail.objects.filter(code='ABSENCE_WARNING', is_active=True).first()
    
    if not email_config:
        return "No ABSENCE_WARNING config"
    
    try:
        condition = email_config.absence_condition
    except:
        return "No absence condition"
    
    delta = email_config.get_send_delta()
    
    # Récupère les N dernières réunions passées
    past_meetings = Meeting.objects.filter(
        Q(date=now.date(), end_time__lt=now.time()) |  
        Q(date__lt=now.date())           
    ).order_by('-date', '-end_time')[:condition.absence_count]
    
    if not past_meetings:
        return "Not enough past meetings"
    
    # Calcule le datetime d'envoi basé sur la DERNIÈRE réunion
    last_meeting = past_meetings.first()
    reference_time = last_meeting.end_time if delta.total_seconds() >= 0 else last_meeting.start_time
    meeting_datetime = datetime.combine(last_meeting.date, reference_time)
    send_datetime = meeting_datetime + delta
    
    # Envoie seulement si on est dans la fenêtre d'envoi
    if now >= send_datetime and now < send_datetime + timedelta(minutes=1):
        # Cherche les membres absents dans TOUTES les réunions
        absent_in_all = None
        for meeting in past_meetings:
            absent_this_meeting = set(
                MeetingAttendance.objects.filter(
                    meeting=meeting,
                    is_present=False
                ).values_list('member_id', flat=True)
            )
            
            if absent_in_all is None:
                absent_in_all = absent_this_meeting
            else:
                absent_in_all = absent_in_all.intersection(absent_this_meeting)
        
        # Envoie aux membres absents
        for member_id in absent_in_all:
            member = Profile.objects.get(id=member_id)
            
            already_sent = SystemEmailLog.objects.filter(
                email_config=email_config,
                recipient=member,
                meeting=last_meeting
            ).exists()
            
            if not already_sent:
                context = {'first_name': member.user.first_name}
                subject = render_template(email_config.subject, context)
                body = render_template(email_config.body, context)
                
                send_system_email(member.user.email, subject, body, email_config.footer)
                
                SystemEmailLog.objects.create(
                    email_config=email_config,
                    recipient=member,
                    meeting=last_meeting
                )
    
    condition.last_triggered_at = now
    condition.save()
    
    return "Done"


@shared_task
def send_role_attribution_email_task(speech_id):
    speech = Speech.objects.get(id=speech_id)
    email_config = SystemEmail.objects.get(code='ROLE_ATTRIBUTION', is_active=True)
    
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
def send_meeting_creation_email_task(meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    email_config = SystemEmail.objects.get(code='MEETING_ALERT', is_active=True)
    
    members = Profile.objects.all()
    
    for member in members:
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
def check_and_send_role_reminder():
    """Envoie les rappels de rôle selon send_offset"""
    now = timezone.now()
    email_config = SystemEmail.objects.filter(code='ROLE_REMINDER', is_active=True).first()
    
    if not email_config:
        return "No ROLE_REMINDER config"
    
    delta = email_config.get_send_delta()
    
    # Cherche les futures réunions
    meetings = Meeting.objects.filter(date__gte=now.date()).order_by('date')
    
    for meeting in meetings:
        reference_time = meeting.start_time if delta.total_seconds() < 0 else meeting.end_time

        meeting_datetime = datetime.combine(meeting.date, reference_time)
        send_datetime = meeting_datetime + delta
        
        if now >= send_datetime and now < send_datetime + timedelta(minutes=1):
            speeches = Speech.objects.filter(meeting=meeting)       
            
            for speech in speeches:
                member = speech.orator
                
                # Vérifie si déjà envoyé
                already_sent = SystemEmailLog.objects.filter(
                    email_config=email_config,
                    recipient=member.profile,
                    meeting=meeting
                ).exists()
                
                if not already_sent:
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
                    
                    SystemEmailLog.objects.create(
                        email_config=email_config,
                        recipient=member.profile,
                        meeting=meeting
                    )
    
    return "DONE"


@shared_task
def check_and_send_certificate_attribution():
    """Envoie les attributions de certificat selon send_offset"""
    now = timezone.now()
    email_config = SystemEmail.objects.filter(code='CERTIFICAT_ATTRIBUTION', is_active=True).first()
    
    if not email_config:
        return "No CERTIFICAT_ATTRIBUTION config"
    
    delta = email_config.get_send_delta()
    
    # Cherche les réunions passées
    past_meetings = Meeting.objects.filter(date__lte=now.date()).order_by('-date')
    
    for meeting in past_meetings:
        reference_time = meeting.end_time if delta.total_seconds() >= 0 else meeting.start_time
        
        meeting_datetime = datetime.combine(meeting.date, reference_time)
        send_datetime = meeting_datetime + delta
        
        if now >= send_datetime and now < send_datetime + timedelta(minutes=1):
            certificates = Certificat.objects.filter(
                speech__meeting=meeting,
                is_won=True
            )
            
            for cert in certificates:
                member = cert.speech.orator
                
                # Vérifie si déjà envoyé
                already_sent = SystemEmailLog.objects.filter(
                    email_config=email_config,
                    recipient=member.profile,
                    meeting=meeting
                ).exists()
                
                if not already_sent:
                    context = {
                        'first_name': member.first_name,
                        'certificate_type': cert.title,
                    }
                    
                    subject = render_template(email_config.subject, context)
                    body = render_template(email_config.body, context)
                    
                    certificate_file = generate_certificat(
                        cert.title, 
                        member.get_full_name(), 
                        meeting.date.strftime('%d/%m/%Y')
                    )
                    
                    if certificate_file:
                        notif = Notification.objects.create(
                            sender=None,
                            title='Nouveau certificat',
                            message=f'Vous avez recu un nouveau certificat, felicitaions a vous !'
                        )
                        notif.recipients.add(member.profile)

                        attachments = [('certificat.png', certificate_file, 'image/png')]
                        send_system_email(member.email, subject, body, email_config.footer, attachments)
                        
                        SystemEmailLog.objects.create(
                            email_config=email_config,
                            recipient=member.profile,
                            meeting=meeting
                        )
    
    return "DONE"


