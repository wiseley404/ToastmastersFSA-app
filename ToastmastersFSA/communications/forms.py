from django import forms
from .models import Notification, EmailList
from members.models import Profile

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'message']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Titre de la notification'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Contenu du message...'
            })
        }
        labels = {
            'title': 'Titre',
            'message': 'Message'
        }


class EmailListForm(forms.ModelForm):
    class Meta:
        model = EmailList
        fields = ['title', 'members']
        widgets = {
            'members': forms.SelectMultiple(attrs={'class': 'select2-members'})
        }
        labels = {
            'title': 'Titre',
            'members': 'Membres'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].queryset = Profile.objects.all()[:10]  # Limite 10 pour test

