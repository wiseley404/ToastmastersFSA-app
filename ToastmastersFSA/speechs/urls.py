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
    path('<speech_id>/delete/', views.delete_role, name='delete_role'),
    path('new-evaluation/', views.start_evaluation, name='start_evaluation'),
    path('evaluations/get-criteria/<int:evaluation_type_id>/', views.get_criteria, name='get_criteria'),
    path('evaluations/get-meeting-members/<int:meeting_id>/', views.get_meeting_members, name='get_meeting_members'),
    path('evaluations/get-all-criteria/', views.get_all_criteria, name='get_all_criteria'),
    path('evaluations/get-all-members/', views.get_all_members, name='get_all_members'),
    path('evaluations/generate-table/', views.generate_evaluation_table, name='generate_evaluation_table'),
    path('evaluations/submit/', views.submit_evaluation, name='submit_evaluation'),
    path('evaluations/number<int:answer_id>/answer/', views.show_evaluation_answer, name='show_evaluation_answer'),
    path('evaluations/get-comment/<int:eval_id>/<int:profile_id>/', views.get_comment, name='get_comment'),
    path('evaluations/save-comment/', views.save_comment, name='save_comment'),

]