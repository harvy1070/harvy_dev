from django.contrib.auth.backends import ModelBackend
from .models import UserInfo

# 인증
class UserIdAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(user_id=username)
            if user.check_password(password):
                return user
        except UserInfo.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserInfo.objects.get(pk=user_id)
        except UserInfo.DoesNotExist:
            return None