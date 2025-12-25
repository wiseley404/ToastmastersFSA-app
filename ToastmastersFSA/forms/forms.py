from django import forms
from .models import Form, Field, Option
from speechs.models import Speech
from datetime import datetime
from django.db import transaction


def make_form(form):
    fields = {}
    for field in form.fields.all():
        choice = [(option.value, option.value) for option in field.options.all()]
        if field.type == 'text':
            fields[field.description] = forms.CharField(required=field.required)
        elif field.type == 'select': 
            fields[field.description] = forms.ChoiceField(
                widget=forms.Select,
                choices=choice, 
                required=field.required
            )
        elif field.type == 'textarea':
            fields[field.description] = forms.CharField(required=field.required)
        elif field.type == 'radio':
            fields[field.description] = forms.ChoiceField(
                widget=forms.RadioSelect,
                choices=choice,
                required=field.required
            )
        else:
            fields[field.description] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                choices=choice,
                required=field.required
            )
    
    Form = type('Form', (forms.Form,), fields)
    return Form



class FormForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ("title", "description", "date")
        widgets = {
            'date':forms.DateInput(attrs={'type':'date'})
        }


class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ("description", "required", "type")
        widgets ={
            'description': forms.Textarea(attrs={
                'placeholder': 'EX: Meilleur discours/ Meilleure improvisation'
            })
        }
FieldFormSet = forms.inlineformset_factory(
    Form, Field,
    fields=('description', 'required', 'type'),
    extra=1,  # to add an empty default field 
    can_delete=True  # to delete fields
)

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['value']


def create_or_update_form(meeting):

    if datetime.today().date() >= meeting.date:
        return

    with transaction.atomic():
        form, _ = Form.objects.get_or_create(
            date=meeting.date,
            defaults={
                'title': 'Toastmasters Votes',
                'description': 'Votez pour le(la) meilleur(e).',
                'is_published': False,
                'is_active': False,
                'in_creation_mode': True
            }
        )

        def add_unique_option(description_field, type_field, value, required=True):
            field, _ = Field.objects.get_or_create(
                formulaire=form,
                description=description_field,
                defaults={'type': type_field, 'required': required}
            )
            if not Option.objects.filter(field=field, value=value).exists():
                Option.objects.create(field=field, value=value)


        for speech in Speech.objects.filter(meeting=meeting, role__title='Discours préparé'):
            add_unique_option(
                'Meilleur discours',
                'radio',
                speech.orator.get_full_name().title()
            )


        for speech in Speech.objects.filter(meeting=meeting, role__title='Discours improvisé'):
            add_unique_option(
                'Meilleure improvisation',
                'radio',
                speech.orator.get_full_name().title()
            )


        roles_eval = [
            'Évaluateur(rice) des improvisations',
            'Évaluateur(rice) de discours',
            'Chronométreur(se)',
            'Grammairien(ne)'
        ]
        for speech in Speech.objects.filter(meeting=meeting, role__title__in=roles_eval):
            add_unique_option(
                'Meilleure évaluation',
                'radio',
                speech.orator.get_full_name().title()
            )


        Field.objects.get_or_create(
            form=form,
            description='Meilleur Français',
            defaults={'type': 'text', 'obligatoire': True}
        )
        Field.objects.get_or_create(
            form=form,
            description='Meilleure amélioration',
            defaults={'type': 'text', 'required': True}
        )




