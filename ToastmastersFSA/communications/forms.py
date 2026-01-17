from django import forms
from .models import Notification, EmailList, EmailScheduled, SystemEmail, AbsenceEmailCondition

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
            'title': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom de la liste e-mail',
                'rows':1,
                'style': 'resize:vertical;',
            }),
            'members': forms.SelectMultiple(
                attrs={
                    'id': 'id_members',
                    'class': 'form-control',
                }
            )
        }
        labels = {
            'title': 'Titre',
            'members': 'Membres'
        }


class EmailScheduledForm(forms.ModelForm):
    class Meta:
        model = EmailScheduled
        exclude = ['attachments', 'created_by', 'created_at', 'last_sent_at', 'is_active']
        labels = {
            'title': 'Objet',
            'message': 'Message',
            'start_date':'Date de debut',
            'end_date':'Date de fin',
            'send_time': 'Heure d\'envoi',
            'to_emails':'Aux emails',
            'to_profiles':'Aux profiles',
            'to_lists':'Aux listes de diffusion',
            'send_now': 'Envoyer maintenant',
            'frequency': 'Frequence',

        }
        widgets = {
            'title': forms.Textarea(attrs={
                'rows': 1,
                'style': 'resize: vertical;',
                'placeholder': "L'objet de votre message...",
            }),
            'message': forms.Textarea(attrs={
                'rows': 10,
                'style': 'resize: vertical;',
                'placeholder': 'Le contenu de votre message...'
            }),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'send_time': forms.TimeInput(attrs={'type': 'time'}),
            'to_emails': forms.Textarea(attrs={
                'rows': 2,
                'style': 'resize: vertical;',
                'placeholder': 'Un email par ligne...'
            }),
            'to_profiles': forms.SelectMultiple(attrs={
                'class': 'select2-profiles'
            }),
            'to_lists': forms.SelectMultiple(attrs={
                'class': 'select2-lists'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', "La date de fin ne peut pas être avant la date de début.")

        return cleaned_data


class SystemEmailForm(forms.ModelForm):
    class Meta:
        model = SystemEmail
        exclude = ['code',]
        widgets = {
            'body': forms.Textarea(attrs={'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.code in ['ROLE_ATTRIBUTION', 'MEETING_ALERT'] :
            self.fields['send_offset'].widget = forms.HiddenInput()



class AbsenceEmailConditionForm(forms.ModelForm):
    class Meta:
        model = AbsenceEmailCondition
        fields = ['absence_count',]