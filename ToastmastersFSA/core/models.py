from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class BoardRole(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title
    

class BoardProfile(models.Model):
    profile = models.ForeignKey('members.Profile', on_delete=models.CASCADE, related_name='board_roles')
    role = models.ForeignKey(BoardRole, on_delete=models.CASCADE, related_name='members')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.is_active:
            exists = BoardProfile.objects.filter(
                profile=self.profile,
                role=self.role,
                is_active=True
            ).exclude(pk=self.pk).exists()
            
            if exists:
                raise ValidationError(f"Un role de {self.role.title.title()} deja en cours")
            

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.is_active and not self.profile.user.is_staff:
            self.profile.user.is_staff = True
            self.profile.user.save()
        
        elif not self.is_active:
            has_other_active_roles = BoardProfile.objects.filter(
                profile=self.profile, 
                is_active=True
            ).exclude(pk=self.pk).exists()
            
            if not has_other_active_roles:
                self.profile.user.is_staff = False
                self.profile.user.save()

    def __str__(self):
        return f"{self.profile.user.get_full_name().title()} - {self.role.title.title()}"
    

    
