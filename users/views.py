from drf_yasg.utils import swagger_auto_schema
from rest_framework import response, views, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .schame import create_user_schema

from users.serializers import CustomUserSerializer


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return response.Response({'token': token.key})


class Register(views.APIView):
    @swagger_auto_schema(
        request_body=create_user_schema,
        operation_description='Create new user',
        response={201: CustomUserSerializer}
    )
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
