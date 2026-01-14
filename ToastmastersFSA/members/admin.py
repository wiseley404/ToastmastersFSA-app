from django.contrib import admin
from .models import Statut, Profile, Curriculum, Progression
from django.utils.html import format_html

# Register your models here.
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('title',)


class StatutAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_last_name', 'get_first_name','get_email',
                     'telephone', 'get_curriculum', 'get_statut', 'get_photo_thumbnail'
                    )
    search_fields = ('user__username', 'user__last_name', 'user__first_name', 'statu')


    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Nom'


    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'Prenom'


    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_curriculum(self, obj):
        return obj.curriculum
    get_curriculum.short_description = 'Programme'

    def get_photo_thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;"/>', obj.photo.url)
        return '-'
    get_photo_thumbnail.short_description = 'Photo'
    

    def get_statut(self, obj):
        return obj.statut
    get_statut.short_description = 'Statut'


class ProgressionAdmin(admin.ModelAdmin):
    list_display = ('user', 'meeting', 'pertinence', 'time_gestion', 'eloquence', 'structure')


admin.site.register(Statut, StatutAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(Progression, ProgressionAdmin)