from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Meeting(models.Model):
    FORMAT_CHOICES = [
        ('en ligne', 'En ligne'),
        ('présentiel', 'Présentiel'),
    ]

    TYPE_CHOICES = [
        ('ordinaire', 'Ordinaire'),
        ('débat', 'Débat'),
        ('concours', 'Concours'),
        ('élections', 'Élections'),
        ('récréative', 'Récréative'),
    ]

    ATTRIBUTION_ROLE_CHOICES = [
        ('manuelle', 'Manuelle'),
        ('automatique', 'Automatique')
    ]

    theme = models.TextField(max_length=64, blank=True, null=True)
    highlight_word = models.CharField(max_length=64, blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='présentiel')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='ordinaire')
    attribution_role = models.CharField(max_length=15, choices=ATTRIBUTION_ROLE_CHOICES, default='manuelle')
    location = models.TextField(max_length=100, null=True)
    url = models.URLField(blank=True, null=True)
    top_grammar = models.CharField(max_length=100, blank=True, null=True)
    top_amelioration = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"Reunion du {self.date}"
    
class MeetingAttendance(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendances')
    member = models.ForeignKey('members.Profile', on_delete=models.CASCADE, related_name='meeting_attendances')
    is_present = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('meeting', 'member')

class Role(models.Model):
    title = models.CharField(max_length=50)
    min_secondes_duration = models.PositiveIntegerField(default=0)
    max_secondes_duration = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title
    

class Ressources(models.Model):
    TYPE_CHOICES =[
        ('video', 'Vidéo'),
        ('youtube', 'Youtube'),
        ('pdf', 'PDF'),
        ('url', 'URL'),
        ('fichier', 'Fichier'),
    ]

    title = models.CharField(max_length=255)
    description =models.TextField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    file = models.FileField(upload_to='ressources/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)


    def icon(self):
        return {
            'video': 'fas fa-video',
            'youtube': 'fab fa-youtube',
            'pdf': 'fas fa-file-pdf',
            'url': 'fas fa-link',
            'fichier': 'fas fa-file',
        }.get(self.type, 'fas fa-file')
    

    def link(self):
        if (self.type == 'url' or self.type == 'youtube') and self.url:
            return self.url
        elif self.file:
            return self.file.url
        return '#'
    

    def __str__(self):
        return self.title
    



    