from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_meetings_list, name='meetings_list'),
    path('meeting/<int:pk>/', views.show_meeting_infos, name='meeting_infos'),
    path('create/', views.create_meeting, name='create_meeting'),
    path('meeting/<meeting_id>/edit/', views.edit_meeting, name='edit_meeting'),
    path('meeting/<meeting_id>/delete/', views.delete_meeting, name='delete_meeting'),
    path('meeting/<int:meeting_id>/download/', views.create_meeting_pdf_download, name='meeting_pdf'),
    path('ressources/', views.show_ressources, name='show_ressources'),
    path('ressources/add/', views.add_ressources, name='add_ressources'),
    path('ressources/<ressource_id>/edit/', views.edit_ressources, name='edit_ressources'),
    path('ressources/<ressource_id>/delete/', views.delete_ressources, name='delete_ressources'),
    path('ressources/<ressource_id>/delete/confirmation/', views.confirm_ressource_deletion, name='confirm_ressource_deletion'),
    path('check-attendance/', views.check_attendance, name='check_attendance'),
    path('<int:meeting_id>/confirm-attendance/', views.confirm_attendance, name='confirm_attendance'),
]