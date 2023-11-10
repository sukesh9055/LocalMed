# Generated by Django 4.2.5 on 2023-11-01 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Medicine_Vendor', '0002_alter_vendor_user_profile'),
        ('menu', '0003_rename_category_fooditem_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine_lobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Medicine_title', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=250)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='foodimages')),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.category')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Medicine_Vendor.vendor')),
            ],
        ),
        migrations.DeleteModel(
            name='FoodItem',
        ),
    ]