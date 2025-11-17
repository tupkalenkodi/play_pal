from django.contrib.auth.backends import BaseBackend
from .models import CustomUser


# CUSTOM BACKEND TO ALLOW AUTHENTICATION WITH E-MAIL, INSTEAD OF USERNAME
class EmailBackend(BaseBackend):
    # AUTHENTICATION WITH E-MAIL
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password) and user.is_active:
                return user
        except CustomUser.DoesNotExist:
            return None
        return None

    # NEEDED FOR DJANGO INTERNAL USE
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
