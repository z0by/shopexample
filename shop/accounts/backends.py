from accounts.models import AuthUser



class EmailBackend:

    def authenticate(self, username=None, password=None):
        if '@' in username:
            print "AAAAAAAAAA"
            try:
                user = AuthUser._default_manager.get(email=username)
            except AuthUser.DoesNotExist:
                return None

            if user and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return AuthUser._default_manager.get(pk=user_id)
        except AuthUser.DoesNotExist:
            return None

class PhoneBackend:

    def authenticate(self, username=None, password=None):
        try:
            user = AuthUser._default_manager.get(phone=username)
        except AuthUser.DoesNotExist:
            return None

        if user and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return AuthUser._default_manager.get(pk=user_id)
        except AuthUser.DoesNotExist:
            return None