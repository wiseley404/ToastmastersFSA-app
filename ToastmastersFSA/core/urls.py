from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.show_settings, name='settings'),
    path('statistiques/', views.show_stats, name='statistiques'),
    path("board/", views.add_member_to_board, name='add_member_to_board'),
    path("board-profile/<int:board_profile_id>/edit/", views.edit_board_role, name='edit_board_role'),
    path("board-profile/<int:board_profile_id>/delete/confirmation/", views.confirm_board_profile_deletion, name='confirm_board_profile_deletion'),
    path("board-profile/<int:board_profile_id>/delete/success/", views.delete_board_profile, name='delete_board_profile'),
    path("member-profile/<int:profile_id>/edit/", views.edit_profile, name='edit_member_profile'),
]