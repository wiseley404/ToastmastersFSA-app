from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from .models import EmailAttachment, Notification, EmailList, EmailScheduled, SystemEmail, AbsenceEmailCondition
from .forms import NotificationForm, EmailListForm, EmailScheduledForm, SystemEmailForm, AbsenceEmailConditionForm
from members.models import Profile
from .tasks import send_scheduled_email


# Create your views here.
@staff_member_required
def manage_communications(request):
    notifs = Notification.objects.all()
    emails_list = EmailList.objects.all()
    emails_scheduled = EmailScheduled.objects.filter(is_active=True)
    system_emails = SystemEmail.objects.filter(is_active=True)
    section_active = request.GET.get('section', 'personnel')
    context = {
        'current_section':section_active,
        'section_active':'communications',
        'published_notifs': notifs,
        'emails_list': emails_list,
        'emails_scheduled': emails_scheduled, 
        'system_emails':system_emails,
        'form': EmailScheduledForm(),
    }
    return render(request, "communications/show_communications.html", context)


@staff_member_required
def create_notif(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notif = form.save(commit=False)
            notif.sender = request.user
            notif.save()
            members = Profile.objects.all()
            notif.recipients.add(*members)
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        form = NotificationForm()
    return render(request, 'communications/create_notif.html', {'form': form})


@staff_member_required
def edit_notif(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id)
    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=notif)
        if form.is_valid():
            form.save()
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        form = NotificationForm(instance=notif)
    return render(request, 'communications/edit_notif.html', {
        'form':form,
        'notif':notif
        })


@staff_member_required
def confirm_notif_deletion(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id) 
    return render(request, 'communications/delete_notif.html', {'notif': notif})    


@staff_member_required
def delete_notif(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id)
    notif.delete()
    return redirect(request.META.get("HTTP_REFERER", "/"))

@staff_member_required
def create_email_list(request):
    if request.method == 'POST':
        form = EmailListForm(request.POST)
        if form.is_valid():
            email_list = form.save(commit=False)
            email_list.created_by = request.user
            email_list.save()
            form.save_m2m()
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        form = EmailListForm()
    return render(request, 'communications/create_email_list.html', {'form':form})    
    

@staff_member_required
def edit_email_list(request, email_list_id):
    email_list = get_object_or_404(EmailList, id=email_list_id)
    if request.method == 'POST':
        form = EmailListForm(request.POST, instance=email_list)
        if form.is_valid():
            form.save()
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        form = EmailListForm(instance=email_list)
    return render(request, 'communications/edit_email_list.html', {
        'form':form,
        'email_list': email_list
        })

@staff_member_required
def confirm_email_list_deletion(request, email_list_id):
    email_list = get_object_or_404(EmailList, id=email_list_id) 
    return render(request, 'communications/delete_email_list.html', {'email_list': email_list})    


@staff_member_required
def delete_email_list(request, email_list_id):
    email_list = get_object_or_404(EmailList, id=email_list_id)
    email_list.delete()
    referer = request.META.get("HTTP_REFERER", "/")
    if '#' not in referer:
        referer = referer.split('#')[0] + '#email-list-section'
    
    return redirect(referer)


@staff_member_required
def edit_email_scheduled(request, email_scheduled_id):
    email_scheduled = get_object_or_404(EmailScheduled, id=email_scheduled_id)
    if request.method == 'POST':
        form = EmailScheduledForm(request.POST, request.FILES, instance=email_scheduled)
        if form.is_valid():
            form.save()
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        form = EmailScheduledForm(instance=email_scheduled)
    return render(request, 'communications/edit_email_scheduled.html', {
        'form':form,
        'email_scheduled': email_scheduled
        })


@staff_member_required
def confirm_email_scheduled_deletion(request, email_scheduled_id):
    email_scheduled = get_object_or_404(EmailScheduled, id=email_scheduled_id)
    return render(request, 'communications/delete_email_scheduled.html', {'email_scheduled': email_scheduled})


@staff_member_required
def delete_email_scheduled(request, email_scheduled_id):
    email_scheduled = get_object_or_404(EmailScheduled, id=email_scheduled_id)
    email_scheduled.delete()
    referer = request.META.get("HTTP_REFERER", "/")
    if '#' not in referer:
        referer = referer.split('#')[0] + '#email-scheduled-section'
    
    return redirect(referer)


@staff_member_required
def create_email_scheduled(request):
    if request.method == 'POST':
        form = EmailScheduledForm(request.POST, request.FILES)
        if form.is_valid():
            email_scheduled = form.save(commit=False)
            email_scheduled.created_by = request.user
            email_scheduled.is_active = True
            email_scheduled.save()

            for file in request.FILES.getlist('attachments'):
                att = EmailAttachment.objects.create(
                        email=email_scheduled,
                        file=file,
                        filename=file.name,
                        mime_type=file.content_type,
                        size=file.size,
                    )
            if email_scheduled.send_now:
                send_scheduled_email.delay(email_scheduled.id)
            return redirect('communications')
    else:
        form = EmailScheduledForm()
    return redirect('communications')

            
@staff_member_required
def edit_system_email(request, system_email_id):
    email_system = get_object_or_404(SystemEmail, id=system_email_id)
    
    if request.method == 'POST':
        form = SystemEmailForm(request.POST, request.FILES, instance=email_system)
        if form.is_valid():
            form.save()
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        form = SystemEmailForm(instance=email_system) 
    
    absence_form = None
    if email_system.code == 'ABSENCE_WARNING':
        try:
            absence_condition = email_system.absence_condition
        except AbsenceEmailCondition.DoesNotExist:
            absence_condition = None
        
        if request.method == 'POST':
            absence_form = AbsenceEmailConditionForm(request.POST, instance=absence_condition)
            if absence_form.is_valid():
                absence_form.save()
        else:
            absence_form = AbsenceEmailConditionForm(instance=absence_condition)
    
    return render(request, 'communications/edit_system_email.html', {
        'form': form,
        'absence_form': absence_form,
        'email_system': email_system
    })