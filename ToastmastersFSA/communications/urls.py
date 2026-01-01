from . import views
from django.urls import path


urlpatterns = [
    path("", views.manage_communications, name='communications'),
    path("notifications/create/", views.create_notif, name='create_notif'),
    path("notification/<int:notif_id>/edit/", views.edit_notif, name='edit_notif'),
    path("notification/<int:notif_id>/delete/confirmation/", views.confirm_notif_deletion, name='confirm_notif_deletion'),
    path("notification/<int:notif_id>/delete/", views.delete_notif, name='delete_notif'),
    path("emails-list/create/", views.create_email_list, name='create_email_list'),
]