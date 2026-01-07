from django.contrib import admin
from .models import Notification, EmailList, EmailScheduled
from .models import SystemEmail, SystemEmailAttachment, AbsenceEmailCondition


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "message", "sender", "created_at")

class EmailListAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at")

class EmailScheduledAdmin(admin.ModelAdmin):
    list_display = ("title", "message", "created_by", "created_at", "start_date", "end_date", "send_time", "frequency")

class SystemEmailAttachmentInline(admin.TabularInline):
    model = SystemEmailAttachment
    extra = 1

class AbsenceEmailConditionInline(admin.StackedInline):
    model = AbsenceEmailCondition
    extra = 0


# Register your models here.
admin.site.register(Notification, NotificationAdmin)
admin.site.register(EmailList, EmailListAdmin)
admin.site.register(EmailScheduled, EmailScheduledAdmin)

@admin.register(SystemEmail)
class SystemEmailAdmin(admin.ModelAdmin):
    list_display = ['code', 'subject', 'send_offset', 'is_active']
    inlines = [SystemEmailAttachmentInline, AbsenceEmailConditionInline]

@admin.register(AbsenceEmailCondition)
class AbsenceEmailConditionAdmin(admin.ModelAdmin):
    list_display = ['email', 'absence_count']