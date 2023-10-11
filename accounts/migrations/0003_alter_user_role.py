# Generated by Django 4.2.5 on 2023-10-10 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'DISPENSARY'), (2, 'Customer')], null=True),
        ),
    ]