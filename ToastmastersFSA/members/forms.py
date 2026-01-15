from django import forms
from .models import Profile, Statut, Curriculum


class ProfileForm(forms.ModelForm):
    remove_photo = forms.BooleanField(
        required=False,
        label="Supprimer la photo actuelle"
    )

    class Meta:
        model = Profile
        fields = ['photo', 'telephone', 'curriculum']
