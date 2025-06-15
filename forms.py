from django import forms
from django.contrib.auth.models import User
from .models import Vote

class VoteForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label="Your Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your username"})
    )

    class Meta:
        model = Vote
        fields = ["username", "recipe"]
        widgets = {
            "recipe": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username does not exist. Please enter a valid username.")
        return username
