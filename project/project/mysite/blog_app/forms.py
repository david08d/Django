from django.forms import ModelForm, Form
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={'rows': 4, 'cols': 40})


class EmailForm(Form):
    to = forms.EmailField()
    subject = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
