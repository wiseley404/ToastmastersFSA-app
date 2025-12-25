from django.contrib import admin
from .models import Form, Field, Option, Submission, Response


class FormAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "date", "is_published")


class FieldAdmin(admin.ModelAdmin):
    list_display = ("form", "description", "type", "required")


class OptionAdmin(admin.ModelAdmin):
    list_display = ("field", "value")


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "form", "submitted_on")


class ResponseAdmin(admin.ModelAdmin):
    list_display = ("submission", "field", "value")

# Register your models here.
admin.site.register(Form, FormAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Response, ResponseAdmin)