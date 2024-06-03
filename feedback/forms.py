# forms.py
from django import forms
from .models import Comment, Rating
from django.core.validators import MinLengthValidator


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {"content": forms.Textarea(attrs={"rows": 3})}

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) < 5:
            raise forms.ValidationError(
                "The comment must be at least 5 characters long."
            )
        return content


class RatingForm(forms.ModelForm):
    rating_choices = [(i, i) for i in range(1, 6)]
    amount = forms.ChoiceField(choices=rating_choices, widget=forms.Select)

    class Meta:
        model = Rating
        fields = ["amount"]
