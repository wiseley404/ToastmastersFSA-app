from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm, CustomAuthentificationForm
from . import views


urlpatterns = [
    path("", views.show_home_page, name='home_page'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        form_class=CustomAuthentificationForm),
        name='login'
    ),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup, name='signup'),

    path('password/reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_index.html',
        email_template_name='accounts/password_reset_email_message.html',
        subject_template_name='accounts/password_reset_subject.txt',
        form_class=CustomPasswordResetForm), 
        name='password_reset'
    ),

    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), 
        name='password_reset_done'
    ),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        form_class=CustomSetPasswordForm), 
        name='password_reset_confirm'
    ),

    path('password/reset/success/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), 
        name='password_reset_complete'
    ),

    path('confirm-email/<key>/', views.MyConfirmEmailView.as_view(), name='account_confirm_email'),

    path('password/change/', views.change_password, name='password_change')

]