# Generated by Django 4.1.4 on 2023-06-22 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_user_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='national_code',
        ),
    ]
