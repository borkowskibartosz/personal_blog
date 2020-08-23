from .models import UserProfile

def get_avatar(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
        ext = url.split('.')[-1]
    if url:
        user_profile = UserProfile.objects.get(user=user)
        user_profile.avatar.url = url
        user_profile.save()