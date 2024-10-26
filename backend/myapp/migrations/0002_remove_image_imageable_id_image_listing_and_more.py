# Generated by Django 5.1.2 on 2024-10-12 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='imageable_id',
        ),
        migrations.AddField(
            model_name='image',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='myapp.listing'),
        ),
        migrations.AlterField(
            model_name='image',
            name='imageable_type',
            field=models.CharField(blank=True, choices=[('user', 'User'), ('listing', 'Listing')], max_length=20, null=True),
        ),
    ]