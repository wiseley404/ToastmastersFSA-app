from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from members.models import Curriculum


class CustomUserCreatioForm(UserCreationForm):
    last_name = forms.CharField(required=True, max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Nom'}))
    first_name = forms.CharField(required=True, max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Prénom'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    curriculum = forms.ModelChoiceField(
        queryset= Curriculum.objects.all(),
        empty_label='Choisissez votre programme'
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez le mot de passe'}))


    class Meta:
        model = User
        fields = ("last_name", "first_name", "username", "email", "curriculum", "password1", "password2")

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email
    

    def save_user(self, commit=True):
        user = super().save(commit=False)
        user.last_name= self.cleaned_data['last_name']
        user.first_name= self.cleaned_data['first_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False
            user.save()
        return user
    

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nouveau mot de passe'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Entrez à nouveau'}))


class CustomAuthentificationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur ou Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))
    error_messages = {
        "invalid_login": "Nom d’utilisateur ou mot de passe incorrect.",
    }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Ancien mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Ancien mot de passe"})
    )
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Nouveau mot de passe"})
    )
    new_password2 = forms.CharField(
        label="Confirmation",
        widget=forms.PasswordInput(attrs={"placeholder": "Password Confirmation"})
    )
