from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token


class IsUser(BasePermission):
    """
    Allows access only to user users.
    """

    def has_permission(self, request, view):
        try:
            token = request.headers["Authorization"]
            if token[:6] != "Bearer":
                return False
            else:
                token = token[7:]
                user = Token.objects.filter(key=token).last()
                if user:
                    return user.user.role in ['user', 'admin', 'field_owner']
                return False
        except Exception as e:
            return False


class IsFieldOwner(BasePermission):
    """
    Allows access only to field owner users.
    """

    def has_permission(self, request, view):
        try:
            token = request.headers["Authorization"]
            if token[:6] != "Bearer":
                print("bearer")
                return False
            else:
                token = token[7:]
                user = Token.objects.filter(key=token).last()
                if user:
                    return user.user.role == 'field_owner'
                return False
        except Exception as e:
            return False


class IsUser(BasePermission):
    """
    Allows access only to regular users.
    """

    def has_permission(self, request, view):
        try:
            token = request.headers["Authorization"]
            if token[:6] != "Bearer":
                print("bearer")
                return False
            else:
                token = token[7:]
                user = Token.objects.filter(key=token).last()
                if user:
                    return user.user.role == 'user'
                return False
        except Exception as e:
            return False


class IsAdminAndFieldOwner(BasePermission):
    """
    Allows access only to admin and field owner users.
    """

    def has_permission(self, request, view):
        try:
            token = request.headers["Authorization"]
            if token[:6] != "Bearer":
                print("bearer")
                return False
            else:
                token = token[7:]
                user = Token.objects.filter(key=token).last()
                if user:
                    return user.user.role in ['admin', 'field_owner']
                return False
        except Exception as e:
            return False


class IsAdminAndUser(BasePermission):
    """
    Allows access only to admin and user users.
    """

    def has_permission(self, request, view):
        try:
            token = request.headers["Authorization"]
            if token[:6] != "Bearer":
                print("bearer")
                return False
            else:
                token = token[7:]
                user = Token.objects.filter(key=token).last()
                if user:
                    print(user.user.role)
                    return user.user.role in ['admin', 'user']
                return False
        except Exception as e:
            return False


def get_authentication_user(request):
    try:
        token = request.headers["Authorization"]
        if token[:6] != "Bearer":
            return None
        else:
            token = token[7:]
            user = Token.objects.filter(key=token).last()
            if user:
                return user.user
            return None
    except Exception as e:
        return None
