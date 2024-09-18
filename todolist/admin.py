from django.contrib import admin
from .models import Contact, TodoItem

class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority' , 'due_date')
    search_fields = ('title', 'description')

admin.site.register(TodoItem, TodoItemAdmin)
admin.site.register(Contact)