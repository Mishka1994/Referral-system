# Generated by Django 5.0.3 on 2024-03-10 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_authorization_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='authorization_code',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Код активации'),
        ),
    ]