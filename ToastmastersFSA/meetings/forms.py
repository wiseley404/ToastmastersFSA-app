from django import forms
from .models import Meeting, Ressources

class MeetingForm(forms.ModelForm):

    class Meta:
        model = Meeting
        fields = ("date", "start_time", "end_time", "theme", "highlight_word", "format", "type", "attribution_role", "location", "url")
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'end_time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'location': forms.Textarea(attrs={
                'placeholder': 'Ex: Pavillon Palasis-Prince, local 1609',
                'rows': 5, 
                'cols': 30,
                'style': 'resize:none;'}
            ),
            'url': forms.URLInput(attrs={
                'placeholder': 'zoom ou Teams, si en ligne.'}),
        }



class RessourcesForm(forms.ModelForm):
    class Meta:
        model = Ressources
        fields = ['title', 'description', 'type', 'file', 'url']
        widgets = {
            'url': forms.URLInput(attrs={'placeholder':'Si youtube ou website :)'})
        }