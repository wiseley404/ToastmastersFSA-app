from django.contrib.auth import get_user_model
import os

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    email = os.getenv('EMAIL_ADMIN')
    password = os.getenv('PASSWORD_ADMIN')
    User.objects.create_superuser('admin', email, password)
