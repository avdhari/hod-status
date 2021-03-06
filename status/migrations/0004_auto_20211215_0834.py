# Generated by Django 3.2.10 on 2021-12-15 08:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0003_auto_20211214_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='assigned_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='status.staff'),
        ),
        migrations.CreateModel(
            name='ProgressOfProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drawing', models.PositiveIntegerField(auto_created=True)),
                ('is_removed', models.BooleanField(default=False)),
                ('progress', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='status.project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
