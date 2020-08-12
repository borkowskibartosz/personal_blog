from django.contrib import admin
from .models import Post, Comment


admin.site.register(Post)
admin.site.register(Comment)



# snippets
# class ArticleAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("title",)}