from Services.models import CustomUser
from django.contrib.sessions.models import Session
from rest_framework.authentication import BaseAuthentication


class AuthenticationClass(BaseAuthentication):
    def authenticate(self, request):
        session_id = request.META.get('HTTP_SESSION')
        if session_id:
            User = CustomUser
            try:
                session = Session.objects.get(session_key=session_id)
                user_id = session.get_decoded().get('_auth_user_id')
                user = CustomUser.objects.get(id=user_id)
                return (user, None)
            except User.DoesNotExist:
                return None
            except Session.DoesNotExist:
                return None
        return None
