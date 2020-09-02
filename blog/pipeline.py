from .models import UserProfile
from django.core.files import File
from django.conf import settings
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
        s3 = boto3.resource(
            's3',
            region_name='us-east-2',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        s3.Object(settings.AWS_STORAGE_BUCKET_NAME, f'{user.username}.jpg').put(Body=open(url, 'rb'))

        # r = requests.get(url)
        # with open(settings.MEDIA_ROOT + f"/profile/{user.username}.jpg", "wb") as f:
        #     f.write(r.content)

        user_profile = UserProfile.objects.get(user=user)
        user_profile.avatar = f"/{user.username}.jpg"
        user_profile.save()
