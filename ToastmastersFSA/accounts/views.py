from django.shortcuts import render, redirect
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
        form = CustomUserCreatioForm(request.POST)
        if form.is_valid():
            user = form.save_user()
            user.profile.programmes.add(form.cleaned_data['programme'])
            user.profile.save()
            email, _ = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                defaults={"primary": True, "verified": False},
            )
            email.send_confirmation(request)
            return render(request, 'accounts/signup.html', {
                'form': CustomUserCreatioForm(),
                'message': 'Un email de vérification a été envoyé pour pouvoir connecter.'
            })
    else:
        form = CustomUserCreatioForm()
    return render(request, 'accounts/signup.html', {'form': form})



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
            return redirect('modifier_profil')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'accounts/password_change.html', {'form': form})

