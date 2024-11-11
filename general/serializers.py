from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .models import User, FailedLoginAttempt, UserBlock
from .utils import get_local_time, SimpleValidationError
from icecream import ic


timestamp = get_local_time()


def ValidUserBlock(existentUser):
    existsBlock = UserBlock.objects.filter(
        user=existentUser, block_until__gte=timestamp)
    ic(existsBlock)
    if existsBlock.exists():
        raise SimpleValidationError('User is blocked')


def FailedAttempt(existentUser):
    FailedLoginAttempt.objects.create(
        user=existentUser, success=False, attempt_time=timestamp)

    failed_attempts = FailedLoginAttempt.objects.filter(
        user=existentUser, success=False, is_resolved=False)
    countAttempts = failed_attempts.count()
    ic(countAttempts)
    if countAttempts >= settings.LOGIN_ATTEMPT_LIMIT:
        UserBlock.objects.create(
            user=existentUser, block_until=timestamp+settings.BLOCK_DURATION)
        raise SimpleValidationError(
            'You have been blocked due to too many failed login attempts')
    raise SimpleValidationError('Invalid credentials')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=25)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        try:
            existentUser = User.objects.get(username=username)
        except User.DoesNotExist:
            raise SimpleValidationError('User does not exist')

        if not existentUser.is_active:
            raise SimpleValidationError('User is inactive')
        
        ValidUserBlock(existentUser)

        user = authenticate(username=username, password=password)

        if user is None:
                FailedAttempt(existentUser)

        failed_attempts = FailedLoginAttempt.objects.filter(
                user=existentUser, success=False, is_resolved=False)

        if failed_attempts.exists():
                failed_attempts.update(is_resolved=True, success=False)

        username = user.username
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        return {
                'access_token': str(access_token),
                'refresh_token': str(refresh_token),
                'username': username,
            }

