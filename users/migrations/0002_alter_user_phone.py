# Generated by Django 5.0.3 on 2024-03-07 13:46

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='RU', unique=True, verbose_name='Телефон'),
        ),
    ]
