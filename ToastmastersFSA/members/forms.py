from django import forms
from .models import Profile, Statut, Curriculum


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'telephone', 'curriculums')
        

class UpdatePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class UpdatePhoneNumberForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telephone']


class UpdateStatutsForm(forms.ModelForm):
    statuts = forms.ModelMultipleChoiceField(
        queryset=Statut.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Profile
        fields = ['statuts']
        

class UpdateCurriculumsForm(forms.ModelForm):
    curriculums = forms.ModelMultipleChoiceField(
        queryset=Curriculum.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Profile
        fields = ['curriculums']