from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets, permissions 
from .serializers import *
from knox.models import AuthToken
from rest_framework.response import Response

# Create your views here.
User = get_user_model()

class LoginViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
           mail = serializer.validated_data['email']
           password = serializer.validated_data['password']
           user =authenticate(request, email=mail, password=password)
           if user:
               _, token = AuthToken.objects.create(user)
               return Response(
                   {
                   'user': self.serializer_class(user).data,
                   'token': token
                   }
               )
           else:
               return Response(
                   {
                   'error': 'Credenciales invalidas'
                   }, status=401)
        else:
            return Response(serializer.errors, status=400)
class RegisterViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors,status=400)


class UserViewset(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def list(self,request):
        queryset = User.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)  