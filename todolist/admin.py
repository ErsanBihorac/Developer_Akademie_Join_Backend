from django.contrib import admin
from .models import Contact, TodoItem

admin.site.register(TodoItem)
admin.site.register(Contact)