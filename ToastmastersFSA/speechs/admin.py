from django.contrib import admin
from .models import Speech, Certificat
from .models import EvaluationType, EvaluationLevel, EvaluationCriteria, Evaluation, EvaluationAnswer


class SpeechAdmin(admin.ModelAdmin):
    list_display = ("meeting", "role", "orator", "title", "votes")
    list_filter = ("meeting", "role", "orator")


class CertificatAdmin(admin.ModelAdmin):
    list_display = ('speech', 'title', 'issue_date', 'is_won', 'file')


# Register your models here.
admin.site.register(Speech, SpeechAdmin)
admin.site.register(Certificat, CertificatAdmin)


@admin.register(EvaluationType)
class EvaluationTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']

@admin.register(EvaluationLevel)
class EvaluationLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'points', 'order']
    list_editable = ['points', 'order']
    ordering = ['order']

@admin.register(EvaluationCriteria)
class EvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ['name', 'progression_field']
    filter_horizontal = ['evaluation_types']
    fields = ['name', 'description', 'evaluation_types', 'progression_field']

class EvaluationAnswerInline(admin.TabularInline):
    model = EvaluationAnswer
    extra = 0

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['evaluator', 'meeting', 'evaluation_type', 'is_submitted', 'date']
    list_filter = ['evaluation_type', 'date']
    readonly_fields = ['date']
    inlines = [EvaluationAnswerInline]