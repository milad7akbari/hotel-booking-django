# Generated by Django 4.1.4 on 2023-07-10 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0016_reviews'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='close_spots',
            options={'verbose_name': 'Hotel Close Spots', 'verbose_name_plural': 'Hotel Close Spots'},
        ),
        migrations.AlterModelOptions(
            name='cover',
            options={'verbose_name': 'Hotel Cover', 'verbose_name_plural': 'Hotel Cover'},
        ),
        migrations.AlterModelOptions(
            name='facility',
            options={'verbose_name': 'Hotel Facility', 'verbose_name_plural': 'Hotel Facility'},
        ),
        migrations.AlterModelOptions(
            name='hotel',
            options={'verbose_name': 'Hotel', 'verbose_name_plural': 'Hotel '},
        ),
        migrations.AlterModelOptions(
            name='reviews',
            options={'verbose_name': 'Hotel Reviews', 'verbose_name_plural': 'Hotel Reviews'},
        ),
        migrations.AlterModelOptions(
            name='room_cover',
            options={'verbose_name': 'Room Cover', 'verbose_name_plural': 'Room Cover'},
        ),
        migrations.AlterModelOptions(
            name='room_facility',
            options={'verbose_name': 'Room Facility', 'verbose_name_plural': 'Room Facility'},
        ),
        migrations.RenameField(
            model_name='reviews',
            old_name='created_at',
            new_name='date_add',
        ),
        migrations.AddField(
            model_name='reviews',
            name='date_upd',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
