from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from .models import Notification
from .forms import NotificationForm, EmailListForm
from members.models import Profile


# Create your views here.
@staff_member_required
def manage_communications(request):
    notifs = Notification.objects.all()
    section_active = request.GET.get('section', 'personnel')
    context = {
        'current_section':section_active,
        'section_active':'communications',
        'published_notifs': notifs,
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
    