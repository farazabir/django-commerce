from functools import partial
from http.client import ResponseNotReady
from unittest import result
from urllib import response
from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.authentication import JwtAuthenticationCookie
from common.serializers import UserSerializer
from core.models import User
from rest_framework_simplejwt.tokens import AccessToken


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException("Password do not match")
        data['is_ambassador'] = 'api/ambassador' in request.path
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginApiView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect Password')

        scope = 'ambassador' if 'api/ambassador' in request.path else 'admin'

        if user.is_ambassador and scope == 'admin':
            raise exceptions.AuthenticationFailed('Unauthorized')

        token = AccessToken.for_user(user)
        token['scope'] = scope
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': 'success'
        }
        return response


class UserAPIView(APIView):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        if 'api/ambassador' in request.path:
            data['revenue'] = user.revenue
        return Response(data)


class LogoutAPIView(APIView):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
            'message': 'success'
        }
        return response


class ProfileInfoAPIView(APIView):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    authentication_classes = [JwtAuthenticationCookie]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException("Password did not match ")

        user.set_password(data['password'])
        user.save()
        return Response(UserSerializer(user).data)
