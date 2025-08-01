# Generated by Django 4.1.4 on 2023-07-06 14:28

import apps.hotel.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0012_provinces_cities'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(blank=True, help_text='Maximum file size allowed is 1Mb', null=True, upload_to=apps.hotel.models.file, validators=[apps.hotel.models.Cover.validate_image])),
                ('title', models.CharField(max_length=256, null=True)),
                ('note', models.CharField(max_length=256, null=True)),
                ('active', models.SmallIntegerField(choices=[(1, 'Yes'), (0, 'NO')], default=0)),
                ('date_upd', models.DateTimeField(auto_now=True)),
                ('date_add', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Cover',
                'verbose_name_plural': 'Cover',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, null=True)),
                ('reference', models.CharField(max_length=256, null=True, unique=True)),
                ('long_desc', models.TextField(null=True)),
                ('short_desc', models.TextField(null=True)),
                ('rule_cancelable', models.TextField(null=True)),
                ('rule_enter', models.TextField(null=True)),
                ('note', models.TextField(null=True)),
                ('address', models.TextField(null=True)),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=10, null=True)),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=11, null=True)),
                ('phone_number', models.CharField(max_length=256, null=True)),
                ('number_rooms', models.SmallIntegerField(default=0)),
                ('number_floor', models.SmallIntegerField(default=0)),
                ('stars', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (4, '3'), (4, '4'), (5, '5')], default=1)),
                ('meta_keywords', models.CharField(default=None, help_text='some tag, espinas, international, etc...', max_length=256)),
                ('available_for_order', models.SmallIntegerField(choices=[(1, 'Yes'), (0, 'NO')], default=1)),
                ('on_sale', models.SmallIntegerField(choices=[(1, 'Yes'), (0, 'NO')], default=0)),
                ('active', models.SmallIntegerField(choices=[(1, 'Yes'), (0, 'NO')], default=0)),
                ('upd_add', models.DateTimeField(auto_now=True)),
                ('date_add', models.DateTimeField(auto_now_add=True, null=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.cities')),
                ('default_cover', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.cover')),
            ],
            options={
                'verbose_name': 'Main',
                'verbose_name_plural': 'Main',
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, null=True)),
                ('note', models.CharField(default=None, max_length=256)),
                ('active', models.SmallIntegerField(choices=[(1, 'Yes'), (0, 'NO')], default=0)),
                ('date_upd', models.DateTimeField(auto_now=True)),
                ('date_add', models.DateTimeField(auto_now_add=True, null=True)),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
            options={
                'verbose_name': 'Facility',
                'verbose_name_plural': 'Facility',
            },
        ),
        migrations.CreateModel(
            name='Close_spots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_desc', models.CharField(max_length=512, null=True)),
                ('note', models.CharField(default=None, max_length=512)),
                ('active', models.SmallIntegerField(choices=[(1, 'Yes'), (0, 'NO')], default=0)),
                ('date_upd', models.DateTimeField(auto_now=True)),
                ('date_add', models.DateTimeField(auto_now_add=True, null=True)),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
            options={
                'verbose_name': 'Close Spots',
                'verbose_name_plural': 'Close Spots',
            },
        ),
    ]
