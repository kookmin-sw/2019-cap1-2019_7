from django import forms
from .models import Video
from .models import Contact

class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields= ["videofile"]
        widgets = {
            'videofile': forms.FileInput(attrs={'class': 'filebox'}),
        }

class URLForm(forms.ModelForm):
    class Meta:
        model = Video
        fields= ["url"]

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']