from django.db import models
from django.conf import settings
import datetime

class Contact(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=254, unique=True, blank=False)
    phone = models.CharField(max_length=15, blank=False)
    first_letter = models.CharField(max_length=1, null=False, blank=False)
    color_id = models.IntegerField(default=1)

    def __str__(self):
        return self.name
class TodoItem(models.Model):
    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    STATUS_CHOICES = [
        ('to_do', 'To do'),
        ('in_progress', 'In progress'),
        ('await_feedback', 'Await feedback'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=25)
    description = models.CharField(max_length=200)
    Assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='todo_items',
        blank=True
    )
    created_at = models.DateField(default=datetime.date.today)
    due_date = models.DateField()
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    status = models.CharField(
        max_length=14,
        choices=STATUS_CHOICES,
        default='to_do'
    )

    def __str__(self):
        return self.title