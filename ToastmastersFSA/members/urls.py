from django.urls import path
from . import views

urlpatterns = [
    path('my-profile/dashboard/', views.show_dashboard, name='dashboard'),
    path('my-profile/edit/', views.edit_profile, name='edit_profile'),
]