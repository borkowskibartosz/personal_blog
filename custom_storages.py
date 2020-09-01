from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):

    location = 'static'

    def _clean_name(self, name):
        return name

    # def _normalize_name(self, name):
    #     if not name.endswith('/'):
    #         name += "/"

    #     name += self.location
    #     return name


class MediaStorage(S3Boto3Storage):

    location = 'media'
    file_overwrite = False

    def _clean_name(self, name):
        return name

    # def _normalize_name(self, name):
    #     if not name.endswith('/'):
    #         name += "/"

    #     name += self.location
    #     return name