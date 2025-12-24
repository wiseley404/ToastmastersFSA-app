from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import Meeting, Ressources
from .forms import MeetingForm, RessourcesForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import date, timedelta
from django.utils.timezone import now
from django.template.loader import render_to_string
from weasyprint import HTML


# Create your views here.
def show_meeting_infos(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    return render(request, 'meetings/meeting_infos.html', {'meeting': meeting})


def show_meetings_list(request):
    meetings = Meeting.objects.filter(date__gte=date.today()).order_by('date')
    meetings_months = [{
        "value": m.date.strftime("%Y-%m"),
        "label": m.date.strftime("%B %Y")
    } for m in meetings]

    today = now().date()
    past_meetings = Meeting.objects.filter(
        date__lt=today
    ).order_by('date')

    # Format filter
    format = request.GET.get("format")
    if format:
        past_meetings = past_meetings.filter(format=format)

    # Type filter
    type = request.GET.get("type")
    if type:
        past_meetings = past_meetings.filter(type=type)


    # Date filter
    date_filter = request.GET.get("date") 
    if date_filter == "7j":
        past_meetings = past_meetings.filter(date__gte=now() - timedelta(days=7))
    elif date_filter == "14j":
        past_meetings = past_meetings.filter(date__gte=now() - timedelta(days=14))
    elif date_filter == "30j":
        past_meetings = past_meetings.filter(date__gte=now() - timedelta(days=30))
    elif date_filter == "90j":
        past_meetings = past_meetings.filter(date__gte=now() - timedelta(days=90))
    elif date_filter == "365j":
        past_meetings = past_meetings.filter(date__gte=now() - timedelta(days=365))

    section_active = request.GET.get('section', 'personnel')
    context ={
        'past_meetings': past_meetings,
        'formats': [c[1] for c in Meeting._meta.get_field('format').choices],
        'types': [c[1] for c in Meeting._meta.get_field('type').choices],
        'meetings': meetings,
        'meetings_months': meetings_months,
        'section_active': 'reunions',
        'current_section': section_active
    }

    return render(request, 'meetings/meetings_list.html', context)



@staff_member_required
def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('meetings_list'))
    else:
        form = MeetingForm()
    return render(request, 'meetings/create_meeting.html', {'meeting':form})


def create_meeting_pdf_download(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)

    html_string = render_to_string('meetings/meeting_infos.html', {'meeting': meeting})
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="programmation_{meeting.date}.pdf"'
    return response


@staff_member_required
def add_ressources(request):
    if request.method == 'POST':
        form = RessourcesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('show_ressources')
    else:
        form = RessourcesForm()
    return render(request, 'meetings/add_ressources.html', {'form':form})


@login_required
def show_ressources(request):
    ressources = Ressources.objects.all()
    return render(request, 'meetings/show_ressources.html', {'ressources':ressources})


@staff_member_required
def edit_ressources(request, ressource_id):
    ressource = get_object_or_404(Ressources, id=ressource_id)
    if request.method == 'POST':
        form = RessourcesForm(request.POST, request.FILES, instance=ressource)
        if form.is_valid():
            form.save()
            return redirect('show_ressources')
    else:
        form = RessourcesForm(instance=ressource)
    return render(request, 'meetings/edit_ressource.html', {
        'form':form,
        'ressource':ressource
        })


@staff_member_required
def confirm_reesource_deletion(request, ressource_id):
    ressource = get_object_or_404(Ressources, id=ressource_id)
    return render(request, 'meetings/delete_ressource.html', {'ressource':ressource})


@staff_member_required
def delete_ressources(request, ressource_id):
    ressource = get_object_or_404(Ressources, id=ressource_id)
    if ressource:
        ressource.delete()
    return redirect('show_ressources')



@staff_member_required
def edit_meeting(request, reunion_id):
    reunion = get_object_or_404(Meeting, id=reunion_id)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=reunion)
        if form.is_valid():
            form.save()
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        form = MeetingForm(instance=reunion)
    return render(request, 'meetings/edit_meeting.html', {'form':form, 'reunion': reunion})


@staff_member_required
def delete_meeting(request, reunion_id):
    reunion = get_object_or_404(Meeting, id=reunion_id)
    if reunion:
        reunion.delete()
    return redirect('meetings_list')

