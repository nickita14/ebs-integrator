from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView


class MinuteRateThrottle(SimpleRateThrottle):
    """
    A rate limiter that limits the number of requests that can be made in a minute.

    Inherits from SimpleRateThrottle.

    """
    rate = '600/min'

    def get_cache_key(self, request: Request, *args) -> str:
        """
        Returns a cache key for the given request and view.

        Args:
        - request (rest_framework.request.Request): The request object.
        - view (rest_framework.views.APIView): The view object.

        Returns:
        - str: A cache key for the given request and view.
        """
        if request.user.is_authenticated:
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.user.pk
            }

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class BasicRestView(APIView):
    """
    A basic REST view that limits the number of requests that can be made in a minute.

    Inherits from APIView.
    """
    throttle_classes = [MinuteRateThrottle]


class AuthenticatedRestView(BasicRestView):
    """
    A basic REST view that requires authentication.

    Inherits from BasicRestView.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
