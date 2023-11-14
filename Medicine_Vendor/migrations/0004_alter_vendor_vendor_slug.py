# Generated by Django 4.2.5 on 2023-11-14 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Medicine_Vendor', '0003_vendor_vendor_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendor_slug',
            field=models.SlugField(max_length=125, unique=True),
        ),
    ]