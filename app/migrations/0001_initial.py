# Generated by Django 5.1.7 on 2025-05-02 07:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('posted', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Опубликована')),
            ],
        ),
    ]
