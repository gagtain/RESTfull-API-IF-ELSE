from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header, BasicAuthentication
from django.utils.translation import gettext_lazy as _
import base64
from .models import MyUser


def get_auth_token(request):
    auth_header = authentication.get_authorization_header(request)
    return auth_header

def getAccountEmailPass(token):
        email_pass_64 = token.split()[1]
        email_pass = base64.b64decode(email_pass_64).decode('ascii').split(':')

        return email_pass

def getAccountObjects(request):
    token = get_auth_token(request)
    email_pass = getAccountEmailPass(token)
    try:
        user = MyUser.objects.get(email=email_pass[0])
        return user
    except:
        return False


class BasicAuthentications(BasicAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            try:
                auth_decoded = base64.b64decode(auth[1]).decode('utf-8')
            except UnicodeDecodeError:
                auth_decoded = base64.b64decode(auth[1]).decode('latin-1')
            auth_parts = auth_decoded.partition(':')
        except (TypeError, UnicodeDecodeError):
            msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)

        userid, password = auth_parts[0], auth_parts[2]
        return self.authenticate_credentials(userid, password, request)

    def authenticate_credentials(self, email, password, request=None):
        try:
            user = MyUser.objects.get(email=email, password=password)
        except:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))
        return user, None

    def authenticate_header(self, request):
        return 'Basic realm="%s"' % self.www_authenticate_realm