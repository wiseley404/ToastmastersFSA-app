from django import forms
from .models import Speech
from meetings.models import Meeting
from datetime import datetime
from django.contrib.auth.models import User


class SpeechForm(forms.ModelForm):
    theme = forms.CharField(max_length=100, required=False, widget=forms.Textarea(attrs={'class':'form-control'}))
    highlight_word = forms.CharField(max_length=100, required=False)
    orator = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        empty_label="--- Choisir un orateur ---", 
        required=False 
    )

    class Meta:
        model = Speech
        fields = ("orator", "meeting", "role", "title", "theme", "highlight_word")
        widgets={
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meeting'].queryset = Meeting.objects.filter(date__gt=datetime.now())
        self.fields['meeting'].empty_label = "--- Choisir une réunion ---"
        self.fields['role'].empty_label = "--- Choisir un rôle disponible ---"

    
    def save(self, commit = True):
        speech = super().save(commit=False)
        meeting = speech.meeting
        meeting.theme = self.cleaned_data['theme']
        meeting.mot_du_jour = self.cleaned_data['highlight_word']
        meeting.save()
        if commit:
            meeting.save()
        return meeting