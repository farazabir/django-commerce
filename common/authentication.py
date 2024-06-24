from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication


class JwtAuthenticationCookie(JWTAuthentication):
    def authenticate(self, request):
        is_ambassador = 'api/ambassador' in request.path
        token = request.COOKIES.get('jwt')
        if not token:
            return None
        try:
            validated_token = self.get_validated_token(token)
            payload = validated_token.payload
            if (is_ambassador and payload['scope'] != 'ambassador') or (not is_ambassador and payload['scope'] != "admin"):
                raise exceptions.AuthenticationFailed('Invalid Scope')
            user = self.get_user(validated_token)
        except exceptions.AuthenticationFailed as e:
            raise e
        except Exception:
            raise exceptions.AuthenticationFailed("Unauthorized")

        return (user, validated_token)
