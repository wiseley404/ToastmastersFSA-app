from django.urls import path
from . import views

urlpatterns = [
    path('historique/', views.show_historique_speeches_list, name='speeches_historique'),
    path('planning/', views.show_future_speeches_list, name='speeches_planning'),
    path('evaluations/', views.show_evaluations, name='evaluations'),
    path('create/', views.create_speech, name='create_speech'),
    path('attribuate/', views.attribuate_speech, name='attribuate_speech'),
    path('certificats/', views.show_certificats, name='myCertificats'),
    path("ajax/available_roles/", views.show_available_roles, name="available_roles"),
    path('<speech_id>/delete/confirmation/', views.confirm_role_deletion, name='confirm_role_deletion'),
    path('<speech_id>/delete/', views.delete_role, name='delete_role')

]