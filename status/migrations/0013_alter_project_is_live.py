# Generated by Django 3.2.10 on 2022-01-21 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0012_auto_20220116_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='is_live',
            field=models.BooleanField(default=True),
        ),
    ]
