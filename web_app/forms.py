from django.forms import ModelForm
from web_app.models import ProfilePic


class ProfileImageForm(ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['profileName', 'profile_Main_Img']
