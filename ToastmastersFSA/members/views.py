from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Progression
from meetings.models import Meeting, MeetingAttendance
from speechs.models import Certificat
from django.contrib.auth.decorators import login_required
from .forms import UpdatePhoneNumberForm, UpdatePhotoForm, UpdateCurriculumForm, UpdateStatutForm
from accounts.forms import UpdateEmailForm, UpdateFirstNameForm, UpdateLastNameForm, UpdateUsernameForm
from django.utils.timezone import now
import json
from django.db.models import Q


# Create your views here.
@login_required
def show_dashboard(request):
    board_profiles = request.user.profile.board_roles.all()
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
    context = {
        'user_firstname_form': UpdateFirstNameForm(instance=user),
        'user_lastname_form': UpdateLastNameForm(instance=user),
        'user_email_form': UpdateEmailForm(instance=user),
        'user_username_form': UpdateUsernameForm(instance=user),
        'user_telephone_form': UpdatePhoneNumberForm(instance=profile),
        'user_statut_form': UpdateStatutForm(instance=profile),
        'user_curriculum_form': UpdateCurriculumForm(instance=profile),
        'user_photo_form': UpdatePhotoForm(instance=profile)
    }
    if request.method == 'POST':
        form_type = request.POST.get("form_type")

        if form_type == "firstname":
            form = UpdateFirstNameForm(request.POST, instance=profile)
        elif form_type == "lastname":
            form = UpdateLastNameForm(request.POST, instance=profile)
        elif form_type == "email":
            form = UpdateEmailForm(request.POST, instance=profile)
        elif form_type == "photo":
            form = UpdatePhotoForm(request.POST, request.FILES, instance=profile)
        elif form_type == "username":
            form = UpdateUsernameForm(request.POST, instance=profile)
        elif form_type == "telephone":
            form = UpdatePhoneNumberForm(request.POST, instance=profile)
        elif form == "statu":
            form = UpdateStatutForm(request.POST, instance=profile)
        elif form == "curriculum":
            form = UpdateCurriculumForm(request.POST, instance=profile)
        else:
            form = None
        
        if form and form.is_valid():
            form.save()
        return redirect('edit_profile')

    return render(request, 'members/edit_profile.html', context)
