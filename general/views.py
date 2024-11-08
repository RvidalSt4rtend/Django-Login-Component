from django.contrib.auth import authenticate
from django.shortcuts import render
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .serializers import LoginSerializer
from icecream import ic


class CustomLoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data
        username = user.username

        if user is None:
            return Response(
                {'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_active:
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return Response(
                {
                    'access_token': str(access_token),
                    'refresh_token': str(refresh_token),
                    'user': username,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {'error': 'User is inactive'}, status=status.HTTP_400_BAD_REQUEST)
