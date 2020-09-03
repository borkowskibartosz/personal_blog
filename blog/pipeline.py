from .models import UserProfile
from django.core.files import File
from django.conf import settings
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import boto3
import urllib.request
import requests
import os

def get_avatar(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    if backend.name == 'github':
        url = response['avatar_url']
    if backend.name == 'google-oauth2':
        url = response['picture']
    if url:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(url).read())
        img_temp.flush()
        user_profile = UserProfile.objects.get(user=user)
        user_profile.avatar.save(f"profile/{user.username}.jpg", File(img_temp))

