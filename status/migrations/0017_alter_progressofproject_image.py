# Generated by Django 3.2.10 on 2022-01-31 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0016_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressofproject',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
