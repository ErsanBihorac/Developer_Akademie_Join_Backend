# Generated by Django 5.1 on 2024-09-03 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0002_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='color_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='contact',
            name='first_letter',
            field=models.CharField(default=None, max_length=2),
        ),
    ]
