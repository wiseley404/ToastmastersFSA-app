from django.db import models

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

    class Meta:
        unique_together = ('profile', 'role')


    def __str__(self):
        return f"{self.profile.user.get_full_name().title()} - {self.role.title.title()}"
    

    
