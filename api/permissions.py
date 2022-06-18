from django.contrib.auth import authenticate
from oauth2_provider.models import AccessToken
from oauth2_provider.views import ProtectedResourceView
from rest_framework import permissions

from user.models import AccessLevel


class BaseAuthPermission(permissions.BasePermission):
    def verify_header(self, request):
        if request.META.get("HTTP_AUTHORIZATION", "").startswith("Bearer"):
            if not hasattr(request, "user") or request.user.is_anonymous:
                user = authenticate(request=request)
                if user:
                    request.user = request._cached_user = user
                    return True
        return False

    def verify_cookie(self, request):
        try:
            access_token = request.COOKIES.get("u-at", None)
            if access_token:
                request.user = AccessToken.objects.get(token=access_token).user
                request.user.access_token = access_token
                return True
            else:
                return False
        except AccessToken.DoesNotExist:
            return False


class IsOauthAuthenticated(BaseAuthPermission):
    def has_permission(self, request, view):
        return self.verify_header(request)


class IsPostOrIsAuthenticated(BaseAuthPermission):
    def has_permission(self, request, view):
        # allow all POST requests
        if request.method == "POST":
            self.verify_header(request)
            return True

        # Otherwise, only allow authenticated requests
        return request.user and request.user.is_authenticated


class IsGetOrIsAuthenticated(permissions.BasePermission, ProtectedResourceView):
    def has_permission(self, request, view):
        # allow all POST requests
        if request.method == "GET":
            if request.META.get("HTTP_AUTHORIZATION", "").startswith("Bearer"):
                if not hasattr(request, "user") or request.user.is_anonymous:
                    user = authenticate(request=request)
                    if user:
                        request.user = request._cached_user = user
            return True

        # Otherwise, only allow authenticated requests
        if request.META.get("HTTP_AUTHORIZATION", "").startswith("Bearer"):
            if not hasattr(request, "user") or request.user.is_anonymous:
                user = authenticate(request=request)
                if user:
                    request.user = request._cached_user = user
                    return True
