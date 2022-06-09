from django.contrib.auth import authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status

from ToolManagmentSystem import settings
from api.utils import send_email
from api.views import BaseAPIView
from user.models import User

from user.serializers import UserSerializer, ChangePasswordSerializer


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
                        user_data["access_token"] = oauth_token.get("access_token")
                        user_data["refresh_token"] = oauth_token.get("refresh_token")
                        return self.send_response(
                            success=True,
                            code=f"200",
                            status_code=status.HTTP_200_OK,
                            payload=user_data,
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
                    "name": user.name,
                    "email": user.email,
                }
                confirmation_token = default_token_generator.make_token(user)
                actiavation_link = f"{settings.HOST_URL}/user/email-verification?user_id={user.id}&confirmation_token={confirmation_token}"

                send_email(user, actiavation_link)
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


class ChangePasswordView(BaseAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsOauthAuthenticated,)

    def put(self, request):
        try:
            obj = request.user
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                if not obj.check_password(serializer.data.get("old_password")):
                    return self.send_response(
                        code=f"422",
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        description="old password in incorect",
                    )
                obj.set_password(serializer.data.get("new_password"))
                obj.save()
                return self.send_response(
                    success=True,
                    code=f"201",
                    status_code=status.HTTP_201_CREATED,
                    payload=[],
                    description="Password is Updated",
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
        except FieldError:
            return self.send_response(
                code=f"500",
                description="Cannot resolve keyword given in 'order_by' into field",
            )
        except Exception as e:
            return self.send_response(code=f"500", description=e)


class UserLogoutView(BaseAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsOauthAuthenticated,)

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


class ForgotPasswordView(BaseAPIView):
    parser_class = ()
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, pk=None):
        try:
            if request.data["email"] == "" or None:
                return self.send_response(
                    code=f"422",
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description="Email is required",
                )
            else:
                user = User.objects.get(email__exact=request.data["email"])
                confirmation_token = default_token_generator.make_token(user)
                actiavation_link = f"{settings.HOST_URL}/user/email-verification?user_id={user.id}&confirmation_token={confirmation_token}"

                send_email(user, actiavation_link)

            return self.send_response(
                success=True,
                code=f"201",
                status_code=status.HTTP_201_CREATED,
                description="Forgot password link sent successfully",
            )
        except User.DoesNotExist:
            return self.send_response(
                code=f"422",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="User does not exists",
            )
        except Exception as e:
            return self.send_response(code=f"500", description=e)



