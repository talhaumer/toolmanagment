from django.contrib.auth import authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from ToolManagmentSystem import settings
from api.permissions import IsOauthAuthenticated
from api.utils import send_email, send_password_email
from api.views import BaseAPIView
from user.models import User

from user.serializers import UserSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from django.http import HttpResponsePermanentRedirect
import os


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

class LoginView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """

    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        email -- valid user email
        password -- password to authenticate user
        """

        password = request.data.get("password", "")
        email = request.data.get("email", "")
        try:
            user = authenticate(request, email=email, password=password)
            if user:
                if user.is_active:
                    oauth_token = self.get_oauth_token(email, password)
                    if "access_token" in oauth_token:
                        serializer = UserSerializer(user)
                        user_data = serializer.data
                        res = {}
                        user = {}
                        user['id'] = user_data['id']
                        user['first_name'] = user_data["first_name"]
                        user['last_name'] = user_data["last_name"]
                        user['email'] = user_data['email']
                        user['role'] = user_data['role']
                        res['user'] = user
                        res["access_token"] = oauth_token.get("access_token")
                        res["refresh_token"] = oauth_token.get("refresh_token")
                        return self.send_response(
                            success=True,
                            code=f"200",
                            status_code=status.HTTP_200_OK,
                            payload=res,
                            description="You are logged in!",
                            log_description=f'User {user_data["email"]}. with id .{user_data["id"]}. has just logged in.',
                        )
                    else:
                        return self.send_response(
                            description=f"Something went wrong with Oauth token generation.",
                            code=f"500",
                        )
                else:
                    description = "Your account is blocked or deleted."
                    return self.send_response(
                        success=False,
                        code=f"422",
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        payload={},
                        description=description,
                    )
            return self.send_response(
                success=False,
                code=f"422",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                payload={},
                description="Email or password is incorrect.",
            )
        except Exception as e:
            return self.send_response(code=f"500", description=e)


class AddUserView(BaseAPIView):
    def post(self, request):
        """
        request: it contains json data for creation of user.
        """
        try:
            user = request.data
            serializer = UserSerializer(data=user)
            if serializer.is_valid():
                user = serializer.save()
                data = {
                    "id": user.id,
                    "name": user.first_name,
                    "email": user.email,
                }
                # confirmation_token = default_token_generator.make_token(user)
                # actiavation_link = f"{settings.HOST_URL}/user/email-verification?user_id={user.id}&confirmation_token={confirmation_token}"

                # send_email(user, actiavation_link)
                return self.send_response(
                    success=True,
                    code=f"201",
                    status_code=status.HTTP_201_CREATED,
                    payload=data,
                    description="User is created",
                )
            else:
                return self.send_response(
                    code=f"422",
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=serializer.errors,
                )
        except User.DoesNotExist:
            return self.send_response(
                code=f"422",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="User doesn't exists",
            )
        except IntegrityError:
            return self.send_response(
                code=f"422",
                description="Email already exists.",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except FieldError:
            return self.send_response(
                code=f"500",
                description="Cannot resolve keyword given in 'order_by' into field",
            )
        except Exception as e:
            return self.send_response(code=f"500", description=e)


class EamilVerification(BaseAPIView):
    permission_classes = ()

    def get(self, request, pk=None):
        user_id = request.query_params.get("user_id", "")
        confirmation_token = request.query_params.get("confirmation_token", "")
        try:
            user = User.objects.get(id=user_id)
            if not default_token_generator.check_token(user, confirmation_token):
                return self.send_response(
                    code="422",
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description="Email didn't verified",
                )
            else:
                user.is_active = True
                user.save()
                return self.send_response(
                    success=True,
                    status_code=status.HTTP_200_OK,
                    payload={},
                    code="200",
                    description="Details of serializer",
                    log_description="",
                )

        except ObjectDoesNotExist:
            return self.send_response(
                code="422",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="No User matches the given query.",
            )

        except User.DoesNotExist:
            return self.send_response(
                code="422",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="User doesn't exists",
            )
        except Exception as e:
            return self.send_response(code=f"500", description=e)


class GetUserView(BaseAPIView):
    permission_classes = ()

    def get(self, request, pk=None):
        try:
            if pk:
                users = User.objects.get(id=pk)
                serializer = UserSerializer(users)
                return self.send_response(
                    success=True,
                    status_code=status.HTTP_200_OK,
                    payload=serializer.data,
                    code="200",
                    description="Details of serializer",
                    log_description="",
                    count=len(serializer.data),
                )
        except ObjectDoesNotExist:
            return self.send_response(
                code="422",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="No User matches the given query.",
            )
        except User.DoesNotExist:
            return self.send_response(
                code="422",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="User doesn't exists",
            )
        except FieldError:
            return self.send_response(
                code=f"500",
                description="Cannot resolve keyword given in 'order_by' into field",
            )
        except Exception as e:
            return self.send_response(code=f"500", description=e)


class UserLogoutView(BaseAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticated,)

    def get(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
            if not self.revoke_oauth_token(token):
                return self.send_response(
                    code=f"422",
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description="User doesn't logout",
                )
            logout(request)
            return self.send_response(
                success=True,
                code=f"201",
                status_code=status.HTTP_201_CREATED,
                payload=[],
                description="User logout successfully",
            )
        except User.DoesNotExist:
            return self.send_response(
                code=f"422",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="User doesn't exists",
            )
        except FieldError:
            return self.send_response(
                code=f"500",
                description="Cannot resolve keyword given in 'order_by' into field",
            )
        except Exception as e:
            return self.send_response(code=f"500", description=e)


class RequestPasswordResetEmail(BaseAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            send_password_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(BaseAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        request.data['token'] = token
        request.data['uidb64'] = uidb64
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Token is not valid, please request a new one'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Password is reset successfuly'}, status=status.HTTP_200_OK)


