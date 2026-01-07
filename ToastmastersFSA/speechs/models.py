from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Speech(models.Model):
    title = models.TextField(max_length=255, blank=True, null=True)
    orator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='speech', null=False)
    meeting = models.ForeignKey('meetings.Meeting', on_delete=models.CASCADE, related_name='speech')
    role = models.ForeignKey('meetings.Role', on_delete=models.CASCADE, related_name='speech')
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


class Evaluation(models.Model):
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations_done')
    speech = models.ForeignKey('speechs.Speech', on_delete=models.CASCADE, related_name='evaluations_received')
    date = models.DateTimeField(auto_now_add=True)
    pertinence = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    structure = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    clarte = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    eloquence = models.PositiveSmallIntegerField(default=0, blank=True, null=True)


    def __str__(self):
        return f'Evaluation de {self.evaluator} pour le discours de {self.speech.orator}'
    
    @property
    def get_type(self):
        return self.evaluator.evaluations_done.speech.role
    
    
