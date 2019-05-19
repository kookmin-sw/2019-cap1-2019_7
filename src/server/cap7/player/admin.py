from django.contrib import admin
from .models import *

class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'videofile', 'language', 'url']
    list_display_links = ['id', 'videofile']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'email', 'phone', 'message']
    list_display_links = ['id', 'name']

admin.site.register(Video, VideoAdmin)
admin.site.register(Contact, ContactAdmin)