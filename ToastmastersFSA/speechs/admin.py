from django.contrib import admin
from .models import Speech, Certificat


class SpeechAdmin(admin.ModelAdmin):
    list_display = ("meeting", "role", "orator", "title", "votes")
    list_filter = ("meeting", "role", "orator")


class CertificatAdmin(admin.ModelAdmin):
    list_display = ('speech', 'title', 'issue_date', 'is_won', 'file')

# Register your models here.
admin.site.register(Speech, SpeechAdmin)
admin.site.register(Certificat, CertificatAdmin)