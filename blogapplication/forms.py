from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

        widgets = {
            'name': forms.TextInput(attrs={'type': 'text',
                                           'class': 'form-control text-black',
                                           'placeholder': 'Name...'
                                           }),
            'email': forms.EmailInput(attrs={'type': 'email',
                                             'class': 'form-control text-black',
                                             'placeholder': 'Email...'
                                             }),
            'body': forms.Textarea(attrs={'type': 'text',
                                          'class': 'form-control text-black',
                                          'placeholder': "Comment..."})
        }
