from django.shortcuts import get_object_or_404, redirect, render
from .forms import BoardProfileForm, MemberProfileForm
from .models import BoardProfile
from members.models import Profile
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
def show_settings(request):
    section_active = request.GET.get('section', 'personnel')
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


def show_stats(request):
    return render(request, 'core/show_stats.html', {'section_active':'statistiques'})


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