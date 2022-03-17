from django import forms
from .models import Comment,connect_comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ( 'comment',)
        widgets={
            'comment':forms.Textarea(attrs={'class':'form-control'})
        }

class community_comment_form(forms.ModelForm):
    class Meta:
        model=connect_comment
        fields=('post_comment',)
        widgets={
            'comment':forms.Textarea(attrs={'class':'form-control'})
        }
