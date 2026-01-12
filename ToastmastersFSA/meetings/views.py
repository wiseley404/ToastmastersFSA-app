import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import Meeting, MeetingAttendance, Ressources
from .forms import MeetingForm, RessourcesForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from datetime import date, timedelta
from django.utils.timezone import now
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import Q
from django.db.models.functions import TruncMonth


# Create your views here.
@login_required
def show_meeting_infos(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    return render(request, 'meetings/meeting_infos.html', {'meeting': meeting})

@login_required
def show_meetings_list(request):
    today = now()
    meetings = Meeting.objects.filter(
        Q(date=today.date(), end_time__gt=today.time()) |  
        Q(date__gt=today.date())
    ).order_by('date', 'start_time')

    unique_months = meetings.annotate(
        month=TruncMonth('date')
    ).values_list('month', flat=True).distinct().order_by('month')

    meetings_months = [{
        "value": d.strftime("%Y-%m"),
        "date": d 
    } for d in unique_months]

    past_meetings = Meeting.objects.filter(
        Q(date=today.date(), end_time__lt=today.time()) |  
        Q(date__lt=today.date())
    ).order_by('-date', '-end_time')

    # Format filter
    selected_format = request.GET.get("format", "")
    if selected_format:
        past_meetings = past_meetings.filter(format=selected_format)

    # Type filter
    selected_type = request.GET.get("type", "")
    if selected_type:
        past_meetings = past_meetings.filter(type=selected_type)

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
    
    context = {
        'past_meetings': past_meetings,
        'format_choices': Meeting._meta.get_field('format').choices,
        'type_choices': Meeting._meta.get_field('type').choices,
        'meetings': meetings,
        'meetings_months': meetings_months,
        'selected_format': selected_format,
        'selected_type': selected_type,
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
            return JsonResponse({'success': True})
        else:
            html = render_to_string('meetings/create_meeting.html', {'meeting': form}, request)
            return JsonResponse({'success': False, 'html': html})
    else:
        form = MeetingForm()
    return render(request, 'meetings/create_meeting.html', {'meeting': form})


@login_required
def create_meeting_pdf_download(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)

    html_string = render_to_string('meetings/meeting_pdf.html', {'meeting': meeting})
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
    return render(request, 'meetings/show_ressources.html', {
        'ressources':ressources, 'section_active': 'ressources'})


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
def confirm_ressource_deletion(request, ressource_id):
    ressource = get_object_or_404(Ressources, id=ressource_id)
    return render(request, 'meetings/delete_ressource.html', {'ressource':ressource})


@staff_member_required
def delete_ressources(request, ressource_id):
    ressource = get_object_or_404(Ressources, id=ressource_id)
    if ressource:
        ressource.delete()
    return redirect('show_ressources')



@staff_member_required
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            html = render_to_string('meetings/edit_meeting.html', {'form': form, 'meeting':meeting}, request)
            return JsonResponse({'success': False, 'html': html})
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'meetings/edit_meeting.html', {'form': form, 'meeting':meeting})


@staff_member_required
def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if meeting:
        meeting.delete()
    return redirect('meetings_list')



@login_required
def check_attendance(request):
    current_time = now()
    print(f"Current time: {current_time}")
    print(f"Date: {current_time.date()}, Time: {current_time.time()}")
    
    meeting = Meeting.objects.filter(
        date=current_time.date(),
        start_time__lte=current_time.time(),
        end_time__gte=current_time.time()
    ).first()
    
    print(f"Meeting found: {meeting}")
    # ...
    if meeting:
        attendance, created = MeetingAttendance.objects.get_or_create(
            meeting=meeting,
            member=request.user.profile
        )
        if attendance.confirmed_at is None:
            return JsonResponse({'meeting_id': meeting.id, 'date': meeting.date})

    return JsonResponse({})


@login_required
def confirm_attendance(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    data = json.loads(request.body)
    is_present = data.get('is_present')
    
    attendance = MeetingAttendance.objects.get(
        meeting=meeting,
        member=request.user.profile
    )
    attendance.is_present = is_present
    attendance.confirmed_at = now()
    attendance.save()
    
    return JsonResponse({'success': True})