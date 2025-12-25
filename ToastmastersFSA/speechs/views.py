from django.shortcuts import render, get_object_or_404, redirect
from .models import Speech, Certificat
from .forms import SpeechForm
from meetings.models import Meeting
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from django.http import HttpResponseRedirect
from django.urls import reverse
from forms.forms import create_or_update_form
from datetime import timedelta
from django.utils.timezone import now
from django.http import JsonResponse
from meetings.models import Role
from members.models import Profile
from django.db.models import Q


# Create your views here.
@login_required
def show_historique_speeches_list(request):
    today = now().date()

    past_personal_speeches = Speech.objects.filter(
        orator=request.user, 
        meeting__date__lt=today
    ).order_by('meeting__date')

    past_club_speeches = Speech.objects.filter(
        meeting__date__lt=today
    ).order_by('meeting__date')

    search = request.GET.get("filtre")
    if search:
        past_club_speeches =  past_club_speeches.filter(
            Q(orator__last_name__icontains=search) |
            Q(orator__first_name__icontains=search)
    )

        # Role filter
    role = request.GET.get("role")
    if role:
        past_personal_speeches = past_personal_speeches.filter(role__title=role)

    # Date filter
    date_filter = request.GET.get("date") 
    if date_filter == "7j":
        past_personal_speeches = past_personal_speeches.filter(meeting__date__gte=now() - timedelta(days=7))
    elif date_filter == "14j":
        past_personal_speeches = past_personal_speeches.filter(meeting__date__gte=now() - timedelta(days=14))
    elif date_filter == "30j":
        past_personal_speeches = past_personal_speeches.filter(meeting__date__gte=now() - timedelta(days=30))
    elif date_filter == "90j":
        past_personal_speeches = past_personal_speeches.filter(meeting__date__gte=now() - timedelta(days=90))
    elif date_filter == "365j":
        past_personal_speeches = past_personal_speeches.filter(meeting__date__gte=now() - timedelta(days=365))

    past_speeches = {
        'personnel': past_personal_speeches,
        'club': past_club_speeches
    }
    certificats_won = Certificat.objects.filter(speech__orator=request.user).count()
    roles_performed = Speech.objects.filter(orator=request.user).count()
    section_active = request.GET.get('section', 'personnel')

    context = {
        'past_speeches': past_speeches,
        'roles': Role.objects.values_list('title', flat=True).distinct(),
        'section_active':'suivi',
        'current_section': section_active,
        'certificats_won': certificats_won,
        'roles_performed':roles_performed,
        'profils': Profile.objects.all()
    }
    return render(request, 'speechs/historique_speeches_list.html', context)


@login_required
def show_future_speeches_list(request):
    today= now().date()

    future_personal_speeches = Speech.objects.filter(
        orator=request.user,
        meeting__date__gte=today
    ).order_by('meeting__date')

    future_club_speeches = Speech.objects.filter(
        meeting__date__gte=today
    ).order_by('meeting__date')

    # Role filter
    role = request.GET.get("role")
    if role:
        future_club_speeches = future_club_speeches.filter(role__title=role)

    meeting = request.GET.get("meeting")
    if meeting:
        future_club_speeches = future_club_speeches.filter(meeting__date=meeting)
    
    future_speeches = {
        'personnel': future_personal_speeches,
        'club': future_club_speeches
    }
         
    meetings = [
        d.strftime("%Y-%m-%d") for d in Meeting.objects.filter(date__gte=now())
        .values_list('date', flat=True).distinct()
    ]

    section_active = request.GET.get('section', 'personnel')
    context = {
        'future_speeches': future_speeches,
        'section_active':'roles',
        'roles': Role.objects.values_list('title', flat=True).distinct(),
        'meetings': meetings,
        'current_section': section_active,
    }
    return render(request, 'speechs/future_speeches_list.html', context)



@login_required
def create_speech(request):
    if request.method == 'POST':
        form = SpeechForm(request.POST)
        if form.is_valid():
            speech = form.save(commit=False)
            speech.orator = request.user
            speech.save()
            create_or_update_form(speech.meeting)
            return HttpResponseRedirect(reverse('meeting_infos', args=[speech.meeting.id]))
    else:
        form = SpeechForm()
    return render(request, 'speechs/add_speech.html', {'speech': form})


@staff_member_required
def attribuate_speech(request):
    if request.method == 'POST':
        form = SpeechForm(request.POST)
        if form.is_valid():
            speech = form.save(commit=False)
            speech.orator = form.cleaned_data['orator']
            speech.save()
            create_or_update_form(speech.meeting)
            return HttpResponseRedirect(reverse('meeting_infos', args=[speech.meeting.id]))
    else:
        form = SpeechForm()
        return render(request, 'speechs/attribuate_speech.html', {'speech': form})
        

@login_required
def confirm_role_deletion(request, speech_id):
    speech = get_object_or_404(Speech, id=speech_id) 
    return render(request, 'speechs/cancel_speech.html', {'speech': speech})    


@login_required
def delete_role(request, speech_id):
    speech = get_object_or_404(Speech, id=speech_id)
    speech.delete()
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def show_available_roles(request):
    meeting_id = request.GET.get("meeting")
    roles = Role.objects.all()

    if meeting_id:
        unique_roles = [
            "Maître(sse) de cérémonie", 
            "Chronométreur(se)",
            "Meneur(se) des improvisations",
            "Évaluateur(rice) des improvisations",
            "Grammairien(ne)",
            "Toast",
            "Lecture de la mission",
            "Mot d'humour",
            "Évaluateur(rice) général(e)"    
            ]
        chosen_roles = Speech.objects.filter(
            meeting_id=meeting_id,
            role__title__in=unique_roles
        ).values_list("role_id", flat=True)
        roles = roles.exclude(id__in=chosen_roles)

        # Évaluateur de discours
        prepared_speechs_count = Speech.objects.filter(
            meetingn_id=meeting_id, role__title="Discours préparé"
        ).count()
        eval_count = Speech.objects.filter(
            meeting_id=meeting_id, role__title="Évaluateur de discours"
        ).count()
        if prepared_speechs_count <= eval_count:
            roles = roles.exclude(title="Évaluateur de discours")

    roles_data = [{"id": r.id, "title": r.title} for r in roles]
    return JsonResponse({"roles": roles_data})



@login_required
def show_certificats(request):
    speech = Speech.objects.filter(orator=request.user, role__title='Discours préparé')
    impro = Speech.objects.filter(orator=request.user, role__title='Discours improvisé')
    evaluation = Speech.objects.filter(orator=request.user, role__title__in=[
        'Évaluateur(rice) des improvisations',
        'Évaluateur(rice) de discours',
        'Grammairien(ne)',
        'Chronométreur(se)',
    ])
    langage = Meeting.objects.filter(top_grammar__icontains=request.user.last_name.title())
    amelioration = Meeting.objects.filter(top_amelioration__icontains=request.user.last_name.title())

    speech_certifs_list = Certificat.objects.filter(speech__in=speech, is_won=True).order_by('-issue_date')
    impro_certifs_list = Certificat.objects.filter(speech__in=impro, is_won=True).order_by('-issue_date')
    evaluation_certifs_list = Certificat.objects.filter(speech__in=evaluation, is_won=True).order_by('-issue_date')
    top_grammar_certifs_list = Certificat.objects.filter(speech__meeting__in=langage, is_won=True).order_by('-issue_date')
    top_amelioration_certifs_list = Certificat.objects.filter(speech__meeting__in=amelioration, is_won=True).order_by('-issue_date')

    certificats_categories = {
        "Meilleur Discours": speech_certifs_list,
        "Meilleure Improvisation": impro_certifs_list,
        "Meilleure Évaluation": evaluation_certifs_list,
        "Meilleur Français": top_grammar_certifs_list,
        "Meilleure Amélioration": top_amelioration_certifs_list,
    }
    return render(request, 'discours/show_certificats.html', {
        'certificats_categories': certificats_categories,
        'section_active': 'certificats'
        })


@login_required
def show_evaluations(request):
    return render(request, 'speechs/show_evaluations.html', {'section_active':'evaluations'})