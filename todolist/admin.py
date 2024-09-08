from django.contrib import admin
from .models import Contact, TodoItem

# Register your models here.
admin.site.register(TodoItem)
admin.site.register(Contact)