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
        #s3boto
        # s3 = boto3.resource(
        #     's3',
        #     region_name='us-east-2',
        #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        # )

        # r = requests.get(url)
        # s3.Object(settings.AWS_STORAGE_BUCKET_NAME, f'{settings.MEDIAFILES_LOCATION}/{user.username}.jpg').put(Body=r.content)
        #/s3boto

        # s3.Bucket('bucketname').upload_file('/local/file/here.txt','folder/sub/path/to/s3key')
        #local
        # r = requests.get(url)
        # with open(settings.MEDIA_ROOT + f"/profile/{user.username}.jpg", "wb") as f:
        #     f.write(r.content)
        #/local
        # r = requests.get(url)
        # with open(settings.MEDIA_ROOT + f"/profile/{user.username}.jpg", "wb") as f:
        #     f.write(r.content)
        # user_profile = UserProfile.objects.get(user=user)
        # user_profile.avatar = f"/{user.username}.jpg"
        # user_profile.save()

        #tutu
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(url).read())
        img_temp.flush()
        user_profile = UserProfile.objects.get(user=user)
        user_profile.avatar.save(f"{user.username}.jpg", File(img_temp))                                

        # user_profile = UserProfile.objects.get(user=user)
        # user_profile.avatar = f"/{user.username}.jpg"
        # user_profile.save()
