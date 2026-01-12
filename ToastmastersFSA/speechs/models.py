from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Speech(models.Model):
    title = models.TextField(max_length=255, blank=True, null=True)
    orator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='speeches', null=False)
    meeting = models.ForeignKey('meetings.Meeting', on_delete=models.CASCADE, related_name='speeches')
    role = models.ForeignKey('meetings.Role', on_delete=models.CASCADE, related_name='speeches')
    votes = models.PositiveIntegerField(default=0)


    @property
    def date(self):
        return self.meeting.date
    

    def __str__(self):
        return f"{self.role.title.title()} .-{self.orator.get_full_name()} - {self.date}"
    

class Certificat(models.Model):
    TITRE_CHOICES = [
        ('Meilleur discours', 'Meilleur discours'),
        ('Meilleure improvisation', 'Meilleure improvisation'),
        ('Meilleure évaluation', 'Meilleure évaluation'),
        ('Meilleur français', 'Meilleur français'),
        ('Meilleure amélioration', 'Meilleure amélioration'),
        
    ]
    speech = models.OneToOneField('speechs.Speech', on_delete=models.CASCADE, related_name='certificat')
    title = models.CharField(max_length=100, choices=TITRE_CHOICES)
    issue_date = models.DateField()
    is_won = models.BooleanField(default=False)
    file = models.FileField(upload_to='certificats/', blank=True, null=True)


    def __str__(self):
        return self.title


class EvaluationType(models.Model):
    TYPES = [
        ('grammaire', 'Grammaire'),
        ('gestion_temps', 'Gestion du temps'),
        ('improvisation', 'Improvisation'),
        ('discours_prepare', 'Discours préparé'),
        ('evaluation_generale', 'Évaluation générale'),
    ]
    name = models.CharField(max_length=50, choices=TYPES, unique=True)

    def __str__(self):
        return self.get_name_display()

class EvaluationLevel(models.Model):
    name = models.CharField(max_length=50, unique=True) 
    points = models.IntegerField()
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class EvaluationCriteria(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True) 
    evaluation_types = models.ManyToManyField(EvaluationType)
    progression_field = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Evaluation(models.Model):
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey('meetings.Meeting', on_delete=models.CASCADE)
    evaluation_type = models.ForeignKey(EvaluationType, on_delete=models.CASCADE)
    profiles = models.ManyToManyField('members.Profile') 
    criteria = models.ManyToManyField(EvaluationCriteria)
    is_submitted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


class EvaluationAnswer(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='answers')
    profile = models.ForeignKey('members.Profile', on_delete=models.CASCADE)
    data = models.JSONField(default=dict)
    comment = models.TextField(blank=True, null=True)

    
    
