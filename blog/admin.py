from django.contrib import admin
from .models import Post, Comment, Category, UserProfile, Photo

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ('status', 'categories')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
  
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'rating', 'author','created_on', 'source_post')
    # list_filter = ('author')
    search_fields = ['content']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Photo)
