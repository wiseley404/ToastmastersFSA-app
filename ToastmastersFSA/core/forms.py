from django import forms
from .models import BoardProfile, BoardRole
from members.models import Profile


class BoardProfileForm(forms.ModelForm):
    class Meta:
        model = BoardProfile
        fields = ('profile', 'role', 'start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile'].queryset = Profile.objects.select_related('user').all()
        self.fields['role'].queryset = BoardRole.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        profile = cleaned_data.get("profile")
        role = cleaned_data.get("role")

        if profile and role:
            exists = BoardProfile.objects.filter(
                profile=profile,
                role=role
            )
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)

            if exists.exists():
                raise forms.ValidationError(
                    "Ce membre a déjà ce rôle."
                )

        return cleaned_data
    

class MemberProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="Prénom")
    last_name = forms.CharField(label="Nom")
    email = forms.EmailField()
    username = forms.CharField()
    
    class Meta:
        model = Profile
        fields = ['telephone', 'statuts', 'curriculums']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username

    def save(self, commit=True):
        profile = super().save(commit=False)

        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']

        if commit:
            user.save()
            profile.save()
            self.save_m2m()

        return profile
