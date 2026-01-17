from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Form (models.Model):
    title = models.TextField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    date = models.DateField(default=datetime.now)
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    in_creation_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.date}"
    
    def submissions_numbers(self):
        return self.submissions.count()
    

class Field(models.Model):
    TYPES_CHOIX=[
        ('text', 'Réponse courte'),
        ('textarea', 'Texte long'),
        ('select', 'Liste déroulante'),
        ('radio', 'Choix unique'),
        ('checkbox', 'Choix multiple'),
    ]

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='fields')
    type = models.CharField(max_length=20, choices=TYPES_CHOIX)
    description = models.TextField(max_length=200)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.description
    
    def stats_per_option(self):
        if self.type in ['select', 'radio', 'checkbox']:
            return (
                self.responses
                .values('option__valeur')
                .annotate(total=models.Count('id')).order_by('-total')
            )
        return {}
    
    def  top_responses(self):
        counts = (
            self.responses
            .annotate(valeur_lower=models.functions.Lower('value'))
            .values('valeur_lower')
            .annotate(total=models.Count('id'))
        )

        max_total = counts.aggregate(max_total=models.Max('total'))['max_total']
        if max_total is None:
            return None, 0
        
        max_values = [data['valeur_lower'].title() for data in counts if data['total'] == max_total]
        return max_values, max_total

        
class Option(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='options')
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.value} de {self.field.description}"
    

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='submissions')
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='submissions')
    submitted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'form')

    def __str__(self):
        return f"{self.form.title}"


class Response(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='responses')
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='responses')
    value = models.TextField()

    def __str__(self):
        return self.value