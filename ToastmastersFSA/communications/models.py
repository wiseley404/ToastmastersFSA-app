from django.db import models
from django.contrib.auth.models import User
from members.models import Profile

# Create your models here.
class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    recipients = models.ManyToManyField(Profile, blank=True, related_name='notifications')
    title = models.CharField(max_length=200) 
    message = models.TextField(max_length=1000) 
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.message[:30]}..."
    

class EmailList(models.Model):
    title = models.CharField(max_length=300)
    members = models.ManyToManyField('members.Profile', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title
    
    @property
    def total_members(self):
        return self.members.count()
