# Generated by Django 4.1.4 on 2023-07-07 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0014_rename_room_room_hotel'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True),
        ),
    ]
