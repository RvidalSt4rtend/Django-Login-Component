from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from .utils import get_local_time
# Create your models here.

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

class FailedLoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField()
    success = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user} failed login attempt at {self.attempt_time}'
    
    def save(self, *args, **kwargs):
        if not self.attempt_time:
            self.attempt_time = get_local_time()  
        super().save(*args, **kwargs)

class UserBlock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block_time = models.DateTimeField()
    block_until = models.DateTimeField()

    def __str__(self):
        return f'{self.user} blocked until {self.block_until}'
    
    def save(self, *args, **kwargs):
        if not self.block_time:
            self.block_time = get_local_time()  
        super().save(*args, **kwargs)