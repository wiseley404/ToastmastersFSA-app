from django import forms
from .models import Profile, Statut, Curriculum


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'statut', 'telephone', 'curriculum')
        

class UpdatePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class UpdatePhoneNumberForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telephone']


class UpdateStatutForm(forms.ModelForm):
    statut = forms.ModelMultipleChoiceField(
        queryset=Statut.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Profile
        fields = ['statut']
        

class UpdateCurriculumForm(forms.ModelForm):
    curriculum = forms.ModelMultipleChoiceField(
        queryset=Curriculum.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Profile
        fields = ['curriculum']