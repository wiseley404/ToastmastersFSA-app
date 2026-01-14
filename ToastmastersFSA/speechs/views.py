import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Evaluation, EvaluationAnswer, EvaluationCriteria, EvaluationLevel, EvaluationType, Speech, Certificat
from .forms import SpeechForm
from meetings.models import Meeting
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from django.http import HttpResponseRedirect
from django.urls import reverse
from forms.forms import create_or_update_form
from datetime import timedelta
from django.http import JsonResponse
from meetings.models import Role
from members.models import Profile, Progression
from django.db.models import Q

# Create your views here.
@login_required
def show_historique_speeches_list(request):
    today = now().date()

    past_personal_speeches = Speech.objects.filter(
        orator=request.user
    ).filter(
        Q(meeting__date__lt=today) |  
        Q(meeting__date=today, meeting__end_time__lt=now().time()) 
    ).order_by('-meeting__date', '-meeting__end_time')

    profils = Profile.objects.all().order_by('user__last_name', 'user__first_name')
    search = request.GET.get("filtre")
    if search:
        profils =  profils.filter(
            Q(user__last_name__icontains=search) |
            Q(user__first_name__icontains=search)
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

    certificats_won = Certificat.objects.filter(speech__orator=request.user).count()
    roles_performed = Speech.objects.filter(orator=request.user).count()
    section_active = request.GET.get('section', 'personnel')

    context = {
        'past_personal_speeches': past_personal_speeches,
        'roles': Role.objects.values_list('title', flat=True).distinct(),
        'section_active':'suivi',
        'current_section': section_active,
        'certificats_won': certificats_won,
        'roles_performed':roles_performed,
        'profils': profils
    }
    return render(request, 'speechs/historique_speeches_list.html', context)


@login_required
def show_future_speeches_list(request):
    today= now().date()

    future_personal_speeches = Speech.objects.filter(
        orator=request.user
    ).filter(
        Q(meeting__date__gt=today) | 
        Q(meeting__date=today, meeting__start_time__gt=now().time())
    ).order_by('meeting__date', 'meeting__start_time')

    future_club_speeches = Speech.objects.filter(
    ).filter(
        Q(meeting__date__gt=today) |
        Q(meeting__date=today, meeting__start_time__gt=now().time())
    ).order_by('meeting__date', 'meeting__start_time')

    # Role filter
    role = request.GET.get("role")
    if role:
        future_club_speeches = future_club_speeches.filter(role__title=role)
         
    meeting_id = request.GET.get("meeting_id")  
    if meeting_id:
        future_club_speeches = future_club_speeches.filter(meeting_id=meeting_id)

    future_speeches = {
        'personnel': future_personal_speeches,
        'club': future_club_speeches
    }

    meetings = Meeting.objects.filter(
        Q(date__gt=today) |
        Q(date=today, start_time__gt=now().time())
    ).distinct()

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
            #create_or_update_form(speech.meeting)
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
            #create_or_update_form(speech.meeting)
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
            meeting_id=meeting_id, role__title="Discours préparé"
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
    speech = Speech.objects.filter(orator=request.user, role__title__iexact='Discours préparé')
    impro = Speech.objects.filter(orator=request.user, role__title__iexact='Discours improvisé')
    evaluation = Speech.objects.filter(
        orator=request.user
    ).filter(
        Q(role__title__iexact='Évaluateur(rice) des improvisations') |
        Q(role__title__iexact='Évaluateur(rice) de discours') |
        Q(role__title__iexact='Grammairien(ne)') |
        Q(role__title__iexact='Chronométreur(se)')
    )
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
    return render(request, 'speechs/show_certificats.html', {
        'certificats_categories': certificats_categories,
        'section_active': 'certificats'
        })


@login_required
def show_evaluations(request):
    section_active = request.GET.get('section', 'personnel')
    evaluations = Evaluation.objects.filter(evaluator=request.user, is_submitted=False)
    evaluation_types = EvaluationType.objects.all()
    evalution_levels = EvaluationLevel.objects.all()
    received_evals = EvaluationAnswer.objects.filter(profile=request.user.profile)
    context = {
        'current_section':section_active,
        'section_active':'evaluations',
        'evaluations': evaluations,
        'evaluation_types': evaluation_types,
        'evaluation_levels': evalution_levels,
        'received_evals': received_evals,
    }
    return render(request, 'speechs/show_evaluations.html', context)


@login_required
def start_evaluation(request):
    current_date = now().date()
    section_active = request.GET.get('section', 'personnel')
    meetings = Meeting.objects.filter(date=current_date)
    evaluation_types = EvaluationType.objects.all()
    context = {
        'current_section':section_active,
        'section_active':'evaluations',
        'meetings':meetings,
        'evaluation_types':evaluation_types,
    }
    return render(request, 'speechs/start_evaluation.html', context)

@login_required
def get_criteria(request, evaluation_type_id):
    evaluation_type = EvaluationType.objects.get(id=evaluation_type_id)
    criteria = EvaluationCriteria.objects.filter(evaluation_types=evaluation_type)
    
    return JsonResponse({
        'criteria': [
            {'id': c.id, 'name': c.name, 'description': c.description}
            for c in criteria
        ]
    })

@login_required
def get_meeting_members(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    members = meeting.speeches.values_list('orator__id', 'orator__first_name', 'orator__last_name').distinct()
    
    return JsonResponse({
        'members': [
            {'id': m[0], 'name': f"{m[1]} {m[2]}"}
            for m in members
        ]
    })

@login_required
def get_all_criteria(request):
    criteria = EvaluationCriteria.objects.all()
    return JsonResponse({
        'criteria': [
            {'id': c.id, 'name': c.name, 'description': c.description}
            for c in criteria
        ]
    })

@login_required
def get_all_members(request):
    profiles = Profile.objects.select_related('user')
    return JsonResponse({
        'members': [
            {'id': p.id, 'name': f"{p.user.first_name} {p.user.last_name}"}
            for p in profiles
        ]
    })


@login_required
def generate_evaluation_table(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        evaluation = Evaluation.objects.create(
            evaluator=request.user,
            meeting_id=data['meeting_id'],
            evaluation_type_id=data['evaluation_type_id'],
            is_submitted=False
        )
        evaluation.criteria.set(data['criteria_ids'])
        evaluation.profiles.set(data['member_ids'])
        
        return JsonResponse({'success': True})
    

@login_required
def submit_evaluation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        eval_id = data['eval_id']
        answers = data['answers']
        comments = data.get('comments', {})
        
        evaluation = Evaluation.objects.get(id=eval_id, evaluator=request.user)
        
        criteria_map = {c.id: c.name for c in evaluation.criteria.all()}
        level_map = {l.id: l.name for l in EvaluationLevel.objects.all()}
        
        by_profile = {}
        for ans in answers:
            profile_id = ans['profile_id']
            if profile_id not in by_profile:
                by_profile[profile_id] = {}
            criteria_name = criteria_map.get(int(ans['criteria_id']), 'Unknown')
            level_name = level_map.get(int(ans['level_id']), 'Unknown')
            by_profile[profile_id][criteria_name] = level_name
        
        for profile_id, criteria_levels in by_profile.items():
            EvaluationAnswer.objects.create(
                evaluation=evaluation,
                profile_id=profile_id,
                data=criteria_levels,
                comment=comments.get(str(profile_id), '')
            )
        
        evaluation.is_submitted = True
        evaluation.save()

        create_progression(evaluation)
        
        return JsonResponse({'success': True})
    

@login_required
def show_evaluation_answer(request, answer_id):
    answer = get_object_or_404(EvaluationAnswer, id=answer_id, profile=request.user.profile)
    
    return render(request, 'speechs/evaluation_answer_detail.html', {
        'answer': answer
    })


@login_required
def get_comment(request, eval_id, profile_id):
    comment = request.session.get(f"comment_{eval_id}_{profile_id}", "")
    return JsonResponse({'comment': comment})

@login_required
def save_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session[f"comment_{data['eval_id']}_{data['profile_id']}"] = data['comment']
        return JsonResponse({'success': True})
    

def create_progression(evaluation):
    """Crée une Progression après une évaluation soumise"""
    from django.db.models import Avg
    
    meeting = evaluation.meeting
    user = evaluation.evaluator 
    
    answers = EvaluationAnswer.objects.filter(evaluation=evaluation)
    
    field_scores = {
        'pertinence': [],
        'eloquence': [],
        'structure': [],
        'time_gestion': []
    }
    
    for answer in answers:
        criteria_list = evaluation.criteria.all()
        for criteria in criteria_list:
            level_name = answer.data.get(criteria.name)
            level = EvaluationLevel.objects.get(name=level_name)

            field = criteria.progression_field
            field_scores[field].append(level.points)
    
    progression_data = {}
    for field, scores in field_scores.items():
        if scores:
            avg = sum(scores) / len(scores)
            percentage = (avg / 5) * 100 
            progression_data[field] = int(percentage)
        else:
            progression_data[field] = 0
    
    progression, created = Progression.objects.get_or_create(
        user=user,
        meeting=meeting,
        defaults={
            'pertinence': progression_data['pertinence'],
            'time_gestion': progression_data['time_gestion'],
            'eloquence': progression_data['eloquence'],
            'structure': progression_data['structure'],
        }
    )
    
    if not created:
        progression.pertinence = progression_data['pertinence']
        progression.time_gestion = progression_data['time_gestion']
        progression.eloquence = progression_data['eloquence']
        progression.structure = progression_data['structure']
        progression.save()
    
    return progression