from django.contrib import admin

# Register your models here.
from .models import Snippet


class SnippetsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')


admin.site.register(Snippet, SnippetsAdmin)
