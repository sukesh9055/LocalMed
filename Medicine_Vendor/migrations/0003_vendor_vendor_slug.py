# Generated by Django 4.2.5 on 2023-11-14 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Medicine_Vendor', '0002_alter_vendor_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='vendor_slug',
            field=models.SlugField(blank=True, max_length=125),
        ),
    ]
