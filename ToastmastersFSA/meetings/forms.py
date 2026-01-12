from django import forms
from .models import Meeting, Ressources
from django.utils.timezone import now

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ("date", "start_time", "end_time", "theme", "highlight_word", "format", "type", "attribution_role", "location", "url")
        labels = {
            'date': 'Date',
            'start_time': 'Heure de début',
            'end_time': 'Heure de fin',
            'theme': 'Thème',
            'highlight_word': 'Mot du jour',
            'format': 'Format',
            'type': 'Type',
            'attribution_role': 'Attribution des rôles',
            'location': 'Lieu',
            'url': 'URL',
        }
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'min': now().date().__str__(),
                'class': 'form-control',
                'id': 'id_date'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'id': 'id_start_time'
            }, format='%H:%M'),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'id': 'id_end_time'
            }, format='%H:%M'),
            'theme': forms.Textarea(attrs={
                'placeholder': 'Entrez le thème de la réunion',
                'rows': 3,
                'class': 'form-control',
                'style': 'resize: vertical;'
            }),
            'highlight_word': forms.Textarea(attrs={
                'placeholder': 'Mot du jour',
                'rows': 2,
                'cols': 35,
                'class': 'form-control',
                'style': 'resize: vertical;'
            }),
            'format': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Textarea(attrs={
                'placeholder': 'Ex: Pavillon Palasis-Prince, local 1609',
                'rows': 3,
                'class': 'form-control',
                'style': 'resize: vertical;'
            }),
            'url': forms.Textarea(attrs={
                'placeholder': 'zoom ou Teams, si en ligne.',
                'rows': 2,
                'class': 'form-control',
                'style': 'resize: vertical;'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        format_meeting = cleaned_data.get('format')
        location = cleaned_data.get('location')
        url = cleaned_data.get('url')

        if not date or not start_time or not end_time:
            return cleaned_data

        is_new = self.instance.pk is None
        date_changed = is_new or date != self.instance.date
        time_changed = is_new or start_time != self.instance.start_time

        if date_changed or time_changed:
            today = now().date()
            current_time = now().time()

            if date < today:
                self.add_error('date', "La date ne peut pas être dans le passé.")

            if date == today and start_time < current_time:
                self.add_error('start_time', "L'heure de début ne peut pas etre inferieure a l'heure actuelle.")

        if end_time <= start_time:
            self.add_error('end_time', "L'heure de fin doit être après l'heure de début.")

        # Validation format/lieu/url
        if format_meeting == 'présentiel' and not location:
            self.add_error('location', 'Le lieu est obligatoire pour une réunion en présentiel.')

        if format_meeting == 'en ligne' and not url:
            self.add_error('url', "L'URL est obligatoire pour une réunion en ligne.")

        return cleaned_data



class RessourcesForm(forms.ModelForm):
    class Meta:
        model = Ressources
        fields = ['title', 'description', 'type', 'file', 'url']
        widgets = {
            'url': forms.URLInput(attrs={'placeholder':'Si youtube ou website :)'})
        }