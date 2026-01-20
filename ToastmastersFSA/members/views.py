from django.shortcuts import render, get_object_or_404, redirect

from communications.models import Notification
from .models import Profile, Progression
from meetings.models import Meeting, MeetingAttendance
from speechs.models import Certificat
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from accounts.forms import UserForm
from django.utils.timezone import now
import json
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.http import JsonResponse


# Create your views here.
@login_required
def show_dashboard(request):
    board_profiles = request.user.profile.board_roles.filter(is_active=True)
    is_board_member = request.user.profile.board_roles.exists()
    

    CIRCLE_LENGTH = 2 * 3.1416 * 45

    pertinence_data = Progression.objects.filter(user=request.user).values_list('pertinence', flat=True)
    time_gestion_data = Progression.objects.filter(user=request.user).values_list('time_gestion', flat=True)
    eloquence_data = Progression.objects.filter(user=request.user).values_list('eloquence', flat=True)
    structure_data = Progression.objects.filter(user=request.user).values_list('structure', flat=True)
    criteres = {
        'Pertinence': round(sum(pertinence_data)/len(pertinence_data)) if pertinence_data else 0,
        'G. Temps': round(sum(time_gestion_data)/len(time_gestion_data)) if time_gestion_data else 0,
        'Éloquence': round(sum(eloquence_data)/len(eloquence_data)) if eloquence_data else 0,
        'Structure': round(sum(structure_data)/len(structure_data)) if structure_data else 0,
    }

    progression = []
    for label, value in criteres.items():
        offset = CIRCLE_LENGTH - (CIRCLE_LENGTH * value / 100)

        progression.append({
            'label': label,
            'value': value,
            'offset': offset,
            'circle_length': CIRCLE_LENGTH,
        })

    progressions = Progression.objects.filter(user=request.user).order_by('meeting__date')

    labels = [progression.meeting.date.strftime("%Y-%m-%d") for progression in progressions]
    data_pertinence = [progression.pertinence for progression in progressions]
    data_temps = [progression.time_gestion for progression in progressions]
    data_eloquence = [progression.eloquence for progression in progressions]
    data_structure = [progression.structure for progression in progressions]

    today = now()

    last_meeting = Meeting.objects.filter(
        Q(date=today.date(), end_time__lt=today.time()) |
        Q(date__lt=today.date())
    ).order_by('-date', '-end_time').first()

    next_meeting = Meeting.objects.filter(
        Q(date=today.date(), start_time__gt=today.time()) |
        Q(date__gt=today.date())
    ).order_by('date', 'start_time').first()

    stats = {
        'next_meetings': Meeting.objects.filter(
            Q(date=today.date(), end_time__gt=today.time()) |  
            Q(date__gt=today.date())
        ).count(),
        'certificats_won': Certificat.objects.filter(speech__orator=request.user).count(),
        'total_presences': MeetingAttendance.objects.filter(member=request.user.profile, is_present=True).count(),
        'total_meetings': Meeting.objects.all().count(),
        'last_meeting_attendance': MeetingAttendance.objects.filter(member=request.user.profile, is_present=True).order_by('-meeting__date').first(),
    }

    certificats = []
    if last_meeting:
        certificats = Certificat.objects.filter(
            speech__meeting=last_meeting,
            is_won=True
        )


    notifications = request.user.profile.notifications.all()[:3]


    context = {
        'labels': json.dumps(labels),
        'data_pertinence': json.dumps(data_pertinence),
        'data_temps': json.dumps(data_temps),
        'data_eloquence': json.dumps(data_eloquence),
        'data_structure': json.dumps(data_structure),
        'is_board_member': is_board_member,
        'board_profiles': board_profiles,
        'section_active':'dashboard',
        'progression': progression,
        'certificats': certificats,
        'last_meeting': last_meeting if last_meeting else None,
        'next_meeting': next_meeting if next_meeting else None,
        'stats': stats,
        'notifications': notifications,
    }

    return render(request, 'members/dashboard.html', context)



@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    user = request.user

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            if profile_form.cleaned_data.get('remove_photo'):
                if profile.photo:
                    profile.photo.delete(save=False)
                    profile.photo = None

            user_form.save()
            profile_form.save()

            return redirect('edit_profile')

    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'members/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    })



@login_required
def show_my_notifications(request):
    filter_param = request.GET.get('filter', 'all')
    
    qs = request.user.profile.notifications.all()
    
    if filter_param == 'unread':
        qs = qs.filter(is_read=False, is_archived=False) 
    elif filter_param == 'archived':
        qs = qs.filter(is_archived=True) 
    else:
        qs = qs.filter(is_archived=False)
    
    my_notifs = qs.order_by('-created_at')
    return render(request, 'members/show_my_notifications.html', {'my_notifs': my_notifs})



@require_POST
@login_required
def update_notification(request):
    notif_id = request.POST.get("id")
    action = request.POST.get("action")

    notif = get_object_or_404(
        request.user.profile.notifications,
        id=notif_id
    )

    if action == "read":
        notif.is_read = True

    elif action == "unread":
        notif.is_read = False

    elif action == "archived":
        notif.is_archived = True

    elif action == "unarchived":
        notif.is_archived = False

    notif.save()
    return JsonResponse({"success": True})