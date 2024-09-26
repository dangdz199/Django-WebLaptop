# Generated by Django 5.1 on 2024-09-26 01:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='laptops/images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('laptop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.laptop')),
            ],
        ),
    ]
