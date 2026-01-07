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
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom de la liste e-mail'
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
        widgets = {
            'message': forms.Textarea(attrs={'rows': 10}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'send_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class SystemEmailForm(forms.ModelForm):
    class Meta:
        model = SystemEmail
        exclude = ['code',]
        widgets = {
            'body': forms.Textarea(attrs={'rows': 10}),
        }


class AbsenceEmailConditionForm(forms.ModelForm):
    class Meta:
        model = AbsenceEmailCondition
        fields = ['absence_count',]