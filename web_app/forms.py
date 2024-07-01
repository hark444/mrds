from django import forms
from .models import *


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['profileName', 'profile_Main_Img']