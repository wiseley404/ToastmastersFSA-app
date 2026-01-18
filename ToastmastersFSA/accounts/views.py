from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CustomUserCreatioForm
from allauth.account.models import EmailAddress
from allauth.account.views import ConfirmEmailView
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def signup(request):
    if request.method == 'POST':
        signup_form = CustomUserCreatioForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save_user()
            user.profile.curriculum = signup_form.cleaned_data['curriculum']
            user.profile.save()
            email, _ = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                defaults={"primary": True, "verified": False},
            )
            email.send_confirmation(request)
            return render(request, 'accounts/authentication.html', {
                'signup_form': CustomUserCreatioForm(),
                'message': 'Un email de vérification a été envoyé pour pouvoir connecter.'
            })
    else:
        signup_form = CustomUserCreatioForm()
    return render(request, 'accounts/authentication.html', {'signup_form': signup_form})



class MyConfirmEmailView(ConfirmEmailView):
    template_name = "accounts/confirm_email.html"  


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Mot de passe modifié avec succès')
            return JsonResponse({
                'success': True,
                'message': 'Mot de passe modifié avec succès',
                'redirect_url':reverse('edit_profile'),
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'accounts/password_change.html', {'form': form})


def show_home_page(request):
    return redirect('login')
