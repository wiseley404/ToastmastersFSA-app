from django.urls import path
from . import views


urlpatterns = [
    path('form/<int:form_id>/', views.show_form, name='show_form'),
    path('form/<int:form_id>/submit', views.submit_form, name='submit_form'),
    path('form/<int:form_id>/edit/', views.edit_form, name='edit_form'),
    path('form/<int:form_id>/delete/confirmation/', views.confirm_form_deletion, name='confirm_form_deletion'),
    path('form/<int:form_id>/delete/', views.delete_form, name='delete_form'),
    path('published/', views.show_published_forms_list, name='forms_list'),
    path('historique/', views.show_historique_forms_list, name='historique_forms'),
    path('form/create/', views.create_form, name='create_form'),
    path('form/<int:form_id>/field/add/', views.add_fields, name='add_fields'),
    path('form/<int:form_id>/publication/confirmation/', views.confirm_form_publication, name='confirm_form_publication'),
    path('form/<int:form_id>/publication/success/', views.publish_form, name='publish_form'),
    path('form/<int:form_id>/results/', views.show_results, name='show_results'),
    path('form/<int:form_id>/close/confirmation/', views.confirm_form_closure, name='confirm_form_closure'),
    path('form/<int:form_id>/close/', views.close_form, name='close_form'),
]