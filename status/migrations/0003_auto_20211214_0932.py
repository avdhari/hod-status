# Generated by Django 3.2.10 on 2021-12-14 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0002_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
    ]
