from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        widgets = {
          'content': forms.Textarea(attrs={'rows':2, 'cols':60}),
        }
        exclude = ['created_on', 'rating', 'source_post', 'author']
