import requests
from requests.auth import HTTPBasicAuth

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import is_server_error
from rest_framework.views import APIView


import http.client

from ToolManagmentSystem import settings

http.client._MAXHEADERS = 1000


class BaseAPIView(APIView):

    """
    Base class for API views.
    """

    authentication_classes = ()
    permission_classes = (AllowAny,)

    def send_response(
        self,
        success=False,
        code="",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        payload={},
        description="",
        exception=None,
        count=0,
        log_description="",
    ):

        """
        Generates response.
        :param success: bool tells if call is successful or not.
        :param code: str status code.
        :param status_code: int HTTP status code.
        :param payload: list data generated for respective API call.
        :param description: str description.
        :param exception: str description.
        :rtype: dict.
        """

        if not success and is_server_error(status_code):
            print(1)
            if settings.DEBUG:
                description = f"error message: {description}"
            else:
                description = "Internal server error."
        return Response(
            data={
                "success": success,
                "code": code,
                "payload": payload,
                "description": description,
                "count": count,
            },
            status=status_code,
        )

    def send_data_response(
        self,
        success=False,
        code="",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        payload={},
        description="",
    ):
        """
        Generates response for data tables.
        :param success: bool tells if call is successful or not.
        :param code: str status code.
        :param status_code: int HTTP status code.
        :param payload: list data generated for respective API call.
        :param description: str description.
        :rtype: dict.
        """
        if not success and is_server_error(status_code):
            if settings.DEBUG:
                description = f"error message: {description}"
            else:
                description = "Internal server error."
        return Response(
            data={
                "data": {
                    "success": success,
                    "code": code,
                    "payload": payload,
                    "description": description,
                }
            },
            status=status_code,
        )

    @staticmethod
    def get_oauth_token(email="", password="", grant_type="password"):

        """
        :email: the user email for authentication
        :password: the password for the authentication
        """

        try:
            url = settings.AUTHORIZATION_SERVER_URL
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {"username": email, "password": password, "grant_type": grant_type}
            auth = HTTPBasicAuth(settings.OAUTH_CLIENT_ID, settings.OAUTH_CLIENT_SECRET)
            response = requests.post(url=url, headers=headers, data=data, auth=auth)
            if response.ok:
                json_response = response.json()
                return {
                    "access_token": json_response.get("access_token", ""),
                    "refresh_token": json_response.get("refresh_token", ""),
                }
            else:
                return {"error": response.json().get("error")}
        except Exception as e:
            # fixme: Add logger to log this exception
            return {"exception": str(e)}

    @staticmethod
    def revoke_oauth_token(token):

        """
        :token: its an oauth2 token for revoking
        """
        try:
            url = settings.REVOKE_TOKEN_URL
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "token": token,
                "client_secret": settings.OAUTH_CLIENT_SECRET,
                "client_id": settings.OAUTH_CLIENT_ID,
            }
            response = requests.post(url=url, headers=headers, data=data)
            if response.ok:
                return True
            else:
                return False
        except Exception:
            # fixme: Add logger to log this exception
            return False

    @staticmethod
    def convert_oauth_token(token, backend):

        """
        :token: its an oauth2 token for revoking
        """
        try:
            url = settings.CONVERT_TOKEN_URL
            data = {
                "grant_type": "convert_token",
                "client_id": settings.OAUTH_CLIENT_ID,
                "client_secret": settings.OAUTH_CLIENT_SECRET,
                "backend": backend,
                "token": token,
            }

            response = requests.post(url=url, data=data)
            json_response = response.json()
            if response.ok:
                return {
                    "access_token": json_response.get("access_token", ""),
                    "refresh_token": json_response.get("refresh_token", ""),
                }
            else:
                return {"error": response.json().get("error")}
        except Exception:
            # fixme: Add logger to log this exception
            return False
