from django.shortcuts import get_object_or_404, redirect, render
from .forms import BoardProfileForm, MemberProfileForm
from core.models import SocialLink
from .models import BoardProfile
from members.models import Profile
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from django.http import JsonResponse
from django.template.loader import render_to_string
from datetime import datetime, timedelta
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q, F
from django.db.models.functions import TruncMonth
from meetings.models import Meeting, MeetingAttendance, Role
from speechs.models import Speech, Certificat
from core.models import BoardProfile


# Create your views here.
def show_settings(request):
    section_active = request.GET.get('section', 'club')
    comite = BoardProfile.objects.filter(is_active=True)
    club_members = Profile.objects.select_related('user').order_by(
        'user__last_name',
        'user__first_name'
    )
    context = {
        'section_active': 'parametres',
        'current_section': section_active,
        'comite': comite,
        'club_members': club_members,
    }
    return render(request, 'core/show_settings.html', context)




@login_required
def show_stats(request):
    # Filters
    period = request.GET.get('period', 'all')
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    
    today = datetime.now().date()
    
    if period == 'custom' and date_from and date_to:
        start_date = datetime.strptime(date_from, '%Y-%m-%d').date()
        end_date = datetime.strptime(date_to, '%Y-%m-%d').date()
    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif period == 'month':
        start_date = today.replace(day=1)
        end_date = today
    elif period == 'year':
        start_date = today.replace(month=1, day=1)
        end_date = today
    else:  # all
        start_date = None
        end_date = today
    
    meeting_filters = {}
    if start_date:
        meeting_filters['date__gte'] = start_date
    meeting_filters['date__lte'] = end_date


    # Stats
    last_meetings = Meeting.objects.filter(
        date__lte=end_date
    ).order_by('-date')[:3]

    if last_meetings.exists():
        active_members = Profile.objects.filter(
            meeting_attendances__meeting__in=last_meetings,
            meeting_attendances__is_present=True
        ).distinct().count()
    else:
        active_members = 0  

    new_members_count = 0
    if start_date:
        new_members_count = Profile.objects.filter(
            user__date_joined__gte=start_date,
            user__date_joined__lte=end_date
        ).count()
    
    # Meetings
    meetings = Meeting.objects.filter(**meeting_filters)
    total_meetings = meetings.count()
    meetings_this_period = total_meetings
    
    # Speech data
    speeches = Speech.objects.filter(meeting__in=meetings)
    prepared_speech_role = Role.objects.filter(title__icontains='préparé').first()

    if prepared_speech_role:
        total_speeches = speeches.filter(role=prepared_speech_role).count()
    else:
        total_speeches = 0

    avg_speeches_per_meeting = total_speeches / total_meetings if total_meetings > 0 else 0
    
    # Presence rate
    attendances = MeetingAttendance.objects.filter(meeting__in=meetings)
    total_attendances = attendances.count()
    present_count = attendances.filter(is_present=True).count()
    attendance_rate = (present_count / total_attendances * 100) if total_attendances > 0 else 0
    
    if start_date:
        period_length = (end_date - start_date).days
        prev_start = start_date - timedelta(days=period_length)
        prev_end = start_date - timedelta(days=1)
        
        prev_attendances = MeetingAttendance.objects.filter(
            meeting__date__gte=prev_start,
            meeting__date__lte=prev_end
        )
        prev_total = prev_attendances.count()
        prev_present = prev_attendances.filter(is_present=True).count()
        prev_rate = (prev_present / prev_total * 100) if prev_total > 0 else 0
        
        attendance_trend = attendance_rate - prev_rate
    else:
        attendance_trend = 0
    
    # Chart Data

    months_labels = []
    members_data = []  
    new_members_data = []  

    for i in range(5, -1, -1):  

        month_date = (today.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        months_labels.append(month_date.strftime('%b'))
        
        if month_date.month == 12:
            next_month = month_date.replace(year=month_date.year + 1, month=1)
        else:
            next_month = month_date.replace(month=month_date.month + 1)
        
        # last 3 meetings
        last_3_meetings_of_month = Meeting.objects.filter(
            date__lt=next_month
        ).order_by('-date')[:3]
        
        if last_3_meetings_of_month.exists():
            active_count = Profile.objects.filter(
                meeting_attendances__meeting__in=last_3_meetings_of_month,
                meeting_attendances__is_present=True
            ).distinct().count()
        else:
            active_count = 0
        
        members_data.append(active_count)
        
        new_in_month = Profile.objects.filter(
            user__date_joined__year=month_date.year,
            user__date_joined__month=month_date.month
        ).count()
        new_members_data.append(new_in_month)
    
    # Meetings by month
    meetings_labels = []
    meetings_data = []
    
    for i in range(6):
        month_date = today.replace(day=1) - timedelta(days=30*i)
        month_date = month_date.replace(day=1)
        meetings_labels.insert(0, month_date.strftime('%b'))
        
        count = Meeting.objects.filter(
            date__year=month_date.year,
            date__month=month_date.month
        ).count()
        
        meetings_data.insert(0, count)
    
    # Presence rate
    attendance_labels = []
    attendance_data = []
    
    for i in range(6):
        month_date = today.replace(day=1) - timedelta(days=30*i)
        month_date = month_date.replace(day=1)
        attendance_labels.insert(0, month_date.strftime('%b'))
        
        month_meetings = Meeting.objects.filter(
            date__year=month_date.year,
            date__month=month_date.month
        )
        
        month_attendances = MeetingAttendance.objects.filter(meeting__in=month_meetings)
        month_total = month_attendances.count()
        month_present = month_attendances.filter(is_present=True).count()
        
        rate = (month_present / month_total * 100) if month_total > 0 else 0
        attendance_data.insert(0, round(rate, 1))
    
    
    # Top active members
    top_members = []
    for profile in Profile.objects.all()[:10]:
        speeches_count = Speech.objects.filter(
            orator=profile.user,
            meeting__in=meetings
        ).count()
        
        member_attendances = MeetingAttendance.objects.filter(
            member=profile,
            meeting__in=meetings
        )
        total_att = member_attendances.count()
        present_att = member_attendances.filter(is_present=True).count()
        att_rate = (present_att / total_att * 100) if total_att > 0 else 0
        
        if speeches_count > 0 or att_rate > 0:
            top_members.append({
                'name': profile.user.get_full_name() or profile.user.username,
                'speeches_count': speeches_count,
                'roles_count': speeches_count, 
                'attendance_rate': round(att_rate, 1),
                'certificats_count': Certificat.objects.filter(
                    speech__orator=profile.user,
                    is_won=True
                ).count()
            })
    
    top_members = sorted(top_members, key=lambda x: x['speeches_count'], reverse=True)[:5]
    
    roles_distribution = []
    total_speeches_count = speeches.count()
    
    for role in Role.objects.all():
        count = speeches.filter(role=role).count()
        if count > 0:
            percentage = (count / total_speeches_count * 100) if total_speeches_count > 0 else 0
            roles_distribution.append({
                'title': role.title,
                'count': count,
                'percentage': round(percentage, 1)
            })
    
    roles_distribution = sorted(roles_distribution, key=lambda x: x['count'], reverse=True)
    
    total_certificats = Certificat.objects.filter(
        speech__meeting__in=meetings,
        is_won=True
    ).count()
    
    online_meetings = meetings.filter(format='en ligne').count()
    in_person_meetings = meetings.filter(format='présentiel').count()
    
    active_board_members = BoardProfile.objects.filter(is_active=True).count()
    
    context = {
        'section_active': 'statistiques',
        
        # Filters
        'current_period': period,
        'date_from': date_from,
        'date_to': date_to,
        
        # others
        'total_members': Profile.objects.all().count(),
        'active_members': active_members,
        'new_members': new_members_count,
        'total_meetings': total_meetings,
        'meetings_this_period': meetings_this_period,
        'total_speeches': total_speeches,
        'avg_speeches_per_meeting': round(avg_speeches_per_meeting, 1),
        'attendance_rate': round(attendance_rate, 1),
        'attendance_trend': round(attendance_trend, 1),
        
        'total_certificats': total_certificats,
        'online_meetings': online_meetings,
        'in_person_meetings': in_person_meetings,
        'active_board_members': active_board_members,
        
        'members_labels': json.dumps(months_labels),
        'members_data': json.dumps(members_data),
        'new_members_data': json.dumps(new_members_data),
        
        'meetings_labels': json.dumps(meetings_labels),
        'meetings_data': json.dumps(meetings_data),
        
        'attendance_labels': json.dumps(attendance_labels),
        'attendance_data': json.dumps(attendance_data),

        'top_members': top_members,
        'roles_distribution': roles_distribution,
    }
    
    return render(request, 'core/show_stats.html', context)


def add_member_to_board(request):
    if request.method == 'POST':
        form = BoardProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            html = render_to_string('core/add_member_to_board.html', {'form': form}, request)
            return JsonResponse({'success': False, 'html': html})
    else:
        form = BoardProfileForm()

    context = {
        'form': form,
        'section_active': 'parametres',
    }
    return render(request, 'core/add_member_to_board.html', context)


def edit_board_role(request, board_profile_id):
    board_profile = get_object_or_404(BoardProfile, id=board_profile_id)
    if request.method == 'POST':
        form = BoardProfileForm(request.POST, instance=board_profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            html = render_to_string('core/edit_board_role.html', {
                'form': form,
                'board_profile': board_profile
            }, request)
            return JsonResponse({'success': False, 'html': html})
    else:
        form = BoardProfileForm(instance=board_profile)
    context = {
        'form': form,
        'board_profile': board_profile,
    }
    return render(request, 'core/edit_board_role.html', context)


@staff_member_required
def confirm_board_profile_remove(request, board_profile_id):
    board_profile = get_object_or_404(BoardProfile, id=board_profile_id)
    return render(request, 'core/remove_board_profile.html', {'board_profile':board_profile})


@staff_member_required
def remove_board_profile(request, board_profile_id):
    board_profile = get_object_or_404(BoardProfile, id=board_profile_id)
    if board_profile:
        board_profile.is_active = False
        board_profile.end_date = now().date()
        board_profile.save() 
    return redirect('settings')



def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            html = render_to_string('core/edit_member_profile.html', {
                'form': form,
                'profile': profile
            }, request)
            return JsonResponse({'success': False, 'html': html})
    else:
        form = MemberProfileForm(instance=profile)
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'core/edit_member_profile.html', context)



@staff_member_required
def update_social_links(request):
    if request.method == 'POST':
        platforms = ['facebook', 'instagram', 'linkedin', 'twitter', 'youtube', 'tiktok', 'contact']
        
        for platform in platforms:
            url = request.POST.get(platform, '').strip()
            
            if url:
                SocialLink.objects.update_or_create(
                    platform=platform,
                    defaults={'url': url}
                )
            else:
                SocialLink.objects.filter(platform=platform).delete()
        
        return redirect(request.META.get('HTTP_REFERER', 'settings'))
    return redirect(request.META.get('HTTP_REFERER', 'settings'))