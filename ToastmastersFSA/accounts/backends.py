from django.db.models import Q 
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


# Create your models here.
class EmailOrUsernameForLogin(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        try:
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
