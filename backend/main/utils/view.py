from django.db import models
from django.db.models.aggregates import Max
from django.utils import timezone as tz
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView


def get_last_modified(request: Request, model: models.Model, *args, **kwargs):
    default = tz.now()
    res = model.objects.aggregate(updated=Max('updated'))
    return (res['updated'] or default).replace(microsecond=0)


class MinuteRateThrottle(SimpleRateThrottle):
    """
    A rate limiter that limits the number of requests that can be made in a minute.

    Inherits from SimpleRateThrottle.
    """
    rate = '60/min'

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


class BasicThrottleView(APIView):
    """
    A basic REST view that limits the number of requests that can be made in a minute.

    Inherits from APIView.
    """
    throttle_classes = [MinuteRateThrottle]


class AuthenticatedView(BasicThrottleView):
    """
    A basic view that requires authentication.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class AuthenticatedRestView(AuthenticatedView):
    """
    A basic REST view that requires authentication.
    """


class AuthenticatedModelViewSet(AuthenticatedView, viewsets.ModelViewSet):
    """
    A basic ModelViewSet that requires authentication.
    """
    http_method_names = [
        'get',
        'post',
        'put',
        'delete',
    ]
