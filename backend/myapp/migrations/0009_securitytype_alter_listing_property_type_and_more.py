# Generated by Django 5.1.2 on 2024-10-18 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_roomtype_alter_listing_room_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('icon_url', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='listing',
            name='property_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings_property', to='myapp.propertype'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='room_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings_room', to='myapp.roomtype'),
        ),
        migrations.AddField(
            model_name='listing',
            name='security_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings_security', to='myapp.securitytype'),
        ),
    ]
