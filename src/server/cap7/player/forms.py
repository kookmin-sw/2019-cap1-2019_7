from django import forms
from .models import Video
from .models import Contact

class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields = ["language", "videofile"]

class URLForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["url","language"]

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']