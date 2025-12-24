from django.db import models
from django.contrib.auth.models import User
from meetings.models import Meeting
from phonenumber_field.modelfields import PhoneNumberField
import os



# Create your models here.
class Statut(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Curriculum(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


def upload_profile_photo(instance, filename):
    return os.path.join('profiles', f'utilisateur_{instance.user.id}', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to=upload_profile_photo, blank=True, null=True)
    statuts = models.ManyToManyField(Statut, default='Membre', blank=True, related_name='profiles')
    telephone = PhoneNumberField(region='CA', blank=True, null=True)
    Curriculums = models.ManyToManyField(Curriculum, blank=True, related_name='profiles')

    def __str__(self):
        return self.user.get_full_name()
    
    @property
    def get_roles_performed(self):
        from speechs.models import Speech
        return Speech.objects.filter(orator=self.user).count()

    @property
    def get_certificats_won(self):
        from speechs.models import Certificat
        return Certificat.objects.filter(speech__orator=self.user).count()
    

class Progression(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progressions')
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='progressions')
    pertinence = models.IntegerField(default=0)
    time_gestion = models.IntegerField(default=0)
    eloquence = models.IntegerField(default=0)
    structure = models.IntegerField(default=0)

    def __str__(self):
        return f"Seance du {self.meeting.date}"

    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']  # plus récentes d'abord

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"


