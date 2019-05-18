from django.contrib import admin

from .models import *

class DictionaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'word', 'part', 'mean', 'ref_word', 'location']
    list_display_links = ['id', 'word']

admin.site.register(Basic, DictionaryAdmin)
admin.site.register(Number, DictionaryAdmin)
admin.site.register(Finger, DictionaryAdmin)
