from .models import UserProfile
from django.core.files import File
from django.conf import settings
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
        r = requests.get(url)
        # with open(settings.MEDIA_ROOT + f"/profile/{user.username}.jpg", "wb") as f:
        #     f.write(r.content)
        # user_profile = UserProfile.objects.get(user=user)
        # user_profile.avatar = f"/profile/{user.username}.jpg"
        # user_profile.save()
