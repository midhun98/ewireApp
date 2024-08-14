from django.contrib.auth import login, authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import (LoginSerializer,
                               UserRegistrationSerializer)


# Create your views here.

class LoginAPI(APIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'status': 'success', 'token': token.key})
            else:
                return Response({'status': 'failed', 'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response({'status': 'failed', 'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserRegistrationView(APIView):
    authentication_classes = []

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'password2'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.FORMAT_EMAIL),
                'phone_number': openapi.Schema(type=openapi.TYPE_NUMBER),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'password2': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(description='User Created successfully.'),
            400: openapi.Response(description='Error Creating User.'),
        },
        operation_description="Create a user",
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
