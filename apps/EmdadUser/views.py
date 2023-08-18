from .models import CustomUser
from django.contrib.auth import authenticate
from .serializers import UserSerializer, CredentialSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication


class ValidateCredentials(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        serializer = CredentialSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']

            user = authenticate(phone=phone, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(CustomUser, phone=user.phone)
        self.check_object_permissions(self.request, obj)
        return obj
