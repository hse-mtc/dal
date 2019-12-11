from rest_framework.authentication import TokenAuthentication
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.utils.translation import gettext_lazy as _


def get_authorization_header(request):
    auth = request.META.get('HTTP_X_TOKEN', b'')
    if isinstance(auth, str):
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class TokenAuthSupportQueryString(TokenAuthentication):

    def authenticate(self, request):
        key = 'token'
        if key in request.query_params \
                and 'HTTP_AUTHORIZATION' not in request.META \
                and 'HTTP_X_TOKEN' not in request.META:
            return self.authenticate_credentials(request.query_params.get(key))
        elif 'HTTP_X_TOKEN' in request.META:
            auth = get_authorization_header(request).split()
            if not auth or auth[0].lower() != self.keyword.lower().encode():
                return None
            if len(auth) == 1:
                msg = _('Invalid token header. No credentials provided.')
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth) > 2:
                msg = _('Invalid token header. Token string should not contain spaces.')
                raise exceptions.AuthenticationFailed(msg)
            try:
                token = auth[1].decode()
            except UnicodeError:
                msg = _('Invalid token header. Token string should not contain invalid characters.')
                raise exceptions.AuthenticationFailed(msg)

            return self.authenticate_credentials(token)
        else:
            return super(TokenAuthSupportQueryString, self).authenticate(request)
