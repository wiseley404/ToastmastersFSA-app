from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Progression
from meetings.models import Meeting
from speechs.models import Certificat
from django.contrib.auth.decorators import login_required
from .forms import UpdatePhoneNumberForm, UpdatePhotoForm, UpdateCurriculumsForm, UpdateStatutsForm
from accounts.forms import UpdateEmailForm, UpdateFirstNameForm, UpdateLastNameForm, UpdateUsernameForm
from django.utils.timezone import now
import json


# Create your views here.
@login_required
def show_dashboard(request):
    statuts = request.user.profile.statuts.all()
    board_profiles = request.user.profile.board_roles.all()
    other_statuts = [s.title.capitalize() for s in statuts if s.title.lower() != 'membre officiel']
    is_official_member = request.user.profile.statuts.filter(title__iexact='membre officiel').exists()
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

    labels = [progression.reunion.date.strftime("%Y-%m-%d") for progression in progressions]
    data_pertinence = [progression.pertinence for progression in progressions]
    data_temps = [progression.gestion_temps for progression in progressions]
    data_eloquence = [progression.eloquence for progression in progressions]
    data_structure = [progression.structure for progression in progressions]

    today = now()
    last_meeting = Meeting.objects.filter(date__lte=today).order_by('-date').first()
    next_meeting = Meeting.objects.filter(date__gte=today).order_by('date').first()

    stats = {
        'next_meetings': Meeting.objects.filter(date__gte=today).count(),
        'certificats_won': Certificat.objects.filter(speech__orator=request.user).count()
    }

    certificats = []
    if last_meeting:
        speechs_last_meeting = last_meeting.speeches.all()
        certificats = Certificat.objects.filter(speech__in=speechs_last_meeting, is_won=True)


    notifications = request.user.profile.notifications.all()[:3]


    context = {
        'labels': json.dumps(labels),
        'data_pertinence': json.dumps(data_pertinence),
        'data_temps': json.dumps(data_temps),
        'data_eloquence': json.dumps(data_eloquence),
        'data_structure': json.dumps(data_structure),
        'other_statuts': other_statuts,
        'is_official_member': is_official_member,
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
        'user_statuts_form': UpdateStatutsForm(instance=profile),
        'user_curriculums_form': UpdateCurriculumsForm(instance=profile),
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
        elif form == "status":
            form = UpdateStatutsForm(request.POST, instance=profile)
        elif form == "curriculums":
            form = UpdateCurriculumsForm(request.POST, instance=profile)
        else:
            form = None
        
        if form and form.is_valid():
            form.save()
        return redirect('edit_profile')

    return render(request, 'members/edit_profile.html', context)
