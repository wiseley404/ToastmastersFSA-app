from django.contrib import admin
from .models import BoardRole, BoardProfile


class BoardRoleAdmin(admin.ModelAdmin):
    list_display = ("title",)

class BoardProfileAdmin(admin.ModelAdmin):
    list_display = ('profile', 'role', 'start_date', 'end_date', 'is_active')


# Register your models here.
admin.site.register(BoardProfile, BoardProfileAdmin)
admin.site.register(BoardRole, BoardRoleAdmin)
