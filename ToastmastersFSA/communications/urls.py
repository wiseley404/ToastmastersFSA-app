from . import views
from django.urls import path


urlpatterns = [
    path("", views.manage_communications, name='communications'),
    path("notifications/create/", views.create_notif, name='create_notif'),
    path("notification/<int:notif_id>/edit/", views.edit_notif, name='edit_notif'),
    path("notification/<int:notif_id>/delete/confirmation/", views.confirm_notif_deletion, name='confirm_notif_deletion'),
    path("notification/<int:notif_id>/delete/success/", views.delete_notif, name='delete_notif'),
    path("emails-list/create/", views.create_email_list, name='create_email_list'),
    path("email-list/<int:email_list_id>/edit/", views.edit_email_list, name='edit_email_list'),
    path("email-list/<int:email_list_id>/delete/confirmation/", views.confirm_email_list_deletion, name='confirm_email_list_deletion'),
    path("email-list/<int:email_list_id>/delete/success/", views.delete_email_list, name='delete_email_list'),
    path("email-scheduled/", views.create_email_scheduled, name='create_email_scheduled'),
    path("email-scheduled/<int:email_scheduled_id>/edit/", views.edit_email_scheduled, name='edit_email_scheduled'),
    path("email-scheduled/<int:email_scheduled_id>/delete/confirmation/", views.confirm_email_scheduled_deletion, name='confirm_email_scheduled_deletion'),
    path("email-scheduled/<int:email_scheduled_id>/delete/success/", views.delete_email_scheduled, name='delete_email_scheduled'),
    path("email-system/<int:system_email_id>/edit/", views.edit_system_email, name='edit_system_email'),
]