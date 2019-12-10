from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter, APIRootView


class CustomAPIRootView(APIRootView):
    """
    The default basic root view for DefaultRouter
    """

    def get(self, request, *args, **kwargs):
        # Return a plain {"name": "hyperlink"} response.

        rest_auth_dict = {
            'login': 'rest_auth:rest_login',
            'logout': 'rest_auth:rest_logout',
            'password_reset': 'rest_auth:rest_password_reset',
            'password_reset_confirm': 'rest_auth:rest_password_reset_confirm',
            'password_change': 'rest_auth:rest_password_change',
            # 'register': 'rest_registration:rest_register',
            # 'verify_email': 'rest_registration:rest_verify_email',
        }

        ret = {}
        namespace = request.resolver_match.namespace
        for key, url_name in self.api_root_dict.items():
            if namespace:
                url_name = namespace + ':' + url_name
            ret[key] = reverse(
                url_name,
                args=args,
                kwargs=kwargs,
                request=request,
                format=kwargs.get('format', None)
            )

        for key, url in rest_auth_dict.items():
            ret[key] = reverse(
                url,
                args=args,
                kwargs=kwargs,
                request=request,
                format=kwargs.get('format', None)
            )

        return Response(ret)


class Router(DefaultRouter):
    """Customize api roote to add rest-auth urls to root view.

    Methods:
        get_api_root_view: Append rest_auth urls to dictionary for inclusion
            in browsable API.

    """

    APIRootView = CustomAPIRootView


# Router instance for entire application
ROUTER = Router()
