from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.show_settings, name='settings'),
    path('statistiques/', views.show_stats, name='statistiques')
]