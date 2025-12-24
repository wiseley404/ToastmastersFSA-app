from django.contrib import admin
from .models import Meeting, Role, Ressources


class MeetingAdmin(admin.ModelAdmin):
    list_display = ("date", "start_time", "end_time", "location", "url")
    list_filter = ("date",)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('title','min_secondes_duration', 'max_secondes_duration')

class RessourcesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'type', 'file', 'url', 'creation_date')

# Register your models here.
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Ressources, RessourcesAdmin)