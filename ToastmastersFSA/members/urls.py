from django.urls import path
from . import views

urlpatterns = [
    path('my-profile/dashboard/', views.show_dashboard, name='dashboard'),
    path('my-profile/edit/', views.edit_profile, name='edit_profile'),
    path('my-notifs/', views.show_my_notifications, name='show_my_notifications'),
]